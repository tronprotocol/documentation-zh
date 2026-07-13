# /wallet/gettransactionfrompending

从待打包池（pending）按交易 ID 取交易。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionFromPendingServlet.java`
- Method：`GET` / `POST`
- Request：`api.BytesMessage`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `value` | GET / POST | string | 是 | 交易 ID hex |
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

示例：

```bash
# 先调用 /wallet/gettransactionlistfrompending 取一个 pending 中的 txID 替换下面的 value
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactionfrompending \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "7a265c89822d2dd9ee2187a728db3f273784943d588fd7b79ce972fc14a3f1de"
}
'
```

## 响应

返回 `protocol.Transaction`（结构同 [`/wallet/gettransactionbyid`](gettransactionbyid.md)）。

响应示例（pending 池中的合约调用，与 `gettransactionbyid` 同结构）：

```json
{
  "signature": ["..."],
  "txID": "<待打包交易 ID>",
  "raw_data": {
    "contract": [ /* 见 /wallet/gettransactionbyid 示例 */ ],
    "ref_block_bytes": "...",
    "ref_block_hash": "...",
    "expiration": 1777445400000,
    "timestamp": 1777445307000
  },
  "raw_data_hex": "..."
}
```

> Pending 内的交易很快会被打包（≈ 3 秒），实测时大概率瞬间从 pending 消失，因此调用很可能直接返回 `{}`。

不在 pending 中（已打包或已失效）返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `value` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
