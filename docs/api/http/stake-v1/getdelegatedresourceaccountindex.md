# /wallet/getdelegatedresourceaccountindex

> **存量查询**：仅返回 Stake 1.0 存储的代理对手地址索引，对 V2 数据无效。源码无版本网关，可在 V2 启用后继续调用以查询历史 V1 仓位。新业务请使用 [`/wallet/getdelegatedresourceaccountindexv2`](../stake-v2/getdelegatedresourceaccountindexv2.md)。

查询账户作为出借方/接收方的代理对手地址列表（Stake 1.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceAccountIndexServlet.java`
- Method：`GET` / `POST`
- Response：`protocol.DelegatedResourceAccountIndex`
- 支持固化接口：`/walletsolidity/getdelegatedresourceaccountindex`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `value` | string | 是 | 查询账户地址 |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresourceaccountindex \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `account` | string | 查询账户 |
| `fromAccounts` | repeated string | 向我代理资源的账户 |
| `toAccounts` | repeated string | 我向其代理资源的账户 |

响应示例（示例账户无 V1 代理对手，proto 默认空数组不序列化）：

```json
{
  "account": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
```

存在 V1 代理对手时的响应：

```json
{
  "account":      "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "fromAccounts": [],
  "toAccounts":   ["4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"]
}
```

完全无记录时返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| `value` 不是合法 base58check（`visible=true`） | 含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回 null → 查询不到记录返回 `{}`（GET、POST 行为一致，POST 在 merge 前先做 base58 → hex 转换） |
| `value` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
