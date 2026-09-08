# /wallet/delegateresource

把已冻结资源代理给其他账户使用（Stake 2.0）。

- 源码：`framework/src/main/java/org/tron/core/services/http/DelegateResourceServlet.java`
- Method：`POST`
- Contract：`protocol.DelegateResourceContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 出借方地址 |
| `receiver_address` | string | 是 | 接收方地址 |
| `balance` | int64 | 是 | 代理对应的冻结量（sun） |
| `resource` | enum | 否 | `BANDWIDTH` / `ENERGY` |
| `lock` | bool | 否 | 是否锁定代理（true 时不可中途撤销） |
| `lock_period` | int64 | 否 | 锁定时长（块数，仅 lock=true） |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/delegateresource \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "receiver_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "balance":          1000000000,
  "resource":         "ENERGY",
  "lock":             false
}
'
```

## 响应

构造前校验 owner 在指定 `resource` 下当前可代理量是否足以覆盖 `balance`。示例账户在 ENERGY 维度无可代理量，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : delegateBalance must be less than or equal to available FreezeEnergyV2 balance"}
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
            "resource":         "ENERGY",
            "lock":             false
          },
          "type_url": "type.googleapis.com/protocol.DelegateResourceContract"
        },
        "type": "DelegateResourceContract"
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
| 链未启用资源代理 | `{"Error": "class org.tron.core.exception.ContractValidateException : No support for resource delegate"}` |
| 提案 #70 `UNFREEZE_DELAY_DAYS` 未激活 | `{"Error": "... : Not support Delegate resource transaction, need to be opened by the committee"}` |
| `owner_address` 非法 | `{"Error": "... : Invalid address"}` |
| owner 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| `balance < 1_000_000`（不足 1 TRX） | `{"Error": "... : delegateBalance must be greater than or equal to 1 TRX"}` |
| BANDWIDTH 可代理量不足 | `{"Error": "... : delegateBalance must be less than or equal to available FreezeBandwidthV2 balance"}` |
| ENERGY 可代理量不足 | `{"Error": "... : delegateBalance must be less than or equal to available FreezeEnergyV2 balance"}` |
| `resource` 是其他非法值 | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` |
| `receiver_address` 非法 | `{"Error": "... : Invalid receiverAddress"}` |
| `receiver_address == owner_address` | `{"Error": "... : receiverAddress must not be the same as ownerAddress"}` |
| receiver 账户不存在 | `{"Error": "... : Account[<address>] not exists"}` |
| `lock_period` 越界（提案 #76 之后） | `{"Error": "... : The lock period of delegate resource cannot be less than 0 and cannot exceed <max>!"}` |
| 已锁定代理仍在锁定期，新锁定期更短 | `{"Error": "... : The lock period for <Resource> this time cannot be less than the remaining time[<n>ms] of the last lock period for <Resource>!"}` |
| receiver 是合约地址 | `{"Error": "... : Do not allow delegate resources to contract addresses"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
