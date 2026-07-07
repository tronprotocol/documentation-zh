# /wallet/listproposals

获取所有提案列表。

- 源码：`framework/src/main/java/org/tron/core/services/http/ListProposalsServlet.java`
- Method：`GET` / `POST`
- Response：`api.ProposalList`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/listproposals \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `proposals` | repeated Proposal | 提案列表（结构同 [`/wallet/getproposalbyid`](getproposalbyid.md)） |

响应示例（Nile 当前共 20000+ 提案，仅截创世首项；`approvals` 在示例中省略）：

```json
{
  "proposals": [
    {
      "proposal_id": 1,
      "proposer_address": "41217179d498883cdbda5699402905d1feb258796c",
      "parameters": [
        { "key": 9,  "value": 1 },
        { "key": 10, "value": 1 }
      ],
      "expiration_time": 1572597600000,
      "create_time": 1572596523000,
      "approvals": [
        "41217179d498883cdbda5699402905d1feb258796c"
        /* ... 其余 SR */
      ],
      "state": "APPROVED"
    }
    /* ... 其余提案 */
  ]
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 节点内部异常（读取 Proposal 存储失败） | `{"Error": "<exceptionClass> : <message>"}` |
