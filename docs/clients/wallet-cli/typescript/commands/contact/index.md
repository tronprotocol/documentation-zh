# wallet-cli contact

管理收款方联系人簿。

一个纯本地的收款方地址簿（名称 → 地址），以明文存放在配置目录中，文件权限为 **0600**（仅你本人可读写）。地址会按它所属的家族校验——`T…` 是 TRON，`0x…` 是 EVM——两者可以共存于同一本地址簿。家族并不是联系人记录的一部分——地址本身已经说明了它属于哪条链——但它决定查找行为：一个名称只能在其地址所属家族的网络上解析到。联系人一旦建立，凡是需要收款方的地方都可以直接用它的名称——[`tx send --to`](../tx/send.md) 和 [`gasfree transfer --to`](../gasfree/transfer.md)。

## 用法

```
wallet-cli contact COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `contact add` | [add.md](add.md) | 添加收款方 |
| `contact list` | [list.md](list.md) | 列出收款方 |
| `contact remove` | [remove.md](remove.md) | 移除收款方 |

## 另请参见

[`token`](../token/index.md)——token 地址簿（结构相同） · [`tx send`](../tx/send.md) · [安全](../../concepts/security.md)
