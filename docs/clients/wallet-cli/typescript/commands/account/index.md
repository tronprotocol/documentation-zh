# wallet-cli account

查询链上账户状态，以及激活账户和为账户命名。

## 用法

```
wallet-cli account COMMAND
```

各子命令默认作用于**当前账户**；可用 `--account <accountId|label>` 覆盖，或用 `wallet-cli use <account>` 更改默认账户。前四条是只读查询；`activate` 和 `set` 会改变链上状态。软件签名需要 master password，Ledger 签名在设备上确认，而 `--dry-run` / `--build-only` 从不解锁钱包。

## 网络

`balance`、`info` 和 `portfolio` 在 TRON 和 EVM 网络上都可运行，按家族各自报告相应字段。`history`、`activate` 和 `set` **仅限 TRON**，在 EVM 网络上会以 `family_mismatch` 失败。参见[哪些命令能在哪些网络上运行](../index.md#which-commands-run-on-which-networks)。

## 子命令

| 命令 | 说明 | 数据来源 |
|---|---|---|
| [`account balance`](balance.md) | 原生币余额 | 节点 RPC |
| [`account info`](info.md) | 链上账户状态——TRON 上是资源，EVM 上是 nonce 和合约代码 | 节点 RPC |
| [`account history`](history.md) | 交易历史 | **需要 TronGrid** |
| [`account portfolio`](portfolio.md) | 原生币 + token 余额，并尽力给出 USD 估值 | 节点 RPC + 价格源 |
| [`account activate`](activate.md) | 激活一个尚不存在的账户（不转移资产） | 广播 |
| [`account set`](set.md) | 设置链上名称 / 账户 id（一次性） | 广播 |

## 另请参见

[`list`](../list.md)——本地账户（不访问链） · [网络与资源](../../concepts/networks.md)
