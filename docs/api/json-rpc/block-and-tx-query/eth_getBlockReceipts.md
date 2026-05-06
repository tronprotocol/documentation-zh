# eth_getBlockReceipts

按高度 / hash / tag 查询整块的所有交易回执。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getBlockReceipts`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | string | 是 | 区块 hash（64 hex 字符）/ 区块高度（hex）/ tag（`latest` / `earliest` / `finalized`；`pending` 显式不支持） |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockReceipts","params":["0x3fe1ca0"],"id":1}'
```

## 响应

`TransactionReceipt` 数组（字段见 [`eth_getTransactionReceipt`](eth_getTransactionReceipt.md)），按交易在块内的下标顺序排列。`cumulativeGasUsed` 累加自第 0 笔交易。

特殊情形：

- 块不存在 → `null`
- **0 号块（创世块）** → `null`
- lite fullnode 已剪枝该块 → `null`

下例为上面 curl 调用 Nile testnet 抓回的真实响应（块 `0x3fe1ca0` 共 4 笔交易：1 笔合约调用 + 3 笔 TRX 转账）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
      "blockNumber": "0x3fe1ca0",
      "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
      "transactionIndex": "0x0",
      "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
      "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "gasUsed": "0xae29",
      "cumulativeGasUsed": "0xae29",
      "effectiveGasPrice": "0x64",
      "contractAddress": null,
      "logs": [
        {
          "address": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
          "topics": [
            "0xc66625d03b4a832d8245f0df593e32e0fbbbad96d4aa45440aa1535b80983083",
            "0x000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
            "0x0000000000000000000000000000000000000000000000000000000000000007"
          ],
          "data": "0x0000...05f",
          "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
          "blockNumber": "0x3fe1ca0",
          "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
          "transactionIndex": "0x0",
          "logIndex": "0x0",
          "removed": false
        }
      ],
      "logsBloom": "0x0000...0000",
      "status": "0x1",
      "type": "0x0"
    },
    {
      "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
      "blockNumber": "0x3fe1ca0",
      "transactionHash": "0x74034bfbb426506e7a0a3c0f329ca84cc9c7783f4307137dcc2fdbb184a9910e",
      "transactionIndex": "0x1",
      "from": "0xf7c3feccb6461aab0fd25f61d9560645b08228cb",
      "to": "0xb06b4139895c9f51c967c9f3d9089ca721e8e34c",
      "gasUsed": "0x0",
      "cumulativeGasUsed": "0xae29",
      "effectiveGasPrice": "0x64",
      "contractAddress": null,
      "logs": [],
      "logsBloom": "0x0000...0000",
      "status": "0x1",
      "type": "0x0"
    }
  ]
}
```

> 实际返回包含全部 4 笔回执，此处仅展示前 2 笔以节省篇幅。`cumulativeGasUsed` 在 index `0x1` 之后保持 `0xae29`，因为该块仅 index `0x0` 的合约调用消耗了 energy（`0xae29`），后续 3 笔 TRX 转账 `gasUsed` 均为 `0x0`。`logsBloom` 实际为 256 字节全 0；其它字段为节点真实返回值。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `params[0]` 既不是 hash-shaped 也不是合法 hex 高度 / tag | `-32602` | `invalid block number` |
| `params[0]` 是 hash-shaped（`(0x)?[a-zA-Z0-9]{64}`）但含非 hex 字符 | `-32602` | 透传 `ByteArray.fromHexString` 异常 message |
| `params[0]` 是 `pending` | `-32602` | `TAG pending not supported` |
| 区块交易列表与 `TransactionInfoList` 长度不一致（不应发生，仅作为防御性校验） | `-32000` | `TransactionList size mismatch: block has %d transactions, but transactionInfoList has %d` |
