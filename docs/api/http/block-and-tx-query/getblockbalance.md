# /wallet/getblockbalance

返回某区块内所有交易引发的余额变动追踪（block balance trace）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBlockBalanceServlet.java`
- Method：`POST`
- Request：`protocol.BlockBalanceTrace.BlockIdentifier`
- Response：`protocol.BlockBalanceTrace`（`balance_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `hash` | string | 是 | 区块哈希 hex |
| `number` | int64 | 是 | 区块高度 |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "hash": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
  "number": 66987565
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `block_identifier.hash` | bytes | 区块哈希 |
| `block_identifier.number` | int64 | 区块高度 |
| `timestamp` | int64 | 区块时间，毫秒 |
| `transaction_balance_trace` | repeated TransactionBalanceTrace | 该区块内每笔交易的余额变动 |

`TransactionBalanceTrace`（`balance_contract.proto`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `transaction_identifier` | bytes | 交易 ID |
| `operation` | repeated Operation | 多个 `(operation_identifier, address, amount)` 三元组 |
| `type` | string | 合约类型，如 `TransferContract` |
| `status` | string | 状态 |

响应示例（截取首笔交易，原响应包含 4 笔）：

```json
{
  "block_identifier": {
    "hash": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
    "number": 66987565
  },
  "timestamp": 1777445121000,
  "transaction_balance_trace": [
    {
      "transaction_identifier": "ff44a2823a870c12f12a4ca6e7647650356bc2bb5e02c5855312cf2db4c950c1",
      "operation": [
        { "operation_identifier": 0, "address": "41f7c3feccb6461aab0fd25f61d9560645b08228cb", "amount": -267000 },
        { "operation_identifier": 1, "address": "41f7c3feccb6461aab0fd25f61d9560645b08228cb", "amount": -848000 },
        { "operation_identifier": 2, "address": "41b06b4139895c9f51c967c9f3d9089ca721e8e34c", "amount": 848000 }
      ],
      "type": "TransferContract",
      "status": "SUCCESS"
    }
  ]
}
```

需开启 `storage.balance.history.lookup = true`（等价启动参数 `--history-balance-lookup`）；否则任意区块查询都会走下方"区块未追踪余额或不存在"那一行的 `ItemNotFoundException`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `BlockIdentifier` 缺失 | `{"Error": "class java.lang.IllegalArgumentException : block_identifier null"}` |
| `number < 0` | `{"Error": "class java.lang.IllegalArgumentException : block_identifier number less than 0"}` |
| `hash` 长度不为 32 字节 | `{"Error": "class java.lang.IllegalArgumentException : block_identifier hash length not equals 32"}` |
| `number` 与 `hash` 不匹配 | `{"Error": "class java.lang.IllegalArgumentException : number and hash do not match"}` |
| 区块未追踪余额或不存在 | `{"Error": "class org.tron.core.exception.ItemNotFoundException : This block does not exist"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
