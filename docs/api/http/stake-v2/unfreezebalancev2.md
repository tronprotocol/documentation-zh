# /wallet/unfreezebalancev2

发起解冻申请（Stake 2.0），进入 14 天等待期，到期后通过 [`/wallet/withdrawexpireunfreeze`](withdrawexpireunfreeze.md) 提取。

- 源码：`framework/src/main/java/org/tron/core/services/http/UnFreezeBalanceV2Servlet.java`
- Method：`POST`
- Contract：`protocol.UnfreezeBalanceV2Contract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 解冻账户地址 |
| `unfreeze_balance` | int64 | 是 | 解冻金额（sun） |
| `resource` | enum | 否 | `BANDWIDTH` / `ENERGY` / `TRON_POWER` |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/unfreezebalancev2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "unfreeze_balance": 1000000000,
  "resource":         "ENERGY"
}
'
```

## 响应

构造前会校验 owner 在指定 `resource` 下有足够冻结额。示例账户在 ENERGY 维度无 V2 冻结，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(Energy)"}
```

校验通过时返回未签名 `protocol.Transaction`，结构示意（`txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` 含义同 [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)）：

```json
{
  "visible": false,
  "txID": "<由 raw_data 计算>",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "unfreeze_balance": 1000000000,
            "resource":         "ENERGY"
          },
          "type_url": "type.googleapis.com/protocol.UnfreezeBalanceV2Contract"
        },
        "type": "UnfreezeBalanceV2Contract"
      }
    ],
    "ref_block_bytes": "<构造时最新固化块>",
    "ref_block_hash":  "<构造时最新固化块>",
    "expiration":      "<timestamp + 60_000>",
    "timestamp":       "<构造时刻>"
  },
  "raw_data_hex": "<raw_data 的 protobuf 编码>"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 提案 #70 `UNFREEZE_DELAY_DAYS` 未激活 | `{"Error": "class org.tron.core.exception.ContractValidateException : Not support UnfreezeV2 transaction, need to be opened by the committee"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] does not exist"}` |
| `resource = BANDWIDTH` 但无对应冻结 | `{"Error": "... : no frozenBalance(BANDWIDTH)"}` |
| `resource = ENERGY` 但无对应冻结 | `{"Error": "... : no frozenBalance(Energy)"}` |
| `resource = TRON_POWER`（启用新资源模型）但无对应冻结 | `{"Error": "... : no frozenBalance(TronPower)"}` |
| `resource = TRON_POWER` 但未启用新资源模型 | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}` |
| `resource` 是其他非法值（启用新资源模型） | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy、TRON_POWER]"}` |
| `resource` 是其他非法值（未启用新资源模型） | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}` |
| `unfreeze_balance` 非法（<=0、超过可解冻额、有授权未召回等） | `{"Error": "... : Invalid unfreeze_balance, [<n>] is error"}` |
| 同时进行的解冻次数超过 `UNFREEZE_MAX_TIMES` | `{"Error": "... : Invalid unfreeze operation, unfreezing times is over limit"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
