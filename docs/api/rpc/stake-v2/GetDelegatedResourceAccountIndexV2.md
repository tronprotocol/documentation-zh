# GetDelegatedResourceAccountIndexV2

查询账户作为出借方/接收方的代理对手地址列表（Stake 2.0）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetDelegatedResourceAccountIndexV2 (BytesMessage) returns (DelegatedResourceAccountIndex) {}
```

相似 HTTP 接口见 [/wallet/getdelegatedresourceaccountindexv2](../../http/stake-v2/getdelegatedresourceaccountindexv2.md)。
