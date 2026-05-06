# /wallet/gettransactioncountbyblocknum

返回某区块号包含的交易数。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionCountByBlockNumServlet.java`
- Method：`GET` / `POST`
- Request：`api.NumberMessage`
- 支持固化接口：`/walletsolidity/gettransactioncountbyblocknum`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `num` | int64 | 是 | 区块号 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactioncountbyblocknum \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "num": 66987565 }
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `count` | int64 | 该区块的交易数；区块不存在返回 0 |

响应示例：

```json
{ "count": 4 }
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `num` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
