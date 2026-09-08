# wallet-cli tx broadcast

广播一笔预先签名的交易。

## 用法

```
wallet-cli tx broadcast (--hex <hex> | --file <path> | --transaction <json> | --tx-stdin)
                        [--dry-run] [--network <id>] [options]
```

## 说明

提交一笔在别处签好名的交易，TRON 与 EVM 网络都适用。不需要解锁钱包；交易已经签好名。已签名的输入可以是 **hex**——`--hex` 内联给出，或 `--file` 从文件读取（也就是 `--sign-only` 和 `tx sign` 输出的那种形式；TRON 上是 protobuf，EVM 上是 RLP `0x02…`）——也可以是 **JSON**——`--transaction` 内联给出，或 `--tx-stdin` 从 stdin 读取，这两者**仅限 TRON**。四选一，只能给一个；hex 较长时优先用 `--file`。

TRON 的已签名交易本身不携带网络 id。EVM 的已签名交易确实带有 EIP-155 链 id，但 `--network` 仍然决定连接哪个端点，并且当该链 id 与所选网络不符时，CLI 会拒绝这笔交易。省略时，`--network` 回落到配置中的默认网络。

### 提交前的校验

广播不是盲目的。无论交易以哪种形式送进来，都会先解码并检查，注定无法成功的交易会在本地被拒绝，而不会被发出去。

**TRON：**

- **已过期** → `tx_expired`
- **签名权重不足** → `not_authorized`，并指出还差多少权重

正是这项检查，让它可以安全地作为多签流程的最后一步：尚未达到权限阈值的交易根本不会到达节点。

> 带有多个签名的交易在广播时会在链上产生额外的 **1 TRX 多签手续费**；无论是试运行还是真实广播，它都以 `multiSignFeeSun` 报告。

**EVM：**

- **未签名** → `invalid_transaction`
- **为另一条链构建** → `chain_id_mismatch`，并同时给出两个链 id

报告出来的 `txId` 是由交易自身的字节推导得出的，绝不取自节点——已签名交易的哈希是这笔交易自身的属性，节点无权通过报出另一个哈希来改变你去轮询的对象。

在 EVM 上，`--dry-run` 会把真正能拦下一笔已签名交易的那几件事解析清楚，并以 `checks` 数组返回（`signature`、`chainId`、`nonce`、`balance`）：

- **nonce 已被用掉** → `nonce_too_low`，退出码 1
- **余额低于转账金额 + 费用上限** → `insufficient_balance`，退出码 1
- **nonce 超前于该账户的下一个值**并不致命——它以一条 `warning` 检查项外加一条 `meta.warnings` 记录的形式报出，因为这笔交易本身合法，只是会一直排队，直到中间缺的那些 nonce 被补上

如果节点无法访问，nonce 和余额这两项检查会降级为 `status: "skipped"` 并给出警告，而不会让命令失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--hex <hex>` | 内联给出已签名交易的 hex |
| `--file <path>` | 存放已签名交易 hex 的文件（大小上限略超 1 MiB） |
| `--transaction <string>` | **仅限 TRON。** 内联给出已签名交易的 JSON |
| `--tx-stdin` | **仅限 TRON。** 从 stdin（fd 0）读取已签名交易的 JSON |
| `--dry-run` | 只校验、**不广播**——TRON 上校验签名、阈值、过期时间和动态多签手续费；EVM 上校验签名、链 id、nonce 和余额。不能与 `--wait` 同用 |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认 60000） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

从文件广播一段已签名的 hex：

```bash
wallet-cli tx broadcast --file tx.signed.hex --network tron:3448148188
```

```console
⏳ Broadcast
  Multi-sign fee  0 TRX
  TxID            72a315303323125708f426c77b94c5215afd8964ed27d67e49c29b56e29078f5
  Status          pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid 72a315303323125708f426c77b94c5215afd8964ed27d67e49c29b56e29078f5
```

或者内联给出 hex，并查看 JSON 回执：

```bash
wallet-cli tx broadcast --hex 0a02...9f31 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.broadcast","data":{"kind":"broadcast","stage":"submitted","txId":"72a315303323125708f426c77b94c5215afd8964ed27d67e49c29b56e29078f5","transaction":{"txId":"72a315303323125708f426c77b94c5215afd8964ed27d67e49c29b56e29078f5","contractType":"TransferContract","operation":"Transfer TRX","from":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","to":"TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA","rawAmount":"1000000","permission":{"id":0,"name":"owner","threshold":1},"currentWeight":1,"missingWeight":0,"thresholdReached":true,"approved":[{"address":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","weight":1}],"expiration":1784388720000,"expired":false,"signatures":1},"multiSignFeeSun":0},"meta":{"durationMs":926,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交，TRON） | `kind`、`stage: "submitted"`、`txId`、`transaction`（批准视图）、`multiSignFeeSun` |
| 默认（提交，EVM） | `kind`、`stage: "submitted"`、`txId`；若节点此前已经见过这笔交易，还会有 `alreadyKnown: true` |
| `--wait`（已确认/失败） | 提交阶段的字段，外加 `confirmed`、`blockNumber`、`failed`，以及结果字段——TRON 上是 `netUsed` / `feeSun`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--dry-run`（TRON） | `kind`、`mode: "dry-run"`、`transaction`（批准视图）、`multiSignFeeSun` |
| `--dry-run`（EVM） | `kind`、`mode: "dry-run"`、`txId`、`hash`、`address`（恢复出的签名者）、`to`、`rawAmount`、`fee`（`feeModel`、`maxCostWei`、`gasLimit`、`maxPerGasWei`）、`tx`，以及 `checks[]`（`name`、`status`——`ok` / `warning` / `skipped`——和 `detail`） |

在 TRON 上，`multiSignFeeSun` 始终存在——单签交易为 `0`，因为这笔手续费从第二个签名开始才收取——因此文本回执里始终有一行 `Multi-sign fee`，位于 `TxID` 之前。

在 EVM 上，若节点已经知道这笔交易，提交回执会带上 `alreadyKnown: true`，而不是报错。

与 `tx send` 一样，默认的返回点是**提交**——请通过 `--wait` 或 [`tx status`](status.md) 确认结果。

## 退出码

`0` 已提交 · `1` 执行失败（节点拒绝了该交易、超时；TRON 上还有 `tx_expired` / `not_authorized`；EVM 上还有 `invalid_transaction`、`chain_id_mismatch`、`nonce_too_low`、`insufficient_balance`） · `2` 用法错误（输入来源给了多个或一个都没给；在 EVM 网络上使用 `--transaction` / `--tx-stdin` 报 `invalid_option`）。

注意 `--dry-run` 在交易注定会失败时会以**非零**退出码结束——这正是脚本想要的答案。

## 另请参见

[`tx send --sign-only`](send.md) · [`tx status`](status.md) · [脚本化指南](../../guide/scripting.md#sign-here-broadcast-there)
