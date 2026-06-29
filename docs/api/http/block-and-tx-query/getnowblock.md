# /wallet/getnowblock

返回当前最新区块。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetNowBlockServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getnowblock`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getnowblock \
     --header 'accept: application/json'
```

## 响应

返回 `protocol.Block`（`Tron.proto`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `blockID` | string | 区块哈希（HTTP 输出额外加的字段） |
| `block_header.raw_data.timestamp` | int64 | 出块时间，毫秒 |
| `block_header.raw_data.txTrieRoot` | bytes | 交易 Merkle 根 |
| `block_header.raw_data.parentHash` | bytes | 父区块哈希 |
| `block_header.raw_data.number` | int64 | 区块号 |
| `block_header.raw_data.witness_address` | bytes | 出块超级代表地址 |
| `block_header.raw_data.version` | int32 | 区块版本 |
| `block_header.witness_signature` | bytes | 超级代表签名 |
| `transactions` | repeated Transaction | 该区块包含的交易 |

响应示例（Nile 上的真实出块，省略 `transactions` 内容）：

```json
{
  "blockID": "0000000003fe266bf6b6d392f654dc2e5011601546ed04623d9fcc4e9d439a25",
  "block_header": {
    "raw_data": {
      "number": 66987627,
      "txTrieRoot": "f8156964cc3e5793a368f938a18ea45c02bd48fe3a412f7091ce8d9ef56df174",
      "witness_address": "41e7860196ad5b5718c1d6326babab039b70b8c1cd",
      "parentHash": "0000000003fe266a65d5194c947f6f7a059d4646c8e9a5293226bc7fdcfc775e",
      "version": 34,
      "timestamp": 1777445307000
    },
    "witness_signature": "55a29981b2ba121613788de5d1b6bd87579ef63479f4fbb7bc99b1c721769487023cb74ea3b604778ed448bf1c90db3db0fd8fedc85102cfda4231fd1c75d6e100"
  },
  "transactions": [ /* 见 /wallet/gettransactionbyid 单笔交易示例 */ ]
}
```

无区块时返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 节点内部异常（读取最新区块或序列化失败） | `{"Error": "<exceptionClass> : <message>"}` |
