# DeployContract

部署智能合约。返回未签名的部署交易。

- 服务：仅支持 `Wallet`

```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```

相似 HTTP 接口见 [/wallet/deploycontract](../../http/smart-contract/deploycontract.md)。
