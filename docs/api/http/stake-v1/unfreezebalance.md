# /wallet/unfreezebalance

> **存量保留**：与 `freezebalance` 不同，本接口在 Stake 2.0 启用后**仍可正常调用**——`UnfreezeBalanceActuator` 没有 `supportUnfreezeDelay` 网关，存量 V1 仓位需要通过它解冻。新业务请使用 [`/wallet/unfreezebalancev2`](../stake-v2/unfreezebalancev2.md)。

解冻已到期的 Stake 1.0 资产。

- 源码：`framework/src/main/java/org/tron/core/services/http/UnFreezeBalanceServlet.java`
- Method：`POST`
- Contract：`protocol.UnfreezeBalanceContract`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 解冻账户地址 |
| `resource` | enum | 否 | `BANDWIDTH` / `ENERGY`，默认 `BANDWIDTH` |
| `receiver_address` | string | 否 | 代理时填代理目标地址 |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/unfreezebalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "resource":      "BANDWIDTH"
}
'
```

## 响应

构造前会校验账户存在到期的 V1 冻结/代理记录。示例账户在 BANDWIDTH 维度无 V1 冻结，Nile 实抓返回：

```json
{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(BANDWIDTH)"}
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
              "resource":      "BANDWIDTH"
          },
          "type_url": "type.googleapis.com/protocol.UnfreezeBalanceContract"
        },
        "type": "UnfreezeBalanceContract"
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
| `owner_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| `owner_address` 在链上不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] does not exist"}` |
| `receiver_address == owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : receiverAddress must not be the same as ownerAddress"}` |
| `receiver_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid receiverAddress"}` |
| 设了 `receiver_address` 但 `AllowTvmConstantinople=0` 且接收方账户不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Receiver Account[<addr>] does not exist"}` |
| 设了 `receiver_address` 但 owner→receiver 没有代理记录 | `{"Error": "class org.tron.core.exception.ContractValidateException : delegated Resource does not exist"}` |
| 代理解冻 `BANDWIDTH` 但代理记录中带宽冻结额为 0 | `{"Error": "class org.tron.core.exception.ContractValidateException : no delegatedFrozenBalance(BANDWIDTH)"}` |
| 代理解冻 `ENERGY` 但代理记录中能量冻结额为 0 | `{"Error": "class org.tron.core.exception.ContractValidateException : no delegateFrozenBalance(Energy)"}` |
| 代理解冻时接收方已使用资源额度小于代理额度（违反不变量） | `{"Error": "class org.tron.core.exception.ContractValidateException : AcquiredDelegatedFrozenBalanceFor<Resource>[<X>] < delegated<Resource>[<Y>]"}` |
| 代理解冻但代理尚未到期 | `{"Error": "class org.tron.core.exception.ContractValidateException : It's not time to unfreeze."}` |
| 自解冻 `BANDWIDTH` 但账户没有 BANDWIDTH 冻结 | `{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(BANDWIDTH)"}` |
| 自解冻 `BANDWIDTH` 但全部记录都未到期 | `{"Error": "class org.tron.core.exception.ContractValidateException : It's not time to unfreeze(BANDWIDTH)."}` |
| 自解冻 `ENERGY` 但账户没有 ENERGY 冻结 | `{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(Energy)"}` |
| 自解冻 `ENERGY` 但尚未到期 | `{"Error": "class org.tron.core.exception.ContractValidateException : It's not time to unfreeze(Energy)."}` |
| 自解冻 `TRON_POWER`（仅当 `AllowNewResourceModel` 已开启）但账户没有 TronPower 冻结 / 尚未到期 | `{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(TronPower)"}` 或 `... It's not time to unfreeze(TronPower).` |
| `resource` 取值非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}`（启用 `AllowNewResourceModel` 时为 `... [BANDWIDTH、Energy、TRON_POWER]`） |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
