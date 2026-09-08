# wallet-cli asset list

分页列出链上的 TRC10 token。

## 用法

```
wallet-cli asset list [--limit <n>] [--offset <n>] [options]
```

## 说明

列出 TRC10 token 及其 id、名称、总供应量、精度和发行方。只读，不需要账户。要查看某个 token 的完整发行记录——ICO 比率与窗口、冻结批次——请用 [`asset info`](info.md)。

分页在节点上进行，且**没有总数**：链上不暴露 TRC10 token 的计数，而为了计数把它们全部取回来代价很高（数千个 token、数 MB 响应）。因此标题报告的是它请求的窗口——`Assets (limit 3, offset 0)`——而不是 `showing 3 of N`，`meta.pagination.total` 恒为 `null`。要取全部，请传一个足够大的 `--limit`。

## 选项

| 选项 | 说明 |
|---|---|
| `--limit <number>` | 返回的最大 token 数（默认 `10`） |
| `--offset <number>` | 分页偏移（默认 `0`） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli asset list --limit 3 --network tron:3448148188
```

```console
Assets (limit 3, offset 0)
| ID      | Name      | Total supply  | Precision | Issuer            |
| ------- | --------- | ------------- | --------- | ----------------- |
| 1000125 | AlphaCoin | 500,000,000   | 2         | TAlpha7k...3nQw   |
| 1000124 | BetaToken | 2,000,000,000 | 6         | TBeta9mR...8pLx   |
| 1000123 | MyToken   | 1,000,000,000 | 6         | TQkXm4vN...5Zt7Uw |
```

```bash
wallet-cli asset list --limit 3 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"asset.list","data":{"kind":"asset-list","assets":[{"assetId":"1000125","name":"AlphaCoin","issuerAddress":"TAlpha7k...","totalSupply":"50000000000","precision":2},{"assetId":"1000124","name":"BetaToken","issuerAddress":"TBeta9mR...","totalSupply":"2000000000000000","precision":6},{"assetId":"1000123","name":"MyToken","issuerAddress":"TQkXm4vN...","totalSupply":"1000000000000000","precision":6}]},"meta":{"durationMs":48,"warnings":[],"pagination":{"offset":0,"limit":3,"total":null}},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data.kind` 为 `asset-list`。`data.assets[]`——每个 token 一项：

| 字段 | 类型 | 含义 |
|---|---|---|
| `assetId` | string | Token id |
| `name` | string | token 名称 |
| `issuerAddress` | string | 发行方，base58 |
| `totalSupply` | string | 总供应量，原始值（完整 token × 10^`precision`）。是**字符串**：供应量会达到 int64，作为 JSON number 会损失精度 |
| `precision` | number | 小数位数，0–6 |

`meta.pagination` 携带 `offset`、`limit` 和 `total`——这里的 `total` 恒为 `null`，表示"不存在计数"，而不是"零"。

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`——limit 或 offset 非法）。

## 另请参见

[`asset info`](info.md) · [`token list`](../token/list.md)
