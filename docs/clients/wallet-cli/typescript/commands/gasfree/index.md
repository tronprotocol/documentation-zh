# wallet-cli gasfree

通过 GasFree 服务进行免 gas 的 token 转账。

`gasfree` 可以在账户没有 TRX 时转移 token：用户签署 TIP-712 结构化数据（TRON 版的 EIP-712），再由 GasFree 服务（[open.gasfree.io](https://open.gasfree.io)）代为提交上链。费用直接从转出的 token 中扣除，包括每笔交易的服务费，以及首次交易的一次性激活费，因此**完全不需要 TRX**。

**仅限 TRON。** GasFree 是 TRON 上的服务；本组每一条子命令在 EVM 网络上都会以 `family_mismatch` 失败。

## 用法

```
wallet-cli gasfree COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `gasfree info` | [info.md](info.md) | 你的 GasFree 地址、激活状态、`nonce` 与费率表 |
| `gasfree transfer` | [transfer.md](transfer.md) | 签署一笔免 gas 转账并提交给服务方 |
| `gasfree trace` | [trace.md](trace.md) | 用 `traceId` 跟踪已提交的转账 |

## 工作原理

- 每个账户都有一个**确定性派生出的 GasFree 地址**。资产在该地址上收取和支付——要通过 GasFree 收 USDT，就把你的 GasFree 地址（见 `gasfree info`）给付款方。
- **首次**转账时，服务方会在链上激活这个 GasFree 地址，并在每笔转账服务费之外额外收取一次性的激活费。两笔费用都从 token 中扣除。
- 每个地址使用独立递增的 **`nonce`**，用于防止重放攻击。
- 需要服务方的 **API 凭据**——用 [`config`](../config.md) 设置 `gasfreeApiKey` / `gasfreeApiSecret`。`--network` 用于选择服务环境（主网 / 测试网）。

与 [`tx send`](../tx/send.md) 相比，`tx send` 直接向链上广播，会消耗带宽、能量或燃烧 TRX；`gasfree transfer` 通过服务方 API 提交，不消耗 TRX，但每笔转账都要支付以 token 计价的费用。账户拥有 TRX 或足够能量时，`tx send` 通常成本更低；`gasfree` 主要用于账户完全没有 TRX 的情况。

## 另请参见

[`gasfree info`](info.md) · [`gasfree transfer`](transfer.md) · [`gasfree trace`](trace.md) · [`config`](../config.md) · [`tx send`](../tx/send.md)
