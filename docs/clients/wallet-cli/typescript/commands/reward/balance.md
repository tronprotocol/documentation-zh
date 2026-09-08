# wallet-cli reward balance

显示可领取的奖励和提取状态。

## 用法

```
wallet-cli reward balance [options]
```

## 说明

显示当前可领取的投票/出块奖励，以及现在能否提取。只读——它是 [`reward withdraw`](withdraw.md) 的“领取前先查一下”搭档，这样你就不必靠触发 `withdraw_too_frequent` 错误来试探 24 小时限制。

`Withdraw status` 由账户链上的 `latest_withdraw_time` + 24 小时推导而来：已超过该时刻（或从未提取过）→ `available now`；否则为 `available from <绝对时间> (in ~<相对时间>)`。

## 选项

没有命令级选项；仅[全局选项](../index.md#global-options-every-command)（`--network` / `--account`）。

## 示例

当前即可领取：

```bash
wallet-cli reward balance --account main --network tron:3448148188
```

```console
Label            main
Claimable        123.456789 TRX
Withdraw status  available now
```

距上次提取不足 24 小时：

```bash
wallet-cli reward balance --account main --network tron:3448148188
```

```console
Label            main
Claimable        5.678901 TRX
Withdraw status  available from 2026-07-06 09:30 (in ~18h)
```

```bash
wallet-cli reward balance --account main --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"reward.balance","data":{"address":"TQk...","rewardSun":"123456789","withdrawableNow":true,"withdrawableAt":null},"meta":{"durationMs":14,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的账户 |
| `rewardSun` | string | 可领取的奖励，单位 SUN |
| `withdrawableNow` | boolean | 当前是否可以提取 |
| `withdrawableAt` | number \| null | 何时变为可提取（epoch 毫秒）；已经可提取时为 `null` |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`）。

## 另请参见

[`reward withdraw`](withdraw.md) · [`vote status`](../vote/status.md)
