# /wallet/getdelegatedresourceaccountindexv2

查询账户作为出借方/接收方的代理对手地址列表（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceAccountIndexV2Servlet.java`
- Method：`GET` / `POST`
- Response：`protocol.DelegatedResourceAccountIndex`
- 支持固化接口：`/walletsolidity/getdelegatedresourceaccountindexv2`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `value` | GET | string | 是 | 查询账户地址 |
| `value` | POST | string | 否 | 查询账户地址；省略时使用空 bytes 并返回默认空结果 |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresourceaccountindexv2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

字段同 [`/wallet/getdelegatedresourceaccountindex`](../stake-v1/getdelegatedresourceaccountindex.md)（Stake 2.0 数据）。

响应示例（账户既未代理给他人也未接收他人代理，仅返回 `account`；`fromAccounts`、`toAccounts` 为 proto 默认空列表）：

```json
{
  "account": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `value` 不是合法 base58check（`visible=true`） | 含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回 null → 查询不到记录返回 `{}`（GET、POST 行为一致，POST 在 merge 前先做 base58 → hex 转换） |
| GET / POST | `value` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| POST | 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
