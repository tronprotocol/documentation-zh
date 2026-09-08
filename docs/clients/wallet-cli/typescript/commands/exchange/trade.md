# wallet-cli exchange trade

用交易对的一侧兑换另一侧。

## 用法

```
wallet-cli exchange trade <id> --sell <TRX|asset-id>
                          (--amount <n> | --raw-amount <n>)
                          [--min-received <n> | --raw-min-received <n> | --slippage <percent>]
                          [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                          [--permission-id <n>] [options]
```

## 说明

沿 Bancor 曲线卖出交易对的一侧、换取另一侧。成交即时完成，不需要对手方，而且**任何人都可以交易**——与流动性不同，交易并不限于交易对的创建者。

下限是可选的，但**不给下限就等于完全没有滑点保护**：

- `--min-received` 是一个绝对下限，**不是估算值**。如果这笔交易换回的量低于它，整笔交易会在链上以 `slippage_exceeded` 被拒，只消耗带宽。它是防止价格在签名与执行之间变动的唯一手段。`--raw-min-received` 是同一数值的最小单位形式。
- `--slippage` 是便捷写法：CLI 读取当前储备，算出这笔交易大致能换回多少，再减去这个百分比，把结果作为下限发出。真正上链的始终是一个绝对数值。
- **三个都不给时**，上链的下限是 `1`——协议允许的最小值——也就是说，不论价格如何，只要返还非零就成交。响应会在 `meta.warnings` 中给出相应告警。

三者最多只能给其中一个；同时给出属于用法错误。

滑点会随着交易规模相对储备的比例上升而变大——这是曲线本身造成的，不是手续费；协议不抽成。用 [`exchange show`](show.md) 查看深度，用 `exchange trade --dry-run` 为某个具体数量定价。

**token 只能通过 ID 指定**：使用 `TRX`（或其链上 ID `_`）以及数字形式的 TRC10 ID，不接受可能包含 `:` 的 TRC10 名称。`--amount` 按卖出资产的完整 token 单位计，`--raw-amount` 按最小单位计；两者必须且只能指定一个。

> **你所在的网络可能根本没有开放交易。** 在 TIP-836 加固提案（`getAllowHardenExchangeCalculation`）激活之前，`java-tron` 会直接拒绝 `ExchangeTransactionContract`——该参数在主网和 Nile 上都未设置，此时命令会以 `exchange_trading_disabled` 失败。[`exchange create`](create.md)、[`inject`](inject.md) 和 [`withdraw`](withdraw.md) 不受影响。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `<id>` | **必填。** 交易对 ID |
| `--sell <TRX\|asset-id>` | **必填。** 要卖出的资产；交易对中的另一种资产为买入资产 |
| `--amount <n>` | 卖出数量，以完整 token 计，须 > 0。`--amount` / `--raw-amount` 二选一 |
| `--raw-amount <n>` | 同一金额，以最小单位计。`--amount` / `--raw-amount` 二选一 |
| `--min-received <n>` | 可接受的最低返还，以完整 token 计；低于它交易就会回滚。三个下限参数最多只能给一个 |
| `--raw-min-received <n>` | 同一下限，以最小单位表示 |
| `--slippage <percent>` | 按当前储备推算下限，并在其基础上扣掉这个百分比；须 > 0 且 < 100 |
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

显式给出下限：

```bash
echo "$PW" | wallet-cli exchange trade 12 --sell TRX --amount 100 --min-received 4900 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Trade completed
  Exchange id   12
  Trader        TQkXm4vN...5Zt7Uw
  Sold          100 TRX
  Received      4,950 MyToken
  Min accepted  4,900 MyToken
  TxID          d9a...
  Block         #57,884,455
  Fee           0 TRX
  Status        success
```

同一笔交易改用 `--slippage 1` 时，CLI 会根据当前储备算出 4,950，再扣除 1%，以 4,900.5 作为下限。滑点百分比会先换算为基点并四舍五入到最接近的整数，因此 `--slippage 1.006` 实际容忍 1.01% 的滑点；随后，下限按整数除法向下取整。

```bash
echo "$PW" | wallet-cli exchange trade 12 --sell TRX --amount 100 --slippage 1 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"exchange.trade","data":{"kind":"exchange-trade","stage":"confirmed","txId":"d9a...","confirmed":true,"blockNumber":57884455,"failed":false,"exchangeId":12,"pair":"TRX:1000123","traderAddress":"TQkXm4vN...","soldTokenId":"_","soldQuant":"100000000","soldLabel":"TRX","soldDecimals":6,"receivedTokenId":"1000123","receivedLabel":"MyToken","receivedDecimals":6,"receivedQuant":"4950000000","estimatedReceivedQuant":"4950000000","minReceivedQuant":"4900500000","feeSun":0},"meta":{"durationMs":6490,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `exchangeId` / `pair` / `traderAddress` | number / string / string | 交易对，以及发起交易的账户 |
| `soldTokenId` / `soldQuant` | string | 卖出资产及其数量，以最小单位计 |
| `soldLabel` / `soldDecimals` | string / number | text 输出把该侧按完整 token 显示时所用的信息 |
| `receivedTokenId` / `receivedLabel` / `receivedDecimals` | — | 买入资产对应的 ID、显示名称和精度 |
| `estimatedReceivedQuant` | string | 构建时按 Bancor 曲线预测的返还量——仅供参考，始终存在 |
| `receivedQuant` | string | 这笔交易实际换回的数量；**只有确认之后才有**，因为它只存在于交易回执中 |
| `minReceivedQuant` | string | 真正上链的下限——你自己给的、由 `--slippage` 推算出来的，或者在没给下限时为 `"1"` |

TRX 以 `"_"` 标识；所有数量都是最小单位下的**字符串**。确认之前，text 输出会用 `Estimated return` 代替 `Received`。`--wait` 会另加 `stage: "confirmed"`、`confirmed`、`blockNumber`、`feeSun`、`failed`。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`exchange_not_found`——没有这个交易对、`token_not_in_exchange`、`exchange_closed`——某一侧储备为零、`exchange_trading_disabled`——该网络不接受 Bancor 交易、`slippage_exceeded`——返还量低于下限、`transaction_rejected`——节点拒绝了它，例如余额不足、`watch_only_no_signer`、`auth_failed`） · `2` 用法错误（`missing_option`——没给 `--sell`；`invalid_option`——`--amount` / `--raw-amount` 两个都给了或都没给，或给了不止一个下限参数；`invalid_amount`——金额或 `--min-received` 不是十进制数字，或小数位数超过该 token 允许的位数；`invalid_value`——金额 ≤ 0，或 `--slippage` 没有同时满足「大于 0」且「小于 100」；`0` 和 `100` 本身也会被拒绝）。

## 另请参见

[`exchange show`](show.md) · [`exchange list`](list.md) · [`asset info`](../asset/info.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
