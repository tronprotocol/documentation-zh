# wallet-cli account portfolio

显示原生 + token 余额，附带尽力而为的 USD 估值。

## 用法

```
wallet-cli account portfolio [options]
```

## 说明

将账户的原生代币和地址簿中的 token 余额汇总到一个视图中，并在数据可用时附加外部价格源提供的 USD 价格。由于需要并发查询多个价格数据，它是 `account` 命令组中耗时最长的查询。

价格字段明确区分以下三种状态：

- **已定价**——`priceUsd` / `valueUsd` 给出具体数值。
- **测试网**——直接记为 `0`，不查询外部价格源。测试网代币没有市场交易价格；网络是否为测试网由网络配置声明，而不是根据 id 推断。
- **未知**——`priceUsd` / `valueUsd` 为 `null`（链未被价格源收录，或价格源查询失败）。`null` 表示无法获得价格，并不表示资产价值为零。如果价格源查询失败，`data.priceUnavailable` 为 `true`，并带有 `priceReason: "price_provider_error"`。

如果某个 token 的**余额**读取失败，该条目仍会保留：`balance` / `rawBalance` 为 `null`，并带有 `balanceUnavailable: true` 和 `reason`。单个 token 查询失败不会导致整个资产组合查询失败。`totalValueUsd` 只累加能够估值的条目；没有任何条目可以估值时，该字段为 `null`。

## 选项

仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli account portfolio --network tron:3448148188
```

```console
"demo" Portfolio
| Token | Balance       | Price (USD) | Value (USD) |
| ----- | ------------- | ----------- | ----------- |
| TRX   | 9,915.80311   | $0.0000     | $0.00       |
| USDT  | 17,061.463423 | $0.0000     | $0.00       |
| USDD  | 0             | $0.0000     | $0.00       |
Total ≈ $0.00
```

```bash
wallet-cli account portfolio --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.portfolio","data":{"network":"tron:3448148188","account":"wlt_gd2x8vyk","address":"TNmoJ3Be59WFEq5dsW6eCkZjveiL3G8HVB","priceSource":"coingecko","holdings":[{"kind":"native","symbol":"TRX","decimals":6,"rawBalance":"9915803110","balance":"9915.80311","priceUsd":0,"valueUsd":0},{"kind":"trc20","symbol":"USDT","decimals":6,"rawBalance":"17061463423","balance":"17061.463423","priceUsd":0,"valueUsd":0,"id":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","name":"Tether USD","source":"official"},{"kind":"trc20","symbol":"USDD","decimals":18,"rawBalance":"0","balance":"0","priceUsd":0,"valueUsd":0,"id":"TYQF9cAeJ3Faq8QXpHxTcFco72DRCQbgFt","name":"Usdd Stablecoin","source":"official"}],"totalValueUsd":0},"meta":{"durationMs":724,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

同一条命令在 EVM 网络上，`kind` 报告的是 `erc20` 而不是 `trc20`：

```bash
wallet-cli account portfolio --network eip155:11155111 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.portfolio","data":{"network":"eip155:11155111","account":"wlt_fjeca27y.0","address":"0x541B10b92b45C08513e67bb8209f035D810212B6","priceSource":"coingecko","holdings":[{"kind":"native","symbol":"ETH","decimals":18,"rawBalance":"0","balance":"0","priceUsd":0,"valueUsd":0}],"totalValueUsd":0},"meta":{"durationMs":232,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `network` / `account` / `address` | string | 查询上下文 |
| `priceSource` | string | e.g. `coingecko` |
| `priceUnavailable` / `priceReason` | boolean / string | 仅在价格源失败时出现 |
| `holdings[].kind` | string | `native`、`trc20`、`trc10`（TRON），`erc20`（EVM） |
| `holdings[].symbol` / `decimals` | — | token 标识 |
| `holdings[].rawBalance` | string\|null | 基础单位；余额读取失败时为 `null` |
| `holdings[].balance` | string\|null | 人类可读单位；余额读取失败时为 `null` |
| `holdings[].balanceUnavailable` / `reason` | boolean / string | 仅出现在余额读取失败的那一行 |
| `holdings[].id` / `name` / `source` | string | 仅 token 行：合约地址（或 TRC10 id）、名称，以及它来自内置列表（`official`）还是用户自行添加 |
| `holdings[].priceUsd` / `valueUsd` | number\|null | **尽力而为的估算**；测试网上为 `0`，未知时为 `null` |
| `totalValueUsd` | number\|null | 已定价持仓之和；全部无价格时为 `null` |

## 退出码

`0`（即使所有价格均为 `null`，或某个 token 的余额不可用） · `1` 执行失败 · `2` 用法错误。

## 另请参见

[`account balance`](balance.md) · `token`——管理决定这里出现哪些 token 的地址簿
