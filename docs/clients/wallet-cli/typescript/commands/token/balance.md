# wallet-cli token balance

查询单个 token 的余额。

## 用法

```
wallet-cli token balance (--contract <address> | --asset-id <id>) [options]
```

## 说明

查询当前账户（或 `--account` 指定的账户）在所选网络上某一个 token 的余额——TRON 上是 TRC20/TRC10，EVM 上是 ERC20。二选一，只能给一个：合约类 token 用 `--contract`，TRC10 资产用 `--asset-id`。只读——不需要密码，也不会签名。

## 选项

| 选项 | 说明 |
|---|---|
| `--contract <string>` | token 合约地址——TRON 上为 TRC20，EVM 上为 ERC20 |
| `--asset-id <string>` | **仅限 TRON。** TRC10 数字资产 id；`--asset-id` / `--contract` 二者必选其一 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli token balance --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188
```

```console
Label    demo
Symbol   USDT
Balance  17,061.463423
```

```bash
wallet-cli token balance --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.balance","data":{"address":"TNmoJ3Be59WFEq5dsW6eCkZjveiL3G8HVB","token":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","balance":"17061463423","symbol":"USDT","decimals":6},"meta":{"durationMs":1215,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

EVM 网络上的 ERC20 余额——字段相同，另加该 token 的 `name`：

```bash
wallet-cli token balance --contract 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238 --network eip155:11155111 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.balance","data":{"address":"0x541B10b92b45C08513e67bb8209f035D810212B6","token":"0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238","balance":"0","symbol":"USDC","decimals":6,"name":"USDC"},"meta":{"durationMs":233,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的账户，格式随所选网络而定 |
| `token` | string | 合约地址，或 TRC10 资产 id |
| `balance` | string | 以 token 最小单位表示的原始余额（`"17061463423"` ÷ 10^`decimals`） |
| `symbol` | string | Token 符号 |
| `decimals` | number | token 精度 |
| `name` | string | token 名称；仅 EVM |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`、`timeout`） · `2` 用法错误（`invalid_value`——未给出选择器，或两个选择器同时给出；`invalid_option`——在 EVM 网络上使用了 `--asset-id`）。

## 另请参见

[`token info`](info.md) · [`account portfolio`](../account/portfolio.md) · [`tx send`](../tx/send.md)
