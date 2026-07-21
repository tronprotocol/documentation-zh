# /wallet/updatewitness

修改 SR 候选人 URL（仅候选人本人）。

- 源码：`framework/src/main/java/org/tron/core/services/http/UpdateWitnessServlet.java`
- Method：`POST`
- Contract：`protocol.WitnessUpdateContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 候选人地址 |
| `update_url` | string | 是 | 新 URL（hex UTF-8） |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updatewitness \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "update_url":    "68747470733a2f2f747261782e696f"
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "9452c5a333ccd579a720e406c2acb0b11d26cad7a8c01876ba3cfddc10f250b5",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "update_url": "68747470733a2f2f747261782e696f"
          },
          "type_url": "type.googleapis.com/protocol.WitnessUpdateContract"
        },
        "type": "WitnessUpdateContract"
      }
    ],
    "ref_block_bytes": "27c7",
    "ref_block_hash": "e51bd4751a4d7222",
    "expiration": 1777446465000,
    "timestamp": 1777446406948
  },
  "raw_data_hex": "0a0227c72208e51bd4751a4d722240e8dbc2c0dd335a620808125e0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5769746e657373557064617465436f6e747261637412280a15419c7c7049d26108be0dcb5f78479c6ff27ba101d1620f68747470733a2f2f747261782e696f70a496bfc0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : account does not exist"}` |
| `update_url` 非法（空、长度过长） | `{"Error": "... : Invalid url"}` |
| 该地址不是 SR 候选人 | `{"Error": "... : Witness does not exist"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
