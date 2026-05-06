# /wallet/votewitnessaccount

为超级代表（SR）投票。一次性覆盖账户当前所有投票。

- 源码：`framework/src/main/java/org/tron/core/services/http/VoteWitnessAccountServlet.java`
- Method：`POST`
- Contract：`protocol.VoteWitnessContract`（`witness_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 投票账户地址 |
| `votes` | array<Vote> | 是 | 投票列表 |
| `votes[].vote_address` | string | 是 | SR 候选人地址 |
| `votes[].vote_count` | int64 | 是 | 票数（消耗 TRON Power） |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/votewitnessaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "votes": [
    {
      "vote_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
      "vote_count": 100
    }
  ]
}
'
```

## 响应

构造前会校验账户当前 TRON Power 是否覆盖总投票数，未质押 TRX 的账户无法投票。示例账户 TRON Power 为 0，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : The total number of votes[100000000] is greater than the tronPower[0]"}
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
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "votes": [
              {
                "vote_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
                "vote_count": 100
              }
            ]
          },
          "type_url": "type.googleapis.com/protocol.VoteWitnessContract"
        },
        "type": "VoteWitnessContract"
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
| `votes` 列表为空 | `{"Error": "... : VoteNumber must more than 0"}` |
| `votes` 列表长度超过 `MAX_VOTE_NUMBER` | `{"Error": "... : VoteNumber more than maxVoteNumber <N>"}` |
| `votes[].vote_address` 非法 | `{"Error": "... : Invalid vote address!"}` |
| `votes[].vote_count <= 0` | `{"Error": "... : vote count must be greater than 0"}` |
| 候选人地址无对应账户 | `{"Error": "... : Account[<address>] not exists"}` |
| 候选人不是 SR | `{"Error": "... : Witness[<address>] not exists"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| 总票数超过账户 TRON Power | `{"Error": "... : The total number of votes[<n>] is greater than the tronPower[<m>]"}` |
| 票数累加溢出 | `{"Error": "... : <ArithmeticException 信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
