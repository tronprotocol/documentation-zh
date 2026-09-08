# /wallet/withdrawbalance

提取 SR 出块奖励或投票账户的分红奖励到余额。

- 源码：`framework/src/main/java/org/tron/core/services/http/WithdrawBalanceServlet.java`
- Method：`POST`
- Contract：`protocol.WithdrawBalanceContract`（`balance_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 领取账户地址（SR 或投票者） |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/withdrawbalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "ee9e2c192a1c9508e5d4944c000dbe3b99f05399221a9b02848cd44ef27cc8a3",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
          },
          "type_url": "type.googleapis.com/protocol.WithdrawBalanceContract"
        },
        "type": "WithdrawBalanceContract"
      }
    ],
    "ref_block_bytes": "27d2",
    "ref_block_hash": "bd570b8df4e022d6",
    "expiration": 1777446498000,
    "timestamp": 1777446439141
  },
  "raw_data_hex": "0a0227d22208bd570b8df4e022d640d0ddc4c0dd335a53080d124f0a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e576974686472617742616c616e6365436f6e747261637412170a15419c7c7049d26108be0dcb5f78479c6ff27ba101d170e591c1c0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| owner 是创世 SR（GP） | `{"Error": "... : Account[<address>] is a guard representative and is not allowed to withdraw Balance"}` |
| 距上次领取不足 24 小时 | `{"Error": "... : The last withdraw time is <ts>, less than 24 hours"}` |
| 没有任何奖励可提取 | `{"Error": "... : witnessAccount does not have any reward"}` |
| 余额累加溢出 | `{"Error": "... : <ArithmeticException 信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
