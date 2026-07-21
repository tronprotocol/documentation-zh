# /wallet/createtransaction

创建一笔 TRX 转账（`TransferContract`）的未签名交易。

- 源码：`framework/src/main/java/org/tron/core/services/http/TransferServlet.java`
- Method：`POST`
- Contract：`protocol.TransferContract`（`balance_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 发起方地址 |
| `to_address` | string | 是 | 接收方地址 |
| `amount` | int64 | 是 | 金额，sun（1 TRX = 1e6 sun） |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `extra_data` | string | 否 | 写入 `raw_data.data`（hex；`visible=true` 时为 UTF-8） |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createtransaction \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "to_address":    "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "amount":        1000000
}
'
```

## 响应

返回未签名 `protocol.Transaction`（含 `txID`、`raw_data`、`raw_data_hex`，`signature` 为空）。响应示例（Nile 实抓）：

```json
{
  "visible": false,
  "txID": "6303c7639f591407ef9f34a7ac8c9c9a21151f5a6af21924502515734fc267ab",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "amount":        1000000,
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "to_address":    "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
          },
          "type_url": "type.googleapis.com/protocol.TransferContract"
        },
        "type": "TransferContract"
      }
    ],
    "ref_block_bytes": "2927",
    "ref_block_hash":  "939ece39d08a7abe",
    "expiration":      1777447527000,
    "timestamp":       1777447470038
  },
  "raw_data_hex": "0a0229272208939ece39d08a7abe40d8c483c1dd335a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541dd791d6b49e190062d650e6a23c575510d35f2f912154192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a18c0843d70d68780c1dd33"
}
```

> 上述 `txID`、`ref_block_bytes` / `ref_block_hash`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异：`ref_block_*` 取构造时最新固化块；`expiration = timestamp + 60_000`；`txID` 是 `raw_data` 的 SHA256；`raw_data_hex` 是 `raw_data` 的 protobuf 编码，签名以 `raw_data_hex` 为输入。其它构造类接口（`/wallet/triggersmartcontract`、`freezebalancev2`、`unfreezebalancev2` 等）的响应包含同样的 ephemeral 字段，语义一致，下文不再赘述。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| 字段类型不符 / 地址解码失败 | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `extra_data` 在 `visible=false` 时不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（`Util.setTransactionExtraData` 直调 `ByteArray.fromHexString`，绕过 `JsonFormat`） |
| `owner_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress!"}` |
| `to_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid toAddress!"}` |
| `to_address == owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Cannot transfer TRX to yourself."}` |
| `owner_address` 在链上不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : Validate TransferContract error, no OwnerAccount."}` |
| `amount <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : Amount must be greater than 0."}` |
| `to_address` 是合约且 `ForbidTransferToContract` 提案已开启 | `{"Error": "class org.tron.core.exception.ContractValidateException : Cannot transfer TRX to a smartContract."}` |
| `to_address` 是 v1 合约且 `AllowTvmCompatibleEvm` 提案已开启 | `{"Error": "class org.tron.core.exception.ContractValidateException : Cannot transfer TRX to a smartContract which version is one. Instead please use TriggerSmartContract "}` |
| 余额不足 `amount + fee`（收方为新账户时 `fee` 含 0.1 TRX 创建费） | `{"Error": "class org.tron.core.exception.ContractValidateException : Validate TransferContract error, balance is not sufficient."}` |
| `amount + fee` 或目标账户余额溢出 `long` | `{"Error": "class org.tron.core.exception.ContractValidateException : <ArithmeticException 信息>"}` |
