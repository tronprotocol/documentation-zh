# GetAccountNet

查询账户的带宽（Net）资源使用情况。**已弃用**，推荐使用 `GetAccountResource`。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetAccountNet (Account) returns (AccountNetMessage) {}
```
