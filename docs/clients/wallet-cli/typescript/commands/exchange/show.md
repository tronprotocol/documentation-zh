# wallet-cli exchange show

查看单个交易对。

## 用法

```
wallet-cli exchange show <id> [options]
```

## 说明

报告一个交易对的创建者、创建时间，以及两侧 token 及其储备。只读，不需要账户。

**这里不显示价格。** 两侧储备之比只是一个报价，仅在交易规模趋近于零时才成立；任何有实际成交量的交易都会沿曲线走得更远，换回的更少。把它打印出来只会诱使人把它当成可执行价格。要针对当前储备为某个具体数量定价，请运行 [`exchange trade --dry-run`](trade.md)。

与 [`exchange list`](list.md) 不同，本命令会解析两侧 token 的名称和精度，因此**储备量按完整 token 显示**。JSON 除原始余额外，还包含 `firstTokenLabel` / `firstTokenDecimals` 以及对应的 `second*` 字段。同一个交易对在本命令中可能显示为 `66.72`，而在 `exchange list` 中显示为最小单位数量 `6,672`。

`pair` 以及 `first*` / `second*` 字段都遵循链上存储的顺序，也就是创建者当初给出的顺序——TRX 不会被规范化到固定的某一侧。text 输出把两侧按同样的顺序汇总成一个 `Reserves` 块。

## 选项

| 选项 | 说明 |
|---|---|
| `<id>` | **必填。** 交易对 id |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli exchange show 12 --network tron:3448148188
```

```console
Exchange id 12
  Creator       TQkXm4vN...5Zt7Uw
  Created time  2026-08-02 09:15:00 UTC
  Reserves
    TRX                   10,000
    MyToken (id 1000123)  500,000
```

```bash
wallet-cli exchange show 12 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"exchange.show","data":{"kind":"exchange-show","exchangeId":12,"pair":"TRX:1000123","creatorAddress":"TQkXm4vN...","createTime":1785662100000,"firstTokenId":"_","firstTokenBalance":"10000000000","firstTokenLabel":"TRX","firstTokenDecimals":6,"secondTokenId":"1000123","secondTokenBalance":"500000000000","secondTokenLabel":"MyToken","secondTokenDecimals":6},"meta":{"durationMs":24,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data.kind` 为 `exchange-show`。

| 字段 | 类型 | 含义 |
|---|---|---|
| `exchangeId` | number | 交易对 id |
| `pair` | string | 两侧写作 `tokenA:tokenB`，按链上存储顺序；TRX 在这里写作 `TRX` |
| `creatorAddress` | string | 创建者，base58 格式——唯一可以注资或撤资的账户 |
| `createTime` | number | 创建时间，epoch 以来的毫秒数 |
| `firstTokenId` / `secondTokenId` | string | 链上 token id，按存储顺序；TRX 为 `"_"`——它可能出现在任意一侧 |
| `firstTokenBalance` / `secondTokenBalance` | string | 储备，各 token 最小单位下的原始数量。是**字符串**：储备会达到 int64，作为 JSON number 会损失精度 |
| `firstTokenLabel` / `secondTokenLabel` | string | token 名称，或 `TRX` |
| `firstTokenDecimals` / `secondTokenDecimals` | number | text 输出按完整 token 渲染数值时所用的小数位数 |

## 退出码

`0` 成功 · `1` 执行失败（`exchange_not_found`——没有这个交易对、`rpc_error`） · `2` 用法错误（`invalid_value`——id 不是数字）。

## 另请参见

[`exchange list`](list.md) · [`exchange trade`](trade.md) · [`exchange inject`](inject.md)
