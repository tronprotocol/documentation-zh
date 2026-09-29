# wallet-cli tx send

用人类可读的 `--amount` 发送原生币或某个 token。

## 用法

```
wallet-cli tx send --to <address|contact> (--amount <n> | --raw-amount <n>)
                   [--token <symbol> | --contract <address> | --asset-id <id>]
                   [--dry-run | --sign-only | --build-only | --wait [--wait-timeout <ms>]]
                   [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>]
                   [--gas-limit <n>] [--max-fee <gwei>] [--priority-fee <gwei>] [--nonce <n>]
                   [options]
```

## 说明

以当前账户（或 `--account`）构建、签名并提交一笔转账，TRON 与 EVM 网络都适用。发送的是什么，取决于你传入哪个选择器：

- **都不传** → 该网络的原生币；
- `--token <symbol>` → 从本地地址簿解析出的 token；
- `--contract <address>` → 按合约地址指定的 token——TRON 上是 TRC20，EVM 上是 ERC20；
- `--asset-id <id>` → 按数字资产 id 指定的 TRC10（**仅限 TRON**）。

金额：`--amount` 是人类可读单位（原生币，或按该 token 精度换算的 token 单位）；`--raw-amount` 是原始整数（SUN / wei，或 token 的最小单位）。两者二选一，只能给一个。原生币的精度由链家族固定（TRON 为 6，EVM 为 18）；token 的精度则从链上读取。

提前退出的几种模式仍然都会先通过所选网络完成构建。`--dry-run` 构建并估算，然后返回方案，不签名也不广播；`--sign-only` 构建、估算、签名，并打印已签名交易的 **hex**，但不广播；`--build-only` 构建并估算，但**不会**解锁、也不会签名，打印的是**未签名**的 hex。这段 hex 在 TRON 上是 protobuf，在 EVM 上是 RLP（`0x02…`）；两者都可以接着交给 [`tx sign`](sign.md) 和 [`tx broadcast`](broadcast.md)。

**费用是按家族区分的。** TRON 消耗带宽/能量，并用 `--fee-limit` 限制能量开销上限；EVM 支付 gas，因此改用 `--gas-limit`、`--max-fee`、`--priority-fee` 和 `--nonce`。`--help` 会为每组打上 `(TRON only)` / `(EVM only)` 标记，把其中一组用在另一个家族上会以 `invalid_option` 被拒绝——在仍按 `gasPrice` 计价的 EVM 链上使用 `--max-fee` / `--priority-fee` 也同样会被拒绝。

EVM 上未给出的值会从节点取得：gas 上限来自 `eth_estimateGas`（不做冗余放大），费用上限来自当前的基础费用，nonce 来自该账户的 pending 计数。当估算本身失败时——账户没有余额、节点判定该调用会 revert——错误信息会说明原因，此时可用 `--gas-limit` 跳过估算继续。若某个费用虽然可以签名但值得怀疑（小费被压到上限、上限低于当前基础费用），它会以 `meta.warnings` 报出，而不是被拒绝。

TRON 的多签用 `--permission-id` 选择签名所用的权限组，用 `--expiration` 延长联署人补签的时间窗口。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。可以使用 `--wait` 阻塞至交易确认或失败，也可以自行轮询 [`tx status`](status.md)。

需要一个账户——默认是当前账户，除非用 `--account <accountId|label>` 覆盖。只有在所选模式确实要签名时，才需要通过 `--password-stdin` 提供 master password；`--dry-run` 和 `--build-only` 从不解锁钱包。签名类命令不会弹出交互提示，因此签名模式下没给密码会以 `auth_required` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--to <address\|contact>` | **必填。** 所选网络上的收款地址，或[联系人簿](../contact/index.md)中的名称 |
| `--amount <string>` | 人类可读金额；与 `--raw-amount` 互斥 |
| `--raw-amount <string>` | 原始整数金额，以原生币最小单位（SUN / wei）或 token 最小单位计 |
| `--token <string>` | 地址簿中的 token 符号；与 `--contract`、`--asset-id` 互斥 |
| `--contract <string>` | token 合约地址——TRON 上是 TRC20，EVM 上是 ERC20；转原生币时省略 |
| `--dry-run` | 通过所选网络构建并估算；不签名、不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 构建、估算、签名，并输出已签名的 hex，但不广播；与 `--dry-run` / `--build-only` 互斥 |
| `--build-only` | 构建并估算，输出**未签名**的 hex，且不解锁钱包；与 `--dry-run` / `--sign-only` 互斥 |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认 60000；达到上限时返回提交回执） |
| `--password-stdin` | 从 stdin 读取 master password |

仅限 TRON：

| 选项 | 说明 |
|---|---|
| `--asset-id <string>` | TRC10 数字资产 id |
| `--fee-limit <string>` | TRC20 转账允许燃烧的最高能量费用，单位 SUN（默认 100000000） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |

仅限 EVM：

| 选项 | 说明 |
|---|---|
| `--gas-limit <string>` | 要授权的 gas 数量；默认取节点的估算值，不做冗余放大 |
| `--max-fee <gwei>` | 每单位 gas 的最高总费用——写作 `25` 或 `25gwei`（仅限 EIP-1559 链） |
| `--priority-fee <gwei>` | 每单位 gas 付给出块者的小费——写作 `25` 或 `25gwei`（仅限 EIP-1559 链） |
| `--nonce <n>` | 交易 nonce；默认取账户的 pending nonce。在 `--dry-run` 下，显式给出的 nonce 会与账户*已入块*的计数比对，若已被用掉，会在任何估算之前以 `nonce_too_low` 失败；而仅仅高于下一个值的 nonce，仍只作为 `meta.warnings` 中的空档提示 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

> **密码**：除 `--dry-run` 外，下面的示例都省略了密码，以便把注意力集中在选择器参数上。真实发送需要通过 stdin 提供 master password——请在前面加上 `printf '%s' "$PW" |`，并在末尾追加 `--password-stdin`（见上文说明）。

```bash
# 1 TRX on Nile; 0.0001 ETH on Sepolia
wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network nile
wallet-cli tx send --to 0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C --amount 0.0001 --network sepolia

