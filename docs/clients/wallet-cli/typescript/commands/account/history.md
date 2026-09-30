# wallet-cli account history

显示交易历史（需要 TronGrid）。

## 用法

```
wallet-cli account history [--limit <n>] [--only <native|token>] [options]
```

## 说明

> **仅限 TRON。** 该列表在 EVM 上没有对应实现，因此在 EVM 网络上本命令会以 `family_mismatch` 失败，而不是返回一个空列表。

列出与该账户相关的近期活动，最新的在前。历史数据由 **TronGrid** 提供，而不是普通的节点 RPC——在没有 TronGrid 的网络或端点上，本命令会失败，而 `balance`/`info` 仍然可用。

`--only token` 选用的是 TronGrid 的 TRC20 转账端点。`--only native` 选用的是通用交易端点，并且不会对其返回的记录做后置过滤，因此结果中可能包含非原生币的合约活动；不带 `--only` 时查询的也是同一个端点。请不要把 JSON 中的 `only: "native"` 理解为「每条记录都是 TRX 转账」的证明。

## 选项

| 选项 | 说明 |
|---|---|
| `--limit <number>` | 最大记录数，1–200（默认 20） |
| `--only token` | 查询 TRC20 转账历史 |
| `--only native` | 选用通用交易端点；它并不是严格意义上「只看原生币转账」的筛选 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli account history --limit 3 --network nile
```

```console
"main" recent transactions
| Time        | Type     | Amount | From / To                          | Status |
| ----------- | -------- | ------ | ---------------------------------- | ------ |
| 07-11 22:35 | Transfer | 1 TRX  | TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH | ✅      |
| 07-11 15:58 | Transfer | 1 TRX  | TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH | ✅      |
| 07-11 15:58 | Transfer | 1 TRX  | TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH | ✅      |
```

```bash
wallet-cli account history --limit 2 --network nile -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.history","data":{"address":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","only":"all","count":2,"records":[{"txId":"fb7f8e6b44cd9100f6d1133acea341a2f3d53ab140a93c95b8f2bd74d3a2b366","time":1783780503000,"type":"Transfer","amount":"1","symbol":"TRX","from":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","to":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","counterparty":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","status":"ok"},{"txId":"aa9c6d96b582201bda4ca1f7f35eff597371f5ca8e99db0df78d02d78f668a31","time":1783779301000,"type":"Transfer","amount":"2","symbol":"TRX","from":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","to":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","counterparty":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","status":"ok"}]},"meta":{"durationMs":1556,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` / `only` / `count` | —— | 查询条件回显与记录数 |
| `records[].txId` | string | 可交给 [`tx info`](../tx/info.md) 查看详情 |
| `records[].time` | number | epoch 毫秒 |
| `records[].type` | string | 交易类型（例如 `Transfer`、`CreateSmart`） |
| `records[].amount` | string | 转账金额；非价值转移时为空 |
| `records[].symbol` | string | 资产符号（例如 `TRX`） |
| `records[].from` / `to` / `counterparty` | string | 各地址（按类型不同可能为空） |
| `records[].status` | string | `ok` 或失败标记 |

## 退出码

`0` · `1` 执行失败（`history_not_supported`——TronGrid 端点缺失或不兼容） · `2` 用法错误（limit 超出 1–200；在 EVM 网络上为 `family_mismatch`）。

## 另请参见

[`tx info`](../tx/info.md) · [`account portfolio`](portfolio.md) · [故障排查](../../troubleshooting.md#not-an-error-code-but-frequently-asked)
