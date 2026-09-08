# wallet-cli stake delegated

代理明细与最大可代理额度。

## 用法

```
wallet-cli stake delegated [--direction out|in] [--resource energy|bandwidth]
                           [--to <address>] [options]
```

## 说明

以只读方式列出资源代理，支持两个方向：`out`（默认）显示当前账户代理给其他地址的资源以及
**最大可代理额度**（`Max delegatable`）；`in` 显示其他地址代理给当前账户的资源。最大可代理额度仅适用于
出向记录。`--to` 可将出向结果筛选到单个接收方。

**锁定时间在两个方向下含义不同。** 两者读取同一个链上到期字段，但：

- **`out`** → `Locked until`：这是*你*设置的锁定——到期前你无法收回（可随时收回时显示 `not locked`）；
- **`in`** → `Guaranteed until`：代理方在此时间前无法收回资源；`none — reclaimable anytime` 表示
  代理方可以随时收回。

`json` 输出在两个方向上都保留原始的 `lockedUntil` 时间戳——机器层不做视角转换。

## 选项

| 选项 | 说明 |
|---|---|
| `--direction <out\|in>` | `out` = 代理给别人（默认）；`in` = 别人代理给我 |
| `--resource <energy\|bandwidth>` | 只看单一资源类型（默认两者都看） |
| `--to <string>` | 只看代理给该接收方的记录（仅出向） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

出向（默认）——包含 **最大可代理额度**（`Max delegatable`）：

```bash
wallet-cli stake delegated --direction out --account main --network tron:3448148188
```

```console
Label      demo
Direction  out (delegated to others)

Max delegatable
  Energy     900 TRX
  Bandwidth  300 TRX

Delegations (2)
  Receiver                            Resource   Amount   Locked until
  TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub  energy     500 TRX  2026-07-08 08:00 (in ~3 day(s))
  TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz  bandwidth  100 TRX  not locked
```

`Max delegatable` 指的是**仍可自由代理出去的已质押 TRX**，而不是资源单位数——在 JSON 中即 `canDelegateMaxSun`，文本按 TRX 呈现。

```bash
wallet-cli stake delegated --direction out --account main --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"stake.delegated","data":{"address":"TQk...","direction":"out","canDelegateMaxSun":{"energy":"900000000","bandwidth":"300000000"},"delegations":[{"receiver":"TBy6...","resource":"energy","amountSun":"500000000","lockedUntil":1783468800000},{"receiver":"TXe4...","resource":"bandwidth","amountSun":"100000000","lockedUntil":null}]},"meta":{"durationMs":28,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

入向（`--direction in`）——锁定列变成 `Guaranteed until`，且没有 `Max delegatable`：

```bash
wallet-cli stake delegated --direction in --account main --network tron:3448148188
```

```console
Label      demo
Direction  in (delegated to me)

Delegations (1)
  From                                Resource  Amount   Guaranteed until
  TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub  energy    500 TRX  2026-07-08 08:00 (in ~3 day(s))
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的账户 |
| `direction` | string | `out` / `in` |
| `canDelegateMaxSun` | object | `{energy, bandwidth}`，SUN 字符串——按方向给出的、仍可自由代理出去的已质押 TRX（仅出向） |
| `delegations[]` | array | 每一项：`receiver`（出向）或 `from`（入向）、`resource`、`amountSun`（string）、`lockedUntil`（epoch 毫秒或 `null`） |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`）。

## 另请参见

[`stake delegate`](delegate.md) · [`stake undelegate`](undelegate.md) · [`stake info`](info.md)
