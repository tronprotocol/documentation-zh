# /wallet/getpaginatednowwitnesslist

分页查询所有 SR 候选人，按当前总票数排序。总票数包含当前周期的投票变化；结果不限于 27 位活跃 SR，也不限于 `isJobs=true` 的候选人。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetPaginatedNowWitnessListServlet.java`
- Method：`GET` / `POST`
- Response：`api.WitnessList`
- 支持固化接口：`/walletsolidity/getpaginatednowwitnesslist`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `offset` | GET | int64 | 是 | 起始偏移；缺失时执行 `Long.parseLong(null)` 并失败 |
| `offset` | POST | int64 | 否 | 起始偏移；Protobuf 默认值为 `0` |
| `limit` | GET | int64 | 是 | 分页大小，上限为 1000；缺失时执行 `Long.parseLong(null)` 并失败 |
| `limit` | POST | int64 | 否 | 分页大小，上限为 1000；Protobuf 默认值为 `0`，此时返回 `{}` |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpaginatednowwitnesslist \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "offset": 0,
  "limit": 2
}
'
```

## 响应

字段同 [`/wallet/listwitnesses`](listwitnesses.md)，但在排序和分页前，`voteCount` 已包含当前周期的投票变化。`/wallet/listwitnesses` 返回的是已存储的票数。

`limit <= 0`、`offset < 0` 或偏移超出候选人列表时返回 `{}`。`limit` 大于 1000 时会自动按 1000 处理；下一页的偏移应增加实际返回的条目数。

响应示例（Nile，limit=2；`voteCount`、`latestBlockNum`、`latestSlotNum` 等随时间变化）：

```json
{
  "witnesses": [
    {
      "address": "41608e7e1c6f6dcc1679ea512503e41ca0254e0948",
      "voteCount": 5405850746,
      "url": "http://sr-8.com",
      "totalProduced": 1891250,
      "totalMissed": 456,
      "latestBlockNum": 66987972,
      "latestSlotNum": 592482114,
      "isJobs": true
    },
    {
      "address": "4139e58c94e9877bbe5556ee7acc6d6d428a3929e9",
      "voteCount": 2322234750,
      "url": "http://sr-27.com",
      "totalProduced": 1896883,
      "totalMissed": 619,
      "latestBlockNum": 66987973,
      "latestSlotNum": 592482115,
      "isJobs": true
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
| GET / POST | 维护期内对 fullnode HEAD 游标调用（非 solidity） | `{"Error": "class org.tron.core.exception.MaintenanceUnavailableException : Service temporarily unavailable during maintenance period. Please try again later."}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
