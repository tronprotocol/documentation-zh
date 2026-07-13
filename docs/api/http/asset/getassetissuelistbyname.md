# /wallet/getassetissuelistbyname

按 token 名查询所有同名 TRC-10。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAssetIssueListByNameServlet.java`
- Method：`GET` / `POST`
- Response：`api.AssetIssueList`
- 支持固化接口：`/walletsolidity/getassetissuelistbyname`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `value` | GET / POST | string | 是 | token 名（hex 编码 UTF-8） |
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuelistbyname \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "54524e"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | 所有同名 token |

响应示例（Nile name `54524e` 解码为 `TRN`，存在两个同名 token，截取前 2 项）：

```json
{
  "assetIssue": [
    {
      "owner_address": "414607716a6ca8fe2dc8f9e27c349a435191e48639",
      "name": "54524e",
      "abbr": "544e",
      "total_supply": 100000000000000000,
      "frozen_supply": [{ "frozen_amount": 1, "frozen_days": 1 }],
      "trx_num": 1,
      "num": 1,
      "start_time": 1737613011138,
      "end_time": 2053134849000,
      "description": "74726964656e74",
      "url": "68747470733a2f2f7777772e74726964656e742e636f6d",
      "free_asset_net_limit": 20,
      "public_free_asset_net_limit": 1,
      "id": "1005415"
    },
    {
      "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
      "name": "54524e",
      "abbr": "544e",
      "total_supply": 100000000000000000,
      "trx_num": 1,
      "precision": 6,
      "num": 1,
      "id": "1005416"
    }
  ]
}
```

无匹配返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `value` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : exception decoding Hex string: <详情>"}` |
| POST | 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
