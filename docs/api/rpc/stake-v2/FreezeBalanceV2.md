# FreezeBalanceV2

冻结 TRX 获取带宽 / 能量 / TronPower（Stake 2.0）。无固定冻结期。

- 服务：仅支持 `Wallet`

```protobuf
rpc FreezeBalanceV2 (FreezeBalanceV2Contract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/freezebalancev2](../../http/stake-v2/freezebalancev2.md)。