# token by address-book symbol on either family; TRC10 by asset id on TRON only
wallet-cli tx send --to T... --token USDT --amount 5 --network nile
wallet-cli tx send --to 0x... --token USDC --amount 5 --network sepolia
wallet-cli tx send --to T... --asset-id 1002000 --raw-amount 1000000 --network nile

# rehearse without signing
wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network nile --dry-run -o json
```

`--dry-run` 按所选网络的费用模型打印费用——TRON 上是带宽/能量，EVM 上是 gas 上限：

```console
⏳ Dry run tx send
  To   TMowUdZm5F4iircH2gnaUSCfDa3hdNLn7V
  Fee  0.1 TRX
  Tx   ff87701b0a...18ad8381
```

```console
⏳ Dry run tx send
  To   0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C
  Fee  ≤ 0.000044 ETH  (21,000 gas × 2.13664 gwei max)
  Tx   {"to":"0x7...000000"}
```

提交回执（默认模式，text 与 json）：

```bash
printf '%s' "$PW" | wallet-cli tx send --to TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --amount 1 --network nile --password-stdin
```

```console
⏳ Sent 1 TRX
  To      TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
  TxID    4574b646adc694e99a1f64e548b2bdf9da62621c2d833f77354f67b751fbd0c4
  Status  pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid 4574b646adc694e99a1f64e548b2bdf9da62621c2d833f77354f67b751fbd0c4
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.send","data":{"kind":"send","stage":"submitted","txId":"4574b646adc694e99a1f64e548b2bdf9da62621c2d833f77354f67b751fbd0c4","rawAmount":"1000000","to":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH"},"meta":{"durationMs":2172,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随模式而变：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "send"`、`stage: "submitted"`、`txId`、`rawAmount`（字符串）、`to`，以及当 `--to` 传的是联系人名称时的 `toContact` |
| `--wait`（已确认） | 同上，但 `stage` 为 `"confirmed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际开销——TRON 上是 `netUsed`（已用带宽）/ `feeSun`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--wait`（已回滚） | 字段相同，但 `stage` 为 `"failed"` 且 `failed: true`——交易已入块，随后被 revert |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`rawAmount`、`to`（EVM 上另加 `nonce`） |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`（已签名的交易 hex）、`signed`、`address`（签名者）、`txId`、`fee`、`rawAmount`、`to` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**的交易 hex）、未签名的 `tx`、`fee`、`rawAmount`、`to` |

`signed` 是该链自身形态下的已签名交易——TRON 上是包含 `signature[]` 的交易对象，EVM 上是 `{raw, hash}`。`fee` 对象遵循该网络的费用模型：`tron-resource` 以 `bandwidthBurnSunIfNoFreeze` 报告估算的资源开销，合约调用还会加上 `energy*` 系列字段；而 `eip1559` / `legacy` 报告的是 `maxCostWei`、`gasLimit` 和 `maxPerGasWei`——其中每单位 gas 的上限，在 EIP-1559 链上是 `maxFeePerGas`，在 legacy 链上是 `gasPrice`。

`tx` 是同样按家族区分形态的未签名交易：TRON 上是 `txID`、`raw_data` 和 `raw_data_hex`；EVM 上是 `to`、`value`、`chainId`、`nonce`、`gasLimit`，再加上 `type: 2` 时的 `maxFeePerGas` / `maxPriorityFeePerGas`，或 legacy 链上 `type: 0` 时的 `gasPrice`。在 EVM 上，`hex` 是 `0x` 开头的 RLP 编码，而不是 protobuf。

被回滚的交易同样会让响应保持 `success: true`、退出码为 `0`——命令完成了，是链拒绝了这笔交易。脚本必须按 `data.stage` 分支，而不是按退出码。

## 退出码

`0` 已提交（提前退出的模式下则为已构建/已签名） · `1` 执行失败（`nonce_too_low`——`--dry-run` 配合一个已入块的 `--nonce`、`rpc_error`、`timeout`——**超时后交易仍可能在途；重发之前请先用 `tx status` 查询**） · `2` 用法错误（选择器/金额/模式互相冲突；`family_mismatch`——收款方或账户属于另一个链家族；`invalid_option`——使用了属于另一个家族的费用参数）。

`0` 同样覆盖 `--wait` 报告 `stage: "failed"` 的情形：退出码反映的是命令本身，而不是链上结果。参见[脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)。

## 另请参见

[`tx status`](status.md) · [`tx broadcast`](broadcast.md) · [费用模型](../../concepts/networks.md#fees-the-tron-resource-model) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
