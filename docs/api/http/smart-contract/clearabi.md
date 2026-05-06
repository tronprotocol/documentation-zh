# /wallet/clearabi

清空合约 ABI（仅合约部署者）。

- 源码：`framework/src/main/java/org/tron/core/services/http/ClearABIServlet.java`
- Method：`POST`
- Contract：`protocol.ClearABIContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 合约部署者地址 |
| `contract_address` | string | 是 | 目标合约地址 |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/clearabi \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
}
'
```

## 响应

构造前会校验 `owner_address` 必须是合约的 `origin_address`（部署者）。示例 `owner_address` 不是 TetherToken 部署者，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : Account[41dd791d6b49e190062d650e6a23c575510d35f2f9] is not the owner of the contract"}
```

校验通过时返回未签名 `protocol.Transaction`，结构示意（`txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` 含义同 [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)）：

```json
{
  "visible": false,
  "txID": "<由 raw_data 计算>",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
              "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
          },
          "type_url": "type.googleapis.com/protocol.ClearABIContract"
        },
        "type": "ClearABIContract"
      }
    ],
    "ref_block_bytes": "<构造时最新固化块>",
    "ref_block_hash":  "<构造时最新固化块>",
    "expiration":      "<timestamp + 60_000>",
    "timestamp":       "<构造时刻>"
  },
  "raw_data_hex": "<raw_data 的 protobuf 编码>"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 链未激活 TVM Constantinople | `{"Error": "class org.tron.core.exception.ContractValidateException : contract type error,unexpected type [ClearABIContract]"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| 合约地址不存在 | `{"Error": "... : Contract not exists"}` |
| owner 不是合约部署者 | `{"Error": "... : Account[<address>] is not the owner of the contract"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
