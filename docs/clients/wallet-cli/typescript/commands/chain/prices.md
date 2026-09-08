# wallet-cli chain prices

显示当前的交易单价。

## 用法

```
wallet-cli chain prices [options]
```

## 说明

显示当前每单位交易资源的价格，可用于估算交易需要燃烧的费用。该命令只读，不需要账户或密码。

**答案的形态由网络的费用模型决定，两者之间没有可比性：**

- **TRON（`tron-resource`）**——能量单价、带宽单价和备注费用。节点为每一项返回价格*历史*时间线；文本输出只显示当前值（最后一段），`-o json` 则保留完整的 `history`。
- **EVM（`eip1559` / `legacy`）**——当前的基础费用、建议的优先费用（小费）、由此得出的 gas 价格，以及按这些数字计算、一笔普通的 21,000 gas 原生转账要花多少钱。

**单位**：TRON 的单价一律以 **SUN** 表示（1 TRX = 1,000,000 SUN）——这是业界惯例，`--fee-limit` 也以 SUN 计价；备注费用属于普通金额，因此按 TRX 显示。EVM 的价格按 **gwei** 显示，费用按原生币显示；json 输出统一使用最小单位（SUN、wei）。

## 选项

没有命令级选项；仅[全局选项](../index.md#global-options-every-command)（`--network`）。

## 示例

```bash
wallet-cli chain prices --network tron:3448148188
```

```console
Energy price     100 SUN / unit    (current)
Bandwidth price  1,000 SUN / unit  (current)
Memo fee         1 TRX
```

```bash
wallet-cli chain prices --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"chain.prices","data":{"energy":{"currentSunPerUnit":100,"history":[{"since":0,"price":100},{"since":1754644200000,"price":100}]},"bandwidth":{"currentSunPerUnit":1000,"history":[{"since":0,"price":10},{"since":1626253800000,"price":1000}]},"memoFeeSun":"1000000"},"meta":{"durationMs":687,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

在 EVM 网络上，给出的则是 gas 价格：

```bash
wallet-cli chain prices --network eip155:11155111
```

```console
Fee model      eip1559
Base fee       0.947033 gwei
Priority fee   0.001 gwei
Gas price      0.948033 gwei
Transfer cost  0.000019 ETH  (21,000 gas)
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"chain.prices","data":{"feeModel":"eip1559","baseFeeWei":"947033827","priorityFeeWei":"1000000","gasPriceWei":"948033827","transferGas":21000,"transferCostWei":"19908710367000"},"meta":{"durationMs":390,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

两个家族的 `data` 没有任何公共字段——请先读 `chain.family`（或 `feeModel`）。

TRON：

| 字段 | 类型 | 含义 |
|---|---|---|
| `energy.currentSunPerUnit` | number | 当前能量单价，每单位多少 SUN |
| `energy.history[]` | array | `{since (epoch 毫秒), price}` 价格时间线 |
| `bandwidth.currentSunPerUnit` | number | 当前带宽单价，每单位多少 SUN |
| `bandwidth.history[]` | array | `{since, price}` 价格时间线 |
| `memoFeeSun` | string | 备注费用，单位 SUN |

EVM：

| 字段 | 类型 | 含义 |
|---|---|---|
| `feeModel` | string | `eip1559` 或 `legacy` |
| `baseFeeWei` | string | 最新区块每单位 gas 的基础费用；仅 EIP-1559 链。基础费用为零时报告为 `"0"`，不会省略 |
| `priorityFeeWei` | string \| null | 节点建议的每单位 gas 小费；节点没有建议时为 `null`。仅在 EIP-1559 链上与 `baseFeeWei` 一同出现 |
| `gasPriceWei` | string | 按上述数字得出的每单位 gas 价格 |
| `transferGas` | number | `21000`——一笔普通原生转账所需的 gas |
| `transferCostWei` | string | `transferGas × gasPriceWei`，即这笔转账现在要花多少 |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`、`timeout`） · `2` 用法错误。

## 另请参见

[`chain params`](params.md) · [`chain node`](node.md) · [能量与带宽](../../concepts/energy-bandwidth.md) · [`tx send`](../tx/send.md)
