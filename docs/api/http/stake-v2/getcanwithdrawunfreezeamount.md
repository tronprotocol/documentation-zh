# /wallet/getcanwithdrawunfreezeamount

查询指定时间点账户可提取的解冻金额（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetCanWithdrawUnfreezeAmountServlet.java`
- Method：`GET` / `POST`
- Response：`api.CanWithdrawUnfreezeAmountResponseMessage`
- 支持固化接口：`/walletsolidity/getcanwithdrawunfreezeamount`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 账户地址 |
| `timestamp` | int64 | 否 | 截止时间戳（毫秒）；缺省或为 `0` 时使用最新区块时间；为负返回 `{}` |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcanwithdrawunfreezeamount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "timestamp":     1900000000000
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `amount` | int64 | 至该时间点可提取的解冻总额（sun） |

响应示例（账户没有进行中的解冻条目，proto 默认值不序列化，返回空对象 `{}`；存在可提取金额时形如 `{"amount": 1500000000}`）：

```json
{}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `timestamp` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| `owner_address` 不是合法 base58check（`visible=true`） | GET：含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回空串 → 查询不到记录返回 `{}`。POST（走 `JsonFormat.merge`）：含非 base58 字符抛 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`；仅校验位错误抛 `{"Error": "class java.lang.NullPointerException : null"}` |
| `owner_address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
