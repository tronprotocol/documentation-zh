# /wallet/broadcasttransaction

广播一笔已签名的交易。

- 源码：`framework/src/main/java/org/tron/core/services/http/BroadcastServlet.java`
- Method：`POST`
- Response：`api.Return` + `txid`

## 请求参数

直接传 `protocol.Transaction` 的 JSON 表示（即 `createtransaction` 类接口的返回 + 签名）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `raw_data` | object | 是 | 与 createtransaction 返回一致；节点据此重新序列化为 protobuf bytes 做 SHA256 验签 |
| `raw_data_hex` | string | 否（节点忽略） | 客户端可视化辅助字段——`raw_data` 的 protobuf 编码。**不是 `protocol.Transaction` 的 proto 字段**，`JsonFormat.merge` 在 parse 阶段直接忽略，节点既不读也不与 `raw_data` 比对。客户端在签名时通常拿它做 SHA256 得到 `txID`，但广播给节点后是否一致、是否合法 hex 都不影响处理 |
| `signature` | string[] | 否 | JSON/Protobuf 解析阶段可选。每个十六进制编码的签名解码后必须为 `65`–`68` 字节（通常为 `130`–`136` 个十六进制字符）；提供的签名超出该范围时会立即以 `SIGERROR` 拒绝。普通交易通常需要一个有效签名才能广播成功，多签交易则必须满足所选权限的阈值。缺少签名或签名在密码学上无效时，通常会在进入签名校验阶段后返回 `SIGERROR` |
| `visible` | bool | 否 | 地址、文本字段格式 |

通过 gRPC `BroadcastTransaction` 方法以及其他使用节点交易广播路径的 API 端点提交交易时，也会执行相同的签名长度校验。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/broadcasttransaction \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "raw_data":     { "...": "..." },
  "raw_data_hex": "0a02...",
  "signature":    ["b8c0...01"]
}
'
```

> 上例为占位结构，实际调用前需把 `raw_data` / `raw_data_hex` / `signature` 替换为来自 [`/wallet/createtransaction`](createtransaction.md) 等接口的真实未签名交易加签后内容。

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `result` | bool | 本次广播是否成功；`false` 是 protobuf 默认值，会在 JSON 中省略。交易进入交易池后，P2P 广播仍可能失败 |
| `code` | enum | `SUCCESS`（默认值，在 JSON 中省略） / `SIGERROR` / `CONTRACT_VALIDATE_ERROR` / `CONTRACT_EXE_ERROR` / `BANDWITH_ERROR` / `DUP_TRANSACTION_ERROR` / `TAPOS_ERROR` / `TOO_BIG_TRANSACTION_ERROR` / `TRANSACTION_EXPIRATION_ERROR` / `SERVER_BUSY` / `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` / `BLOCK_UNSOLIDIFIED` / `OTHER_ERROR` |
| `message` | string | 失败原因；`visible=true` 时为 UTF-8 文本，`visible=false` 时为 UTF-8 字节的 hex |
| `txid` | string | 交易哈希 |

`result: true` 仅代表节点已收且入池，最终是否上链需通过 [`/wallet/gettransactioninfobyid`](../block-and-tx-query/gettransactioninfobyid.md) 查询。

响应示例：

```json
{
  "result": true,
  "txid": "d5ec749ecc2a615399d8a6c864ea4c74ff9f8453eaa44d6b1e2f0b7b3e2f3b6a"
}
```

protobuf JSON 解析器也接受将单个 hex 字符串作为 `signature`，并将其视为仅含一个元素的列表；非数组值不一定导致解析错误。正常请求请使用文档规定的数组形式。

### 异常响应

业务级错误使用 `code` / `message` / `txid` 返回；默认值 `result=false` 会被省略。以下示例假设 `visible=true`，因此消息以文本表示：

```json
{ "code": "DUP_TRANSACTION_ERROR", "message": "Dup transaction.", "txid": "..." }
```

```json
{ "code": "SIGERROR", "message": "Validate signature error: <详情>", "txid": "..." }
```

```json
{ "code": "TAPOS_ERROR", "message": "Tapos check error.", "txid": "..." }
```

当 `visible=false`（默认值）时，`message` 使用 hex 编码；例如 `Dup transaction.` 会变为 `447570207472616e73616374696f6e2e`。成功响应会省略默认值 `code=SUCCESS`。

`code` 含义：

| code | 含义 |
|---|---|
| `SIGERROR` | 签名校验失败，或者提供的签名短于 `65` 字节或长于 `68` 字节 |
| `CONTRACT_VALIDATE_ERROR` | 合约前置校验失败（余额不足、参数非法等） |
| `CONTRACT_EXE_ERROR` | 执行期失败 |
| `BANDWITH_ERROR` | 带宽不足 |
| `DUP_TRANSACTION_ERROR` | 重复交易 |
| `TAPOS_ERROR` | `ref_block_*` 不在链上（最常见于交易过期或链未同步） |
| `TOO_BIG_TRANSACTION_ERROR` | 交易体积超限 |
| `TRANSACTION_EXPIRATION_ERROR` | 过期时间早于下一个出块时隙、不晚于头块时间戳，或晚于头块时间戳超过 24 小时 |
| `SERVER_BUSY` | 节点繁忙（pending 满） |
| `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` | 当 `node.rpc.minEffectiveConnection` 非零（默认值为 `1`）时：没有活跃对等节点、已完成同步的对等节点数量不足，或 P2P 广播未送达任何对等节点 |
| `BLOCK_UNSOLIDIFIED` | 启用未固化区块检查时，头块与已固化区块的高度差达到配置的 `maxUnsolidifiedBlocks` 阈值，因此拒绝广播 |
| `OTHER_ERROR` | 其他 |

请求 JSON 或外层结构错误走 `Util.processError`；单个合约格式错误则可能在解析时被丢弃，具体如下：

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| `raw_data` / `raw_data.contract` 缺失或为 null | 访问缺失的对象或数组时返回 `{"Error": "class java.lang.NullPointerException : <message>"}` |
| `raw_data` 不是对象，或 `raw_data.contract` 不是数组（不包括能解析为所需结构的 JSON 字符串） | `{"Error": "class org.tron.json.JSONException : <message>"}`，例如 `Field 'contract' is not an array` |
| 签名 hex 非法，或 `raw_data` 中的字段值无法由 `JsonFormat.merge` 解码 | `packTransaction` 捕获最终的 `JsonFormat$ParseException` 并返回 `null`，下游操作随后返回 `{"Error": "class java.lang.NullPointerException : <message>"}` |
| `raw_data.contract[i].parameter.value` 内字段类型不符 | 有问题的合约会在 `packTransaction` 内被捕获并丢弃。若解析后没有剩余合约，且通过广播前置检查，响应包含 `code: "CONTRACT_VALIDATE_ERROR"`，`message` 为 `Contract validate error : No contract!` 的编码结果（默认为 hex；`visible=true` 时为文本） |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
