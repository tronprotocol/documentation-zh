# ProposalApprove

SR 对提案投票（赞成/取消赞成）。

- 服务：仅支持 `Wallet`

```protobuf
rpc ProposalApprove (ProposalApproveContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/proposalapprove](../../http/witness-and-governance/proposalapprove.md)。
