# wallet-cli stake info

质押与资源总览。

## 用法

```
wallet-cli stake info [options]
```

## 说明

用一屏只读信息呈现账户的质押状态：质押金额、投票权（TP）、能量/带宽用量、待解锁的解质押、当前可提取的 TRX，以及剩余的解质押名额。执行 [`stake unfreeze`](unfreeze.md) / [`stake withdraw`](withdraw.md) / [`vote cast`](../vote/cast.md) 之前先看这里。

字段解读：

- **已质押**（`Staked`）——括号里把质押的 TRX 按资源方向拆开（质押给能量的 TRX 与质押给带宽的 TRX），*不是*换到的资源单位数。真正的额度是 `Energy` / `Bandwidth` 两行的上限（动态值，按全网换算比例计算）。
- **投票权**（`Voting power`）——与 [`vote status`](../vote/status.md) 同源：1 TP = 1 TRX 质押。列在这里是为了打通质押 → 投票。
- **解质押中**（`Unfreezing`）——Stake 2.0 允许同时最多 **32 笔待解锁的解质押**；`N more allowed` 是链上剩余的名额数。名额用满时，要先提取已到期的条目，才能继续解质押。
- **可提取**（`Withdrawable`）——现在执行 [`stake withdraw`](withdraw.md) 能领到的金额。

## 选项

没有命令级选项；仅[全局选项](../index.md#global-options-every-command)（`--network` / `--account`）。

## 示例

```bash
wallet-cli stake info --account main --network nile
```

```console
Label         main
Staked        1,500 TRX  (for energy 1,000 TRX + for bandwidth 500 TRX)
Voting power  1,500 TP  (used 1,000 / available 500)
Energy        used 12,000 / 65,000
Bandwidth     used 600 / 1,500
Unfreezing    2 pending  (max 32 at a time, 30 more allowed)
              ├─ 500 TRX  withdrawable 2026-07-15 08:00 (in ~10 day(s))
              └─ 300 TRX  withdrawable 2026-07-16 08:00 (in ~11 day(s))
Withdrawable  0 TRX now
```

```bash
wallet-cli stake info --account main --network nile -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"stake.info","data":{"address":"TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V","staked":{"energySun":"1000000000","bandwidthSun":"500000000"},"votingPower":{"total":1500,"used":1000,"available":500},"resource":{"energy":{"used":12000,"limit":65000},"bandwidth":{"used":600,"limit":1500}},"unfreezing":[{"amountSun":"500000000","withdrawableAt":1784073600000},{"amountSun":"300000000","withdrawableAt":1784160000000}],"withdrawableSun":"0","unfreeze":{"used":2,"max":32,"remaining":30}},"meta":{"durationMs":22,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的账户 |
| `staked.energySun` / `.bandwidthSun` | string | 按资源方向划分的质押 TRX，单位 SUN（不是资源单位） |
| `votingPower.total` / `.used` / `.available` | number | TP 总量 / 已用 / 可用 |
| `resource.energy` / `.bandwidth` | object | `{used, limit}`，单位为资源单位 |
| `unfreezing[]` | array | 待解锁的解质押：`{amountSun, withdrawableAt (epoch 毫秒)}` |
| `withdrawableSun` | string | 当前可提取的 TRX，单位 SUN |
| `unfreeze` | object | 名额占用情况 `{used, max, remaining}` |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`）。

## 另请参见

[`stake delegated`](delegated.md) · [`vote status`](../vote/status.md) · [质押指南](../../guide/stake-and-resources.md)
