# /wallet/getavailableunfreezecount

查询账户剩余可发起解冻次数（Stake 2.0 一个账户最多有 32 个解冻进行中）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAvailableUnfreezeCountServlet.java`
- Method：`GET` / `POST`
- Response：`api.GetAvailableUnfreezeCountResponseMessage`
- 支持固化接口：`/walletsolidity/getavailableunfreezecount`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 账户地址（也接受 `ownerAddress`） |
| `visible` | bool | 否 | 地址格式 |

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

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `owner_address` 不是合法 base58check（`visible=true`） | `{"Error": "class java.lang.IllegalArgumentException : <message>"}`（GET）；`{"Error": "class java.lang.NullPointerException : <message>"}`（POST） |
| `owner_address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
