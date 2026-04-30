# DeployContract

部署智能合约。返回未签名的部署交易。

- 服务：仅支持 `Wallet`

```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```
