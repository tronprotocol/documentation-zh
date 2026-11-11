# /wallet/getaccountbalance

按指定区块查询账户的 TRX 余额（带 block 锚点）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAccountBalanceServlet.java`
- Method：`POST`
- Request：`protocol.AccountBalanceRequest`（`balance_contract.proto`）
- Response：`protocol.AccountBalanceResponse`（`balance_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `account_identifier.address` | string | 是 | 账户地址 |
| `block_identifier.hash` | string | 是 | 区块哈希 |
| `block_identifier.number` | int64 | 否 | 区块高度；省略时默认为 `0`。仅查询创世块时可以省略；查询其他区块时必须与 `block_identifier.hash` 匹配 |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccountbalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "account_identifier": { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9" },
  "block_identifier": {
    "hash": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
    "number": 66987565
  }
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `balance` | int64 | 请求区块或之前最近一次记录的账户余额（sun）；准确性取决于节点的历史记录覆盖范围 |
| `block_identifier` | object | 返回的余额记录所在区块的 hash/number；没有找到记录时为请求的区块 |

响应示例（Nile 返回的 `block_identifier` 为节点上最近一次追踪过该账户余额的区块，可能与请求中的锚点不同）：

```json
{
  "balance": 1793227200,
  "block_identifier": {
    "hash": "0000000003fe25c69a3321cd009c484efe62b11abf0f8966fc81c1ff4a917cad",
    "number": 66987462
  }
}
```

要获得准确结果，节点必须已记录相关余额历史。`storage.balance.history.lookup = true`（等价启动参数 `--history-balance-lookup`）用于开启记录；查询本身会读取已有记录，不受当前开关设置影响。关闭记录后，之前的记录仍可查询，但查询较晚区块时可能返回过时的余额。开启或重新开启记录不会补齐缺失的历史。如果在请求区块或之前找不到记录，响应会原样返回请求的 `block_identifier`，并返回 `balance: 0`；这并不能证明账户当时的余额确实为零。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `account_identifier` 缺失 | `{"Error": "class java.lang.IllegalArgumentException : account_identifier is null"}` |
| `account_identifier.address` 缺失 | `{"Error": "class java.lang.IllegalArgumentException : account_identifier address is null"}` |
| `block_identifier` 缺失 | `{"Error": "class java.lang.IllegalArgumentException : block_identifier null"}` |
| `block_identifier.number < 0` | `{"Error": "class java.lang.IllegalArgumentException : block_identifier number less than 0"}` |
| `block_identifier.hash` 长度不为 32 字节 | `{"Error": "class java.lang.IllegalArgumentException : block_identifier hash length not equals 32"}` |
| `block_identifier` 的 `number` 与 `hash` 不匹配 | `{"Error": "class java.lang.IllegalArgumentException : number and hash do not match"}` |
| 区块高度不存在 | `{"Error": "class org.tron.core.exception.ItemNotFoundException : number: <N> is not found!"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
