# /wallet/getblockbylimitnext

获取区间 `[startNum, endNum)` 的区块列表（不包含 endNum）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBlockByLimitNextServlet.java`
- Method：`GET` / `POST`
- Request：`api.BlockLimit`
- 支持固化接口：`/walletsolidity/getblockbylimitnext`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `startNum` | GET | int64 | 是 | 起始区块高度（包含）；缺失时执行 `Long.parseLong(null)` 并失败 |
| `startNum` | POST | int64 | 否 | 起始区块高度（包含）；Protobuf 默认值为 `0` |
| `endNum` | GET | int64 | 是 | 结束区块高度（不包含）；缺失时执行 `Long.parseLong(null)` 并失败 |
| `endNum` | POST | int64 | 否 | 结束区块高度（不包含）；Protobuf 默认值为 `0` |
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

约束：`endNum > startNum`，且 `endNum - startNum <= 100`。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbylimitnext \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "startNum": 66987565, "endNum": 66987567 }
'
```

## 响应

返回 `api.BlockList`：

| 字段 | 类型 | 说明 |
|---|---|---|
| `block` | repeated Block | 区块数组 |

响应示例（省略 `transactions` 内容）：

```json
{
  "block": [
    {
      "blockID": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
      "block_header": {
        "raw_data": {
          "number": 66987565,
          "txTrieRoot": "faf8fe3858339ead25cc892461c82a59b84dca4a51c45b026676bf3f45a352a2",
          "witness_address": "41b2f713d57dbcec679d93a8849fa0cd0e4db594ba",
          "parentHash": "0000000003fe262c85cd6b02033f4c3e5c1efa35de256a17bd906dc61fb1aeed",
          "version": 34,
          "timestamp": 1777445121000
        },
        "witness_signature": "5b3cf6cb15d52947989f7726f4907a144b39ccd667a1a0f98707b40cdfe65b96173ddf34ae8dcc5e78f136e0cf903a15c7128984aa2191f02333209d1879d3f900"
      },
      "transactions": [ /* ... */ ]
    },
    {
      "blockID": "0000000003fe262e...",
      "block_header": { /* ... */ },
      "transactions": [ /* ... */ ]
    }
  ]
}
```

无可用区块返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET | `startNum` / `endNum` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
