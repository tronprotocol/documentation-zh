# /wallet/getcandelegatedmaxsize

查询账户当前可代理的最大资源额度（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetCanDelegatedMaxSizeServlet.java`
- Method：`GET` / `POST`
- Response：`api.CanDelegatedMaxSizeResponseMessage`
- 支持固化接口：`/walletsolidity/getcandelegatedmaxsize`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 账户地址 |
| `type` | int32 | 否 | 资源类型：`0`=BANDWIDTH（默认），`1`=ENERGY |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcandelegatedmaxsize \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "type": 1
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `max_size` | int64 | 可代理的最大冻结量（sun） |

响应示例（账户当前 ENERGY 可代理量为 0，proto 默认值不序列化，返回空对象 `{}`；存在可代理资源时形如 `{"max_size": 5000000000}`）：

```json
{}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| `type` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| `owner_address` 不是合法 base58check（`visible=true`） | GET：含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回空串 → 查询不到记录返回 `{}`。POST（走 `JsonFormat.merge`）：含非 base58 字符抛 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`；仅校验位错误抛 `{"Error": "class java.lang.NullPointerException : null"}` |
| `owner_address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
