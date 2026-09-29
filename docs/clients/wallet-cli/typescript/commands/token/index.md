# wallet-cli token

管理 token 地址簿并查询 token。

## 用法

```
wallet-cli token COMMAND
```

## 网络

全部五条子命令在 TRON 和 EVM 网络上都可运行——TRON 上是 TRC20/TRC10，EVM 上是 ERC20。地址簿按**网络 + 账户**分别存储，因此同一条命令在 `tron:3448148188` 和 `eip155:11155111` 上列出的 token 并不相同。只有 `--asset-id`（TRC10）仅限 TRON：`--help` 会为它标注 `(TRON only)`，在 EVM 网络上传入它会在任何节点调用之前就以 `invalid_option` 失败。

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `token balance` | [balance.md](balance.md) | 查询单个 token 的余额（`--contract` / `--asset-id`） |
| `token info` | [info.md](info.md) | 从链上读取 token 元数据 |
| `token add` | [add.md](add.md) | 把某个 token 加入地址簿，并抓取它的元数据 |
| `token list` | [list.md](list.md) | 列出地址簿（官方 + 用户） |
| `token remove` | [remove.md](remove.md) | 移除用户添加的 token |

## 另请参见

[发送 token](../../guide/send-tokens.md) · [`tx send`](../tx/send.md)
