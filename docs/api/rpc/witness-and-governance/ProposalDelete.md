# ProposalDelete

撤销自己创建的提案（仅提案发起人）。

- 服务：仅支持 `Wallet`

```protobuf
rpc ProposalDelete (ProposalDeleteContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/proposaldelete](../../http/witness-and-governance/proposaldelete.md)。
