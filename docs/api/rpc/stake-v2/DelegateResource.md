# DelegateResource

把已冻结资源代理给其他账户使用（Stake 2.0）。

- 服务：仅支持 `Wallet`

```protobuf
rpc DelegateResource (DelegateResourceContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/delegateresource](../../http/stake-v2/delegateresource.md)。
