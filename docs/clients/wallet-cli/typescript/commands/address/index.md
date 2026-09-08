# wallet-cli address

生成随机密钥对（本地，不保存）。

一个纯本地的工具组——它从不访问节点。生成的密钥**不会**存入钱包；要用它签名，请用 [`import private-key`](../import/private-key.md) 导入。

## 用法

```
wallet-cli address COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `address generate` | [generate.md](generate.md) | 生成随机密钥对，并打印 TRON 和 EVM 地址 |

## 另请参见

[`encoding convert`](../encoding/convert.md) · [`create`](../create.md) · [`import private-key`](../import/private-key.md)
