# /wallet/getblock

按区块高度或区块哈希查询区块，可选返回完整交易明细。统一替代 `getnowblock` / `getblockbynum` / `getblockbyid`。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBlockServlet.java`
- Method：`GET` / `POST`
- Request：`api.BlockReq`
- 支持固化接口：`/walletsolidity/getblock`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `id_or_num` | GET / POST | string | 否 | 区块高度（十进制字符串）或区块哈希 hex；为空时取最新区块 |
| `detail` | GET / POST | bool | 否 | 是否返回完整 `transactions`；false 时只返回 header（默认 false） |
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblock \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "id_or_num": "66987565", "detail": false }
'
```

## 响应

返回 `protocol.Block`（只是 `transactions` 是否填充取决于 `detail`），字段同 [`/wallet/getnowblock`](getnowblock.md)。

响应示例（`detail=false`，省略 `transactions`）：

```json
{
  "blockID": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
  "block_header": {
    "raw_data": {
      "number": 66987565,
      "txTrieRoot": "faf8fe3858339ead25cc892461c82a59b84dca4a51c45b026676bf3f45a352a2",
      "witness_address": "41b2f713d57dbcec679d93a8849fa0cd0e4db594ba",
      "parentHash": "0000000003fe262c85cd6b02033f4c3e5c1efa35de256a17bd906dc61fb1aeed",
      "version": 34,
      "timestamp": 1777445121000
    },
    "witness_signature": "5b3cf6cb15d52947989f7726f4907a144b39ccd667a1a0f98707b40cdfe65b96173ddf34ae8dcc5e78f136e0cf903a15c7128984aa2191f02333209d1879d3f900"
  }
}
```

不存在返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| POST | 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| GET / POST | `id_or_num` 是负数 | `{"Error": "num must be non-positive number."}` |
| GET / POST | `id_or_num` 长度不等于 64（不是合法区块哈希长度） | `{"Error": "id must be legal block hash."}` |
| GET / POST | `id_or_num` 是 hex 但解析失败 / 哈希无法对应到区块高度 | `{"Error": "id must be legal block hash."}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
