# wallet-cli vote

为超级代表（SR）投票。

投票消耗的是 **Tron Power（TP）**：1 TP = 质押 1 TRX（见 [`stake freeze`](../stake/freeze.md)）。票数在下一个维护周期（约 6 小时）统计，之后便持续产生奖励——用 [`reward`](../reward/index.md) 查询和领取。

**仅限 TRON。** 超级代表投票是 TRON 的协议特性；本组每一条子命令在 EVM 网络上都会以 `family_mismatch` 失败。

## 用法

```
wallet-cli vote COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `vote cast` | [cast.md](cast.md) | 投出/替换你的完整票数分配 |
| `vote list` | [list.md](list.md) | 列出超级代表和候选人 |
| `vote status` | [status.md](status.md) | 你当前的投票、投票权与奖励概览 |

## 另请参见

[`reward`](../reward/index.md) · [`stake info`](../stake/info.md) · [质押与资源](../../guide/stake-and-resources.md)
