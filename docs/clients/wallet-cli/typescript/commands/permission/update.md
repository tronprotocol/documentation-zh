# wallet-cli permission update

替换账户的权限结构。

## 用法

```
wallet-cli permission update (--file <path> | --json <str>)
                             [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                             [--permission-id <n>] [options]
```

## 说明

用 `--file`（一个 JSON 文件）或 `--json`（内联 JSON 字符串）给出的新结构，替换账户**整个**权限结构——TRON 的 `UpdateAccountPermission` 采用替换语义，因此你提供的 JSON 就是全部结构。链上会为这次变更燃烧 **100 TRX**。

该命令不会弹出确认提示。它需要一个账户；只有在所选模式确实要签名时，才需要通过 `--password-stdin` 提供 master password，因为 `--dry-run` 和 `--build-only` 从不解锁钱包。在签名模式下，仅观察账户会以 `watch_only_no_signer` 失败。

**输入格式。** 权限 JSON 与 [`permission show -o json`](show.md) 的 `data` 结构相同（`owner` / `witness` / `actives`；密钥中的 `local` 字段可以省略）。每个 active 组的 `operations` 要写**合约类型名**，而不是原始位图——位图由 CLI 编码生成。要得到一份合法输入，最方便的办法是导出当前结构、编辑后再把文件提交回去。

CLI 会在构建交易前严格校验权限结构，不符合规则时返回用法错误（退出码 `2`），不会自动修正输入。
权限组的 `threshold` **不得超过各密钥权重之和**；无法达到的阈值会导致账户无法授权，因此会以
`invalid_permission` 被拒绝（`owner.threshold exceeds the total key weight`）。阈值和权重采用无损解析，
超出安全整数范围的值会被拒绝，不会进行舍入。

**编辑导出的结构。** `permission show -o json` 会为每个 active 组同时输出 `operations`（合约类型名）和 `operationsHex`（原始位图）。可以同时提供两者，但内容必须**一致**；如果同一权限组的两种表示相互矛盾，CLI 会拒绝输入，避免实际上链结构与已审核内容不一致。修改 `operations` 后，请删除该组原有的 `operationsHex`，CLI 会重新生成位图：

```bash
wallet-cli permission show -o json --network nile | jq '.data' > perms.json
# edit operations, then drop the stale operationsHex from the same active group
```

只改 `keys`、`threshold` 或 `name` 则无需删除它。

⚠️ **链上不做任何安全检查。** 即使新结构中没有任何你能签名的密钥，交易仍可能成功，导致账户永久无法操作，且链上无法补救。本 CLI 可能给出四种**本地警告码**，但**不会**阻止提交（在 JSON 中它们进入 `meta.warnings`，`success` 仍为 `true`）：

- **锁死风险**——当你本地可签名的 owner 密钥（软件 / Ledger）权重之和低于新的 owner 阈值时，stderr 上会出现一行 `warning:`，明确指出你已无法独自达到 owner 阈值（完全没有权重时为 `owner_lockout`，需要联署人时为 `owner_lockout_partial`）。多方托管本来就意味着「我一个人达不到阈值」，因此这只是提示，不是阻止。
- **危险操作**——当某个 active 组包含 `Update Account Permissions` 时（该组从此可以修改权限本身，实际上等同于 owner 级别），会有一行 `warning:` 标出（`active_can_update_permission`）。
- **未知操作**——当某个 active 组的位图授予了本版本无法命名的合约类型时，这些位会原样保留，并由一行 `warning:` 列出它们的 id（`active_unknown_operations`）。

## 选项

| 选项 | 说明 |
|---|---|
| `--file <path>` | **必填**（二选一）。含新结构的 JSON 文件（结构与 `permission show -o json` 的 data 相同）；整体替换 |
| `--json <string>` | **必填**（二选一）。内联给出含新结构的 JSON 字符串（结构同上） |
| `--dry-run` | 模拟回执——手续费、变更后的结构卡片和各项警告，与真实提交一致；不签名、不广播、不需要密码。与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 构建并签名，输出已签名的 hex 而不广播（交给 [`tx broadcast`](../tx/broadcast.md) 走链上联署）。与 `--dry-run` / `--build-only` 互斥；可与 `--expiration` 搭配 |
| `--build-only` | 构建并估算，输出**未签名**的 hex（交给 [`tx multisig --create`](../tx/multisig.md) 走服务中转的多签）。与 `--dry-run` / `--sign-only` 互斥；可与 `--expiration` 搭配 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 签名所用的权限组（0=owner，1=witness，2-9=active）；默认 `0`——修改权限属于 owner 级操作，因此通常就是 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password，通过 `--password-stdin` 从 stdin 传入。

先导出再编辑，以此准备新结构（无需手写操作位图）：

```bash
wallet-cli permission show --network nile -o json | jq '.data' > perms.json
```

```bash
# 编辑 perms.json——例如把 owner 组改成 2-of-3
$EDITOR perms.json
```

