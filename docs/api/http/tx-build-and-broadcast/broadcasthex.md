# /wallet/broadcasthex

广播一笔已签名交易，输入直接是 `Transaction` 的 protobuf hex 编码。比 `/wallet/broadcasttransaction` 体积更小。

- 源码：`framework/src/main/java/org/tron/core/services/http/BroadcastHexServlet.java`
- Method：`POST`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `transaction` | string | 是 | 完整 `protocol.Transaction` 的 protobuf 序列化结果 hex |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/broadcasthex \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "transaction": "0a8a010a02..." }
'
```

> `transaction` 字段需为 [`/wallet/createtransaction`](createtransaction.md) 等接口产出的 `raw_data_hex` 加签后再次 protobuf 序列化的整笔 Transaction hex；上例 `0a8a010a02...` 为占位。

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `result` | bool | 是否进入交易池 |
| `code` | string | 同 `broadcasttransaction`，但是用 enum name 直接输出 |
| `message` | string | 失败原因（UTF-8） |
| `transaction` | string | 解析后的 Transaction JSON 的**字符串形式**（servlet 强制 `visible=true` 调用 `JsonFormat.printToString`，再以 string 放入响应；客户端需对该字段再做一次 JSON 解析） |
| `txid` | string | 交易哈希 |

响应示例：

```json
{
  "result": true,
  "code": "SUCCESS",
  "message": "",
  "transaction": "{...}",
  "txid": "d5ec749ecc2a615399d8a6c864ea4c74ff9f8453eaa44d6b1e2f0b7b3e2f3b6a"
}
```

### 异常响应

业务级错误（`SIGERROR` / `DUP_TRANSACTION_ERROR` / `TAPOS_ERROR` 等）按 `result/code/message` 形态返回，`code` 取值与 [`/wallet/broadcasttransaction`](broadcasttransaction.md) 一致。

入参 `transaction` 字段缺失、不是合法 hex、`Transaction.parseFrom` 反序列化失败时走 `Util.processError`（servlet 不调用 `Util.checkBodySize`，因此无 body-size 分支）：

| 触发条件 | 响应 |
|---|---|
| 请求体不是合法 JSON | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` |
| `transaction` 字段缺失或非字符串 | `{"Error": "class java.lang.NullPointerException : <message>"}`（`getString("transaction")` 返 null → `ByteArray.fromHexString(null)` 空指针） |
| `transaction` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（`ByteArray.fromHexString`） |
| `transaction` 不是合法 protobuf | `{"Error": "class com.google.protobuf.InvalidProtocolBufferException : <message>"}`（`Transaction.parseFrom`） |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
