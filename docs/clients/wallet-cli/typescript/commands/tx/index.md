# wallet-cli tx

构建、发送、广播、联署以及查看交易。

## 用法

```
wallet-cli tx COMMAND
```

## 子命令

| 命令 | 说明 | 适用网络 |
|---|---|---|
| [`tx send`](send.md) | 用人类可读的 `--amount` 发送原生币或某个 token | TRON、EVM |
| [`tx broadcast`](broadcast.md) | 广播一笔预先签名的交易 | TRON、EVM |
| [`tx status`](status.md) | 查看交易的确认状态 | TRON、EVM |
| [`tx info`](info.md) | 查看交易的完整详情和交易回执 | TRON、EVM |
| [`tx sign`](sign.md) | 对在别处构建好的交易签名 | TRON、EVM |
| [`tx approvals`](approvals.md) | 查看一笔多签交易上已收集的签名 | 仅 TRON |
| [`tx multisig`](multisig.md) | 通过 TronLink 服务进行多签协作（列出 / 创建 / 联署 / 监听） | 仅 TRON |

这些命令之间传递的交易 **hex**，在 TRON 上是 `protocol.Transaction` protobuf，在 EVM 上是 RLP（`0x02…`）。费用参数也因家族而异——TRON 上是 `--fee-limit` / `--permission-id` / `--expiration`，EVM 上是 `--gas-limit` / `--max-fee` / `--priority-fee` / `--nonce`——两组参数用在另一个家族上都会以 `invalid_option` 被拒绝。

## 交易生命周期

```
build ──sign──> submit ──receipt──> confirmed
  │                │                     │
  └ --dry-run      └ default return      └ tx status: confirmed/failed
    stops here       point ("submitted")   (pending/not_found while in flight)
```

`tx send` 一步完成构建+签名+提交（用 `--dry-run` / `--sign-only` 可以提前停下）；`tx broadcast` 提交在别处签好名的交易；`tx status` / `tx info` 用于观察结果。`confirmed` 表示已入块并取得回执，不表示已最终确定。**提交不等于确认**——脚本必须遵循[机器接口 → 脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)。

## 多签联署

**仅限 TRON。** EVM 交易只带一个签名，因此既没有阈值可达，也没有联署流程；在 EVM 上 `tx sign` 只是单纯签名，而 `tx approvals` / `tx multisig` 根本不绑定到 EVM。

对于需要多个签名的 TRON 账户，有两条联署路径：

- **链上方式**——[`tx sign`](sign.md) / [`tx approvals`](approvals.md) / [`tx broadcast`](broadcast.md)：发起方用 `--sign-only` 生成一段部分签名的 hex，每位签名者依次传递该 hex，并用 `tx sign` 追加自己的签名；达到阈值后，任何人都可以广播。整个流程无需借助外部服务。
- **服务方式**——[`tx multisig`](multisig.md)：由 TronLink 多签服务保管交易、累计签名并推送通知。开启一次签名收集就是发起方自己的第一个签名，达到阈值后由服务负责广播。这是可选的便利层，需要凭据。

无论采用哪条路径，都可以用 [`tx approvals`](approvals.md) 检查签名是否达到阈值。[`tx broadcast`](broadcast.md) 会拒绝提交签名权重不足的交易，因此这类交易不会到达节点。

联署所依赖的账户权限结构，参见 [`permission`](../permission/index.md)。

## 另请参见

[`account history`](../account/index.md) · [网络与费用](../../concepts/networks.md) · [脚本编写指南](../../guide/scripting.md)
