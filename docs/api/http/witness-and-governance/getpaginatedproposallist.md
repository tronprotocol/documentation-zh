# /wallet/getpaginatedproposallist

分页获取提案列表。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetPaginatedProposalListServlet.java`
- Method：`GET` / `POST`
- Response：`api.ProposalList`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `offset` | GET | int64 | 是 | 起始偏移；缺失时执行 `Long.parseLong(null)` 并失败 |
| `offset` | POST | int64 | 否 | 起始偏移；Protobuf 默认值为 `0` |
| `limit` | GET | int64 | 是 | 分页大小；缺失时执行 `Long.parseLong(null)` 并失败 |
| `limit` | POST | int64 | 否 | 分页大小；Protobuf 默认值为 `0`，此时返回空列表 |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpaginatedproposallist \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "offset": 0,
  "limit": 1
}
'
```

## 响应

字段同 [`/wallet/listproposals`](listproposals.md)。

响应示例（Nile，limit=1；`approvals` 实际包含 27 位 SR 的地址，示例省略）：

```json
{
  "proposals": [
    {
      "proposal_id": 1,
      "proposer_address": "41217179d498883cdbda5699402905d1feb258796c",
      "parameters": [
        { "key": 9,  "value": 1 },
        { "key": 10, "value": 1 }
      ],
      "expiration_time": 1572597600000,
      "create_time": 1572596523000,
      "approvals": [
        "41217179d498883cdbda5699402905d1feb258796c"
        /* ... 其余 SR */
      ],
      "state": "APPROVED"
    }
  ]
}
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET | `offset` / `limit` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
