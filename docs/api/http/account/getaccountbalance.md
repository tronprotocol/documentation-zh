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
| `block_identifier.number` | int64 | 是 | 区块号 |
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
| `balance` | int64 | 该区块下账户余额（sun） |
| `block_identifier` | object | 锚定区块的 hash/number |

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

需要节点开启 `storage.balance.history.lookup = true`（等价启动参数 `--history-balance-lookup`）。否则不会报错，而是返回 `balance: 0` + 原样回显的 `block_identifier`——与"该账户在该区块前确实没有任何记录"的成功响应无法区分，容易被误判。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `account_identifier` 缺失 | `{"Error": "class java.lang.IllegalArgumentException : account_identifier is null"}` |
| `account_identifier.address` 缺失 | `{"Error": "class java.lang.IllegalArgumentException : account_identifier address is null"}` |
| `block_identifier` 缺失 | `{"Error": "class java.lang.IllegalArgumentException : block_identifier null"}` |
| `block_identifier.number < 0` | `{"Error": "class java.lang.IllegalArgumentException : block_identifier number less than 0"}` |
| `block_identifier.hash` 长度不为 32 字节 | `{"Error": "class java.lang.IllegalArgumentException : block_identifier hash length not equals 32"}` |
| `block_identifier` 的 `number` 与 `hash` 不匹配 | `{"Error": "class java.lang.IllegalArgumentException : number and hash do not match"}` |
| 区块号不存在 | `{"Error": "class org.tron.core.exception.ItemNotFoundException : number: <N> is not found!"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
