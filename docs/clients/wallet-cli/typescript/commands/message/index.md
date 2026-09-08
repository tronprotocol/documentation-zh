# wallet-cli message

对任意消息进行签名。

## 用法

```
wallet-cli message COMMAND
```

## 子命令

| 命令 | 页面 | 说明 | 适用网络 |
|---|---|---|---|
| `message sign` | [sign.md](sign.md) | 对任意消息签名（TIP-191/V2 · EIP-191） | TRON、EVM |

签名完全在本地完成——不访问任何节点。所选网络决定用该账户的哪把密钥签名、以及报告哪个地址。

## 另请参见

[安全模型](../../concepts/security.md)
