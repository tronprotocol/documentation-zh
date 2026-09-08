# wallet-cli exchange withdraw

按交易对的储备比例从中撤资。

## 用法

```
wallet-cli exchange withdraw <id> --token <TRX|asset-id>
                             (--amount <n> | --raw-amount <n>)
                             [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                             [--permission-id <n>] [options]
```

## 说明

该命令与 [`exchange inject`](inject.md) 相反：指定一侧的撤出金额后，另一侧按当前储备比例计算，两种资产会一并转回账户。只有交易对创建者可以撤资。

**无法被储备比例整除的金额会被拒绝。** 链上把一侧折算成另一侧时有精度要求——商必须精确到 0.01% 以内——不满足的金额会直接以 `precision_loss` 被拒，而不是四舍五入。请把金额调整成该比例能整除的数值再试。

**token 只能通过 ID 指定**：使用 `TRX`（或其链上 ID `_`）以及数字形式的 TRC10 ID，不接受可能包含 `:` 的 TRC10 名称。`--amount` 按所选资产的完整 token 单位计；`--raw-amount` 则直接使用最小单位。两者必须且只能指定一个。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `<id>` | **必填。** 交易对 ID |
| `--token <TRX\|asset-id>` | **必填。** 用于指定撤出金额的资产 |
| `--amount <n>` | 该侧的金额，以完整 token 计；另一侧按储备比例跟随。`--amount` / `--raw-amount` 二选一 |
| `--raw-amount <n>` | 同一金额，以最小单位计。`--amount` / `--raw-amount` 二选一 |
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

```bash
echo "$PW" | wallet-cli exchange withdraw 12 --token TRX --amount 1000 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Liquidity withdrawn
  Exchange id  12
  Creator      TQkXm4vN...5Zt7Uw
  Withdrawn    1,000 TRX / 50,000 MyToken
  Reserves     10,000 TRX / 500,000 MyToken
  TxID         8f6...
  Block        #57,884,310
  Fee          0 TRX
  Status       success
```

```bash
echo "$PW" | wallet-cli exchange withdraw 12 --token TRX --amount 1000 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"exchange.withdraw","data":{"kind":"exchange-withdraw","stage":"confirmed","txId":"8f6...","confirmed":true,"blockNumber":57884310,"failed":false,"exchangeId":12,"pair":"TRX:1000123","creatorAddress":"TQkXm4vN...","tokenId":"_","tokenQuant":"1000000000","tokenLabel":"TRX","tokenDecimals":6,"otherTokenId":"1000123","otherTokenQuant":"50000000000","otherTokenLabel":"MyToken","otherTokenDecimals":6,"reserveAfter":"10000000000","otherReserveAfter":"500000000000","feeSun":0},"meta":{"durationMs":6460,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 是扁平结构，形状与 [`exchange inject`](inject.md#output) 完全一致：

| 字段 | 类型 | 含义 |
|---|---|---|
| `exchangeId` / `pair` / `creatorAddress` | number / string / string | 交易对及其创建者 |
| `tokenId` / `tokenQuant` | string | 指定金额的资产及其撤出量，以最小单位计 |
| `tokenLabel` / `tokenDecimals` | string / number | text 输出把该侧按完整 token 显示时所用的信息 |
| `otherTokenId` / `otherTokenQuant` / `otherTokenLabel` / `otherTokenDecimals` | — | 按比例算出的另一侧对应的同样四个字段 |
| `reserveAfter` / `otherReserveAfter` | string | 本次撤资之后交易对两侧的余额，顺序与上面一致 |

TRX 以 `"_"` 标识；所有数量都是最小单位下的**字符串**。`--wait` 会另加 `stage: "confirmed"`、`confirmed`、`blockNumber`、`feeSun`、`failed`。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`exchange_not_found`——没有这个交易对、`not_exchange_creator`、`token_not_in_exchange`、`exchange_closed`——某一侧储备为零、`insufficient_reserve`——超过该侧持有量、`precision_loss`——金额无法整除折算、`watch_only_no_signer`、`auth_failed`） · `2` 用法错误（`missing_option`——没给 `--token`；`invalid_option`——`--amount` / `--raw-amount` 两个都给了或都没给；`invalid_amount`——金额不是十进制数字，或小数位数超过该 token 允许的位数；`invalid_value`——金额 ≤ 0，或小到算出的另一侧结果为零）。

## 另请参见

[`exchange inject`](inject.md) · [`exchange show`](show.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
