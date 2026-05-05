# GetAccountNet

查询账户的带宽（Net）资源使用情况。**已弃用**，推荐使用 [`GetAccountResource`](GetAccountResource.md)。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetAccountNet (Account) returns (AccountNetMessage) {}
```

相似 HTTP 接口见 [/wallet/getaccountnet](../../http/account/getaccountnet.md)。
