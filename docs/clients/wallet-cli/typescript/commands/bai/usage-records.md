# wallet-cli bai usage-records

列出 B.AI 的单条用量记录。

## 用法

```
wallet-cli bai usage-records [--limit <n>] [--offset <n>] [--sort <asc|desc>] [--cursor <c>] [options]
```

## 说明

列出该 API key 的用量，每个请求一条记录：模型、token 数、额度消耗和延迟。不需要钱包，也不需要密码。

用 `--limit` / `--offset` 翻页，或把某一页返回的 `nextCursor` 通过 `--cursor` 传回以获取下一页。

需要先用 [`config baiApiKey`](../config.md) 保存 B.AI API key；见 [`bai`](index.md#the-api-key)。

## 选项

| 选项 | 说明 |
|---|---|
| `--limit <n>` | 每页行数，1–200（默认 `20`） |
| `--offset <n>` | 跳过的行数（默认 `0`）；必须是 `--limit` 的整数倍，因为 B.AI 按页码翻页 |
| `--sort <asc\|desc>` | 按创建时间排序（默认 `desc`） |
| `--cursor <c>` | 上一页返回的 `nextCursor` |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli bai usage-records --limit 3
```

```console
B.AI usage records
  records:
    1.
      id: usg_8f3a2c71
      created At: 2026-09-15T08:21:44.000Z
      model: gpt-5-mini
      input Tokens: 1840
      output Tokens: 612
      total Tokens: 2452
      credits: 1200
      latency Ms: 2,840
      source: api
    2.
      id: usg_8f3a2b09
      created At: 2026-09-15T08:19:02.000Z
      model: claude-sonnet-5
      input Tokens: 3210
      output Tokens: 958
      total Tokens: 4168
      credits: 4600
      latency Ms: 5,120
      source: api
    3.
      id: usg_8f39f6d4
      created At: 2026-09-14T13:05:37.000Z
      model: gpt-5-mini
      input Tokens: 920
      output Tokens: 301
      total Tokens: 1221
      credits: 600
      latency Ms: 1,730
      source: api
  pagination:
    offset: 0
    limit: 3
    total: Not available
    has More: Yes
    next Cursor: eyJpZCI6InVzZ184ZjM5ZjZkNCJ9
```

```bash
wallet-cli bai usage-records --limit 3 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"bai.usage-records","data":{"records":[{"id":"usg_8f3a2c71","createdAt":"2026-09-15T08:21:44.000Z","model":"gpt-5-mini","inputTokens":"1840","outputTokens":"612","totalTokens":"2452","credits":"1200","latencyMs":2840,"source":"api"},{"id":"usg_8f3a2b09","createdAt":"2026-09-15T08:19:02.000Z","model":"claude-sonnet-5","inputTokens":"3210","outputTokens":"958","totalTokens":"4168","credits":"4600","latencyMs":5120,"source":"api"},{"id":"usg_8f39f6d4","createdAt":"2026-09-14T13:05:37.000Z","model":"gpt-5-mini","inputTokens":"920","outputTokens":"301","totalTokens":"1221","credits":"600","latencyMs":1730,"source":"api"}]},"meta":{"durationMs":1323,"warnings":[],"pagination":{"offset":0,"limit":3,"total":null,"hasMore":true,"nextCursor":"eyJpZCI6InVzZ184ZjM5ZjZkNCJ9"}}}
```

记录按时间倒序排列。`credits` 是每个请求消耗的额度，`latencyMs` 是它的耗时。`hasMore: true`（文本中为 `has More: Yes`）表示后面还有记录：用 `--offset 3` 或 `--cursor eyJpZCI6InVzZ184ZjM5ZjZkNCJ9` 取下一页。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `records[]` | array | 用量记录，字段见下 |

分页信息在 `meta.pagination` 中：`offset`、`limit`、`total`（恒为 `null`，因为 B.AI 不返回总数），以及 B.AI 提供时才有的 `hasMore` 和 `nextCursor`。`hasMore: false` 表示这已是最后一页。

每条记录（B.AI 未提供的字段不会出现）：

| 字段 | 类型 | 含义 |
|---|---|---|
| `id` | string | 记录 id |
| `createdAt` | string | 请求发生的时间 |
| `model` | string | 使用的模型 |
| `inputTokens` / `outputTokens` / `totalTokens` | string | token 计数 |
| `credits` | string | 扣除的额度 |
| `latencyMs` | number | 请求耗时，单位毫秒 |
| `source` | string | 请求的来源 |

## 退出码

`0` 成功 · `1` 执行失败（`bai_auth_failed`；`bai_rejected`；`provider_error`——包括 B.AI 不接受的 `--cursor`；`timeout`） · `2` 用法错误（`bai_credentials_missing`；`invalid_value`——`--offset` 不是 `--limit` 的整数倍，或越界）。

## 另请参见

[`bai usage-summary`](usage-summary.md) · [`bai recharge-orders`](recharge-orders.md)
