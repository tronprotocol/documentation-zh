# wallet-cli exchange list

分页列出链上的交易对。

## 用法

```
wallet-cli exchange list [--limit <n>] [--offset <n>] [options]
```

## 说明

列出各交易对的 id、两侧 token、储备和创建者。只读，不需要账户。若只想看单个交易对，请用 [`exchange show`](show.md)。

**`Pair` 按链上存储的顺序显示**，也就是创建者当初给出的顺序——TRX 不会被规范化到固定的某一侧，因此 `1000124:TRX` 和 `TRX:1000123` 两种形式都会出现。`Reserves` 中的两个数字也遵循同样的顺序。

**这里的储备以最小单位计，而不是完整 token。** 本命令只发起一次 RPC 请求，因此不会额外查询各 token 的精度；`exchange show` 会读取精度并按完整 token 显示。于是同一个交易对在本命令中显示为 `6,672`，在 `exchange show` 中则为 `66.72`。

分页在节点侧完成，而且**没有总数**：链上并不暴露交易对的数量。标题只报告它请求的那个窗口——`Exchanges (limit 3, offset 0)`——而不是 `showing 3 of N`，`meta.pagination.total` 恒为 `null`。想取到全部数据，就用 `--offset` 一页页翻，直到返回的这一页不满为止：`--limit` 上限为 `1000`，超过会以 `invalid_value` 被拒绝。

## 选项

| 选项 | 说明 |
|---|---|
| `--limit <number>` | 最多返回多少个交易对，1–1000（默认 `10`） |
| `--offset <number>` | 分页偏移（默认 `0`） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli exchange list --limit 3 --network tron:3448148188
```

```console
Exchanges (limit 3, offset 0)
| ID | Pair        | Reserves (minimal units)           | Creator           |
| -- | ----------- | ---------------------------------- | ----------------- |
| 14 | 1000124:TRX | 2,500,000,000,000 / 50,000,000,000 | TBeta9mR...8pLx   |
| 13 | 1000125:TRX | 16,000,000 / 8,000,000,000         | TAlpha7k...3nQw   |
| 12 | TRX:1000123 | 10,000,000,000 / 500,000,000,000   | TQkXm4vN...5Zt7Uw |
```

```bash
wallet-cli exchange list --limit 3 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"exchange.list","data":{"kind":"exchange-list","exchanges":[{"exchangeId":14,"pair":"1000124:TRX","creatorAddress":"TBeta9mR...","firstTokenId":"1000124","firstTokenBalance":"2500000000000","secondTokenId":"_","secondTokenBalance":"50000000000"},{"exchangeId":13,"pair":"1000125:TRX","creatorAddress":"TAlpha7k...","firstTokenId":"1000125","firstTokenBalance":"16000000","secondTokenId":"_","secondTokenBalance":"8000000000"},{"exchangeId":12,"pair":"TRX:1000123","creatorAddress":"TQkXm4vN...","firstTokenId":"_","firstTokenBalance":"10000000000","secondTokenId":"1000123","secondTokenBalance":"500000000000"}]},"meta":{"durationMs":52,"warnings":[],"pagination":{"offset":0,"limit":3,"total":null}},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data.kind` 为 `exchange-list`。`data.exchanges[]`——每个交易对一条记录：

| 字段 | 类型 | 含义 |
|---|---|---|
| `exchangeId` | number | 交易对 id |
| `pair` | string | 两侧写作 `tokenA:tokenB`，按链上存储顺序；TRX 在这里写作 `TRX` |
| `creatorAddress` | string | 创建者，base58 格式 |
| `firstTokenId` / `secondTokenId` | string | 链上 token id，按存储顺序；TRX 为 `"_"`——它可能出现在任意一侧 |
| `firstTokenBalance` / `secondTokenBalance` | string | 储备，各 token 最小单位下的原始数量。是**字符串**：储备会达到 int64，作为 JSON number 会损失精度 |

`meta.pagination` 携带 `offset`、`limit` 和 `total`——这里的 `total` 恒为 `null`，表示"不存在计数"，而不是"零"。

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`——limit 或 offset 非法）。

## 另请参见

[`exchange show`](show.md) · [`exchange trade`](trade.md) · [`asset list`](../asset/list.md)
