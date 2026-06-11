# /wallet/getpaginatedassetissuelist

按分页查询全网 TRC10 token。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetPaginatedAssetIssueListServlet.java`
- Method：`GET` / `POST`
- Response：`api.AssetIssueList`
- 支持固化接口：`/walletsolidity/getpaginatedassetissuelist`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `offset` | int64 | 否 | 起始偏移；缺省为 `0` |
| `limit` | int64 | 否 | 返回条数；缺省为 `0`，此时返回空列表 |
| `visible` | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpaginatedassetissuelist \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "offset": 0,
  "limit": 2
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | 分页后的 token 列表 |

响应示例（Nile，limit=2）：

```json
{
  "assetIssue": [
    {
      "owner_address": "41a8a906cd9d5e7ff3e472d34ca568441ceeb4cf5b",
      "name": "303044696365",
      "abbr": "307830",
      "total_supply": 1000000000000000000,
      "trx_num": 1000000,
      "precision": 6,
      "num": 100000000,
      "start_time": 1592841600000,
      "end_time": 1592928000000,
      "description": "e794a8e4ba8ee6b58be8af95",
      "url": "68747470733a2f2f7777772e62616964752e636f6d",
      "id": "1000052"
    },
    {
      "owner_address": "41f18b0c6d290d57464aeddeb98f429c9dd318e31e",
      "name": "3031303031313031303130313031",
      "abbr": "3031303031313031303130313031",
      "total_supply": 1000000,
      "frozen_supply": [{ "frozen_amount": 1000, "frozen_days": 2 }],
      "trx_num": 1,
      "precision": 6,
      "num": 1,
      "start_time": 1663344000000,
      "end_time": 1694880000000,
      "description": "e68f8fe8bfb0",
      "url": "75726c33",
      "free_asset_net_limit": 1000,
      "public_free_asset_net_limit": 1000,
      "id": "1004963"
    }
  ]
}
```

无返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `offset` / `limit` 不是数字（GET） | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
