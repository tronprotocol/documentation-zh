# wallet-cli vote status

你当前的投票、投票权与奖励概览。

## 用法

```
wallet-cli vote status [options]
```

## 说明

在一个只读视图中汇总“质押 → 投票 → 奖励”的完整状态，包括当前票数分配、各 SR 的奖励分配比例、投票权（TP 总量 / 已用 / 可用），以及当前可领取的奖励。

- **投票权（TP）**——总量 = 已质押的 TRX；已用 = 已投出的票；可用 = 总量 − 已用。
- **APR / Reward ratio**——语义与 [`vote list`](list.md) 相同；APR 是预留字段，始终显示 `—`。值得反复核对：超级代表随时可以修改自己的比例（链上的 UpdateBrokerage）——按 80% 投出去的票，一旦对方降到 0%，就会在你不知情的情况下不再产生收益。
- **0% 警告**——如果有票落在奖励比例为 0% 的超级代表上，文本输出会追加一行 `!`，JSON 则在 `meta.warnings` 中为每个受影响的超级代表各加一条纯字符串记录。
- **可领取**——与 [`reward balance`](../reward/balance.md) 同源；用 [`reward withdraw`](../reward/withdraw.md) 领取。

## 选项

没有命令级选项；仅[全局选项](../index.md#global-options-every-command)（`--network` / `--account`）。

## 示例

```bash
wallet-cli vote status --account main --network nile
```

```console
Label           main
Voting power    1,500 TP  (used 1,000 / available 500)
Claimable       12.345678 TRX

Current votes (2)
| Name         | Votes | APR | Reward ratio | Address                            |
| ------------ | ----- | --- | ------------ | ---------------------------------- |
| tronscan.org | 600   | —   | 80%          | TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g |
| binance.com  | 400   | —   | 0%           | TNXpQ9nzSJ3bVbmmd4VPhfgHirti3vMFmq |
! 400 votes on binance.com earn nothing — 0% reward ratio
```

```bash
wallet-cli vote status --account main --network nile -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"vote.status","data":{"address":"TQk...","votingPower":{"total":1500,"used":1000,"available":500},"claimableRewardSun":"12345678","votes":[{"witness":"TZ4...","name":"tronscan.org","count":600,"rewardRatioPct":80,"brokeragePct":20,"aprPct":null},{"witness":"TT5...","name":"binance.com","count":400,"rewardRatioPct":0,"brokeragePct":100,"aprPct":null}]},"meta":{"durationMs":16,"warnings":["400 votes on TT5... (binance.com) earn nothing: reward ratio is 0%"]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的账户 |
| `votingPower.total` / `.used` / `.available` | number | TP 总量 / 已占用 / 可用 |
| `claimableRewardSun` | string | 当前可领取的奖励，单位 SUN |
| `votes[]` | array | 当前的票数分配：`witness`、取自 URL 主机名的 `name`、`count`、可为 null 的 `rewardRatioPct` / `brokeragePct`，以及预留的 `aprPct`（恒为 `null`） |

分成比例为零的警告以纯字符串形式出现在 `meta.warnings` 中——参见[读取 `meta.warnings`](../../machine-interface.md#reading-metawarnings)。

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`）。

## 另请参见

[`vote cast`](cast.md) · [`vote list`](list.md) · [`reward balance`](../reward/balance.md) · [`stake info`](../stake/info.md)
