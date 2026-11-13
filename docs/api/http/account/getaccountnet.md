# /wallet/getaccountnet

查询账户的带宽（Net）资源使用情况。**已弃用**，推荐使用 [`/wallet/getaccountresource`](getaccountresource.md)。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAccountNetServlet.java`
- Method：`GET` / `POST`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `address` | GET | string | 是 | 账户地址 |
| `address` | POST | string | 否 | 账户地址；省略时使用 Protobuf 空地址并返回 `{}` |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccountnet \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

返回 `api.AccountNetMessage`（`protocol/src/main/protos/api/api.proto`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `freeNetUsed` | int64 | 已使用的免费带宽 |
| `freeNetLimit` | int64 | 每个账户的免费带宽总额度，由可通过治理提案修改的链参数设定。已使用的免费带宽会在 24 小时恢复窗口内逐步恢复可用。 |
| `NetUsed` | int64 | 已使用的质押带宽 |
| `NetLimit` | int64 | 质押获得的带宽上限 |
| `assetNetUsed` | map\<string,int64\> | 持有 TRC-10 各自使用的带宽 |
| `assetNetLimit` | map\<string,int64\> | 持有 TRC-10 各自的带宽上限 |
| `TotalNetLimit` | int64 | 全网总带宽上限 |
| `TotalNetWeight` | int64 | 全网带宽质押总量（TRX） |

响应示例：

```json
{
  "freeNetUsed": 441,
  "freeNetLimit": 600,
  "assetNetUsed": [
    { "key": "1005416", "value": 0 }
  ],
  "assetNetLimit": [
    { "key": "1005416", "value": 10000 }
  ],
  "TotalNetLimit": 43200000000,
  "TotalNetWeight": 68305209098
}
```

`address` 缺失或对应账户不存在均返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `address` 不是合法 base58check（`visible=true`） | GET：长度为 34 个字符且含非 base58 字符时，返回 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；空值、长度不为 34、地址前缀非法或校验和错误时，`Util.getHexAddress` 返回空字符串，查询不到记录并返回 `{}`。POST（通过 `JsonFormat.merge`）：非法字符、长度不正确或校验和错误均返回 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: invalid address for field: protocol.Account.address"}` |
| GET / POST | `address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
