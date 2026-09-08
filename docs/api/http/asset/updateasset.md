# /wallet/updateasset

修改 TRC-10 token 的描述、URL 及带宽限额（仅发行方）。

- 源码：`framework/src/main/java/org/tron/core/services/http/UpdateAssetServlet.java`
- Method：`POST`
- Contract：`protocol.UpdateAssetContract`（`asset_issue_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 发行方地址 |
| `description` | string | 否 | 新描述（hex UTF-8） |
| `url` | string | 是 | 新 URL（hex UTF-8）；省略时默认为空值并导致 URL 校验失败 |
| `new_limit` | int64 | 否 | 单账户免费带宽限额 |
| `new_public_limit` | int64 | 否 | token 公共免费带宽限额 |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updateasset \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41088a2bfcb1c7271029fd69a66859d55560895884",
  "description":      "44494345",
  "url":              "68747470733a2f2f747261782e696f",
  "new_limit":        5000,
  "new_public_limit": 10000
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "6c1b46170308da102f2b70b4976ead59b3c9c02bba044c18da27f7e25779e10d",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
            "description": "44494345",
            "url": "68747470733a2f2f747261782e696f",
            "new_limit": 5000,
            "new_public_limit": 10000
          },
          "type_url": "type.googleapis.com/protocol.UpdateAssetContract"
        },
        "type": "UpdateAssetContract"
      }
    ],
    "ref_block_bytes": "2799",
    "ref_block_hash": "0734893a1ba1ff5e",
    "expiration": 1777446327000,
    "timestamp": 1777446269173
  },
  "raw_data_hex": "0a02279922080734893a1ba1ff5e40d8a5bac0dd335a6c080f12680a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5570646174654173736574436f6e747261637412340a1541088a2bfcb1c7271029fd69a66859d555608958841204444943451a0f68747470733a2f2f747261782e696f20882728904e70f5e1b6c0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| 账户不存在 | `{"Error": "... : Account does not exist"}` |
| 该账户没有发行过 token（V1） | `{"Error": "... : Account has not issued any asset"}` |
| AssetIssueStore 中 token 不存在（V1） | `{"Error": "... : Asset is not existed in AssetIssueStore"}` |
| AssetIssueV2Store 中 token 不存在 | `{"Error": "... : Asset is not existed in AssetIssueV2Store"}` |
| `url` 非法 | `{"Error": "... : Invalid url"}` |
| `description` 非法 | `{"Error": "... : Invalid description"}` |
| `new_limit` 非法 | `{"Error": "... : Invalid FreeAssetNetLimit"}` |
| `new_public_limit` 非法 | `{"Error": "... : Invalid PublicFreeAssetNetLimit"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
