# /wallet/deploycontract

部署智能合约。返回未签名的部署交易。

- 源码：`framework/src/main/java/org/tron/core/services/http/DeployContractServlet.java`
- Method：`POST`
- Contract：`protocol.CreateSmartContract`（`smart_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 部署者地址 |
| `name` | string | 否 | 合约名，不得超过 32 字节。该限制按 UTF-8 编码后的字节数计算 |
| `abi` | json string | 否 | 合约 ABI（JSON 数组字符串） |
| `bytecode` | string | 是 | 合约字节码（hex） |
| `parameter` | string | 否 | 构造函数参数（hex，紧接 bytecode） |
| `fee_limit` | int64 | 否 | 交易费用上限（sun）；省略时默认为 `0` |
| `call_value` | int64 | 否 | 调用合约带入的 TRX（sun） |
| `consume_user_resource_percent` | int64 | 否 | 用户承担能量百分比 0–100；省略时默认为 `0` |
| `origin_energy_limit` | int64 | 否 | 部署者承担能量上限；省略时默认为 `0` |
| `token_id` | int64 | 否 | 调用合约带入的 TRC-10 token id |
| `call_token_value` | int64 | 否 | 调用合约带入的 TRC-10 数量 |
| `Permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/deploycontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "name": "MyContract",
  "abi":  "[]",
  "bytecode": "608060405234801561001057600080fd5b5060f78061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80636d4ce63c14602d575b600080fd5b60336047565b604051603e9190606b565b60405180910390f35b6000600190565b6000819050919050565b6065816052565b82525050565b6000602082019050607e6000830184605c565b9291505056fea264697066735822122000000000000000000000000000000000000000000000000000000000000000006c6578706572696d656e74616cf564736f6c63430008100033",
  "fee_limit": 1000000000,
  "consume_user_resource_percent": 100,
  "origin_energy_limit": 10000000
}
'
```

## 响应

返回未签名 `protocol.Transaction`（contract 类型 `CreateSmartContract`）。

`Util.printTransactionToJSON` 检测到 `CreateSmartContract` 时，会在顶层添加 hex 格式的 `contract_address`。节点先对 protobuf 编码的交易 `raw_data` 计算哈希（标准 TRON 交易使用 SHA-256），将该哈希与 `owner_address` 字节拼接，再通过 `sha3omit12` 推导地址。修改 `raw_data` 会改变预测地址。只有签名后的部署交易在链上成功执行，合约才会在该地址创建。

响应示例（Nile 实抓）：

```json
{
  "visible": false,
  "txID": "7fe721c3f85b6c1c9491df43778c98903b565bc4210592f449f41342041729b3",
  "contract_address": "41584587b353166787b37d1b05a4a91e59c5370bcf",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "new_contract": {
              "origin_address":                "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "consume_user_resource_percent": 100,
              "name":                          "MyContract",
              "bytecode":                      "608060405234801561001057600080fd5b5060f78061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80636d4ce63c14602d575b600080fd5b60336047565b604051603e9190606b565b60405180910390f35b6000600190565b6000819050919050565b6065816052565b82525050565b6000602082019050607e6000830184605c565b9291505056fea264697066735822122000000000000000000000000000000000000000000000000000000000000000006c6578706572696d656e74616cf564736f6c63430008100033",
              "abi":                           {},
              "origin_energy_limit":           10000000
            }
          },
          "type_url": "type.googleapis.com/protocol.CreateSmartContract"
        },
        "type": "CreateSmartContract"
      }
    ],
    "ref_block_bytes": "28c7",
    "ref_block_hash":  "b89ca57e9cbb96dd",
    "fee_limit":       1000000000,
    "expiration":      1777447239000,
    "timestamp":       1777447181980
  },
  "raw_data_hex": "0a0228c72208b89ca57e9cbb96dd40d8faf1c0dd335ae402081e12df020a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e437265617465536d617274436f6e747261637412aa020a1541dd791d6b49e190062d650e6a23c575510d35f2f91290020a1541dd791d6b49e190062d650e6a23c575510d35f2f91a0022e101608060405234801561001057600080fd5b5060f78061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80636d4ce63c14602d575b600080fd5b60336047565b604051603e9190606b565b60405180910390f35b6000600190565b6000819050919050565b6065816052565b82525050565b6000602082019050607e6000830184605c565b9291505056fea264697066735822122000000000000000000000000000000000000000000000000000000000000000006c6578706572696d656e74616cf564736f6c6343000810003330643a0a4d79436f6e74726163744080ade204709cbdeec0dd3390018094ebdc03"
}
```

> `txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` / `contract_address` 因构造时机而异；其它 ephemeral 字段语义同 [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)。`contract_address` 按上述方法，由交易原始数据的哈希和 `owner_address` 在本地预测。只有部署交易成功执行，合约才会在该地址创建。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| `owner_address` 不是合法 base58check（`visible=true`） | 仅当输入恰好为 34 个字符时，非 base58 字符才会抛出 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`。输入长度错误、校验和错误或解码后的地址无效时，`Util.getHexAddress` 返回空 hex 字符串；若其他输入有效，构造会返回缺少 `owner_address` 字段的交易（广播时会被节点拒绝） |
| `owner_address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（直调 `ByteArray.fromHexString`） |
| `bytecode` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（直调 `ByteArray.fromHexString`） |
| `abi` 不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `consume_user_resource_percent` 不在 [0, 100] | `{"Error": "class org.tron.core.exception.ContractValidateException : percent must be >= 0 and <= 100"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |

> 部署阶段的错误（例如 origin energy 不足、合约代码或合约名超长、构造函数 revert）只会在交易广播或区块打包时触发，不会由此接口在构造未签名交易时触发。