用 `--wait` 提交。回执包含交易记录，以及变更后的链上结构（确认之后读回，卡片样式与 `permission show` 相同）。警告会先于回执输出到 stderr：

```bash
echo "$PW" | wallet-cli permission update --file perms.json --network nile --wait --password-stdin
```

```console
warning: local keys hold 1 of 2 owner weight; co-signers are required for owner-level operations
✅ Permissions updated
  TxID    b3c...
  Block   #84,335,102
  Fee     100.268 TRX
  Status  success

Account  TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V

Permission Name   owner  (id 0)
Threshold         2
Authorized To     Address                             Weight
                  TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V       1  (this wallet: main)
                  TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c       1
                  TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP       1

Permission Name   finance  (id 2, active)
Operation(s)      Transfer TRX · Transfer TRC10 · Trigger Smart Contract  (3 total)
Threshold         2
Authorized To     Address                             Weight
                  TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V       1  (this wallet: main)
                  TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c       1
                  TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP       1
```

存在该字段时，JSON 回执中的 `data.permissions` 与 `permission show` 的 `data` **结构完全相同**，因此你可以拿它与变更前导出的内容做 diff。如果确认后的复查读取不到，该字段会被省略，并在 `meta.warnings` 中带上 `permission_postcheck_unavailable`；已确认的交易仍然是 `success: true`。锁死警告同样放在 `meta.warnings` 里：

```bash
echo "$PW" | wallet-cli permission update --file perms.json --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"permission.update","data":{"kind":"permission-update","stage":"confirmed","txId":"b3c...","confirmed":true,"blockNumber":84335102,"feeSun":100268000,"failed":false,"permissions":{"address":"TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V","owner":{"id":0,"name":"owner","threshold":2,"keys":[{"address":"TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V","weight":1,"local":"main"},{"address":"TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c","weight":1,"local":null},{"address":"TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP","weight":1,"local":null}]},"witness":null,"actives":[{"id":2,"name":"finance","threshold":2,"operations":["TransferContract","TransferAssetContract","TriggerSmartContract"],"operationLabels":["Transfer TRX","Transfer TRC10","Trigger Smart Contract"],"operationsHex":"0600008000000000000000000000000000000000000000000000000000000000","unknownOperationIds":[],"keys":[{"address":"TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V","weight":1,"local":"main"},{"address":"TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c","weight":1,"local":null},{"address":"TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP","weight":1,"local":null}]}]}},"meta":{"durationMs":6810,"warnings":[{"code":"owner_lockout_partial","message":"local keys hold 1 of 2 owner weight; co-signers are required for owner-level operations"}]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随模式而变：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "permission-update"`、`stage: "submitted"`、`txId` |
| `--wait`（已确认） | 同上，但 `stage` 为 `"confirmed"`，另加 `confirmed`、`blockNumber`、`feeSun`、`failed`，以及 `permissions`（结构与 `permission show` 的 data 相同，从链上读回） |
| `--dry-run` | `kind`、`mode: "dry-run"`、`tx`、`fee`（账户权限费）和 `permissions`（变更后的结构）；没有 `txId` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`signed`、`hex`（已签名的交易 hex——交给 `tx broadcast --hex`）、`fee`、`address`、`txId`，以及 `permissions` |
| `--build-only` | `kind`、`mode: "build-only"`、`tx`、`hex`（未签名的交易 hex——交给 `tx multisig --create`）、`fee`，以及 `permissions` |

本地警告（`owner_lockout`、`owner_lockout_partial`、`active_can_update_permission`、`active_unknown_operations`）在交易构建之前产生，以 `{code, message}` 对象的形式出现在 `meta.warnings` 中，且不影响 `success`——参见[读取 `meta.warnings`](../../machine-interface.md#reading-metawarnings)。

确认之后，`permission_postcheck_unavailable` 表示回读失败，`permission_postcheck_mismatch` 表示回读到的结构与预期不符。无论哪种情况，交易都已经确认，因此命令仍算成功，调用方必须把 `permissions` 当作可选字段处理。

## 退出码

`0` 已提交（早退模式下为已构建/已签名/试运行） · `1` 执行失败（`not_authorized`、`watch_only_no_signer`、`auth_failed`、`insufficient_balance`、`rpc_error`、`timeout`） · `2` 用法错误（`invalid_permission`——JSON 格式错误或权限结构非法；`invalid_value`）。

在多签账户上，若累计签名权重低于权限阈值，提交会在**签名之后、广播之前**被拒绝，报 `not_authorized`（`signature threshold is not reached; missing N weight`）——不会发出任何内容，也不会燃烧费用。此时请改用 `--sign-only` + [`tx sign`](../tx/sign.md) 收齐剩余签名，再用 [`tx broadcast`](../tx/broadcast.md) 提交。`--sign-only` 和 `--build-only` 仍会返回部分签名的交易，联署流程正是由此开始的。

## 另请参见

[`permission show`](show.md) · [`tx sign`](../tx/sign.md) · [`tx broadcast`](../tx/broadcast.md) · [`tx multisig`](../tx/multisig.md) · [安全](../../concepts/security.md)
