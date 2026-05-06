# GetCanDelegatedMaxSize

查询账户当前可代理的最大资源额度（Stake 2.0）。

- 服务：同时支持 `Wallet` 和 `WalletSolidity`

```protobuf
rpc GetCanDelegatedMaxSize (CanDelegatedMaxSizeRequestMessage) returns (CanDelegatedMaxSizeResponseMessage) {}
```

相似 HTTP 接口见 [/wallet/getcandelegatedmaxsize](../../http/stake-v2/getcandelegatedmaxsize.md)。
