# /wallet/proposaldelete

撤销自己创建的提案（仅提案发起人）。

- 源码：`framework/src/main/java/org/tron/core/services/http/ProposalDeleteServlet.java`
- Method：`POST`
- Contract：`protocol.ProposalDeleteContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 提案发起人地址 |
| `proposal_id` | int64 | 是 | 提案 ID |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/proposaldelete \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "proposal_id":   1
}
'
```

## 响应

构造前会校验调用者必须是该提案的发起人且提案未过期 / 未被取消，因此真实调用须使用 `/wallet/listproposals` 中 `state=PENDING` 且 `proposer_address` 等于 `owner_address` 的提案。示例账户不是 `proposal_id=1` 的发起人，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : Proposal[1] is not proposed by 419c7c7049d26108be0dcb5f78479c6ff27ba101d1"}
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
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "proposal_id":   1
          },
          "type_url": "type.googleapis.com/protocol.ProposalDeleteContract"
        },
        "type": "ProposalDeleteContract"
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
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| `proposal_id` > 最新提案编号 | `{"Error": "... : Proposal[<id>] not exists"}` |
| 提案 ID 在存储中找不到 | `{"Error": "... : Proposal[<id>] not exists"}` |
| 调用者不是该提案的发起人 | `{"Error": "... : Proposal[<id>] is not proposed by <address>"}` |
| 提案已过期 | `{"Error": "... : Proposal[<id>] expired"}` |
| 提案已被取消 | `{"Error": "... : Proposal[<id>] canceled"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
