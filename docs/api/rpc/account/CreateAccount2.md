# CreateAccount2

创建一个新账户的未签名交易。被动激活：付费方（owner_address）支付激活费用，新账户地址（account_address）即被创建。

- 服务：仅支持 `Wallet`

```protobuf
rpc CreateAccount2 (AccountCreateContract) returns (TransactionExtention) {}
```
