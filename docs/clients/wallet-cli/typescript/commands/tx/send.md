# wallet-cli tx send

用人类可读的 `--amount` 发送原生币或某个 token。

## 用法

```
wallet-cli tx send --to <address|contact> (--amount <n> | --raw-amount <n>)
                   [--token <symbol> | --contract <address> | --asset-id <id>]
                   [--dry-run | --sign-only | --build-only | --wait [--wait-timeout <ms>]]
                   [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>]        # TRON
                   [--gas-limit <n>] [--max-fee <gwei>] [--priority-fee <gwei>] [--nonce <n>]  # EVM
                   [options]
```

## 说明

以当前账户（或 `--account`）构建、签名并提交一笔转账，TRON 与 EVM 网络都适用。发送的是什么，取决于你传入哪个选择器：

- **都不传** → 该网络的原生币（TRX、ETH、BNB……）；
- `--token <symbol>` → 从本地地址簿解析出的 token；
- `--contract <address>` → 按合约地址指定的 token（TRON 上是 TRC20，EVM 上是 ERC20）；
- `--asset-id <id>` → **仅限 TRON**，按数字资产 id 指定的 TRC10。

金额：`--amount` 是人类可读单位（原生币，或按该 token 精度换算的 token 单位）；`--raw-amount` 是原始整数（SUN / wei，或 token 的最小单位）。两者二选一，只能给一个。

精度从哪里来：原生币的精度由链家族固定（TRON 为 6，EVM 为 18），而 token 的精度是从链上读取的——TRC20/ERC20
从合约读取，TRC10 从资产记录读取。因此 `--amount` 会按节点提供的这个数字做换算，而一旦节点谎报了这个精度，
你签名的那个金额小数点就会随之挪位。这个值会按协议范围校验（TRC10 精度必须在 0..6 之间，返回的记录若对应的是
另一个 id 则直接拒绝），但落在该范围*之内*的错误值在本地无从发现——没有任何东西可供比对。当精确的最小单位
数量很重要时，请传 `--raw-amount`，它会被原样使用，绝不重新换算。

提前退出的几种模式仍然都会先通过所选网络完成构建。`--dry-run` 构建并估算，然后返回方案，不签名也不广播；`--sign-only` 构建、估算、签名，并打印已签名交易的 **hex**，但不广播；`--build-only` 构建并估算，但**不会**解锁、也不会签名，打印的是**未签名**的 hex。这段 hex 在 TRON 上是 protobuf，在 EVM 上是 RLP（`0x02…`）；两者都可以接着交给 [`tx sign`](sign.md) 和 [`tx broadcast`](broadcast.md)。

**费用是按家族区分的。** TRON 消耗带宽/能量，并用 `--fee-limit` 限制能量开销上限；EVM 支付 gas，因此改用 `--gas-limit`、`--max-fee`、`--priority-fee` 和 `--nonce`。`--help` 会为每组打上 `(TRON only)` / `(EVM only)` 标记，把其中一组用在另一个家族上会以 `invalid_option` 被拒绝——在仍按 `gasPrice` 计价的 EVM 链上使用 `--max-fee` / `--priority-fee` 也同样会被拒绝。

EVM 上未给出的值会从节点取得：gas 上限来自 `eth_estimateGas`（不做冗余放大），费用上限来自当前的基础费用，nonce 来自该账户的 pending 计数。当估算本身失败时——账户没有余额、节点判定该调用会 revert——错误信息会说明原因，此时可用 `--gas-limit` 跳过估算继续。若某个费用虽然可以签名但值得怀疑（小费被压到上限、上限低于当前基础费用），它会以 `meta.warnings` 报出，而不是被拒绝。

TRON 的多签用 `--permission-id` 选择签名所用的权限组，用 `--expiration` 延长联署人补签的时间窗口。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。可以使用 `--wait` 阻塞至交易确认或失败，也可以自行轮询 [`tx status`](status.md)。

需要：

```text
  仅在需要签名的模式下提供 master password；此时请传 --password-stdin，其他模式无需密码
  一个账户；默认使用当前账户，可用 --account <accountId|label> 覆盖（或执行 `wallet-cli use <account>` 更改当前账户）
```

## 选项

| 选项 | 说明 |
|---|---|
| `--to <address\|contact>` | **必填。** 所选网络下的接收方地址，或[联系人簿](../contact/index.md)中的一个名称 |
| `--amount <string>` | 人类可读金额；与 `--raw-amount` 互斥 |
| `--raw-amount <string>` | 原始整数金额，单位是原生币最小单位（SUN / wei）或 token 最小单位 |
| `--token <string>` | 地址簿中的 token 符号；与 `--contract`、`--asset-id` 互斥 |
| `--contract <string>` | token 合约地址；发送原生币时省略 |
| `--dry-run` | 通过所选网络构建并估算；不签名、不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 构建、估算并签名，输出已签名的 hex，但不广播；与 `--dry-run` / `--build-only` 互斥 |
| `--build-only` | 构建并估算，输出**未签名**的 hex，不解锁钱包；与 `--dry-run` / `--sign-only` 互斥 |
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
| `--gas-limit <string>` | 授权的 gas 单位数；默认取节点的估算值，不做冗余放大 |
| `--max-fee <gwei>` | 每单位 gas 的最高总费用——写作 `25` 或 `25gwei`（仅 EIP-1559 链） |
| `--priority-fee <gwei>` | 支付给出块者的每单位 gas 小费——写作 `25` 或 `25gwei`（仅 EIP-1559 链） |
| `--nonce <n>` | 交易 nonce；默认取该账户的 pending nonce |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

