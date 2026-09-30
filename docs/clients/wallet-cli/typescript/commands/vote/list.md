# wallet-cli vote list

列出超级代表和候选人。

## 用法

```
wallet-cli vote list [--limit <n>] [--candidates] [options]
```

## 说明

列出 SR（默认显示当选的 27 位）及其得票数和奖励分配比例，供执行 [`vote cast`](cast.md) 前参考。该命令只读，不需要账户。

各列的含义：

- **APR**——预留字段。该列存在，但当前实现并不计算任何估值：它始终显示 `—`（JSON 中为 `null`）。
- **Reward ratio**——超级代表分给投票者的奖励比例（链上数据，可靠）。80% 表示投票者瓜分 80% 的奖励；**0% 意味着你的投票一分钱也拿不到**。JSON 中还带有链上原生的 `brokeragePct`（= 100 − rewardRatioPct）。
- **排名与资格**——第 1–27 名是当选的超级代表（出块奖励 + 投票奖励）；第 28–127 名是合作伙伴（仅投票奖励）；127 名之后的候选人没有任何收益，因此 `--limit` 的上限就是 127。

## 选项

| 选项 | 说明 |
|---|---|
| `--limit <number>` | 最多返回多少个名次（默认 27，最大 127）。默认只列出当选的 27 位 SR，所以除非同时加上 `--candidates`，调大这个值不会有任何效果 |
| `--candidates` | 同时列出未当选的候选人（第 28 名及之后），此时 `--limit` 才能超过 27、最多到 127 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli vote list --limit 3 --network nile
```

```console
| Rank | Name         | Votes         | APR | Reward ratio | Address                            |
| ---- | ------------ | ------------- | --- | ------------ | ---------------------------------- |
| 1    | tronscan.org | 1,203,456,789 | —   | 80%          | TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g |
| 2    | binance.com  | 998,765,432   | —   | 0%           | TNXpQ9nzSJ3bVbmmd4VPhfgHirti3vMFmq |
| 3    | justlend.org | 876,543,210   | —   | 80%          | TBWEKNMfjjcF8y1hgJvQ8mgvNMfcSMGhx1 |
```

```bash
wallet-cli vote list --limit 3 --network nile -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"vote.list","data":{"witnesses":[{"rank":1,"name":"tronscan.org","address":"TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g","voteCount":"1203456789","rewardRatioPct":80,"brokeragePct":20,"aprPct":null},{"rank":2,"name":"binance.com","address":"TNXpQ9nzSJ3bVbmmd4VPhfgHirti3vMFmq","voteCount":"998765432","rewardRatioPct":0,"brokeragePct":100,"aprPct":null},{"rank":3,"name":"justlend.org","address":"TBWEKNMfjjcF8y1hgJvQ8mgvNMfcSMGhx1","voteCount":"876543210","rewardRatioPct":80,"brokeragePct":20,"aprPct":null}]},"meta":{"durationMs":40,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data.witnesses[]`——每个名次一条：

| 字段 | 类型 | 含义 |
|---|---|---|
| `rank` | number | 按票数排名（1 = 票数最多） |
| `name` | string | 由见证人 URL 推出的主机名；取不到时退回 URL 文本，再退回地址 |
| `address` | string | 超级代表的 base58 地址 |
| `voteCount` | string | 总票数，原始整数 |
| `rewardRatioPct` | number \| null | 分给投票者的奖励百分比；读不到佣金比例时为 `null` |
| `brokeragePct` | number \| null | 超级代表自留的比例（= 100 − `rewardRatioPct`）；不可用时为 `null` |
| `aprPct` | null | 预留字段；当前实现中恒为 `null` |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`——limit 超出取值范围）。

## 另请参见

[`vote cast`](cast.md) · [`vote status`](status.md)
