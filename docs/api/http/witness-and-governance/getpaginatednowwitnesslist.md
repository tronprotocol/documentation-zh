# /wallet/getpaginatednowwitnesslist

按分页获取当前生效的 SR 列表。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetPaginatedNowWitnessListServlet.java`
- Method：`GET` / `POST`
- Response：`api.WitnessList`
- 支持固化接口：`/walletsolidity/getpaginatednowwitnesslist`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `offset` | int64 | 是 | 起始偏移 |
| `limit` | int64 | 是 | 返回条数 |
| `visible` | bool | 否 | 地址格式 |

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

字段同 [`/wallet/listwitnesses`](listwitnesses.md)。

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

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `offset` / `limit` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 维护期内对 fullnode HEAD 游标调用（非 solidity） | `{"Error": "class org.tron.core.exception.MaintenanceUnavailableException : Service temporarily unavailable during maintenance period. Please try again later."}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
