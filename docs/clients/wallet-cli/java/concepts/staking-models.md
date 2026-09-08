# 质押模型：Stake 1.0 与 2.0

wallet-cli 支持两代 TRON 质押机制。新的用法应优先选择 Stake 2.0。

## Stake 1.0（旧版）

最初的模型，由 `freezeBalance` / `unfreezeBalance` 驱动：

- 冻结时需指定 `frozen_duration`，目前只允许为 **3 天**。
- 冻结时间到期后即可解冻；发生解冻操作时，带宽不会被清空。
- 资源代理通过同一组冻结/解冻命令的可选参数 `receiverAddress` 表达。

参见 [commands/stake-v1-legacy](../commands/stake-v1-legacy.md)。

## Stake 2.0（当前）

当前的模型，由 `freezeBalanceV2` / `unfreezeBalanceV2` 驱动，带有资源代理和显式的解绑/提取流程：

- `freezeBalanceV2` 为 BANDWIDTH、ENERGY 或 TRON_POWER 质押 TRX。
- `delegateResource` / `unDelegateResource` 把资源代理给另一个账户（可选择锁定 3 天）。
- `unfreezeBalanceV2` 开始解绑；`withdrawExpireUnfreeze` 在到期后提取相应金额；
  `cancelAllUnfreezeV2` 取消待处理的解冻。
- 专门的 v2 查询命令用于报告代理状态以及可用/可提取金额。

参见 [commands/stake-v2](../commands/stake-v2.md)。

## 另请参见

- [concepts/resources](resources.md)——份额、带宽和能量是什么
