# /wallet/participateassetissue

参与 TRC10 募集（用 TRX 购买）。

- 源码：`framework/src/main/java/org/tron/core/services/http/ParticipateAssetIssueServlet.java`
- Method：`POST`
- Contract：`protocol.ParticipateAssetIssueContract`（`asset_issue_contract.proto:55`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 购买方 |
| `to_address` | string | 是 | 通证发行方地址 |
| `asset_name` | string | 是 | 通证 ID（自 `ALLOW_SAME_TOKEN_NAME` 提案生效后是字符串形式的 token id，如 `1000001`，hex UTF-8 编码） |
| `amount` | int64 | 是 | 支付的 TRX，sun |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式 |

约束：必须在 `[start_time, end_time)` 期间内；获得的通证数量按 `num/trx_num` 折算。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/participateassetissue \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "to_address":    "41088a2bfcb1c7271029fd69a66859d55560895884",
  "asset_name":    "31303035343136",
  "amount": 1000000
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`asset_name` `31303035343136` 解码为 token id `1005416`；`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "1c2d37ad679f720266a0565d0170bcce2b4d096953badf5c848b85137005b5d4",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "amount": 1000000,
            "asset_name": "31303035343136",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "to_address": "41088a2bfcb1c7271029fd69a66859d55560895884"
          },
          "type_url": "type.googleapis.com/protocol.ParticipateAssetIssueContract"
        },
        "type": "ParticipateAssetIssueContract"
      }
    ],
    "ref_block_bytes": "2794",
    "ref_block_hash": "ba3c3fb8fa06d426",
    "expiration": 1777446312000,
    "timestamp": 1777446253445
  },
  "raw_data_hex": "0a0227942208ba3c3fb8fa06d42640c0b0b9c0dd335a7d080912790a3a747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e506172746963697061746541737365744973737565436f6e7472616374123b0a1541dd791d6b49e190062d650e6a23c575510d35f2f9121541088a2bfcb1c7271029fd69a66859d555608958841a073130303534313620c0843d7085e7b5c0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| `to_address` 非法 | `{"Error": "... : Invalid toAddress"}` |
| `amount <= 0` | `{"Error": "... : Amount must greater than 0!"}` |
| owner == to | `{"Error": "... : Cannot participate asset Issue yourself !"}` |
| owner 账户不存在 | `{"Error": "... : Account does not exist!"}` |
| owner 余额不足支付 amount + fee | `{"Error": "... : No enough balance !"}` |
| 指定 token 不存在 | `{"Error": "... : No asset named <name>"}` |
| `to_address` 不是该 token 的发行方 | `{"Error": "... : The asset is not issued by <toAddress hex>"}` |
| 不在募集时段内 | `{"Error": "... : No longer valid period!"}` |
| 兑换不能整除（无法精确换算） | `{"Error": "... : Can not process the exchange!"}` |
| `to_address` 账户不存在 | `{"Error": "... : To account does not exist!"}` |
| 募集方剩余可分发余额不足 | `{"Error": "... : Asset balance is not enough !"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
