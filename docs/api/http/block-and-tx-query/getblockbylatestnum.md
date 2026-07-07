# /wallet/getblockbylatestnum

获取最新的 N 个区块。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBlockByLatestNumServlet.java`
- Method：`GET` / `POST`
- Request：`api.NumberMessage`
- 支持固化接口：`/walletsolidity/getblockbylatestnum`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `num` | int64 | 是 | 取最近多少个区块（要求 `0 < num < 100`，最大 99；超出范围静默返回 `{}`） |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbylatestnum \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "num": 2 }
'
```

## 响应

返回 `api.BlockList`，字段同 [`/wallet/getblockbylimitnext`](getblockbylimitnext.md)。

响应示例（最近 2 个 Nile 区块，省略 `transactions` 内容）：

```json
{
  "block": [
    {
      "blockID": "0000000003fe266c55d8ec678995cff469dd46ee18671a96f5866f8cb227eed8",
      "block_header": {
        "raw_data": {
          "number": 66987628,
          "txTrieRoot": "1e45d06980078902492470bbce85cf652261f50881503ee81df6fd041af98848",
          "witness_address": "416606973497a56dcfcedb684e60a2386f2ae39db5",
          "parentHash": "0000000003fe266bf6b6d392f654dc2e5011601546ed04623d9fcc4e9d439a25",
          "version": 34,
          "timestamp": 1777445310000
        },
        "witness_signature": "22bb7fdb5cdd33b8eca9104925f0dbd89f65d8e6ee4f7eed6f21d81b1428977e521865406b3ef70abc77b051d930081c2b9e368dc3f2c20c4b5e31187ba945bd00"
      },
      "transactions": [ /* ... */ ]
    },
    {
      "blockID": "0000000003fe266bf6b6d392f654dc2e5011601546ed04623d9fcc4e9d439a25",
      "block_header": { /* ... */ },
      "transactions": [ /* ... */ ]
    }
  ]
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| `num` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
