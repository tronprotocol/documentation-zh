# wallet-cli contract

调用、发送、部署、查看并管理智能合约。

真正起治理作用的是部署者那一侧：一次调用的能量由谁承担，以及该合约是否在链上保留 ABI。这些设置属于 TRON，归属部署该合约的账户，并在交易确认后立即生效。`create2` 与这些都无关——它只是对一个尚不存在的地址做的本地运算。

## 用法

```
wallet-cli contract COMMAND
```

## 子命令

| 命令 | 页面 | 说明 | 网络 |
|---|---|---|---|
| `contract call` | [call.md](call.md) | 只读调用 | TRON、EVM |
| `contract send` | [send.md](send.md) | 会改变状态的调用 | TRON、EVM |
| `contract deploy` | [deploy.md](deploy.md) | 部署智能合约 | TRON、EVM |
| `contract info` | [info.md](info.md) | 显示合约 ABI + 元数据 | 仅 TRON |
| `contract clear-abi` | [clear-abi.md](clear-abi.md) | 清除链上 ABI（不可逆） | 仅 TRON |
| `contract set-origin-energy-limit` | [set-origin-energy-limit.md](set-origin-energy-limit.md) | 每次调用中由部署者承担的能量 | 仅 TRON |
| `contract set-user-resource-percent` | [set-user-resource-percent.md](set-user-resource-percent.md) | 一次调用的能量中由调用者承担的比例 | 仅 TRON |
| `contract create2` | [create2.md](create2.md) | 在本地计算 CREATE2 地址 | 仅 TRON |

`call`、`send` 和 `deploy` 在两个家族上都可运行；其余命令实现的是 TRON 独有的协议特性，EVM 上没有对应物，在那里会以 `family_mismatch` 失败。这三条通用命令共享的是家族，而不是参数：`contract call` 是只读的，接收调用入参；而 `contract send` 和 `contract deploy` 是写入交易，带有费用与签名相关的一整套词汇——TRON 上是 `--fee-limit` / `--permission-id` / `--expiration`，EVM 上是 `--gas-limit` / `--max-fee` / `--priority-fee` / `--nonce`，各自在另一个家族上都会以 `invalid_option` 被拒绝。

## 另请参见

[能量与带宽](../../concepts/energy-bandwidth.md) · [`tx status`](../tx/status.md)
