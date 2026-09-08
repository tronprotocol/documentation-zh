# wallet-cli proposal

创建治理提案并对提案投票。

提案是一组**链参数变更**——就是 [`chain params`](../chain/params.md) 报告的那些参数——由超级代表投票决定。读取提案对所有人开放；创建、批准和删除提案则要求是已注册的见证人（[`witness create`](../witness/create.md)）。

决定各个子命令行为的几条机制：

- **只有批准和撤销批准两种动作。** 不存在"反对"票——超级代表要么投出批准，要么把批准撤回。
- **不会提前结算。** 提案会一直停留在投票窗口内直到 `expiration_time`，即使批准数早已够了；它在随后的维护周期才被统计。
- **只有前 27 名活跃超级代表算数。** 任何已注册的见证人都可以批准，交易也会成功，但统计时只筛选活跃超级代表，且需要达到其中的 ≥ 70 %。
- **通过的变更在计票完成时立即生效**。

状态：`voting`（仍在窗口内） · `approved`（达到阈值、已生效、终态） · `disapproved`（到期时未达阈值、终态） · `canceled`（创建者在到期前撤回、终态）。

**仅限 TRON。** 链上参数治理是 TRON 的协议特性；本组每一条子命令在 EVM 网络上都会以 `family_mismatch` 失败。

## 用法

```
wallet-cli proposal COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `proposal list` | [list.md](list.md) | 列出提案及其批准进度 |
| `proposal show` | [show.md](show.md) | 单个提案的完整详情 |
| `proposal create` | [create.md](create.md) | 创建变更链参数的提案 |
| `proposal approve` | [approve.md](approve.md) | 批准提案，或取消你的批准 |
| `proposal delete` | [delete.md](delete.md) | 删除你创建的提案 |

## 另请参见

[`witness`](../witness/index.md) · [`chain params`](../chain/params.md) · [`vote list`](../vote/list.md)
