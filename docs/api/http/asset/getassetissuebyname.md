# /wallet/getassetissuebyname

按 token 名查询单个 TRC-10。**注意**：自 `ALLOW_SAME_TOKEN_NAME` 提案后，name 不再唯一，调用此接口在重名时会报错；推荐用 [`/wallet/getassetissuebyid`](getassetissuebyid.md) 或 [`/wallet/getassetissuelistbyname`](getassetissuelistbyname.md)。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAssetIssueByNameServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getassetissuebyname`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `value` | GET | string | 是 | token 名（hex 编码 UTF-8） |
| `value` | POST | string | 否 | token 名；省略时使用空值，`visible=false` 时通常返回 `{}` |
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuebyname \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "303044696365"
}
'
```

## 响应

返回 `protocol.AssetIssueContract`，字段同 [`/wallet/createassetissue`](createassetissue.md) 请求体。

响应示例（Nile token name `303044696365` 解码为 `00Dice`）：

```json
{
  "owner_address": "41a8a906cd9d5e7ff3e472d34ca568441ceeb4cf5b",
  "name": "303044696365",
  "abbr": "307830",
  "total_supply": 1000000000000000000,
  "trx_num": 1000000,
  "precision": 6,
  "num": 100000000,
  "start_time": 1592841600000,
  "end_time": 1592928000000,
  "description": "e794a8e4ba8ee6b58be8af95",
  "url": "68747470733a2f2f7777772e62616964752e636f6d",
  "id": "1000052"
}
```

不存在返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `value` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : exception decoding Hex string: <详情>"}` |
| GET / POST | 重名 token 数量 > 1（`ALLOW_SAME_TOKEN_NAME` 提案后） | `{"Error": "class org.tron.core.exception.NonUniqueObjectException : To get more than one asset, please use getAssetIssueById syntax"}` |
| POST | 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
