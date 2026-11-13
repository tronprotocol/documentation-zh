# /wallet/getassetissuebyaccount

查询某账户作为发行方发行的所有 TRC-10。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAssetIssueByAccountServlet.java`
- Method：`GET` / `POST`
- Response：`api.AssetIssueList`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `address` | GET | string | 是 | 账户地址 |
| `address` | POST | string | 否 | 账户地址；省略时使用 Protobuf 空地址并返回 `{}` |
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuebyaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41088a2bfcb1c7271029fd69a66859d55560895884"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | 该账户发行的 TRC-10 列表（结构见 `asset_issue_contract.proto`，字段同 [`/wallet/createassetissue`](createassetissue.md) 请求体） |

响应示例：

```json
{
  "assetIssue": [
    {
      "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
      "name": "54524e",
      "abbr": "544e",
      "total_supply": 100000000000000000,
      "frozen_supply": [{ "frozen_amount": 1, "frozen_days": 1 }],
      "trx_num": 1,
      "precision": 6,
      "num": 1,
      "start_time": 1737690890434,
      "end_time": 2053134849000,
      "vote_score": 1,
      "description": "7465737420747263313020636f696e20666f72206e696c65",
      "url": "68747470733a2f2f6e696c6565782e696f2f",
      "free_asset_net_limit": 10000,
      "public_free_asset_net_limit": 20000,
      "id": "1005416"
    }
  ]
}
```

未发行返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `address` 不是合法 base58check（`visible=true`） | GET：长度为 34 个字符且含非 base58 字符时，返回 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；空值、长度不为 34、地址前缀非法或校验和错误时，`Util.getHexAddress` 返回空字符串，查询不到记录并返回 `{}`。POST（通过 `JsonFormat.merge`）：非法字符、长度不正确或校验和错误均返回 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: invalid address for field: protocol.Account.address"}` |
| GET / POST | `address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
