# wallet-cli exchange

TRON 协议层的 Bancor 交易所。

交易对交易的是 **TRX 和 TRC10 资产**，不涉及 TRC20，并按照 Bancor 联合曲线即时结算。两侧都可以是 TRX 或某个 TRC10 id，因此 TRC10 对 TRC10 的交易对同样合法；唯一的规则是两侧必须不同：不使用订单簿、对手方或撮合机制。使用本组命令前，需要注意以下几点与常见自动做市商的区别：

- **交易对专属于它的创建者。** 只有创建该交易对的账户才能对它注资或撤资，而且这层绑定无法转移。这里没有 LP token，也没有外部流动性提供者。
- **任何人都可以交易。** 流动性管理仅限创建者，但交易本身对所有账户开放。
- **协议不收取任何手续费。** `trade`、`inject` 和 `withdraw` 只消耗带宽；唯一要花钱的是 `create`，它会燃烧 `getExchangeCreateFee`。
- **人类可读金额按节点提供的小数位换算。** 每个 `--amount` / `--amounts` /
  `--min-received` 都会用节点报告的 TRC10 `precision` 换算成基本单位，也就是说，
  这个值决定了你签名时的实际数量。它会按协议允许的 0..6 范围以及所请求的
  token id 做校验，但落在该范围内的错误值本地无从发现。当精确的基本单位数量很重要时，
  请改用 `--raw-*` 系列参数——它们会被原样使用。
- **TRX 在链上的 token id 是下划线 `_`。** 可以写 `TRX`（大小写不限）或某个 asset id；`_` 也一样接受。json 展示的是真正上链的内容，因此 TRX 在其中显示为 `"_"`。

**定价由曲线决定，而不是简单使用储备比例。** 两侧储备的比值只表示交易量趋近于零时的边际价格。
实际交易会改变曲线位置，交易量相对储备越大，滑点通常越高。这段差额就是滑点。[`exchange trade`](trade.md) 接受一个可选的下限（`--min-received`、`--raw-min-received` 或 `--slippage`）；三个都不给也是允许的，但会给出一条警告，并按协议最小值 `expected = 1` 提交，这实际上等于没有任何滑点保护。要估算特定数量的兑换结果，请基于当前储备执行
`exchange trade --dry-run`。储备量还受链参数 `getExchangeBalanceLimit` 限制。

**本组命令只通过 ID 指定 token**，即 `TRX` 或数字形式的 asset ID，不接受 token 名称。交易对使用冒号分隔（`--pair TRX:1000123`、`--amounts 10000:500000`）；由于 TRC10 名称本身可以包含冒号，允许使用名称会导致 `--pair` 产生歧义。可通过 [`asset info <name>`](../asset/info.md) 将名称解析为 ID。

**仅限 TRON。** Bancor 交易所内置于 TRON 协议中；本组每一条子命令在 EVM 网络上都会以 `family_mismatch` 失败。

## 用法

```
wallet-cli exchange COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `exchange create` | [create.md](create.md) | 创建交易对并为两侧注入初始资金 |
| `exchange inject` | [inject.md](inject.md) | 按储备比例注资 |
| `exchange withdraw` | [withdraw.md](withdraw.md) | 按储备比例撤资 |
| `exchange trade` | [trade.md](trade.md) | 用一侧换取另一侧 |
| `exchange show` | [show.md](show.md) | 查看单个交易对的创建者、创建时间和储备 |
| `exchange list` | [list.md](list.md) | 分页列出交易对 |

## 另请参见

[`asset`](../asset/index.md) · [`tx send`](../tx/send.md) · [`chain params`](../chain/params.md)
