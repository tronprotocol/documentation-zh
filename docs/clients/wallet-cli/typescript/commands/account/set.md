# wallet-cli account set

设置账户的链上名称或账户 id。

## 用法

```
wallet-cli account set (--name <name> | --id <account-id>)
                       [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                       [--permission-id <n>] [options]
```

## 说明

设置账户的链上**名称**（显示别名，最多 32 字节）或其**账户 id**（全局唯一标识，8–32 字节）。一次只能设置一个——`--name` 与 `--id` 互斥；两者都要设置就运行两次。

⚠️ **两者各自只能设置一次，且永远无法更改**——该值是永久性的，写入前也不会再次提示确认。这项规则适用于所有网络，包括 Nile 和 Shasta；第二次写入会返回 `name_already_set` / `id_already_set`。因此，即使在测试网上也不能把该操作当作可重复的演练。这与 [`rename`](../rename.md) 不同，后者只修改本地标签，可以随时再次更改。

命令需要所修改的账户。仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。
`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回
`watch_only_no_signer`。账户 ID 的唯一性由链上保证；ID 已被占用时返回 `id_taken`。

Ledger 的支持情况因字段而异：TRON 应用可以对 `--name` 签名，但无法对 `--id`（`SetAccountIdContract`）签名。Ledger 账户仍可对这两个字段做构建或试运行；但带 `--id` 的签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--name <name>` | **必填**（二选一）。链上账户名称，最多 32 字节；在任何网络上都只能设置一次 |
| `--id <account-id>` | **必填**（二选一）。账户 id，8–32 字节，全局唯一；在任何网络上都只能设置一次 |
| `--dry-run` | 只构建和估算；不签名、不广播、不需要密码。与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 构建并签名，输出已签名的 hex（交给 [`tx broadcast`](../tx/broadcast.md)）。与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex（交给 [`tx multisig --create`](../tx/multisig.md)）。与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password，通过 `--password-stdin` 从 stdin 传入。

设置链上名称并等待确认：

```bash
echo "$PW" | wallet-cli account set --name "Acme Treasury" --network tron:3448148188 --wait --password-stdin
```

```console
✅ On-chain name set
  Address  TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  Name     Acme Treasury
  TxID     f2b...
  Block    #84,341,590
  Fee      0.3 TRX
  Status   success
```

```bash
echo "$PW" | wallet-cli account set --name "Acme Treasury" --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.set","data":{"kind":"account-set","stage":"confirmed","txId":"f2b...","confirmed":true,"blockNumber":84341590,"feeSun":300000,"failed":false,"field":"name","value":"Acme Treasury","address":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw"},"meta":{"durationMs":6420,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

改为设置账户 id（`--id`）；id 的唯一性由链上强制：

```bash
echo "$PW" | wallet-cli account set --id acme-treasury-01 --network tron:3448148188 --wait --password-stdin
```

```console
✅ On-chain id set
  Address  TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  ID       acme-treasury-01
  TxID     3d9...
  Block    #84,341,730
  Fee      0.3 TRX
  Status   success
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "account-set"`、`stage: "submitted"`、`txId`、`field`（`name`/`id`）、`value`、`address` |
| `--wait`（已确认） | 同上，但 `stage: "confirmed"`，另加 `confirmed`、`blockNumber`、`feeSun`、`failed` |
| `--dry-run` | `kind`、`mode: "dry-run"`、费用估算、`field`、`value`、`address`；没有 `txId` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名/试运行） · `1` 执行失败（`name_already_set`、`id_already_set`、`id_taken`、`watch_only_no_signer`、`ledger_unsupported`——用 Ledger 对 `--id` 签名、`auth_failed`、`rpc_error`、`timeout`） · `2` 用法错误（`invalid_value`、`invalid_option`——name/id 格式错误或缺失）。

在交易**已确认**之后，本命令会回读账户以核实改动是否生效。这一后续检查绝不会把一笔已经付过费的交易变成命令失败：不一致或读取失败会作为 `meta.warnings` 条目（`account_set_postcheck_mismatch` / `account_set_postcheck_unavailable`）报告，`success` 仍为 `true`，退出码为 `0`。

## 另请参见

[`account activate`](activate.md) · [`rename`](../rename.md) · [`account info`](info.md)
