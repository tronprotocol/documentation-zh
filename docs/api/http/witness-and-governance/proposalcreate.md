# /wallet/proposalcreate

创建链参数提案（仅 SR）。

- 源码：`framework/src/main/java/org/tron/core/services/http/ProposalCreateServlet.java`
- Method：`POST`
- Contract：`protocol.ProposalCreateContract`（`proposal_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | SR 地址 |
| `parameters` | array<{key, value}> | 是 | 提案参数项；`key` 为参数编号，`value` 为目标取值 |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

参数编号见 [`/wallet/getchainparameters`](getchainparameters.md) 返回的 key。

> 注意：servlet 通过 `JsonFormat` 解析 protobuf；`parameters` 须是数组形式 `[{"key":N,"value":V}]`，使用 map 形式 `{"<N>": V}` 时所有 key 都会被解析为 0 而触发参数 0 的范围校验。

示例（提案 31 号参数 `getAllowMultiSign` 设为 1）：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/proposalcreate \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "parameters": [
    {"key": 31, "value": 1}
  ]
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "d749a445802ea86230d52fb35645ab497612dec59794f815d1418c1b03b67d02",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "parameters": [
              { "key": 31, "value": 1 }
            ]
          },
          "type_url": "type.googleapis.com/protocol.ProposalCreateContract"
        },
        "type": "ProposalCreateContract"
      }
    ],
    "ref_block_bytes": "27e2",
    "ref_block_hash": "c4c88851291881b3",
    "expiration": 1777446546000,
    "timestamp": 1777446488573
  },
  "raw_data_hex": "0a0227e22208c4c88851291881b340d0d4c7c0dd335a58081012540a33747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e50726f706f73616c437265617465436f6e7472616374121d0a15419c7c7049d26108be0dcb5f78479c6ff27ba101d11204081f100170fd93c4c0dd33"
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
| `parameters` 为空 | `{"Error": "... : This proposal has no parameter."}` |
| 参数 key/value 非法（编号越界、取值超限、未达提案生效条件等） | `{"Error": "... : <ProposalUtil 校验信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
