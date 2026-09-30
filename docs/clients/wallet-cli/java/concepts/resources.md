# 资源：带宽、能量与 TRON Power

TRON 账户通过 `freezeBalanceV2`（Stake 2.0）**质押** TRX 来获得资源。本页汇总各操作页面所引用的机制。命令本身见 [commands/stake-v2](../commands/stake-v2.md)。

## 质押能带来什么

| 资源 | 由什么消耗 | 如何获得 |
|---|---|---|
| **带宽（Bandwidth）** | 你广播的每一笔交易，按其字节数计 | 为 `BANDWIDTH` 质押（ResourceCode 0），另有每日免费额度 |
| **能量（Energy）** | 仅智能合约执行，包括 TRC20 转账 | 为 `ENERGY` 质押（ResourceCode 1） |
| **TRON Power** | 为超级代表[投票](../commands/vote-reward.md#how-to-vote) | 为 `TRON_POWER` 质押（ResourceCode 2）——质押 1 TRX = 1 票 |

质押的 TRX 仍然归你所有；它是被锁定，而不是被花掉。解质押（`unfreezeBalanceV2`）会立即失去相应资源，并让这笔 TRX 进入一段等待期后才能提取；用已解质押的 TRON Power 投出的票也会失效。

查询类命令（`getaccount`、`getblock` 等）只是读取节点，不是交易，不消耗任何资源。

## 带宽是怎么被消耗的

一笔交易消耗的带宽等于**已签名交易的字节数**——一笔普通的 TRX 转账在几百字节量级。并不存在一个固定的每笔交易数值；签名更多、或带了备注的交易体积更大，消耗也更多。

节点会按顺序动用三种来源：

1. **每日免费额度**——即链参数 `getFreeNetLimit`，当前主网为每天 600 字节。TRC10 转账可以先动用发行方的 `free_asset_net_limit`。
2. **质押得来的带宽**，它会在 24 小时内逐步恢复。
3. 仍未覆盖的部分通过**燃烧 TRX** 支付，按 `getTransactionFee` 计价——当前主网为每字节 1,000 SUN。

能量在第三步的机制相同，按 `getEnergyFee` 燃烧（当前主网为每点能量 100 SUN），但它没有免费额度：没有质押能量的账户，每一次合约调用都要用 TRX 支付。

## 一笔质押能换来多少带宽或能量

质押并不会买到一个固定的数量。每种资源都是**一个全网固定的池子，按所有人质押量的占比来分配**：

```
your bandwidth = getTotalNetLimit           * yourBandwidthStake / totalBandwidthStaked
your energy    = getTotalEnergyCurrentLimit * yourEnergyStake    / totalEnergyStaked
```

当前主网上，这两个池子分别是 43,200,000,000 带宽和 180,000,000,000 能量。由于分母是其他所有人的质押量，全网质押越多，同样的质押换来的就越少——请用 `getaccountresource` 查看你实际持有多少，而不要去推算一个理论值。

上面提到的每个数值都是链参数，超级代表可以通过提案修改它们。请用 [`GetChainParameters`](../commands/chain-data.md#getchainparameters) 读取当前值，不要写死。

## Stake 1.0：过去是怎么做的

在 Stake 2.0 之前，`freezeBalance` 需要一个 `frozen_duration`（3 天），每次冻结都是与该时长绑定的独立仓位，到期后各自解冻。那些把带宽描述为 `常数 * 冻结金额 * 天数` 的说法，就来自这套模型。

`freezeBalanceV2` 不再接收时长参数——它只接收数量和资源类型——现在适用的是上文那套按占比分配的规则。Stake 1.0 的命令仍然保留，用于了结旧仓位；见 [commands/stake-v1-legacy](../commands/stake-v1-legacy.md)。

## 资源价格

带宽和能量的历史单价以及备注费均可查询——参见 [commands/resources](../commands/resources.md)。

## 另请参见

- [commands/stake-v2](../commands/stake-v2.md)——当前的质押模型
- [commands/stake-v1-legacy](../commands/stake-v1-legacy.md)——旧版冻结
- [concepts/staking-models](staking-models.md)
