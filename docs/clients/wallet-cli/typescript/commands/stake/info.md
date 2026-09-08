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
wallet-cli stake info --account main --network tron:3448148188
```

```console
Label         demo
Staked        0 TRX  (for energy 0 TRX + for bandwidth 0 TRX)
Voting power  14 TP  (used 1 / available 13)
Energy        used 0 / 0
Bandwidth     used 317 / 600
Unfreezing    4 pending  (max 32 at a time, 32 more allowed)
              ├─ 100 TRX        withdrawable 2026-08-11 18:26 (~16 day(s) ago)
              ├─ 1,800,151 TRX  withdrawable 2026-08-11 18:44 (~16 day(s) ago)
              ├─ 176 TRX        withdrawable 2026-08-11 18:45 (~16 day(s) ago)
              └─ 13 TRX         withdrawable 2026-08-11 18:45 (~16 day(s) ago)
Withdrawable  1,800,440 TRX now
```

待处理的解质押以树状列在 `Unfreezing` 之下，每一条都标明它何时可提取，以及距离那一刻还有多久。时间已过的条目已经计入 `Withdrawable`；用 [`stake withdraw`](withdraw.md) 一次性全部领回。

```bash
wallet-cli stake info --account main --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"stake.info","data":{"address":"TNmoJ3Be59WFEq5dsW6eCkZjveiL3G8HVB","staked":{"energySun":"0","bandwidthSun":"0"},"votingPower":{"total":14,"used":1,"available":13},"resource":{"energy":{"used":0,"limit":0},"bandwidth":{"used":317,"limit":600}},"unfreezing":[{"amountSun":"100000000","withdrawableAt":1786444011000},{"amountSun":"1800151000000","withdrawableAt":1786445097000},{"amountSun":"176000000","withdrawableAt":1786445103000},{"amountSun":"13000000","withdrawableAt":1786445148000}],"withdrawableSun":"1800440000000","unfreeze":{"used":4,"max":32,"remaining":32}},"meta":{"durationMs":728,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
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
