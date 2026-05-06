# /wallet/freezebalance

> **链上已禁用**：提案 #70 `UNFREEZE_DELAY_DAYS` 通过后（主网已生效），`FreezeBalanceActuator.validate()` 会直接抛出 `freeze v2 is open, old freeze is closed`，新请求一律失败。请改用 [`/wallet/freezebalancev2`](../stake-v2/freezebalancev2.md)。

冻结 TRX 获取带宽或能量，可代理给他人。冻结期最少 3 天。

- 源码：`framework/src/main/java/org/tron/core/services/http/FreezeBalanceServlet.java`
- Method：`POST`
- Contract：`protocol.FreezeBalanceContract`（`balance_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 冻结账户地址 |
| `frozen_balance` | int64 | 是 | 冻结金额（sun） |
| `frozen_duration` | int64 | 是 | 冻结天数（必须 ≥ 3） |
| `resource` | enum | 否 | `BANDWIDTH` / `ENERGY`，默认 `BANDWIDTH` |
| `receiver_address` | string | 否 | 资源代理目标地址（不填为自己） |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/freezebalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":   "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "frozen_balance":  1000000000,
  "frozen_duration": 3,
  "resource":        "BANDWIDTH"
}
'
```

## 响应

主网／Nile 已开启 Stake 2.0，本接口直接返回 `Error`：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : freeze v2 is open, old freeze is closed"}
```

提案 #70 未激活的链上仍会返回未签名 `protocol.Transaction`，结构示意（`txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` 含义同 [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)）：

```json
{
  "visible": false,
  "txID": "<由 raw_data 计算>",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
              "owner_address":   "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "frozen_balance":  1000000000,
              "frozen_duration": 3,
              "resource":        "BANDWIDTH"
          },
          "type_url": "type.googleapis.com/protocol.FreezeBalanceContract"
        },
        "type": "FreezeBalanceContract"
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
| 提案 #70 `UNFREEZE_DELAY_DAYS` 已激活（主网默认开启） | `{"Error": "class org.tron.core.exception.ContractValidateException : freeze v2 is open, old freeze is closed"}` |
| `owner_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| `owner_address` 在链上不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] not exists"}` |
| `frozen_balance <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenBalance must be positive"}` |
| `frozen_balance < 1_000_000`（不足 1 TRX） | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenBalance must be greater than or equal to 1 TRX"}` |
| 账户已有的 frozen 记录数不在 `{0,1}` | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenCount must be 0 or 1"}` |
| `frozen_balance > 账户余额` | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenBalance must be less than or equal to accountBalance"}` |
| `frozen_duration` 超出 `[minFrozenTime, maxFrozenTime]`（仅当 `--check-frozen-time=1`） | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenDuration must be less than <max> days and more than <min> days"}` |
| `resource` 取值非法（未启用 `AllowNewResourceModel` 时不允许 `TRON_POWER`） | `{"Error": "class org.tron.core.exception.ContractValidateException : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` 或 `... [BANDWIDTH、ENERGY、TRON_POWER]` |
| `resource=TRON_POWER` 但同时设置了 `receiver_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : TRON_POWER is not allowed to delegate to other accounts."}` |
| `receiver_address == owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : receiverAddress must not be the same as ownerAddress"}` |
| `receiver_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid receiverAddress"}` |
| `receiver_address` 在链上不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] not exists"}` |
| `receiver_address` 是合约地址且 `AllowTvmConstantinople` 已开启 | `{"Error": "class org.tron.core.exception.ContractValidateException : Do not allow delegate resources to contract addresses"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
