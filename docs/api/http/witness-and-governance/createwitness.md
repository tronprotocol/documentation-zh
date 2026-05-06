# /wallet/createwitness

申请成为超级代表候选人，需消耗 9999 TRX（链参数 `getAccountUpgradeCost`）。

- 源码：`framework/src/main/java/org/tron/core/services/http/CreateWitnessServlet.java`
- Method：`POST`
- Contract：`protocol.WitnessCreateContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 申请账户地址 |
| `url` | string | 是 | 候选人 URL（hex UTF-8） |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createwitness \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "url":           "68747470733a2f2f747261782e696f"
}
'
```

## 响应

构造前校验账户余额是否大于等于 `getAccountUpgradeCost`（9999 TRX），且账户当前不在 SR 候选人列表中。示例账户余额不足，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : balance < AccountUpgradeCost"}
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
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "url":           "68747470733a2f2f747261782e696f"
          },
          "type_url": "type.googleapis.com/protocol.WitnessCreateContract"
        },
        "type": "WitnessCreateContract"
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
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| `url` 非法（空、长度过长） | `{"Error": "... : Invalid url"}` |
| owner 账户不存在 | `{"Error": "... : account[<address>] not exists"}` |
| 该地址已是 SR 候选人 | `{"Error": "... : Witness[<address>] has existed"}` |
| 余额 < `AccountUpgradeCost`（默认 9999 TRX） | `{"Error": "... : balance < AccountUpgradeCost"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
