# /wallet/getdelegatedresourcev2

查询 from→to 之间的资源代理记录（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceV2Servlet.java`
- Method：`GET` / `POST`
- Response：`api.DelegatedResourceList`
- 支持固化接口：`/walletsolidity/getdelegatedresourcev2`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `fromAddress` | GET | string | 是 | 出借方地址 |
| `fromAddress` | POST | string | 否 | 出借方地址；省略时使用空 bytes 并返回空结果 |
| `toAddress` | GET | string | 是 | 接收方地址 |
| `toAddress` | POST | string | 否 | 接收方地址；省略时使用空 bytes 并返回空结果 |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresourcev2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "fromAddress": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "toAddress":   "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
}
'
```

## 响应

字段同 [`/wallet/getdelegatedresource`](../stake-v1/getdelegatedresource.md)，但仅包含 Stake 2.0 的代理记录。

响应示例（from→to 之间没有代理关系，返回空对象 `{}`；存在代理时形如）：

```json
{}
```

```json
{
  "delegatedResource": [
    {
      "from": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
      "to":   "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
      "frozen_balance_for_energy": 1000000000,
      "expire_time_for_energy":    1700000000000
    }
  ]
}
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `fromAddress` / `toAddress` 不是合法 base58check（`visible=true`） | GET：仅当输入恰好为 34 个字符时，非 base58 字符才会抛出 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`。输入长度错误、校验和错误或解码后的地址无效时，`Util.getHexAddress` 返回空 hex 字符串，因此接口返回 `{}`。POST（通过 `JsonFormat.merge`）：非法字符、校验和错误或地址长度无效均返回 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: invalid address for field: <fully-qualified proto field>"}` |
| GET / POST | `fromAddress` / `toAddress` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| POST | 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
