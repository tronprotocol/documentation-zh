# wallet-cli token

管理 token 地址簿并查询 token。TRON 与 EVM 均可用。

## 用法

```
wallet-cli token COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `token balance` | [balance.md](balance.md) | 查询单个 token 的余额 |
| `token info` | [info.md](info.md) | 查看 token 元数据 |
| `token add` | [add.md](add.md) | 向地址簿中添加 token |
| `token list` | [list.md](list.md) | 列出地址簿（official + user） |
| `token remove` | [remove.md](remove.md) | 删除一条自行添加的 token |

本组每一条子命令在 TRON 和 EVM 网络上都可运行。`--contract` 在 TRON 上接收 TRC20 地址，在 EVM 上接收 ERC20 地址；`--asset-id`（TRC10）仅限 TRON，用在别处会以 `invalid_option` 被拒绝。地址簿的作用范围是**网络 + 账户**，因此每个网络各有一张表。

## 另请参见

[发送 token](../../guide/send-tokens.md) · [`tx send`](../tx/send.md)
