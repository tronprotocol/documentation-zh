# 多重签名概念

多重签名允许多个密钥共同管理一个账户。这是[多签命令](../commands/multisig.md)背后的权限模型。

## 权限类型

访问权限分为三类：

- **owner**——账户的最高权限，可用于修改整个权限结构。
- **active**——用于授权转账、质押等具体操作，可通过 `operations` 字段限制允许执行的操作类型；不包含
  见证人出块权限。
- **witness**——仅供见证人账户使用，用于授权出块密钥。

如果一个账户不是见证人，就不需要设置 `witness_permission`，否则会报错。

## 密钥、权重与阈值

一个权限会列出一个或多个密钥，每个密钥带有一个**权重（weight）**，以及一个**阈值（threshold）**。
当收集到的签名的权重之和达到阈值时，该权限下的交易即为有效。

例如，如果某个权限把 active 访问权授予两个账户、各自权重为 1、阈值为 2，那么两者都必须签名，交易
才会生效。签名可以在同一个 CLI 上收集，也可以在多个 CLI 上通过对交易十六进制字符串执行
`addTransactionSign` 来收集——之后手动广播最终交易。

你可以用以下命令查看进度：

- [`getTransactionSignWeight`](../commands/multisig.md#gettransactionsignweight)——当前累计权重与
  权限阈值的对比。
- [`getTransactionApprovedList`](../commands/multisig.md#gettransactionapprovedlist)——哪些账户
  已经批准。

## 另请参见

- [commands/multisig](../commands/multisig.md)——命令本身
