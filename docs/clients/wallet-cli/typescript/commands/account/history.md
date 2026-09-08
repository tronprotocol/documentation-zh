# wallet-cli account history

显示交易历史。仅限 TRON。

## 用法

```
wallet-cli account history [--limit <n>] [--only <native|token>] [options]
```

## 说明

按时间倒序列出与该账户相关的近期活动。仅限 TRON——它没有 EVM 实现，因此在 EVM 网络上本命令会以 `family_mismatch` 失败，而不是返回空列表。历史数据由 **TronGrid** 提供，而非普通的节点 RPC，因此在没有 TronGrid 的 TRON 网络/端点上本命令会失败，而 `balance`/`info` 仍然可用。

`--only token` 使用 TronGrid 的 TRC20 转账接口。当前的 `--only native` 使用通用交易接口，且不会再次过滤返回记录，因此结果中可能包含非原生币的合约活动；省略 `--only` 时也使用该接口。JSON 中的 `only: "native"` 仅表示选择了该接口，不能证明每条记录都是 TRX 转账。

## 选项

| 选项 | 说明 |
|---|---|
| `--limit <number>` | 最大记录数，1–200（默认 20） |
| `--only token` | 查询 TRC20 转账历史 |
| `--only native` | 选择通用交易接口；目前并不是严格的原生转账过滤器 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli account history --limit 3 --network tron:3448148188
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
wallet-cli account history --limit 2 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.history","data":{"address":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","only":"all","count":2,"records":[{"txId":"fb7f8e6b44cd9100f6d1133acea341a2f3d53ab140a93c95b8f2bd74d3a2b366","time":1783780503000,"type":"Transfer","amount":"1","symbol":"TRX","from":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","to":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","counterparty":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","status":"ok"},{"txId":"aa9c6d96b582201bda4ca1f7f35eff597371f5ca8e99db0df78d02d78f668a31","time":1783779301000,"type":"Transfer","amount":"2","symbol":"TRX","from":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","to":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","counterparty":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","status":"ok"}]},"meta":{"durationMs":1556,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` / `only` / `count` | — | 查询回显与返回的记录条数；`only` 只是回显所选项，并不会强化上面所说的过滤保证 |
| `records[].txId` | string | 交给 [`tx info`](../tx/info.md) 查看详情 |
| `records[].time` | number | epoch 毫秒 |
| `records[].type` | string | 交易类型（例如 `Transfer`、`CreateSmart`） |
| `records[].amount` | string | 转账金额；非价值转移时为空 |
| `records[].symbol` | string | 资产符号（例如 `TRX`） |
| `records[].from` / `to` / `counterparty` | string | 相关地址（按类型可能为空） |
| `records[].status` | string | `ok` 或失败标记 |

## 退出码

`0` · `1` 执行失败（`history_not_supported`，包括 TronGrid 端点缺失或不兼容） · `2` 用法错误（limit 超出 1–200）。

## 另请参见

[`tx info`](../tx/info.md) · [`account portfolio`](portfolio.md) · [故障排查](../../troubleshooting.md#not-an-error-code-but-frequently-asked)
