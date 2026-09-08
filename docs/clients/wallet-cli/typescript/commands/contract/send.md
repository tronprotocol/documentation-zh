# wallet-cli contract send

改变链上状态的合约调用。

## 用法

```
wallet-cli contract send --contract <address> --method <sig> [--params <json>] [--value <n>]
                         [--dry-run | --sign-only | --build-only | --wait [--wait-timeout <ms>]]
                         [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>]        # TRON
                         [--gas-limit <n>] [--max-fee <gwei>] [--priority-fee <gwei>] [--nonce <n>]  # EVM
                         [options]
```

## 说明

以当前账户（或 `--account`）在 TRON 或 EVM 上构建、签名并广播一次会改变链上状态的合约调用。参数沿用与 [`contract call`](call.md) 相同的 `{type,value}` JSON 数组约定；函数签名和类型都由你显式给出，不会参考任何 ABI。

`--value` 用于在调用时附带原生代币，单位是**完整的币**（写 `1.5`，不是最小单位）。TRON 的 `--call-value-sun` 仍然可用、并且以 SUN 计，但它**已废弃，将在下个版本移除**——请改用 `--value`。

两种提前退出方式：`--dry-run` 预览开销但不签名、不广播——TRON 上是能量，EVM 上是 gas 上限；`--sign-only` 完成签名并打印交易，供之后 [`tx broadcast`](../tx/broadcast.md) 使用，`--build-only` 则打印未签名的交易。

费用相关的参数跟随链家族——TRON 上是 `--fee-limit` / `--permission-id` / `--expiration`，EVM 上是 `--gas-limit` / `--max-fee` / `--priority-fee` / `--nonce`。`--help` 会为每组打上标记，把其中一组用在另一个家族上会以 `invalid_option` 被拒绝。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。链上执行失败时返回 `stage: "failed"`：TRON 会在 `result` 中给出原因（`revert` / `OUT_OF_ENERGY`），EVM 则通过回执中的失败状态表示。

命令需要一个账户。仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。
`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回
`watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--contract <string>` | **必填。** 合约地址——TRON 为 base58，EVM 为 `0x` |
| `--method <string>` | **必填。** 函数签名，例如 `transfer(address,uint256)` |
| `--params <string>` | ABI 参数的 JSON 数组，元素形如 `{type,value}` |
| `--value <string>` | 随调用发送的原生代币，单位为完整的币 |
| `--dry-run` | 只做估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥 |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

仅限 TRON：

| 选项 | 说明 |
|---|---|
| `--call-value-sun <number>` | **已废弃**，将在下个版本移除——随调用附带的原生 TRX，单位 SUN。请改用 `--value` |
| `--fee-limit <number>` | 允许燃烧的最高能量费用，单位 SUN（默认 100000000） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |

仅限 EVM：

| 选项 | 说明 |
|---|---|
| `--gas-limit <n>` | 授权的 gas 单位数；默认取节点的估算值，不做冗余放大 |
| `--max-fee <gwei>` | 每单位 gas 的最高总费用（仅 EIP-1559 链） |
| `--priority-fee <gwei>` | 每单位 gas 的小费（仅 EIP-1559 链） |
| `--nonce <n>` | 交易 nonce；默认取该账户的 pending nonce |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

默认——广播并返回**已提交**的回执：

```bash
echo "$PW" | wallet-cli contract send --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --method "transfer(address,uint256)" --params '[{"type":"address","value":"TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc"},{"type":"uint256","value":"1000000"}]' --network tron:3448148188 --password-stdin
```

```console
⏳ Called transfer
  Contract  TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf
  TxID      c8d...
  Status    pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid c8d...
```

```bash
echo "$PW" | wallet-cli contract send --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --method "transfer(address,uint256)" --params '[...]' --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.send","data":{"kind":"contract-send","stage":"submitted","txId":"c8d...","method":"transfer(address,uint256)","contract":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf"},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

加上 `--wait` 会阻塞直到确认——成功时：

```bash
echo "$PW" | wallet-cli contract send --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --method "transfer(address,uint256)" --params '[...]' --network tron:3448148188 --wait --password-stdin
```

```console
✅ Called transfer
  Contract  TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf
  TxID      0adc5737b724d35c486a05a169b64a01ad311ed27f79d308f245b00c69b3bc42
  Block     #69,095,391
  Energy    14,584
  Fee       0.345 TRX
  Status    success
```

链上执行失败（例如能量不足）会返回 `stage: "failed"`：

```bash
echo "$PW" | wallet-cli contract send --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --method "transfer(address,uint256)" --params '[...]' --network tron:3448148188 --wait --password-stdin
```

```console
❌ Called transfer
  Contract  TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf
  TxID      c8d...
  Block     #66,000,123
  Energy    31,200
  Status    failed
  Reason    OUT_OF_ENERGY
```

## 输出

`data` 随阶段而变：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-send"`、`stage: "submitted"`、`txId`、`method`、`contract` |
| `--wait`（已确认/失败） | 同上，但 `stage` 为 `"confirmed"` 或 `"failed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际发生的成本——TRON 上是 `feeSun` / `energyUsed` / `result`（`SUCCESS`、`OUT_OF_ENERGY` 等），EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`（已签名交易的 hex）、`signed`、`address`（签名者）、`txId`、`fee`、`method`、`contract` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**交易的 hex）、未签名的 `tx`、`fee`、`method`、`contract` |

`signed` 是该链自身形式的已签名交易——TRON 上是含 `signature[]` 的交易对象，EVM 上则是 `{raw, hash}`。

`fee` 对象的形状由该网络的费用模型决定：`tron-resource` 报告估算的 `energy` 和 `availableEnergy`；`eip1559` / `legacy` 报告 `maxCostWei`、`gasLimit` 和 `maxPerGasWei`。EVM 上 `data` 还会带上 `nonce`，而 `hex` 是 `0x` 开头的 RLP 编码，而不是 protobuf。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`——超时后交易可能仍在途中，请用 [`tx status`](../tx/status.md) 查询） · `2` 用法错误（`invalid_value`、模式冲突；把标注为 `(TRON only)` 的参数用在 EVM 上、或反之，则为 `invalid_option`）。

## 另请参见

[`contract call`](call.md) · [`contract deploy`](deploy.md) · [`tx broadcast`](../tx/broadcast.md) · [能量与带宽](../../concepts/energy-bandwidth.md)
