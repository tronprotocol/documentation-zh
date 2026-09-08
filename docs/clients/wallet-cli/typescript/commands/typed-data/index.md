# wallet-cli typed-data

签名 EIP-712 / TIP-712 结构化数据。

## 用法

```
wallet-cli typed-data COMMAND
```

## 子命令

| 命令 | 页面 | 说明 | 适用网络 |
|---|---|---|---|
| `typed-data sign` | [sign.md](sign.md) | 签名 EIP-712 / TIP-712 结构化数据 | TRON、EVM |

签名完全在本地完成——不访问任何节点。所选网络决定用该账户的哪把密钥签名、以及报告哪个地址。

## 另请参见

[`message sign`](../message/sign.md)——签名纯文本消息 · [安全模型](../../concepts/security.md)
