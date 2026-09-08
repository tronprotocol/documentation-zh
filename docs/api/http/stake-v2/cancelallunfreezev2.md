# /wallet/cancelallunfreezev2

取消账户所有未到期的解冻申请，未到期部分重新转为冻结状态，已到期部分自动提取到余额。

- 源码：`framework/src/main/java/org/tron/core/services/http/CancelAllUnfreezeV2Servlet.java`
- Method：`POST`
- Contract：`protocol.CancelAllUnfreezeV2Contract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 账户地址 |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/cancelallunfreezev2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

构造前校验账户存在未到期的解冻条目。示例账户无解冻条目，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : No unfreezeV2 list to cancel"}
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
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
          },
          "type_url": "type.googleapis.com/protocol.CancelAllUnfreezeV2Contract"
        },
        "type": "CancelAllUnfreezeV2Contract"
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
| 提案 #75 `CANCEL_ALL_UNFREEZE_V2` 未激活 | `{"Error": "class org.tron.core.exception.ContractValidateException : Not support CancelAllUnfreezeV2 transaction, need to be opened by the committee"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| 没有任何待解冻条目 | `{"Error": "... : No unfreezeV2 list to cancel"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
