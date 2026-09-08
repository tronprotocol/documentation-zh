# 能量与带宽

本页介绍 TRON 的费用模型，以及使用 `stake` 的原因。**仅限 TRON**——EVM 网络使用 gas 为交易计价，参见[网络 → `evm-gas` 模型](networks.md#fees-the-evm-gas-model)。基本单位为 **1 TRX = 1,000,000 SUN**，所有名为 `*-sun` 的 CLI 参数都以 SUN 计。JSON 中的数值同样使用 SUN，但类型并不统一：余额等 int64 量级的金额为十进制字符串，`feeSun`、`multiSignFeeSun`、`energyUsed`、`netUsed` 等有界的计数和费用则可能是 JSON 数字。请以各命令的字段表为准，不要假定它们采用同一种类型；参见 [machine-interface](../machine-interface.md#the-result-envelope)。

## 用两种资源代替 gas

| 资源 | 由什么消耗 | 免费额度 |
|---|---|---|
| **带宽** | 每笔交易的字节数 | 每个账户每天有少量配额 |
| **能量** | 智能合约执行（包括 TRC20 转账） | 无 |

当交易所需资源超过账户现有额度时，节点会从余额中**燃烧 TRX** 来补足差额。对于合约调用，`--fee-limit`（用于 `tx send` / `contract` 命令，默认 100000000 SUN）用于限制最多可燃烧的 TRX，避免有缺陷或恶意的合约无限制消耗能量。

可以随时查看当前资源状态：

```bash
wallet-cli account info --network tron:3448148188 -o json | jq '.data.resources'
```

```json
{ "bandwidth": { "used": 0, "limit": 600 }, "energy": { "used": 0, "limit": 888 } }
```

## 如何获得资源：质押

质押会锁定 TRX（它仍然属于你），换来持续的资源配额以及 TRON Power（治理投票权）。`stake` 命令组与链上操作一一对应：

| 命令 | 链上操作 | 效果 |
|---|---|---|
| `stake freeze` | FreezeBalanceV2 | 为 `--resource energy\|bandwidth` 锁定 TRX |
| `stake unfreeze` | UnfreezeBalanceV2 | 请求解锁；资源立即下降，TRX 进入**等待期**（主网 14 天） |
| `stake withdraw` | WithdrawExpireUnfreeze | 领取等待期已过的解质押 |
| `stake cancel-unfreeze` | CancelAllUnfreezeV2 | 把**所有**待处理的解质押回滚为已质押 |
| `stake delegate` | DelegateResourceV2 | 把资源配额借给 `--receiver`（可选 `--lock`，锁定 `--lock-period` 个区块，约 3 秒/区块） |
| `stake undelegate` | UnDelegateResourceV2 | 收回一笔代理 |

代理转移的是**资源配额**，而不是 TRX——质押始终留在所有者账户上。一种常见配置是：冷账户持有质押，并把能量代理给负责发起交易的热账户。

## 实际影响

- “免费”的 TRX 转账并不一定免费：超出带宽配额后仍会燃烧 TRX。
- 能量不足时，TRC20 转账会燃烧更多 TRX。操作前可通过 `--dry-run` 的 `fee` 字段查看预估费用。
- 发送时出现提到 bandwidth/energy/balance 的 `rpc_error` → 请充值、质押，或者等待每日配额刷新；见[故障排查](../troubleshooting.md#rpc_error-exit-1)。

## 另请参见

[质押实操](../guide/stake-and-resources.md) · [网络](networks.md) · [`account info`](../commands/account/info.md)
