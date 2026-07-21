# /wallet/proposalapprove

SR 对提案投票（赞成/取消赞成）。

- 源码：`framework/src/main/java/org/tron/core/services/http/ProposalApproveServlet.java`
- Method：`POST`
- Contract：`protocol.ProposalApproveContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | SR 地址 |
| `proposal_id` | int64 | 是 | 提案 ID |
| `is_add_approval` | bool | 否 | `true`=赞成，`false`=取消赞成；省略时默认为 `false` |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/proposalapprove \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":   "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "proposal_id":     1,
  "is_add_approval": true
}
'
```

## 响应

构造前会校验提案当前状态，因此真实调用须使用未过期 / 未被取消的提案 ID（`/wallet/listproposals` 中 `state` 为 `PENDING` 的项）。示例的 `proposal_id=1` 在 Nile 上早已过期，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : Proposal[1] expired"}
```

省略 `is_add_approval` 时，请求进入取消赞成分支；仅当该 witness 此前已赞成该提案时才会成功。

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
            "owner_address":   "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "proposal_id":     1,
            "is_add_approval": true
          },
          "type_url": "type.googleapis.com/protocol.ProposalApproveContract"
        },
        "type": "ProposalApproveContract"
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
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| owner 不是 SR | `{"Error": "... : Witness[<address>] not exists"}` |
| `proposal_id` > 最新提案编号 | `{"Error": "... : Proposal[<id>] not exists"}` |
| 提案 ID 在存储中找不到 | `{"Error": "... : Proposal[<id>] not exists"}` |
| 提案已过期 | `{"Error": "... : Proposal[<id>] expired"}` |
| 提案已被取消 | `{"Error": "... : Proposal[<id>] canceled"}` |
| `is_add_approval=false` 且此前未投赞成 | `{"Error": "... : Witness[<address>]has not approved proposal[<id>] before"}` |
| `is_add_approval=true` 且此前已投赞成 | `{"Error": "... : Witness[<address>]has approved proposal[<id>] before"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
