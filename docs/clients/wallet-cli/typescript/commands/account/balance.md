# wallet-cli account balance

显示原生代币余额。

## 用法

```
wallet-cli account balance [options]
```

## 说明

从节点获取当前账户（或 `--account` 指定账户）的原生代币余额。只读；无需解锁。

查询的币种和余额均由所选网络决定：余额以该链的最小单位报告（TRON 为 SUN，EVM 为 wei），`decimals` 由链家族决定，`symbol` 则由具体网络决定。例如，`eip155:1` 和 `eip155:56` 同属 EVM 家族，但原生币分别是 ETH 和 BNB。

## 选项

仅[全局选项](../index.md#global-options-every-command)（`--account`、`--network` 等）。

## 示例

```bash
wallet-cli account balance --network tron:3448148188
```

```console
Label    demo
Balance  9,915.80311 TRX
```

```bash
wallet-cli account balance --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.balance","data":{"address":"TNmoJ3Be59WFEq5dsW6eCkZjveiL3G8HVB","balance":"9915803110","decimals":6,"symbol":"TRX"},"meta":{"durationMs":681,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

同一条命令在 EVM 网络上读取的则是该账户的 EVM 地址：

```bash
wallet-cli account balance --network eip155:11155111 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.balance","data":{"address":"0x541B10b92b45C08513e67bb8209f035D810212B6","balance":"0","decimals":18,"symbol":"ETH"},"meta":{"durationMs":234,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的地址，格式随所选网络而定（TRON 为 base58，EVM 为 `0x` 十六进制） |
| `balance` | string | 以该链最小单位计的原始余额——TRON 上是 SUN（`"9915803110"` = 9915.80311 TRX），EVM 上是 wei |
| `decimals` | number | 每枚币包含的最小单位数：TRON 为 `6`，EVM 为 `18` |
| `symbol` | string | 该网络的原生币——`TRX`、`ETH`、`BNB` |

## 退出码

`0` · `1` 执行失败（节点不可达、超时） · `2` 用法错误。

## 另请参见

[`account portfolio`](portfolio.md)——包含 token · [`account info`](info.md) · [单位：TRX 与 SUN](../../concepts/networks.md#fees-the-tron-resource-model)
