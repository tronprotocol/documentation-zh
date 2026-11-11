# /wallet/getcandelegatedmaxsize

查询账户当前可代理的最大资源额度（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetCanDelegatedMaxSizeServlet.java`
- Method：`GET` / `POST`
- Response：`api.CanDelegatedMaxSizeResponseMessage`
- 支持固化接口：`/walletsolidity/getcandelegatedmaxsize`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `owner_address` | GET | string | 是 | 账户地址 |
| `owner_address` | POST | string | 否 | 账户地址；省略时使用空 bytes 并返回默认结果 |
| `type` | GET / POST | int32 | 否 | 资源类型：`0`=BANDWIDTH（默认），`1`=ENERGY |
| `visible` | GET / POST | bool | 否 | 地址格式 |

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

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET | `type` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| GET / POST | `owner_address` 不是合法 base58check（`visible=true`） | GET：仅当输入恰好为 34 个字符时，非 base58 字符才会抛出 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`。输入长度错误、校验和错误或解码后的地址无效时，`Util.getHexAddress` 返回空 hex 字符串，因此查询不到账户并返回 `{}`。POST（通过 `JsonFormat.merge`）：非法字符、校验和错误或地址长度无效均返回 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: invalid address for field: <fully-qualified proto field>"}` |
| GET / POST | `owner_address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
