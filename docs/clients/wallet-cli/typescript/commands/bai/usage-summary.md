# wallet-cli bai usage-summary

显示你的 B.AI 额度余额与逐月用量。

## 用法

```
wallet-cli bai usage-summary [options]
```

## 说明

读取该 API key 所属 B.AI 账户的账户摘要：当前额度余额、本月已消耗额度，以及逐月消耗额度。数字均以 B.AI 报告的为准。不需要钱包，也不需要密码。

需要先用 [`config baiApiKey`](../config.md) 保存 B.AI API key；见 [`bai`](index.md#the-api-key)。

## 选项

没有本命令特有的选项；仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli bai usage-summary
```

```console
B.AI usage summary
  Credit balance: 2025000
  Month: 2026-09
  Credits spent this month: 88000
  Monthly usage:
    1.
      month: 2025-10
      credits: 0
    2.
      month: 2025-11
      credits: 0
    3.
      month: 2025-12
      credits: 0
    4.
      month: 2026-01
      credits: 0
    5.
      month: 2026-02
      credits: 0
    6.
      month: 2026-03
      credits: 42000
    7.
      month: 2026-04
      credits: 118500
    8.
      month: 2026-05
      credits: 96000
    9.
      month: 2026-06
      credits: 203400
    10.
      month: 2026-07
      credits: 175200
    11.
      month: 2026-08
      credits: 231900
    12.
      month: 2026-09
      credits: 88000
```

```bash
wallet-cli bai usage-summary -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"bai.usage-summary","data":{"credits":"2025000","thisMonth":{"month":"2026-09","credits":"88000"},"trend":[{"month":"2025-10","credits":"0"},{"month":"2025-11","credits":"0"},{"month":"2025-12","credits":"0"},{"month":"2026-01","credits":"0"},{"month":"2026-02","credits":"0"},{"month":"2026-03","credits":"42000"},{"month":"2026-04","credits":"118500"},{"month":"2026-05","credits":"96000"},{"month":"2026-06","credits":"203400"},{"month":"2026-07","credits":"175200"},{"month":"2026-08","credits":"231900"},{"month":"2026-09","credits":"88000"}]},"meta":{"durationMs":1119,"warnings":[]}}
```

`Credit balance`（JSON 中的 `credits`）是当前余额。`Credits spent this month`（JSON 中的 `thisMonth`）是本月的消耗，`Monthly usage`（JSON 中的 `trend`）列出最近 12 个月每月的消耗。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `credits` | string | 当前额度余额 |
| `thisMonth` | object | `{month, credits}`——当前月份（`YYYY-MM`）及该月已消耗的额度，均为字符串 |
| `trend[]` | array | B.AI 报告的每个月的 `{month, credits}`，按时间从早到晚 |

## 退出码

`0` 成功 · `1` 执行失败（`bai_auth_failed`——B.AI 拒绝了该 key；`bai_rejected`；`provider_error`；`timeout`） · `2` 用法错误（`bai_credentials_missing`）。

## 另请参见

[`bai usage-records`](usage-records.md) · [`bai recharge`](recharge.md)
