# wallet-cli contact

管理收款方联系人簿。

一个纯本地的收款方地址簿（名称 → 地址），以明文存放在配置目录中，文件权限为 **0600**（只有你本人可读写）。每个条目属于一个链家族——`tron` 或 `evm`，由地址自动识别——因此某个名称只能在该家族的网络上解析。联系人一旦存在，凡是需要填收款方的地方都可以直接用它的名称——[`tx send --to`](../tx/send.md) 和 [`gasfree transfer --to`](../gasfree/transfer.md)。

## 用法

```
wallet-cli contact COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `contact add` | [add.md](add.md) | 向地址簿中添加一个收款方 |
| `contact list` | [list.md](list.md) | 列出全部联系人 |
| `contact remove` | [remove.md](remove.md) | 删除一个联系人 |

## 另请参见

[`token`](../token/index.md)——token 地址簿（结构相同） · [`tx send`](../tx/send.md) · [安全](../../concepts/security.md)
