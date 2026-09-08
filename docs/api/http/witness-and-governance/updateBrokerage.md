# /wallet/updateBrokerage

SR 修改分红比例（佣金）。

- 源码：`framework/src/main/java/org/tron/core/services/http/UpdateBrokerageServlet.java`
- Method：`POST`
- Contract：`protocol.UpdateBrokerageContract`（`storage_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | SR 地址 |
| `brokerage` | int32 | 否 | 新佣金百分比 0–100；省略时默认为合法值 `0` |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updateBrokerage \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "brokerage": 20
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "63732aa3bc1e95227af2d09782d430f7032ee9500bf035d4fd82001f50744745",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "brokerage": 20,
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
          },
          "type_url": "type.googleapis.com/protocol.UpdateBrokerageContract"
        },
        "type": "UpdateBrokerageContract"
      }
    ],
    "ref_block_bytes": "27c9",
    "ref_block_hash": "c22bba19ac9d6cf3",
    "expiration": 1777446471000,
    "timestamp": 1777446411781
  },
  "raw_data_hex": "0a0227c92208c22bba19ac9d6cf340d88ac3c0dd335a55083112510a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e55706461746542726f6b6572616765436f6e747261637412190a15419c7c7049d26108be0dcb5f78479c6ff27ba101d110147085bcbfc0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 链未启用 ChangeDelegation 提案 | `{"Error": "class org.tron.core.exception.ContractValidateException : contract type error, unexpected type [UpdateBrokerageContract]"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid ownerAddress"}` |
| `brokerage` 不在 [0, 100] | `{"Error": "... : Invalid brokerage"}` |
| 该地址不是 SR | `{"Error": "... : Not existed witness:<address hex>"}` |
| owner 账户不存在 | `{"Error": "... : Account does not exist"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
