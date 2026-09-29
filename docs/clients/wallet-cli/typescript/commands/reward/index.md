# wallet-cli reward

查询 / 提取投票奖励。

奖励会随着你的投票（[`vote cast`](../vote/cast.md)）持续累积——如果你是 SR，还包括出块奖励——并且**每 24 小时最多只能提取一次**（这是链上规则；提前尝试会被拒绝）。

> **仅限 TRON。** 本组的每条命令实现的都是 TRON 独有的协议特性，EVM 上没有对应物；在 EVM 网络上，它们会在任何节点调用之前就以 `family_mismatch` 失败。

## 用法

```
wallet-cli reward COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `reward balance` | [balance.md](balance.md) | 显示可领取的奖励和提取状态 |
| `reward withdraw` | [withdraw.md](withdraw.md) | 把累积的奖励提取到余额 |

## 另请参见

[`vote`](../vote/index.md) · [`stake info`](../stake/info.md)
