# wallet-cli stake

质押/代理资源，并查看质押状态。

质押生命周期为 `freeze ──► unfreeze ──(waiting period)──► withdraw`。`cancel-unfreeze` 将所有待处理的
解质押恢复为质押状态；`delegate` / `undelegate` 用于代理和收回资源。建议在操作前通过只读命令
`info` 和 `delegated` 查看当前状态。

**仅限 TRON。** 为带宽/能量而做的质押是 TRON 的协议特性；本组每一条子命令在 EVM 网络上都会以 `family_mismatch` 失败。

## 用法

```
wallet-cli stake COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `stake freeze` | [freeze.md](freeze.md) | 质押 TRX 换取能量/带宽 |
| `stake unfreeze` | [unfreeze.md](unfreeze.md) | 解质押 TRX |
| `stake withdraw` | [withdraw.md](withdraw.md) | 提取已到期的解冻 TRX |
| `stake cancel-unfreeze` | [cancel-unfreeze.md](cancel-unfreeze.md) | 取消所有待解锁的解质押 |
| `stake delegate` | [delegate.md](delegate.md) | 将资源代理给其他地址 |
| `stake undelegate` | [undelegate.md](undelegate.md) | 收回已代理的资源 |
| `stake info` | [info.md](info.md) | 质押与资源总览 |
| `stake delegated` | [delegated.md](delegated.md) | 代理明细与最大可代理额度 |

## 另请参见

[质押指南](../../guide/stake-and-resources.md) · [能量与带宽](../../concepts/energy-bandwidth.md) · [`vote`](../vote/index.md)
