# VoteWitnessAccount2

为超级代表（SR）投票。一次性覆盖账户当前所有投票。

- 服务：仅支持 `Wallet`

```protobuf
rpc VoteWitnessAccount2 (VoteWitnessContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/votewitnessaccount](../../http/witness-and-governance/votewitnessaccount.md)。
