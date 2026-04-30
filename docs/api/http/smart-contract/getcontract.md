# /wallet/getcontract

按合约地址获取合约元信息。返回 `SmartContract` 本体（含 deploy 时的 `bytecode`），但**不含运行时码 `runtimecode` 与 `contract_state`**。如需运行时信息，请用 [`/wallet/getcontractinfo`](getcontractinfo.md)。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetContractServlet.java`
- Method：`GET` / `POST`
- Response：`protocol.SmartContract`（`smart_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `value` | string | 是 | 合约地址 |
| `visible` | bool | 否 | 地址格式（响应中 `name` 为 proto `string`，不受 `visible` 影响） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `origin_address` | string | 部署者地址 |
| `contract_address` | string | 合约地址 |
| `abi` | ABI | 合约 ABI |
| `bytecode` | string(hex) | 部署字节码（创建字节码 + 构造参数 拼接，与 deploy 时传入一致；非 runtime code，runtime code 见 [`/wallet/getcontractinfo`](getcontractinfo.md)） |
| `call_value` | int64 | 部署时附带的 TRX |
| `consume_user_resource_percent` | int64 | 用户承担能量百分比 |
| `name` | string | 合约名 |
| `origin_energy_limit` | int64 | 部署者能量上限 |
| `code_hash` | string(hex) | 字节码哈希 |
| `trx_hash` | string(hex) | 部署交易哈希 |
| `version` | int32 | 版本 |

> proto 默认值不序列化：`call_value=0`、`consume_user_resource_percent=0`、`version=0`、`trx_hash` 为空时不会出现在响应中。

响应示例（Nile 上的 TetherToken）：

```json
{
  "origin_address": "4165fa68800fff5a10346d1a3aa1fb2ce92f2e2971",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "abi": {
    "entrys": [
      {
        "outputs": [{ "type": "string" }],
        "constant": true,
        "name": "name",
        "stateMutability": "View",
        "type": "Function"
      }
    ]
  },
  "bytecode": "60806040526000600260146101000a81548160ff02191690831515021790555060...",
  "name": "TetherToken",
  "origin_energy_limit": 1000000000,
  "code_hash": "1c32379f645df32d2a8e45de37319983d01d47185588337985aeefb4672a91f2"
}
```

不存在返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `value` 不是合法 base58check（`visible=true`） | 含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回空串 → 查询不到合约，返回 `{}` |
| `value` 不是合法 hex（`visible=false`） | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <详情>"}` |
| 请求体不是合法 JSON（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
