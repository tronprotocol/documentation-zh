# /wallet/getdelegatedresourceaccountindexv2

查询账户作为出借方/接收方的代理对手地址列表（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceAccountIndexV2Servlet.java`
- Method：`GET` / `POST`
- Response：`protocol.DelegatedResourceAccountIndex`
- 支持固化接口：`/walletsolidity/getdelegatedresourceaccountindexv2`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `value` | string | 是 | 查询账户地址 |
| `visible` | bool | 否 | 地址格式 |

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

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `value` 不是合法 base58check（`visible=true`） | `{"Error": "class java.lang.IllegalArgumentException : <message>"}`（GET）；`{"Error": "class java.lang.NullPointerException : <message>"}`（POST） |
| `value` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
