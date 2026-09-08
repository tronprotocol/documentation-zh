# wallet-cli contract call

只读合约调用。

## 用法

```
wallet-cli contract call --contract <address> --method <sig> [--params <json>] [options]
```

## 说明

在 TRON 或 EVM 上以 `constant`（只读）方式调用合约方法：不签名、不广播、不消耗任何费用，也不需要账户。

函数签名和参数类型都由你显式给出——不会去获取或参考任何 ABI。参数是一个 JSON 数组，元素为与方法签名逐一对应的 `{type, value}` 对象。

## 选项

| 选项 | 说明 |
|---|---|
| `--contract <string>` | **必填。** 合约地址——TRON 为 base58，EVM 为 `0x` |
| `--method <string>` | **必填。** 函数签名，例如 `balanceOf(address)` |
| `--params <string>` | ABI 参数的 JSON 数组，元素形如 `{type,value}`；省略表示不传参数 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli contract call --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --method "balanceOf(address)" --params '[{"type":"address","value":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ"}]' --network tron:3448148188
```

```console
Method  balanceOf
Result  0000000000000000000000000000000000000000000000000000000000000000 (raw)
```

```bash
wallet-cli contract call --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --method "balanceOf(address)" --params '[{"type":"address","value":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ"}]' --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.call","data":{"contract":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","method":"balanceOf(address)","result":["0000000000000000000000000000000000000000000000000000000000000000"]},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

同一个调用在 EVM 网络上是这样。注意 `result` 的形状：TRON 原样透传节点的 `constant_result` 数组，而 EVM 节点返回的是单个 `0x` 字符串：

```bash
wallet-cli contract call --contract 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238 --method "balanceOf(address)" --params '[{"type":"address","value":"0x541B10b92b45C08513e67bb8209f035D810212B6"}]' --network eip155:11155111
```

```console
Method  balanceOf
Result  0x0000000000000000000000000000000000000000000000000000000000000000 (raw)
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.call","data":{"contract":"0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238","method":"balanceOf(address)","result":"0x0000000000000000000000000000000000000000000000000000000000000000"},"meta":{"durationMs":236,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `contract` | string | 被调用的合约地址 |
| `method` | string | 实际调用的方法签名 |
| `result` | string[] \| string | ABI 编码的原始返回数据。TRON 上是节点 `constant_result` 数组的原样透传——CLI 不做任何切分或重新分组；EVM 上则是单个 `0x` 字符串。需按方法的返回类型自行解码 |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`、合约 `revert`） · `2` 用法错误（`invalid_value`——方法签名或参数 JSON 有误）。

## 另请参见

[`contract send`](send.md) · [`contract info`](info.md) · [`token balance`](../token/balance.md)
