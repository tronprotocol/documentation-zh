# /wallet/undelegateresource

撤销资源代理（Stake 2.0），收回代理量。

- 源码：`framework/src/main/java/org/tron/core/services/http/UnDelegateResourceServlet.java`
- Method：`POST`
- Contract：`protocol.UnDelegateResourceContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 出借方地址 |
| `receiver_address` | string | 是 | 接收方地址 |
| `balance` | int64 | 是 | 撤销代理的冻结量（sun） |
| `resource` | enum | 否 | `BANDWIDTH` / `ENERGY` |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/undelegateresource \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "receiver_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "balance":          1000000000,
  "resource":         "ENERGY"
}
'
```

## 响应

构造前校验 (owner, receiver) 之间在指定 `resource` 下存在足够的可撤销代理量。示例账户对该 receiver 无 ENERGY 代理记录，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : delegated Resource does not exist"}
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
            "receiver_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
            "balance":          1000000000,
            "resource":         "ENERGY"
          },
          "type_url": "type.googleapis.com/protocol.UnDelegateResourceContract"
        },
        "type": "UnDelegateResourceContract"
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
| 链未启用资源代理 | `{"Error": "class org.tron.core.exception.ContractValidateException : No support for resource delegate"}` |
| 提案 #70 `UNFREEZE_DELAY_DAYS` 未激活 | `{"Error": "... : Not support unDelegate resource transaction, need to be opened by the committee"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] does not exist"}` |
| `receiver_address` 非法 | `{"Error": "... : Invalid receiverAddress"}` |
| `receiver_address == owner_address` | `{"Error": "... : receiverAddress must not be the same as ownerAddress"}` |
| 该 (owner, receiver) 之间没有代理关系 | `{"Error": "... : delegated Resource does not exist"}` |
| `balance <= 0` | `{"Error": "... : unDelegateBalance must be more than 0 TRX"}` |
| BANDWIDTH 可撤销量不足（含未到期锁定不计入） | `{"Error": "... : insufficient delegatedFrozenBalance(BANDWIDTH), request=<n>, unlock_balance=<m>"}` |
| ENERGY 可撤销量不足 | `{"Error": "... : insufficient delegateFrozenBalance(Energy), request=<n>, unlock_balance=<m>"}` |
| `resource` 是其他非法值 | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
