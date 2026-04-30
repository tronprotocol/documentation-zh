# /wallet/gettransactioninfobyid

按交易 ID 查询**执行结果**（包含 receipt、log、内部调用、资源消耗）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionInfoByIdServlet.java`
- Method：`GET` / `POST`
- Request：`api.BytesMessage`
- Response：`protocol.TransactionInfo`（`Tron.proto:454`）
- 支持固化接口：`/walletsolidity/gettransactioninfobyid`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `value` | string | 是 | 交易 ID hex |
| `visible` | bool | 否 | 地址、文本字段格式；`visible=true` 时 servlet 额外把 `log[].address`（EVM 20 字节）补 `0x41` 前缀后转 base58 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactioninfobyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | bytes | 交易 ID |
| `fee` | int64 | 实际扣除的 TRX 手续费（sun） |
| `blockNumber` | int64 | 所在区块号 |
| `blockTimeStamp` | int64 | 区块时间，毫秒 |
| `contractResult` | repeated bytes | 合约调用返回值 |
| `contract_address` | bytes | 部署/调用的合约地址 |
| `receipt` | ResourceReceipt | 资源消耗（见下） |
| `log` | repeated Log | 事件日志（`{address, topics[], data}`） |
| `result` | enum | `SUCESS` / `FAILED` |
| `resMessage` | bytes | 失败原因 |
| `internal_transactions` | repeated InternalTransaction | 内部交易 |
| `withdraw_amount` | int64 | 提取见证人奖励金额（仅 WithdrawBalance） |
| `unfreeze_amount` | int64 | 解冻金额（仅 UnfreezeBalance V1） |
| `withdraw_expire_amount` | int64 | 解冻提现金额（V2） |
| `cancel_unfreezeV2_amount` | map\<string,int64\> | 取消解冻金额（V2） |
| `assetIssueID` | string | 创建的 TRC10 ID（仅 CreateAssetIssue） |
| `exchange_*` / `orderId` | — | Exchange / Market 相关字段 |

`ResourceReceipt`（`Tron.proto:318`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `energy_usage` | int64 | 调用方燃烧的能量（自身能量） |
| `energy_fee` | int64 | 因能量不足烧的 TRX |
| `origin_energy_usage` | int64 | 合约创建者承担的能量 |
| `energy_usage_total` | int64 | 总能量消耗 |
| `net_usage` | int64 | 带宽消耗 |
| `net_fee` | int64 | 因带宽不足烧的 TRX |
| `result` | enum | 合约执行结果（同 `Transaction.Result.contractResult`） |
| `energy_penalty_total` | int64 | 能量惩罚 |

响应示例（Nile 上的真实合约调用，截断 `data` 与 `internal_transactions` 完整内容）：

```json
{
  "id": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
  "fee": 5254500,
  "blockNumber": 66985120,
  "blockTimeStamp": 1777437762000,
  "contractResult": [""],
  "contract_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
  "receipt": {
    "energy_fee": 4458500,
    "energy_usage_total": 44585,
    "net_fee": 796000,
    "result": "SUCCESS"
  },
  "log": [
    {
      "address": "9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "topics": [
        "c66625d03b4a832d8245f0df593e32e0fbbbad96d4aa45440aa1535b80983083",
        "000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
        "0000000000000000000000000000000000000000000000000000000000000007"
      ],
      "data": "0000000000000000000000000000000000000000000000000000000000000007..."
    }
  ],
  "internal_transactions": [
    {
      "hash": "61318c1e41c5fd387f1e4e4e8ec1fc98f295d3ef002bab1b33dd1cba2f93cb75",
      "caller_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "transferTo_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "callValueInfo": [{}],
      "note": "63616c6c"
    }
    /* ... 省略其余内部调用 */
  ]
}
```

未上链返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `value` 不是合法 hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
