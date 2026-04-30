# /wallet/getdelegatedresourcev2

查询 from→to 之间的资源代理记录（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceV2Servlet.java`
- Method：`GET` / `POST`
- Response：`api.DelegatedResourceList`
- 支持固化接口：`/walletsolidity/getdelegatedresourcev2`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fromAddress` | string | 是 | 出借方地址 |
| `toAddress` | string | 是 | 接收方地址 |
| `visible` | bool | 否 | 地址格式 |

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

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `fromAddress` / `toAddress` 不是合法 base58check（`visible=true`） | `{"Error": "class java.lang.IllegalArgumentException : <message>"}`（GET）；`{"Error": "class java.lang.NullPointerException : <message>"}`（POST） |
| `fromAddress` / `toAddress` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
