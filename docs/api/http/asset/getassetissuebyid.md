# /wallet/getassetissuebyid

按 token id 查询 TRC-10（推荐方式，token id 全局唯一）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAssetIssueByIdServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getassetissuebyid`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `value` | GET / POST | string | 是 | token id（数字字符串，例如 `"1000001"`） |
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuebyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "1005416"
}
'
```

## 响应

返回 `protocol.AssetIssueContract`，字段同 [`/wallet/createassetissue`](createassetissue.md) 请求体。

响应示例（Nile 上 token id `1005416`，name `54524e` 解码为 `TRN`）：

```json
{
  "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
  "name": "54524e",
  "abbr": "544e",
  "total_supply": 100000000000000000,
  "frozen_supply": [
    { "frozen_amount": 1, "frozen_days": 1 }
  ],
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
```

不存在返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| POST | 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
