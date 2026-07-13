# /wallet/gettransactioncountbyblocknum

返回某区块高度包含的交易数。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionCountByBlockNumServlet.java`
- Method：`GET` / `POST`
- Request：`api.NumberMessage`
- 支持固化接口：`/walletsolidity/gettransactioncountbyblocknum`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `num` | GET | int64 | 是 | 区块高度；缺失时执行 `Long.parseLong(null)` 并失败 |
| `num` | POST | int64 | 否 | 区块高度；Protobuf 默认值为 `0` |
| `int64_as_string` | GET | bool | 否 | 仅 GET；为 `true` 时将 `count` 作为 JSON 字符串返回 |

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

使用 GET 请求并添加 `?int64_as_string=true` 时：

```json
{ "count": "4" }
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET | `num` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
