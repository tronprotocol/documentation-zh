# /wallet/getdelegatedresource

> **存量查询**：仅返回 Stake 1.0 存储的代理记录，对 V2 数据无效。源码无版本网关，可在 V2 启用后继续调用以查询历史 V1 仓位。新业务请使用 [`/wallet/getdelegatedresourcev2`](../stake-v2/getdelegatedresourcev2.md)。

查询 from→to 之间所有的资源代理记录（Stake 1.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceServlet.java`
- Method：`GET` / `POST`
- Response：`api.DelegatedResourceList`
- 支持固化接口：`/walletsolidity/getdelegatedresource`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fromAddress` | string | 是 | 资源出借方地址 |
| `toAddress` | string | 是 | 资源接收方地址 |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresource \
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

| 字段 | 类型 | 说明 |
|---|---|---|
| `delegatedResource` | repeated DelegatedResource | 代理记录列表 |

`DelegatedResource` 字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `from` | string | 出借方 |
| `to` | string | 接收方 |
| `frozen_balance_for_bandwidth` | int64 | 代理给对方的带宽冻结量 |
| `frozen_balance_for_energy` | int64 | 代理给对方的能量冻结量 |
| `expire_time_for_bandwidth` | int64 | 带宽代理到期时间 |
| `expire_time_for_energy` | int64 | 能量代理到期时间 |

响应示例（示例账户在 Nile 上无 V1 代理记录，返回空对象）：

```json
{}
```

存在 V1 代理记录时的响应：

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

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| `fromAddress` / `toAddress` 不是合法 base58check（`visible=true`） | GET：含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回空串 → 查询不到记录返回 `{}`。POST（走 `JsonFormat.merge`）：含非 base58 字符抛 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`；仅校验位错误抛 `{"Error": "class java.lang.NullPointerException : null"}` |
| `fromAddress` / `toAddress` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
