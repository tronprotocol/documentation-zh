# /wallet/transferasset

TRC-10 token 转账。

- 源码：`framework/src/main/java/org/tron/core/services/http/TransferAssetServlet.java`
- Method：`POST`
- Contract：`protocol.TransferAssetContract`（`asset_issue_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 发起方 |
| `to_address` | string | 是 | 接收方 |
| `asset_name` | string | 是 | token ID（自 `ALLOW_SAME_TOKEN_NAME` 提案生效后是字符串形式的 token id，如 `1000001`，hex UTF-8 编码） |
| `amount` | int64 | 是 | 转账数量（最小单位） |
| `extra_data` | string | 否 | 交易备注（hex；`visible=true` 时为 UTF-8 文本） |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/transferasset \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "to_address":    "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "asset_name":    "31303035343136",
  "amount": 100
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`asset_name` `31303035343136` 解码为 token id `1005416`；`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "7a8b50753079977b2cc0ddc19309c568e5bcaa8d2d865b3d96b40719b1b8df6f",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "amount": 100,
            "asset_name": "31303035343136",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "to_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
          },
          "type_url": "type.googleapis.com/protocol.TransferAssetContract"
        },
        "type": "TransferAssetContract"
      }
    ],
    "ref_block_bytes": "2765",
    "ref_block_hash": "d2e724f76534cfc4",
    "expiration": 1777446171000,
    "timestamp": 1777446111063
  },
  "raw_data_hex": "0a0227652208d2e724f76534cfc440f8e2b0c0dd335a730802126f0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e736665724173736574436f6e747261637412390a0731303035343136121541dd791d6b49e190062d650e6a23c575510d35f2f91a154192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a206470d78eadc0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| `to_address` 非法 | `{"Error": "... : Invalid toAddress"}` |
| `amount <= 0` | `{"Error": "... : Amount must be greater than 0."}` |
| 转账给自己 | `{"Error": "... : Cannot transfer asset to yourself."}` |
| owner 账户不存在 | `{"Error": "... : No owner account!"}` |
| 指定 token 不存在 | `{"Error": "... : No asset!"}` |
| owner 该 token 余额不存在 | `{"Error": "... : assetBalance must be greater than 0."}` |
| owner 该 token 余额不足 | `{"Error": "... : assetBalance is not sufficient."}` |
| 转账目标为合约地址（提案 #41 之后） | `{"Error": "... : Cannot transfer asset to smartContract."}` |
| 余额累加溢出 | `{"Error": "... : long overflow"}` |
| 接收方账户不存在且 owner 余额不足创建账户费 | `{"Error": "... : Validate TransferAssetActuator error, insufficient fee."}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
