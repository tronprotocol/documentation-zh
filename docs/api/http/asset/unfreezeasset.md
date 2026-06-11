# /wallet/unfreezeasset

解冻发行方在 `frozen_supply` 中冻结的 token 份额（仅 TRC10 发行方调用，到期后才能成功）。

- 源码：`framework/src/main/java/org/tron/core/services/http/UnFreezeAssetServlet.java`
- Method：`POST`
- Contract：`protocol.UnfreezeAssetContract`（`asset_issue_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | TRC10 发行方地址 |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/unfreezeasset \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884"
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "bd5088fe645fbbaf7e4410a170e78d9645ecaa1c52f457fa9635a76ddc74276b",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884"
          },
          "type_url": "type.googleapis.com/protocol.UnfreezeAssetContract"
        },
        "type": "UnfreezeAssetContract"
      }
    ],
    "ref_block_bytes": "2799",
    "ref_block_hash": "0734893a1ba1ff5e",
    "expiration": 1777446327000,
    "timestamp": 1777446268128
  },
  "raw_data_hex": "0a02279922080734893a1ba1ff5e40d8a5bac0dd335a51080e124d0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a654173736574436f6e747261637412170a1541088a2bfcb1c7271029fd69a66859d5556089588470e0d9b6c0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] does not exist"}` |
| 没有任何冻结供应（`frozen_supply` 为空） | `{"Error": "... : no frozen supply balance"}` |
| 该账户从未发行过 token | `{"Error": "... : this account has not issued any asset"}` |
| 没有任何冻结到期 | `{"Error": "... : It's not time to unfreeze asset supply"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
