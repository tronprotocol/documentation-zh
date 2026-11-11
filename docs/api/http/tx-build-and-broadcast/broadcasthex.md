# /wallet/broadcasthex

广播一笔已签名交易，输入直接是 `Transaction` 的 protobuf hex 编码。比 `/wallet/broadcasttransaction` 体积更小。

- 源码：`framework/src/main/java/org/tron/core/services/http/BroadcastHexServlet.java`
- Method：`POST`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `transaction` | string | 是 | 完整 `protocol.Transaction` 的 protobuf 序列化结果 hex。交易中嵌入的每个签名必须为 `65`–`68` 字节，否则广播会返回 `SIGERROR` |

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
| `result` | bool | 本次广播是否成功。交易进入交易池后，P2P 广播仍可能失败 |
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

非法 hex 和 protobuf 反序列化错误走 `Util.processError`。缺失或为 null 的 `transaction` 会被解析为空交易；如果通过广播前置检查，节点返回 `CONTRACT_VALIDATE_ERROR`，消息为 `Contract validate error : No contract!`。该 servlet 本身不调用 `Util.checkBodySize`，但共享 HTTP `SizeLimitHandler` 仍可能拒绝超大请求体。

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large`；该 servlet 本身没有额外调用 `Util.checkBodySize` |
| 请求体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| `transaction` 字段缺失或为 null | 如果通过广播前置检查，返回业务级响应 `{"result": false, "code": "CONTRACT_VALIDATE_ERROR", "message": "Contract validate error : No contract!", "transaction": "{}", "txid": "<空 raw_data 的 SHA256>"}`（`getString` 返回 null → `ByteArray.fromHexString(null)` 得到空数组 → `Transaction.parseFrom` 得到空 Transaction → 被节点拒绝） |
| `transaction` 非字符串（数组/对象/数字） | 不支持的输入形式。`getString` 将标量转换为文本，并将数组/对象序列化；非法 hex 会触发 `DecoderException`，合法 hex 但非法 protobuf 会触发 `InvalidProtocolBufferException`，合法 protobuf 内容则进入广播流程。例如，数字 `10` 转换为 hex `10`，随后 protobuf 解析失败 |
| `transaction` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` |
| `transaction` 不是合法 protobuf | `{"Error": "class com.google.protobuf.InvalidProtocolBufferException : <message>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
