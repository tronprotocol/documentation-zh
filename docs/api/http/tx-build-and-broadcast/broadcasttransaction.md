# /wallet/broadcasttransaction

广播一笔已签名的交易。

- 源码：`framework/src/main/java/org/tron/core/services/http/BroadcastServlet.java`
- Method：`POST`
- Response：`api.Return` + `txid`

## 请求参数

直接传 `protocol.Transaction` 的 JSON 表示（即 `createtransaction` 类接口的返回 + 签名）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `raw_data` | object | 是 | 与 createtransaction 返回一致 |
| `raw_data_hex` | string | 是 | raw_data 的 hex 编码 |
| `signature` | string[] | 是 | 签名数组（普通账户 1 个；多签按权限要求） |
| `visible` | bool | 否 | 地址、文本字段格式 |

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
| `result` | bool | 是否进入交易池 |
| `code` | enum | `SUCCESS` / `SIGERROR` / `CONTRACT_VALIDATE_ERROR` / `CONTRACT_EXE_ERROR` / `BANDWITH_ERROR` / `DUP_TRANSACTION_ERROR` / `TAPOS_ERROR` / `TOO_BIG_TRANSACTION_ERROR` / `TRANSACTION_EXPIRATION_ERROR` / `SERVER_BUSY` / `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` / `BLOCK_UNSOLIDIFIED` / `OTHER_ERROR` |
| `message` | string | 失败原因；`visible=true` 时为 UTF-8 文本，`visible=false` 时为 UTF-8 字节的 hex |
| `txid` | string | 交易哈希 |

`result: true` 仅代表节点已收且入池，最终是否上链需通过 [`/wallet/gettransactioninfobyid`](../block-and-tx-query/gettransactioninfobyid.md) 查询。

响应示例：

```json
{
  "result": true,
  "code": "SUCCESS",
  "txid": "d5ec749ecc2a615399d8a6c864ea4c74ff9f8453eaa44d6b1e2f0b7b3e2f3b6a"
}
```

### 异常响应

业务级错误**仍按上面的 `result/code/message` 形态返回**，例如：

```json
{ "result": false, "code": "DUP_TRANSACTION_ERROR", "message": "Dup transaction.", "txid": "..." }
{ "result": false, "code": "SIGERROR", "message": "validateSignature error", "txid": "..." }
{ "result": false, "code": "TAPOS_ERROR", "message": "Tapos failed", "txid": "..." }
```

`code` 含义：

| code | 含义 |
|---|---|
| `SIGERROR` | 签名校验失败 |
| `CONTRACT_VALIDATE_ERROR` | 合约前置校验失败（余额不足、参数非法等） |
| `CONTRACT_EXE_ERROR` | 执行期失败 |
| `BANDWITH_ERROR` | 带宽不足 |
| `DUP_TRANSACTION_ERROR` | 重复交易 |
| `TAPOS_ERROR` | `ref_block_*` 不在链上（最常见于交易过期或链未同步） |
| `TOO_BIG_TRANSACTION_ERROR` | 交易体积超限 |
| `TRANSACTION_EXPIRATION_ERROR` | `expiration` 已过期 |
| `SERVER_BUSY` | 节点繁忙（pending 满） |
| `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` | 节点对外连接不足，未广播 |
| `BLOCK_UNSOLIDIFIED` | 区块尚未固化（针对相关查询） |
| `OTHER_ERROR` | 其他 |

JSON 解析失败、`raw_data_hex` 非法 hex、签名数组类型错等走 `Util.processError`：

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` |
| `raw_data_hex` 不是合法 hex | `{"Error": "class java.lang.NullPointerException : <message>"}`（`Util.packTransaction` 捕获 `JsonFormat$ParseException` 后返 null，下游空指针） |
| 字段类型不符 / `signature` 非 hex 等 | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
