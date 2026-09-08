# /wallet/getcontractinfo

获取合约的完整运行时信息（包含 runtime code、状态、能量信息）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetContractInfoServlet.java`
- Method：`GET` / `POST`
- Response：`protocol.SmartContractDataWrapper`（`smart_contract.proto`）

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `value` | GET / POST | string | 否 | 合约地址；省略时使用空 bytes 查询并返回 `{}` |
| `visible` | GET / POST | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcontractinfo \
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
| `smart_contract` | SmartContract | 合约元信息（同 [`/wallet/getcontract`](getcontract.md)） |
| `runtimecode` | string(hex) | 链上运行时字节码（proto 字段名无下划线） |
| `contract_state` | ContractState | 合约状态：`energy_usage`、`energy_factor`、`update_cycle` |

响应示例（Nile TetherToken）：

```json
{
  "smart_contract": {
    "origin_address": "4165fa68800fff5a10346d1a3aa1fb2ce92f2e2971",
    "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
    "abi": { "entrys": [/* 46 entries */] },
    "bytecode": "60806040526000600260146101000a81548160ff021916908315150217905550...",
    "name": "TetherToken",
    "origin_energy_limit": 1000000000,
    "code_hash": "1c32379f645df32d2a8e45de37319983d01d47185588337985aeefb4672a91f2"
  },
  "runtimecode": "608060405234801561001057600080fd5b50d3801561001d57600080fd5b50d28...",
  "contract_state": {
    "energy_usage": 236150,
    "update_cycle": 256749
  }
}
```

> `contract_state` 的 `energy_factor` 为 0 时不出现（proto 默认值不序列化）。

不存在返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `value` 不是合法 base58check（`visible=true`） | 含非 base58 字符抛 `{"Error": "class java.lang.IllegalArgumentException : <详情>"}`；仅校验位错误时 `Util.getHexAddress` 静默返回空串 → 查询不到合约，返回 `{}` |
| GET / POST | `value` 不是合法 hex（`visible=false`） | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <详情>"}` |
| POST | 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
