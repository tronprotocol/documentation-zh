# /wallet/getassetissuelist

查询全网所有 TRC-10 token。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAssetIssueListServlet.java`
- Method：`GET` / `POST`
- Response：`api.AssetIssueList`
- 支持固化接口：`/walletsolidity/getassetissuelist`

## 请求参数

GET 和 POST 都从 URL 查询参数读取以下字段；servlet 不解析 POST 请求体。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `visible` | GET / POST | bool | 否 | 地址、文本字段格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuelist \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | 全部 TRC-10 token（结构同 [`/wallet/createassetissue`](createassetissue.md) 请求体） |

响应示例（Nile 全量列表很长，仅截取首项；如需翻页请使用 [`/wallet/getpaginatedassetissuelist`](getpaginatedassetissuelist.md)）：

```json
{
  "assetIssue": [
    {
      "owner_address": "417e95e45f5a60cc45f2d0afe37ee9f77fb8ce9fff",
      "name": "74726f6e6c696e6b5f746f6b656e",
      "abbr": "74726f6e6c696e6b5f746f6b656e",
      "total_supply": 1000000000000000,
      "frozen_supply": [{ "frozen_amount": 1, "frozen_days": 1 }],
      "trx_num": 1,
      "precision": 6,
      "num": 1,
      "start_time": 1574757000000,
      "end_time": 1757595000000,
      "description": "4465736372697074696f6e",
      "id": "1000001"
    }
    /* ... 其余 token */
  ]
}
```

无返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | 节点内部异常（读取 AssetIssue 存储失败） | `{"Error": "<exceptionClass> : <message>"}` |
