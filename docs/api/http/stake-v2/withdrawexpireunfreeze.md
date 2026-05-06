# /wallet/withdrawexpireunfreeze

提取已到期的解冻 TRX 到余额（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/WithdrawExpireUnfreezeServlet.java`
- Method：`POST`
- Contract：`protocol.WithdrawExpireUnfreezeContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 账户地址 |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/withdrawexpireunfreeze \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

构造前校验账户是否存在到期解冻条目。示例账户无可提取条目，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : no unFreeze balance to withdraw "}
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
          "type_url": "type.googleapis.com/protocol.WithdrawExpireUnfreezeContract"
        },
        "type": "WithdrawExpireUnfreezeContract"
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
| 提案 #70 `UNFREEZE_DELAY_DAYS` 未激活 | `{"Error": "class org.tron.core.exception.ContractValidateException : Not support WithdrawExpireUnfreeze transaction, need to be opened by the committee"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| 没有到期可提取的解冻余额 | `{"Error": "... : no unFreeze balance to withdraw "}` |
| 余额累加溢出 | `{"Error": "... : <ArithmeticException 信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
