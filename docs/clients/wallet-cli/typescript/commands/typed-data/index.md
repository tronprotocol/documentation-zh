# wallet-cli typed-data

签名 EIP-712 / TIP-712 结构化数据。

## 用法

```
wallet-cli typed-data COMMAND
```

在 TRON 和 EVM 网络上都可运行。EIP-712 与 TIP-712 是同一套构造，因此同一份载荷对两者都能签名；用账户的哪一把密钥，由所选网络决定。

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `typed-data sign` | [sign.md](sign.md) | 对 EIP-712 / TIP-712 结构化数据签名 |

## 另请参见

[`message sign`](../message/sign.md)——签名纯文本消息 · [安全模型](../../concepts/security.md)
