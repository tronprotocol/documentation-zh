# /wallet/gettransactioninfobyblocknum

按区块号返回该区块所有交易的 `TransactionInfo`（执行结果）数组。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionInfoByBlockNumServlet.java`
- Method：`GET` / `POST`
- Request：`api.NumberMessage`
- Response：`api.TransactionInfoList`
- 支持固化接口：`/walletsolidity/gettransactioninfobyblocknum`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `num` | int64 | 是 | 区块号 |
| `visible` | bool | 否 | 地址、文本字段格式；`visible=true` 时 servlet 额外把 `log[].address`（EVM 20 字节）补 `0x41` 前缀后转 base58 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactioninfobyblocknum \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "num": 66987565
}
'
```

## 响应

返回 JSON 数组（与原 `TransactionInfoList.transactionInfo` 等价），每个元素结构同 [`/wallet/gettransactioninfobyid`](gettransactioninfobyid.md)。

> **注意**：在解析各个交易的 `log` 字段之前，请逐笔确认其结果为 "success"——这是保证数据一致性的推荐做法。

响应示例（区块号 66987565 共 4 笔交易，截取前 2 笔）：

```json
[
  {
    "id": "ff44a2823a870c12f12a4ca6e7647650356bc2bb5e02c5855312cf2db4c950c1",
    "fee": 267000,
    "blockNumber": 66987565,
    "blockTimeStamp": 1777445121000,
    "contractResult": [""],
    "receipt": { "net_fee": 267000 }
  },
  {
    "id": "0419405287081aa44f4d78725e6fabac8d14e71abf9e28825ad4f4e61a5bccb7",
    "fee": 267000,
    "blockNumber": 66987565,
    "blockTimeStamp": 1777445121000,
    "contractResult": [""],
    "receipt": { "net_fee": 267000 }
  }
]
```

空区块（无交易）返回 `[]`；`num <= 0` 时返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `num` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
