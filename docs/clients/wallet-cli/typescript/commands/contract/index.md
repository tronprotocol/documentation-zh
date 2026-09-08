# wallet-cli contract

调用、发送、部署、查看并管理智能合约。

调用、发送和部署在 TRON 与 EVM 上都可用。管理类命令仅适用于 TRON，并且只能由部署者操作；它们用于设置调用方承担的能量比例、部署者的能量上限，以及是否在链上保留 ABI。相关交易确认后立即生效。`create2` 与这些设置无关，它只在本地计算一个尚未部署的 TRON 合约地址。

## 用法

```
wallet-cli contract COMMAND
```

## 子命令

| 命令 | 页面 | 说明 | 适用网络 |
|---|---|---|---|
| `contract call` | [call.md](call.md) | 只读合约调用 | TRON、EVM |
| `contract send` | [send.md](send.md) | 改变链上状态的合约调用 | TRON、EVM |
| `contract deploy` | [deploy.md](deploy.md) | 部署合约字节码 | TRON、EVM |
| `contract info` | [info.md](info.md) | 查看合约 ABI 与元数据 | 仅 TRON |
| `contract clear-abi` | [clear-abi.md](clear-abi.md) | 清除链上 ABI（不可逆） | 仅 TRON |
| `contract set-origin-energy-limit` | [set-origin-energy-limit.md](set-origin-energy-limit.md) | 部署者为每次调用承担的能量 | 仅 TRON |
| `contract set-user-resource-percent` | [set-user-resource-percent.md](set-user-resource-percent.md) | 调用方承担的能量比例 | 仅 TRON |
| `contract create2` | [create2.md](create2.md) | 预先计算 CREATE2 地址 | 仅 TRON |

跨家族命令虽然名称相同，参数仍会随链家族变化。`contract call` 是只读操作，只接收调用参数；`contract send` 和 `contract deploy` 会写入链上，因此还需要费用和签名参数：TRON 使用 `--fee-limit` / `--permission-id` / `--expiration`，EVM 使用 `--gas-limit` / `--max-fee` / `--priority-fee` / `--nonce`。把某个家族的参数用于另一个家族会返回 `invalid_option`。标注为**仅 TRON** 的命令在 EVM 上没有对应功能：链上 ABI 登记和「部署者承担能量」属于 TRON 协议特性，TRON 的 CREATE2 地址推导方式也不同于以太坊。在 EVM 网络上运行这些命令会返回 `family_mismatch`。

## 另请参见

[能量与带宽](../../concepts/energy-bandwidth.md) · [`tx status`](../tx/status.md)
