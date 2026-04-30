# /wallet/getaccountnet

查询账户的带宽（Net）资源使用情况。**已弃用**，推荐使用 `/wallet/getaccountresource`。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAccountNetServlet.java`
- Method：`GET` / `POST`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `address` | string | 是 | 账户地址 |
| `visible` | bool | 否 | 地址格式 |

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

返回 `api.AccountNetMessage`（`protocol/src/main/protos/api/api.proto:1187`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `freeNetUsed` | int64 | 已使用的免费带宽 |
| `freeNetLimit` | int64 | 免费带宽上限（每 24h 重置） |
| `NetUsed` | int64 | 已使用的质押带宽 |
| `NetLimit` | int64 | 质押获得的带宽上限 |
| `assetNetUsed` | map\<string,int64\> | 持有 TRC10 各自使用的带宽 |
| `assetNetLimit` | map\<string,int64\> | 持有 TRC10 各自的带宽上限 |
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

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `address` 不是合法 base58check（`visible=true`） | GET：含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回空串 → 查询不到记录返回 `{}`。POST（走 `JsonFormat.merge`）：含非 base58 字符抛 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`；仅校验位错误抛 `{"Error": "class java.lang.NullPointerException : null"}` |
| `address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
