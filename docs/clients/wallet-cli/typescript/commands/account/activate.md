# wallet-cli account activate

在链上激活一个尚不存在的账户。

## 用法

```
wallet-cli account activate --address <T...>
                            [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                            [--permission-id <n>] [options]
```

## 说明

一个 TRON 地址在收到第一笔资产或被显式创建之前，并不存在于链上。在激活之前，`account set` 会返回 `not_found`（普通的 `account info` 仍会成功，但只返回空的 `account` 对象），该地址也无法发起交易。本命令可以在**不转移任何资产**的情况下创建（激活）账户，链上账户创建费用由付款账户承担。

只有在地址需要独立存在于链上，以便接受查询或自行发起交易时，才需要使用本命令。如果本来就要向该地址转账，[`tx send`](../tx/send.md) 会在转账过程中自动激活收款方；将地址加入多签权限则**不需要**激活。

命令需要一个付款账户。仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。
`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回
`watch_only_no_signer`。

Ledger 的 TRON 应用无法对 `AccountCreateContract` 签名：Ledger 账户可以使用 `--dry-run` 或 `--build-only`，但 `--sign-only`、默认提交和 `--wait` 会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--address <T...>` | **必填。** 要激活的地址（一个有效且尚未激活的 TRON 地址） |
| `--dry-run` | 只构建和估算；不签名、不广播、不需要密码。与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 构建并签名，输出已签名的 hex（交给 [`tx broadcast`](../tx/broadcast.md)）。与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex（交给 [`tx multisig --create`](../tx/multisig.md)）。与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。`--account` 用于选择付款账户。

## 示例

示例中的 `$PW` 是你的 master password，通过 `--password-stdin` 从 stdin 传入。

默认——广播并返回**已提交**的回执：

```bash
echo "$PW" | wallet-cli account activate --address TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz --network tron:3448148188 --password-stdin
```

```console
⏳ Account activated
  Address  TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz
  Payer    TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  TxID     a1b...
  Status   pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid a1b...
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.activate","data":{"kind":"account-activate","stage":"submitted","txId":"a1b...","address":"TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz","payer":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw"},"meta":{"durationMs":17,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

加 `--wait` 可阻塞直到已确认，并给出实际的区块和费用：

```bash
echo "$PW" | wallet-cli account activate --address TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz --network tron:3448148188 --wait --password-stdin
```

```console
✅ Account activated
  Address  TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz
  Payer    TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  TxID     e7a...
  Block    #84,340,277
  Fee      1.1 TRX
  Status   success
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.activate","data":{"kind":"account-activate","stage":"confirmed","txId":"e7a...","confirmed":true,"blockNumber":84340277,"feeSun":1100000,"failed":false,"address":"TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz","payer":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw"},"meta":{"durationMs":6540,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "account-activate"`、`stage: "submitted"`、`txId`、`address`、`payer` |
| `--wait`（已确认） | 同上，但 `stage: "confirmed"`，另加 `confirmed`、`blockNumber`、`feeSun`、`failed` |
| `--dry-run` | `kind`、`mode: "dry-run"`、费用估算、`address`、`payer`；没有 `txId` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名/试运行） · `1` 执行失败（`account_already_active`、`watch_only_no_signer`、`ledger_unsupported`、`auth_failed`、`insufficient_balance`、`rpc_error`、`timeout`） · `2` 用法错误（`invalid_value`——地址格式错误）。

在交易**已确认**之后，本命令会回读账户以核实改动是否生效。这一后续检查绝不会把一笔已经付过费的交易变成命令失败：不一致或读取失败会作为 `meta.warnings` 条目（`account_activate_postcheck_mismatch` / `account_activate_postcheck_unavailable`）报告，`success` 仍为 `true`，退出码为 `0`。

## 另请参见

[`account set`](set.md) · [`tx send`](../tx/send.md) · [`account info`](info.md) · [`chain params`](../chain/params.md)
