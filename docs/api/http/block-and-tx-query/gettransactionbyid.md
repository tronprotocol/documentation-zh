# /wallet/gettransactionbyid

按交易 ID 查询交易（**不含执行结果**，只返回打包前的交易体）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionByIdServlet.java`
- Method：`GET` / `POST`
- Request：`api.BytesMessage`
- 支持固化接口：`/walletsolidity/gettransactionbyid`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `value` | string | 是 | 交易 ID hex（32 字节） |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactionbyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"
}
'
```

## 响应

返回 `protocol.Transaction`：

| 字段 | 类型 | 说明 |
|---|---|---|
| `txID` | string | 交易 ID（HTTP 输出额外加） |
| `raw_data.contract` | repeated Contract | 合约数组（一般 1 个） |
| `raw_data.ref_block_*` | bytes/int64 | 关联块信息 |
| `raw_data.expiration` | int64 | 过期时间，毫秒 |
| `raw_data.timestamp` | int64 | 交易时间戳 |
| `raw_data.fee_limit` | int64 | 智能合约调用的费用上限 |
| `raw_data_hex` | string | raw_data 的 hex 编码 |
| `signature` | repeated bytes | 签名 |
| `ret` | repeated Result | 交易结果（含 `contractRet`） |

响应示例（Nile 上的真实合约调用，截断 `data` / `raw_data_hex` 长字段）：

```json
{
  "ret": [{ "contractRet": "SUCCESS" }],
  "signature": ["2154e8ef08f014063de8a88bafe748c8cbb48633c1657c083dca1a73439b289f6aa796bfa58797da6354d35fb7334a8c145c48ae266e4a885f7ee44791b5a3c31b"],
  "txID": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "data": "a6bd98ac0000000000000000000000000000000000000000000000000000000000000007...",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "contract_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825"
          },
          "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
        },
        "type": "TriggerSmartContract"
      }
    ],
    "ref_block_bytes": "1c8b",
    "ref_block_hash": "d78785ed02dd918f",
    "expiration": 1777437813000,
    "fee_limit": 10000000000,
    "timestamp": 1777437756016
  },
  "raw_data_hex": "0a021c8b2208d78785ed02dd918f4088d2b2bcdd335af004081f12eb04..."
}
```

不存在返回 `{}`。需要交易执行结果（包含 receipt、log）请用 [`/wallet/gettransactioninfobyid`](gettransactioninfobyid.md)。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| `value` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
