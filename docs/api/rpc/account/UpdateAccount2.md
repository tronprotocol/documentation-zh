# UpdateAccount2

修改账户昵称（account_name）。该字段不唯一。

- 服务：仅支持 `Wallet`

```protobuf
rpc UpdateAccount2 (AccountUpdateContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/updateaccount](../../http/account/updateaccount.md)。
