# wallet-cli chain params

显示链上治理参数。

## 用法

```
wallet-cli chain params [--key <name>] [options]
```

## 说明

列出链的治理参数——由 SR 提案修改的全网系统设置（参见 [`proposal create`](../proposal/create.md)）；本命令只负责读取。**仅限 TRON**：EVM 网络没有这样一套参数，会以 `family_mismatch` 失败。`--key` 只返回其中一个。参数键原样透传，与链返回的完全一致；文本输出会为已知的数值型键加上千位分隔符和单位（SUN / ms），`-o json` 保留原始值。

常用的键：

| 键 | 含义 |
|---|---|
| `getEnergyFee` | 能量单价（SUN/能量）——能量不足时按此价燃烧 TRX；费用估算的核心输入 |
| `getTransactionFee` | 带宽单价（SUN/字节）——免费带宽用尽后按此价燃烧 |
| `getCreateAccountFee` | 系统侧的账户创建费（SUN）——向全新地址转账时额外开销的一部分 |
| `getWitnessPayPerBlock` | SR 每出一个块的奖励（SUN）——投票奖励池的来源 |
| `getMaintenanceTimeInterval` | 维护周期长度（ms；21,600,000 = 6 小时）——票数统计 / SR 排名的周期 |

若想以更友好的形式查看与费用相关的单价，请用 [`chain prices`](prices.md)。

## 选项

| 选项 | 说明 |
|---|---|
| `--key <string>` | 只返回这一个参数（例如 `getEnergyFee`） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

用 `--key` 查询单个参数：

```bash
wallet-cli chain params --key getEnergyFee --network tron:3448148188
```

```console
Key    getEnergyFee
Value  210 SUN
```

全部参数（节选）：

```bash
wallet-cli chain params --network tron:3448148188
```

```console
| Key                        | Value          |
| -------------------------- | -------------- |
| getEnergyFee               | 210 SUN        |
| getTransactionFee          | 1,000 SUN      |
| getCreateAccountFee        | 100,000 SUN    |
| getWitnessPayPerBlock      | 16,000,000 SUN |
| getMaintenanceTimeInterval | 21,600,000 ms  |
```

```bash
wallet-cli chain params --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"chain.params","data":{"params":[{"key":"getEnergyFee","value":210},{"key":"getTransactionFee","value":1000},{"key":"getCreateAccountFee","value":100000}]},"meta":{"durationMs":19,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data.params[]`——每个参数一条：

| 字段 | 类型 | 含义 |
|---|---|---|
| `key` | string | 参数名，与链上返回的完全一致 |
| `value` | number | 链上原始值，不带单位后缀（单位由文本输出补上：SUN / ms）。若节点报告某参数时不带值，该字段会整个缺席。承载它的端口类型标注为 `number \| string`，但其背后的 TronWeb 网关只会给出数字 |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`not_found`——`--key` 指定的参数不存在；`invalid_value`）。

## 另请参见

[`chain prices`](prices.md) · [`chain node`](node.md)
