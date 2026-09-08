# wallet-cli chain

查询链与节点状态。

三个只读查询，用于费用估算、质押/投票决策和故障排查。注意与 [`networks`](../networks.md) 区分：后者只列出本地已知的网络，不访问任何节点；而 `chain` 查询的是 `--network` 选中的那个节点。

## 用法

```
wallet-cli chain COMMAND
```

## 子命令

| 命令 | 页面 | 说明 | 适用网络 |
|---|---|---|---|
| `chain params` | [params.md](params.md) | 链上治理参数 | 仅 TRON |
| `chain prices` | [prices.md](prices.md) | 当前的交易单价 | TRON、EVM |
| `chain node` | [node.md](node.md) | 所连节点的状态 | TRON、EVM |

`chain params` 仅限 TRON——由超级代表治理的系统参数在 EVM 上没有对应物，因此在 EVM 网络上会以 `family_mismatch` 失败。`chain prices` 按所选网络的费用模型作答，**每个家族返回的字段集合不同**：TRON 上是能量/带宽单价，EVM 上是 gas 价格。

## 另请参见

[`networks`](../networks.md) · [能量与带宽](../../concepts/energy-bandwidth.md) · [故障排查](../../troubleshooting.md)
