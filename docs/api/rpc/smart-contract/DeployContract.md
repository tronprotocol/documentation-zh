# DeployContract

部署智能合约。返回未签名的部署交易。

- 服务：仅支持 `Wallet`

```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```

构造 `CreateSmartContract` 时，请确保 `new_contract.name` 不超过 32 字节。该限制按 UTF-8 编码后的字节数计算，而不是按字符数计算。例如，大多数汉字在 UTF-8 编码中各占三个字节。

请将 `new_contract.code_hash` 和 `new_contract.trx_hash` 留空。这两个字段预留给节点设置；`VERSION_4_8_2_2` 升级生效后，如果任一字段非空，部署将失败。

相似 HTTP 接口见 [/wallet/deploycontract](../../http/smart-contract/deploycontract.md)。