> **关于密码**：下面的示例都省略了密码，以便把注意力放在选择器参数上。软件签名模式需要从 stdin 传入 master password——在前面加上 `printf '%s' "$PW" |`，并在命令末尾加上 `--password-stdin`；而 `--dry-run`、`--build-only` 和 Ledger 签名不需要。

```bash
# 在 Nile 上发送 1 TRX；在 Sepolia 上发送一笔以 ETH 计价的金额
wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network tron:3448148188
wallet-cli tx send --to 0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C --amount 0.0001 --network eip155:11155111

# 两个家族都可以用地址簿中的 token 符号；TRC10 按资产 id 指定，仅限 TRON
wallet-cli tx send --to T... --token USDT --amount 5 --network tron:3448148188
wallet-cli tx send --to 0x... --token USDC --amount 5 --network eip155:11155111
wallet-cli tx send --to T... --asset-id 1002000 --raw-amount 1000000 --network tron:3448148188

# 只演练，不签名
wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network tron:3448148188 --dry-run -o json
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

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.send","data":{"kind":"send","mode":"dry-run","fee":{"feeModel":"eip1559","maxCostWei":"41797991046000","gasLimit":"21000","maxPerGasWei":"1990380526"},"tx":{"to":"0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C","value":"100000000000000","chainId":11155111,"nonce":0,"gasLimit":"21000","type":2,"maxFeePerGas":"1990380526","maxPriorityFeePerGas":"1000000"},"nonce":0,"rawAmount":"100000000000000","to":"0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C"},"meta":{"durationMs":753,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

提交回执（默认模式，text 与 json）：

```bash
printf '%s' "$PW" | wallet-cli tx send --to TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --amount 1 --network tron:3448148188 --password-stdin
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
| 默认（提交） | `kind: "send"`、`stage: "submitted"`、`txId`、`rawAmount`（字符串）、`to`；`--to` 传的是联系人名称时还有 `toContact` |
| `--wait`（已确认） | 同上，但 `stage: "confirmed"`，另加 `confirmed`、`blockNumber`、`netUsed`（消耗的带宽）或 `feeSun`（燃烧的手续费）、`failed` |
| `--wait`（已回滚） | 字段相同，但 `stage: "failed"` 且 `failed: true`——交易已入块，随后执行失败被回滚 |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`rawAmount`、`to` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`（已签名交易的 hex）、`signed`、`address`（签名者）、`txId`、`fee`、`rawAmount`、`to` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**交易的 hex）、未签名的 `tx`、`fee`、`rawAmount`、`to` |

`signed` 是该链自身形式的已签名交易：TRON 上是含 `signature[]` 的交易对象；EVM 上则是 `{raw, hash}`——即 `eth_sendRawTransaction` 接受的那种序列化形式，加上由这些字节推导出的哈希。

在 EVM 上，`data` 还会带上 `nonce`，而确认回执报告的是 `gasUsed`、`feeWei` 和 `effectiveGasPriceWei`，取代 TRON 的 `netUsed` / `feeSun`。

`fee` 对象的形状由该网络的费用模型决定，`feeModel` 会指明是哪一种：

| `feeModel` | 字段 |
|---|---|
| `tron-resource` | `bandwidthBurnSunIfNoFreeze`；合约调用时还有 `energy*` 系列字段 |
| `eip1559` / `legacy` | `maxCostWei`、`gasLimit`、`maxPerGasWei`——每单位 gas 的上限在 EIP-1559 链上是 `maxFeePerGas`，在 legacy 链上是 `gasPrice` |

`tx` 在 TRON 上是 TRON 交易对象（`txID`、`raw_data`、`raw_data_hex`），在 EVM 上则是一个 EVM 交易请求——`to`、`value`、`chainId`、`nonce`、`gasLimit`，外加 `type: 2` 时的 `maxFeePerGas` / `maxPriorityFeePerGas`，或 legacy 链上 `type: 0` 时的 `gasPrice`。`hex` 在 TRON 上是 protobuf hex，在 EVM 上是以 `0x` 开头的 RLP 编码。

被回滚的交易同样会让响应保持 `success: true`、退出码为 `0`——命令完成了，是链拒绝了这笔交易。脚本必须按 `data.stage` 分支，而不是按退出码。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`rpc_error`、`timeout`——**超时后交易可能仍在传播中；重发之前请先用 `tx status` 查询**） · `2` 用法错误（选择器/金额/模式冲突；把标注为 `(TRON only)` 的参数用在 EVM 上、或反之，则为 `invalid_option`）。

节点拒绝 EVM gas 估算时，会以 `rpc_error` 呈现并点名 `eth_estimateGas`，同时提示可用 `--gas-limit` 跳过估算继续。

`0` 同样覆盖 `--wait` 报告 `stage: "failed"` 的情形：退出码反映的是命令本身，而不是链上结果。参见[脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)。

## 另请参见

[`tx status`](status.md) · [`tx broadcast`](broadcast.md) · [手续费与资源](../../concepts/networks.md#fees-the-tron-resource-model) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
