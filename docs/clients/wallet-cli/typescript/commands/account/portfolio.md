# wallet-cli account portfolio

显示原生币与 token 余额，并尽力给出 USD 估值。

## 用法

```
wallet-cli account portfolio [options]
```

## 说明

将账户的原生代币和地址簿中的 token 余额汇总到一个视图中，并在数据可用时附加外部价格源提供的 USD 价格。由于需要并发查询多个价格数据，它是 `account` 命令组中耗时最长的查询。

价格字段明确区分以下三种状态：

- **有报价**——`priceUsd` / `valueUsd` 给出数值。
- **测试网**——直接按 `0` 计价，不向任何人询价。测试网的币不参与交易，因此没什么可查的；网络会自行声明它是测试网，而不是从 id 去猜。
- **未知**——`priceUsd` / `valueUsd` 为 `null`（未收录的链，或价格源失败）。`null` 的意思是「我们查不到」，这与「一文不值」并不是一回事。如果是价格源本身出错，`data.priceUnavailable` 为 `true`，并带上 `priceReason`。

**余额**读不到的 token 会保留其行，而不是凭空消失：`balance` / `rawBalance` 为 `null`，`balanceUnavailable` 为 `true` 并带上 `reason`。一个读不到的 token 绝不会拖垮整个组合视图。`totalValueUsd` 只累加那些能够估值的行。

## 选项

仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli account portfolio --network nile
```

```console
"main" Portfolio
| Token | Balance   | Price (USD) | Value (USD) |
| ----- | --------- | ----------- | ----------- |
| TRX   | 1,976.489 | $0.0000     | $0.00       |
| USDT  | 0         | $0.0000     | $0.00       |
| USDD  | 0         | $0.0000     | $0.00       |
Total ≈ $0.00
```

```bash
wallet-cli account portfolio --network nile -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.portfolio","data":{"network":"tron:3448148188","account":"wlt_4473p34m.0","address":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","priceSource":"coingecko","holdings":[{"kind":"native","symbol":"TRX","decimals":6,"rawBalance":"1976489000","balance":"1976.489","priceUsd":0,"valueUsd":0},{"kind":"trc20","symbol":"USDT","decimals":6,"rawBalance":"0","balance":"0","priceUsd":0,"valueUsd":0,"id":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","name":"Tether USD","source":"official"},{"kind":"trc20","symbol":"USDD","decimals":18,"rawBalance":"0","balance":"0","priceUsd":0,"valueUsd":0,"id":"TYQF9cAeJ3Faq8QXpHxTcFco72DRCQbgFt","name":"Usdd Stablecoin","source":"official"}],"totalValueUsd":0},"meta":{"durationMs":11031,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

同一条命令在 EVM 网络上，`kind` 报告的是 `erc20` 而不是 `trc20`：

```bash
wallet-cli account portfolio --network sepolia -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.portfolio","data":{"network":"eip155:11155111","account":"wlt_fjeca27y.0","address":"0x541B10b92b45C08513e67bb8209f035D810212B6","priceSource":"coingecko","holdings":[{"kind":"native","symbol":"ETH","decimals":18,"rawBalance":"0","balance":"0","priceUsd":0,"valueUsd":0}],"totalValueUsd":0},"meta":{"durationMs":1204,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `network` / `account` / `address` | string | 查询上下文 |
| `priceSource` | string | e.g. `coingecko` |
| `priceUnavailable` / `priceReason` | boolean / string | 仅在价格源失败时才出现 |
| `holdings[].kind` | string | `native`、`trc20`、`trc10`（TRON）、`erc20`（EVM） |
| `holdings[].symbol` / `decimals` | — | token 身份信息 |
| `holdings[].id` / `name` / `source` | string | 仅 token 行：合约地址（或 TRC10 id）、名称，以及该条目来自内置列表（`official`）还是用户添加（`user`） |
| `holdings[].rawBalance` | string\|null | 最小单位；余额读不到时为 `null` |
| `holdings[].balance` | string\|null | 人类可读单位；余额读不到时为 `null` |
| `holdings[].balanceUnavailable` / `reason` | boolean / string | 仅出现在余额读不到的那一行上 |
| `holdings[].priceUsd` / `valueUsd` | number\|null | **尽力而为的估值**；测试网上为 `0`，未知时为 `null` |
| `totalValueUsd` | number\|null | 能够估值的那些持仓之和；一个都估不出来时为 `null` |

## 退出码

`0`（即使所有价格均为 `null`，或某个 token 的余额不可用） · `1` 执行失败 · `2` 用法错误。

## 另请参见

[`account balance`](balance.md) · `token`——管理决定这里出现哪些 token 的地址簿
