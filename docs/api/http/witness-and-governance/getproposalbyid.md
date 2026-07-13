# /wallet/getproposalbyid

按 ID 查询提案。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetProposalByIdServlet.java`
- Method：`GET` / `POST`
- Response：`protocol.Proposal`（`Tron.proto`）

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `id` | GET / POST | int64 | 是 | 提案 ID |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getproposalbyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "id": 70
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `proposal_id` | int64 | 提案 ID |
| `proposer_address` | string | 提案人地址 |
| `parameters` | map<int64, int64> | 参数项 |
| `expiration_time` | int64 | 过期时间（毫秒时间戳） |
| `create_time` | int64 | 创建时间（毫秒时间戳） |
| `approvals` | repeated string | 已赞成的 SR 地址 |
| `state` | enum | `PENDING` / `DISAPPROVED` / `APPROVED` / `CANCELED` |

响应示例（Nile，`id=70`，将 `getAccountUpgradeCost` 从 9999 TRX 降至 9997 TRX；过期前未达赞成阈值，`approvals` 字段不存在）：

```json
{
  "proposal_id": 70,
  "proposer_address": "412e9d9ea27e51b0307afc7ce64654cf9359b74cec",
  "parameters": [
    { "key": 1, "value": 9997000000 }
  ],
  "expiration_time": 1582381800000,
  "create_time": 1582381197000,
  "state": "DISAPPROVED"
}
```

不存在返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET | `id` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| POST | 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| POST | `id` 缺失（POST） | `{"Error": "class java.security.InvalidParameterException : key [id] does not exist"}` |
| POST | `id` 不是数字（POST，含字符串/布尔/数组/对象） | `{"Error": "class java.lang.NumberFormatException : null"}`（`Util.getJsonLongValue` 走 `org.tron.json.JSONObject#getBigDecimal`） |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
