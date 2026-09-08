# wallet-cli account

查询链上账户状态，以及激活账户和为账户命名。

## 用法

```
wallet-cli account COMMAND
```

子命令默认作用于**当前账户**；可用 `--account <accountId|label>` 覆盖，或用 `wallet-cli use <account>` 更改默认值。查询的是哪个地址取决于所选网络所属的链家族——同一个账户既有 TRON 的 base58 地址，也有 EVM 的 `0x` 地址。前四条是只读查询；`activate` 和 `set` 会改变链上状态。软件签名需要 master password，Ledger 签名需在设备上确认，而 `--dry-run` / `--build-only` 不会解锁钱包。

## 子命令

| 命令 | 说明 | 适用网络 | 数据来源 |
|---|---|---|---|
| [`account balance`](balance.md) | 原生代币余额 | TRON、EVM | 节点 RPC |
| [`account info`](info.md) | 链上账户状态（TRON 还包含带宽/能量） | TRON、EVM | 节点 RPC |
| [`account history`](history.md) | 交易历史 | 仅 TRON | **需要 TronGrid** |
| [`account portfolio`](portfolio.md) | 原生 + token 余额，尽力而为的 USD 估值 | TRON、EVM | 节点 RPC + 价格源 |
| [`account activate`](activate.md) | 激活尚不存在的账户（不转账） | 仅 TRON | 广播 |
| [`account set`](set.md) | 设置链上名称 / 账户 id（一次性） | 仅 TRON | 广播 |

**仅 TRON** 的命令若在 EVM 网络上执行，会在任何节点调用之前就以 `family_mismatch` 失败。

## 另请参见

[`list`](../list.md)——本地账户（不访问链） · [网络与资源](../../concepts/networks.md)
