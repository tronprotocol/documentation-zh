# /wallet/getavailableunfreezecount

查询账户剩余可发起解冻次数（Stake 2.0 一个账户最多有 32 个解冻进行中）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAvailableUnfreezeCountServlet.java`
- Method：`GET` / `POST`
- Response：`api.GetAvailableUnfreezeCountResponseMessage`
- 支持固化接口：`/walletsolidity/getavailableunfreezecount`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

GET 还接受 `ownerAddress` 作为 `owner_address` 的别名。POST 只接受规范字段 `owner_address`；`ownerAddress` 会被视为未知 JSON 字段并忽略。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `owner_address` | GET / POST | string | 是 | 账户地址；`ownerAddress` 别名仅 GET 支持 |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getavailableunfreezecount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `count` | int64 | 剩余可解冻次数 |

响应示例（无未到期解冻申请，全部 32 次额度可用）：

```json
{ "count": 32 }
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `owner_address` 不是合法 base58check（`visible=true`） | GET：含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回空串 → 查询不到记录返回 `{}`。POST（走 `JsonFormat.merge`）：含非 base58 字符抛 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`；仅校验位错误抛 `{"Error": "class java.lang.NullPointerException : null"}` |
| GET / POST | `owner_address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
