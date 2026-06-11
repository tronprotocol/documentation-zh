# /wallet/createassetissue

创建一个 TRC10 token 发行交易。

- 源码：`framework/src/main/java/org/tron/core/services/http/CreateAssetIssueServlet.java`
- Method：`POST`
- Contract：`protocol.AssetIssueContract`（`asset_issue_contract.proto`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 发行方地址 |
| `name` | string | 是 | token 名（hex 编码 UTF-8） |
| `abbr` | string | 否 | 缩写（hex 编码 UTF-8） |
| `total_supply` | int64 | 是 | 总发行量 |
| `frozen_supply` | repeated FrozenSupply | 否 | 冻结部分；元素 `{frozen_amount, frozen_days}` |
| `trx_num` | int32 | 是 | 兑换比例分母（trx_num TRX = num token） |
| `num` | int32 | 是 | 兑换比例分子 |
| `precision` | int32 | 否 | 精度 |
| `start_time` | int64 | 是 | 募集开始时间，毫秒 |
| `end_time` | int64 | 是 | 募集结束时间，毫秒 |
| `description` | string | 否 | 描述（hex UTF-8） |
| `url` | string | 是 | 项目 URL（hex UTF-8，长度 ≤ 256 字节） |
| `free_asset_net_limit` | int64 | 否 | 单账户该 token 免费带宽 |
| `public_free_asset_net_limit` | int64 | 否 | token 公共免费带宽 |
| `permission_id` | int32 | 否 | 多签权限 ID |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createassetissue \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "name": "44494345",
  "abbr": "44494345",
  "total_supply": 1000000000,
  "trx_num": 1,
  "num": 1,
  "start_time": 1900000000000,
  "end_time": 2000000000000,
  "description": "44494345",
  "url": "68747470733a2f2f747261782e696f"
}
'
```

## 响应

返回未签名 `protocol.Transaction`。上链后会得到一个 `assetIssueID`，可在 `TransactionInfo.assetIssueID` 中查看。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异；`start_time` 必须晚于当前出块时间）：

```json
{
  "visible": false,
  "txID": "a9c125300a5e5c6fa9490ab599b3f37db756aa1e421d883167955c91e4cfe409",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "name": "44494345",
            "abbr": "44494345",
            "total_supply": 1000000000,
            "trx_num": 1,
            "num": 1,
            "start_time": 1900000000000,
            "end_time": 2000000000000,
            "description": "44494345",
            "url": "68747470733a2f2f747261782e696f"
          },
          "type_url": "type.googleapis.com/protocol.AssetIssueContract"
        },
        "type": "AssetIssueContract"
      }
    ],
    "ref_block_bytes": "275a",
    "ref_block_hash": "8aeea897e90cdc79",
    "expiration": 1777446138000,
    "timestamp": 1777446080622
  },
  "raw_data_hex": "0a02275a22088aeea897e90cdc794090e1aec0dd335a8c0108061287010a2f747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e41737365744973737565436f6e747261637412540a1541dd791d6b49e190062d650e6a23c575510d35f2f91204444943451a0444494345208094ebdc03300140014880f0cc86a6375080c0a8ca9a3aa2010444494345aa010f68747470733a2f2f747261782e696f70eea0abc0dd33"
}
```

费用：发行 TRC10 需消耗一笔较高的 TRX 销毁（链参数 `getAssetIssueFee`，目前 1024 TRX）。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `owner_address` 非法 | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| `name` 非法（空、长度 > 32、含非法字符） | `{"Error": "... : Invalid assetName"}` |
| `name` 解析为 "trx" | `{"Error": "... : assetName can't be trx"}` |
| `precision` 超过 6 | `{"Error": "... : precision cannot exceed 6"}` |
| `abbr` 非法 | `{"Error": "... : Invalid abbreviation for token"}` |
| `url` 非法 | `{"Error": "... : Invalid url"}` |
| `description` 非法（长度过长） | `{"Error": "... : Invalid description"}` |
| `start_time` 缺失 | `{"Error": "... : Start time should be not empty"}` |
| `end_time` 缺失 | `{"Error": "... : End time should be not empty"}` |
| `end_time <= start_time` | `{"Error": "... : End time should be greater than start time"}` |
| `start_time <= 当前出块时间` | `{"Error": "... : Start time should be greater than HeadBlockTime"}` |
| 同名 token 已存在 | `{"Error": "... : Token exists"}` |
| `total_supply <= 0` | `{"Error": "... : TotalSupply must greater than 0!"}` |
| `trx_num <= 0` | `{"Error": "... : TrxNum must greater than 0!"}` |
| `num <= 0` | `{"Error": "... : Num must greater than 0!"}` |
| `public_free_asset_net_usage` 非 0 | `{"Error": "... : PublicFreeAssetNetUsage must be 0!"}` |
| `frozen_supply` 长度过长 | `{"Error": "... : Frozen supply list length is too long"}` |
| `free_asset_net_limit` 非法 | `{"Error": "... : Invalid FreeAssetNetLimit"}` |
| `public_free_asset_net_limit` 非法 | `{"Error": "... : Invalid PublicFreeAssetNetLimit"}` |
| `frozen_amount <= 0` | `{"Error": "... : Frozen supply must be greater than 0!"}` |
| `frozen_amount` 累加超过 `total_supply` | `{"Error": "... : Frozen supply cannot exceed total supply"}` |
| `frozen_days` 不在合法区间 | `{"Error": "... : frozenDuration must be less than <max> days and more than <min> days"}` |
| `start_time + frozen_days` 溢出 | `{"Error": "... : Start time and frozen days would cause expire time overflow"}` |
| `owner_address` 账户不存在 | `{"Error": "... : Account not exists"}` |
| 该账户已发行过 token | `{"Error": "... : An account can only issue one asset"}` |
| 余额不足扣发行手续费 | `{"Error": "... : No enough balance for fee!"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
