# CancelAllUnfreezeV2

取消账户所有未到期的解冻申请，未到期部分重新转为冻结状态，已到期部分自动提取到余额。

- 服务：仅支持 `Wallet`

```protobuf
rpc CancelAllUnfreezeV2 (CancelAllUnfreezeV2Contract) returns (TransactionExtention) {}
```
