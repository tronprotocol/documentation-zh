# wallet-cli exchange

TRON 协议层的 Bancor 交易所。

交易对撮合的是 **TRX 与 TRC10 资产**——绝不涉及 TRC20——并按联合曲线即时结算。任一侧都可以是 TRX 或某个 TRC10 id，因此 TRC10 兑 TRC10 的交易对也是合法的；唯一的规则是两侧不能相同。没有订单簿，没有对手方，也没有撮合。有四个特性与大多数人熟悉的 AMM 不同，在动用这组命令之前，这四点都很要紧：

- **交易对归创建者私有。** 只有创建该交易对的账户才能为它注入或撤出流动性，而且这种绑定无法转移。没有 LP token，也没有外部流动性提供者。
- **但任何人都可以交易**——尽管流动性不开放，交易是开放的。
- **协议不收手续费。** `trade`、`inject` 和 `withdraw` 只消耗带宽；唯一的收费项是 `create`，它会燃烧 `getExchangeCreateFee`。
- **人类可读金额按节点提供的精度换算。** 每一个 `--amount` / `--amounts` / `--min-received` 都会用节点报告的 TRC10 `precision` 换算成最小单位，而那个值决定了你签名时的数量。它会按协议范围 0–6 以及所请求的 token id 做校验，但落在该范围内的错误值在本地无从发现——当精确的最小单位数量很重要时，请用 `--raw-*` 系列，因为它们会被原样使用。
- **TRX 在链上的 token id 是下划线 `_`。** 你可以写 `TRX`（大小写不限）或某个资产 id；`_` 同样接受。JSON 显示的是实际上链的内容，因此 TRX 在那里显示为 `"_"`。

**定价遵循曲线，而不是储备比例。** 两侧储备的比例只是一个边际报价——仅在交易量为零时才成立。真实的交易会沿曲线移动，且相对储备越大，拿到的价格就越差。这中间的差额就是滑点。[`exchange trade`](trade.md) 接受一个可选的下限（`--min-received`、`--raw-min-received` 或 `--slippage`）；三者都不给是允许的，但会给出警告，并提交协议允许的最小值 `expected = 1`，那实际上等于没有保护。本组的任何命令都不会打印「价格」。要为某个具体数额定价，请对当前储备执行 `exchange trade --dry-run`。储备本身还受链参数 `getExchangeBalanceLimit` 的上限约束。

**本组命令只通过 ID 指定 token**，即 `TRX` 或数字形式的 asset ID，不接受 token 名称。交易对使用冒号分隔（`--pair TRX:1000123`、`--amounts 10000:500000`）；由于 TRC10 名称本身可以包含冒号，允许使用名称会导致 `--pair` 产生歧义。可通过 [`asset info <name>`](../asset/info.md) 将名称解析为 ID。

> **仅限 TRON。** 本组的每条命令实现的都是 TRON 独有的协议特性，EVM 上没有对应物；在 EVM 网络上，它们会在任何节点调用之前就以 `family_mismatch` 失败。

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
