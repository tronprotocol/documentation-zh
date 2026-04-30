# /wallet/updateaccount

修改账户昵称（account_name）。该字段不唯一。

- 源码：`framework/src/main/java/org/tron/core/services/http/UpdateAccountServlet.java`
- Method：`POST`（`GET` 不实现）
- Contract：`protocol.AccountUpdateContract`（`account_contract.proto:33`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 账户地址 |
| `account_name` | string | 是 | 新的账户名（hex 编码 UTF-8） |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updateaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "account_name": "6e69636b6e616d65"
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "cc4a646f211c1f92a6b1491ee625c7f6d055d031eba38e3fe8bfe2075ecc11c9",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "account_name": "6e69636b6e616d65",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
          },
          "type_url": "type.googleapis.com/protocol.AccountUpdateContract"
        },
        "type": "AccountUpdateContract"
      }
    ],
    "ref_block_bytes": "2704",
    "ref_block_hash": "f6ca8374136773d8",
    "expiration": 1777445880000,
    "timestamp": 1777445820842
  },
  "raw_data_hex": "0a0227042208f6ca8374136773d840c0819fc0dd335a5b080a12570a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74557064617465436f6e747261637412210a086e69636b6e616d65121541dd791d6b49e190062d650e6a23c575510d35f2f970aab39bc0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `account_name` 长度超过 200 字节 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid accountName"}` |
| `owner_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| `owner_address` 在链上不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Account does not exist"}` |
| 账户已设置过 `account_name` 且 `AllowUpdateAccountName=0` | `{"Error": "class org.tron.core.exception.ContractValidateException : This account name is already existed"}` |
| 该 `account_name` 已被其他账户占用且 `AllowUpdateAccountName=0` | `{"Error": "class org.tron.core.exception.ContractValidateException : This name is existed"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
