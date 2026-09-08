# wallet-cli asset

发行和管理 TRC10 token。

TRC10 是 TRON 的**链原生** token 标准，发行、ICO 销售和供应量冻结均由协议实现，而不是由智能合约
实现。因此，本组命令不同于处理 TRC20 合约 token 的 [`token`](../token/index.md) 和
[`contract`](../contract/index.md)；TRC10 本身没有合约地址。

使用本组命令前，需要了解以下四项规则：

- **每个账户只能发行一个 token。** 已发行过 TRC10 的账户无法再次发行；如果发行参数有误，只能更换
  账户重新发行。
- **发行后大部分参数不可更改。** 发行费用会被燃烧，之后只有描述、URL 和两项免费带宽限额仍可编辑（[`asset update`](update.md)）。供应量、精度、ICO 比率、ICO 窗口和冻结批次在发行时即固定，链上无法修改。
- **participate 是 ICO，不是市场。** [`asset participate`](participate.md) 在募集窗口内，按 token 创建时设定的固定比率从发行中购买。这里没有订单簿；TRX↔TRC10 的交易在 [`exchange`](../exchange/index.md) 中。
- **转账不在本组。** 用 [`tx send --asset-id <id>`](../tx/send.md) 发送 TRC10，与其他 token 一样。

**仅限 TRON。** TRC10 是 TRON 的协议特性，EVM 上没有对应物；本组每一条子命令在 EVM 网络上都会以 `family_mismatch` 失败。

命令行和 text 输出中的金额以**完整 token** 计；json 携带链上的原始值（完整 token × 10^precision）。

## 用法

```
wallet-cli asset COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `asset issue` | [issue.md](issue.md) | 发行 TRC10 并锁定其 ICO 条款 |
| `asset update` | [update.md](update.md) | 修改四个可变字段 |
| `asset participate` | [participate.md](participate.md) | 用 TRX 参与某个 token 的 ICO |
| `asset unfreeze` | [unfreeze.md](unfreeze.md) | 释放已到期的冻结供应量 |
| `asset info` | [info.md](info.md) | 某个 TRC10 的完整详情 |
| `asset list` | [list.md](list.md) | 分页列出 TRC10 token |

## 另请参见

[`tx send`](../tx/send.md) · [`token info`](../token/info.md) · [`exchange`](../exchange/index.md)
