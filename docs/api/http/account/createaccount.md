# /wallet/createaccount

创建一个新账户的未签名交易。被动激活：付费方（owner_address）支付激活费用，新账户地址（account_address）即被创建。

- 源码：`framework/src/main/java/org/tron/core/services/http/CreateAccountServlet.java`
- Method：`POST`
- Contract：`protocol.AccountCreateContract`（`protocol/src/main/protos/core/contract/account_contract.proto:26`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 付费方地址 |
| `account_address` | string | 是 | 待创建的新账户地址 |
| `type` | enum | 否 | 0=Normal（默认），1=AssetIssue，2=Contract |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "account_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
}
'
```

## 响应

返回未签名 `protocol.Transaction`（包含 `txID`、`raw_data`、`raw_data_hex`，`signature` 为空）。需要本地签名后再调用 `/wallet/broadcasttransaction` 或 `/wallet/broadcasthex`。

响应示例（`txID`、`ref_block_bytes`、`ref_block_hash`、`expiration`、`timestamp`、`raw_data_hex` 由当前节点高度决定，每次调用都会变化）：

```json
{
  "visible": false,
  "txID": "411bbca37a92b5a9554274c5f0f05b0e486136d3bfe072c1c6454460b5290df3",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "account_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
          },
          "type_url": "type.googleapis.com/protocol.AccountCreateContract"
        },
        "type": "AccountCreateContract"
      }
    ],
    "ref_block_bytes": "26fc",
    "ref_block_hash": "e6e9a02b83e65c03",
    "expiration": 1777445856000,
    "timestamp": 1777445797130
  },
  "raw_data_hex": "0a0226fc2208e6e9a02b83e65c034080c69dc0dd335a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a1541dd791d6b49e190062d650e6a23c575510d35f2f912154192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a708afa99c0dd33"
}
```

激活账户费用从 `owner_address` 扣除，金额由链参数决定（一般 1 TRX）。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| `owner_address` 在链上不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] not exists"}` |
| `owner_address` 余额不足以支付激活费用 | `{"Error": "class org.tron.core.exception.ContractValidateException : Validate CreateAccountActuator error, insufficient fee."}` |
| `account_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid account address"}` |
| `account_address` 已存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Account has existed"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
