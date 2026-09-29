# wallet-cli proposal create

创建变更链参数的治理提案。

## 用法

```
wallet-cli proposal create --set <name|id>=<value> [--set ...]
                           [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                           [--permission-id <n>] [options]
```

## 说明

提交一个携带一项或多项链参数变更的提案，交由超级代表投票。只有已注册的见证人才能创建；其他账户会以 `not_a_witness` 失败。

`--set` 接受参数**名称**——即 [`chain params`](../chain/params.md) 的 `getXxx` 词汇表——并把它解析成链上的参数 id；直接写数字 id 也可以。未知名称和超出取值范围的值会在本地就被拒绝，不会发出任何广播。

每个参数写一次 `--set`。回执和 `data.changes[]` 按参数 id 排序，而不是按你输入的先后顺序，所以同一个提案的呈现方式始终一致。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--set <name\|id>=<value>` | **必填，可重复。** 一项参数变更，例如 `--set getTransactionFee=15`；`name` 是 `chain params` 中的键，也接受直接写参数 id |
| `--dry-run` | 只构建和估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

单个参数，并等待确认：

```bash
echo "$PW" | wallet-cli proposal create --set getTransactionFee=15 --network nile --wait --password-stdin
```

```console
✅ Proposal created
  Proposal  #48
  Proposer  TSRmq8kP...9dEf (main)
  TxID      9c4...
  Block     57,880,102
  Fee       0 TRX  (268 bandwidth)
  Status    success
  Parameter changes (1)
    getTransactionFee   10 → 15   sun/byte
```

一个提案里包含多个参数——回执按参数 id 列出它们：

```bash
echo "$PW" | wallet-cli proposal create --set getTransactionFee=15 --set getCreateAccountFee=200000 --network nile --wait --password-stdin
```

```console
✅ Proposal created
  Proposal  #49
  Proposer  TSRmq8kP...9dEf (main)
  TxID      a1b...
  Block     57,880,140
  Fee       0 TRX  (292 bandwidth)
  Status    success
  Parameter changes (2)
    getCreateAccountFee   100000 → 200000   sun
    getTransactionFee         10 →     15   sun/byte
```

```bash
echo "$PW" | wallet-cli proposal create --set getTransactionFee=15 --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"proposal.create","data":{"kind":"proposal-create","stage":"confirmed","txId":"9c4...","confirmed":true,"blockNumber":57880102,"feeSun":0,"energyUsed":0,"netUsed":268,"energyFeeSun":0,"netFeeSun":0,"resource":{"netUsage":268,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0},"failed":false,"proposerAddress":"TSRmq8kP...","proposalId":48,"changes":[{"id":3,"name":"getTransactionFee","currentValue":10,"proposedValue":15,"unit":"sun/byte"}]},"meta":{"durationMs":6480,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "proposal-create"`、`stage: "submitted"`、`txId`、`proposerAddress`、`changes[]` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（布尔）、`blockNumber`、有返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`）、`failed`，以及可选的 `proposalId`——新提案的 id，只有在它上链之后才可知 |

`changes[]` 的每一项包含 `id`、`name`、`currentValue`、`proposedValue` 和 `unit`，按 `id` 排序。

当无法确凿地确定 id 时，`proposalId` 会被**省略**。链上并不返回它，因此 CLI 的做法是把提案列表与提交前拍下的快照做比对。如果列表尚未跟上，或者有多个新提案都与这些参数匹配，该字段就会被略去，并给出相应警告。这种情况下请用 [`proposal list`](list.md) 查出 id，而不要去猜——这个 id 后续要用于 `proposal approve` 和不可逆的 `proposal delete`。无论如何，交易本身是成功的。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`not_a_witness`、`watch_only_no_signer`、`auth_failed`） · `2` 用法错误（`missing_option`——没有给出 `--set`；`unknown_parameter`——没有该名称或 id；`invalid_value`——取值超出范围或不是数字）。

## 另请参见

[`proposal approve`](approve.md) · [`proposal delete`](delete.md) · [`proposal show`](show.md) · [`chain params`](../chain/params.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
