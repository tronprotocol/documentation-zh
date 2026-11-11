# GetBlockBalanceTrace

返回区块余额变动追踪，仅包含记录了 TRX 余额变动的交易。请通过 `transaction_identifier` 匹配条目；列表不一定包含区块内的所有交易。

- 服务：仅支持 `Wallet`

```protobuf
rpc GetBlockBalanceTrace (BlockBalanceTrace.BlockIdentifier) returns (BlockBalanceTrace) {}
```

相似 HTTP 接口见 [/wallet/getblockbalance](../../http/block-and-tx-query/getblockbalance.md)。
