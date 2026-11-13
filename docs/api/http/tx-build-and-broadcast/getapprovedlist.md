# /wallet/getapprovedlist

根据账户当前权限验证全部签名后，返回交易的签名地址。验证失败时返回错误，不返回已批准地址列表。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionApprovedListServlet.java`
- Method：`POST`
- Response：`api.TransactionApprovedList`（`api.proto`）

## 请求参数

请求体同 [`/wallet/getsignweight`](getsignweight.md)：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `raw_data` | object | 是 | 与 createtransaction 返回一致 |
| `raw_data_hex` | string | 否（节点忽略） | 同 [`broadcasttransaction`](broadcasttransaction.md)：客户端可视化辅助字段，不参与验签 |
| `signature` | string[] | 否 | 已收集的签名；省略时仍可解析请求，若账户和权限检查通过，已批准地址列表为空 |
| `visible` | bool | 否 | 控制地址及 bytes 字段的格式；`result.message` 是 protobuf string，无论 `visible` 取值如何，均保持为 JSON 文本 |

示例：请求体为带 `signature` 的 Transaction JSON，结构同 [`/wallet/broadcasttransaction`](broadcasttransaction.md)。

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getapprovedlist \
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

> 上例为占位结构。实际权限检查通常使用由 [`/wallet/createtransaction`](createtransaction.md) 等接口生成并加签的多签交易 JSON，但该接口也接受空的或省略的 `signature` 数组；若账户和权限检查通过，则不返回任何已批准地址。

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `approved_list` | repeated bytes | 已签名地址；`visible=true` 时为 base58 数组，`visible=false` 时为 hex（21 字节，带 `41` 前缀） |
| `result.code` | enum | `SUCCESS` / `SIGNATURE_FORMAT_ERROR` / `COMPUTE_ADDRESS_ERROR` / `OTHER_ERROR` |
| `result.message` | string | 错误描述，始终为 JSON 文本，不受 `visible` 影响 |
| `transaction` | TransactionExtention | 提交的交易及其已收集的签名 |

成功时，`result.code` 为 protobuf 默认值 `SUCCESS`，会在 JSON 中省略；因此没有消息时，result 对象为 `{}`。

响应示例：

```json
{
  "approved_list": ["41dd791d6b49e190062d650e6a23c575510d35f2f9"],
  "result":       {},
  "transaction": {
    "txid":        "<由 raw_data 计算>",
    "result":      { "result": true },
    "transaction": { "...": "..." }
  }
}
```

> 注意：交易 JSON 解码后，签名格式、地址恢复和权限检查失败会写入响应的 `result.code` / `result.message`（HTTP 200）。下表列出返回 `{"Error": ...}` 形式响应的情况，包括 JSON 解码阶段的非法签名 hex。

protobuf JSON 解析器也接受将单个 hex 字符串作为 `signature`，并将其视为仅含一个元素的列表；非数组值不一定导致解析错误。正常请求请使用文档规定的数组形式。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| `raw_data` / `raw_data.contract` 缺失或为 null | 访问缺失的对象或数组时返回 `{"Error": "class java.lang.NullPointerException : <message>"}` |
| `raw_data` 不是对象，或 `raw_data.contract` 不是数组（不包括能解析为所需结构的 JSON 字符串） | `{"Error": "class org.tron.json.JSONException : <message>"}`，例如 `Field 'contract' is not an array` |
| 签名 hex 非法，或 `raw_data` 中的字段值无法由 `JsonFormat.merge` 解码 | `packTransaction` 捕获最终的 `JsonFormat$ParseException` 并返回 `null`，下游操作随后返回 `{"Error": "class java.lang.NullPointerException : <message>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
