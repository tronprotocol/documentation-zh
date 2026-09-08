# /wallet/freezebalancev2

冻结 TRX 获取带宽 / 能量 / TronPower（Stake 2.0）。无固定冻结期。

- 源码：`framework/src/main/java/org/tron/core/services/http/FreezeBalanceV2Servlet.java`
- Method：`POST`
- Contract：`protocol.FreezeBalanceV2Contract`（`balance_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 冻结账户地址 |
| `frozen_balance` | int64 | 是 | 冻结金额（sun） |
| `resource` | enum | 否 | `BANDWIDTH` / `ENERGY` / `TRON_POWER`，默认 `BANDWIDTH` |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/freezebalancev2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":  "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "frozen_balance": 1000000000,
  "resource":       "ENERGY"
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "081256264131fbc9f3d4686aab15ae69c0e77b39d276367c11a7ab13e39747ec",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "resource": "ENERGY",
            "frozen_balance": 1000000000,
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
          },
          "type_url": "type.googleapis.com/protocol.FreezeBalanceV2Contract"
        },
        "type": "FreezeBalanceV2Contract"
      }
    ],
    "ref_block_bytes": "283b",
    "ref_block_hash": "51bf0b88daaaea37",
    "expiration": 1777446819000,
    "timestamp": 1777446761432
  },
  "raw_data_hex": "0a02283b220851bf0b88daaaea3740b8a9d8c0dd335a5b083612570a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121f0a1541dd791d6b49e190062d650e6a23c575510d35f2f9108094ebdc03180170d8e7d4c0dd33"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 提案 #70 `UNFREEZE_DELAY_DAYS` 未激活 | `{"Error": "class org.tron.core.exception.ContractValidateException : Not support FreezeV2 transaction, need to be opened by the committee"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| `frozen_balance <= 0` | `{"Error": "... : frozenBalance must be positive"}` |
| `frozen_balance < 1_000_000`（不足 1 TRX） | `{"Error": "... : frozenBalance must be greater than or equal to 1 TRX"}` |
| `frozen_balance` 超过账户余额 | `{"Error": "... : frozenBalance must be less than or equal to accountBalance"}` |
| `resource = TRON_POWER` 但未启用新资源模型 | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` |
| `resource` 是其他非法值（启用新资源模型） | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY、TRON_POWER]"}` |
| `resource` 是其他非法值（未启用新资源模型） | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
