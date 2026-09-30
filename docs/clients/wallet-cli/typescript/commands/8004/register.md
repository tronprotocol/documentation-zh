# wallet-cli 8004 register

注册一个新 Agent。

## 用法

```
wallet-cli 8004 register <uri>
                  [--wait [--wait-timeout <ms>] | --sign-only | --build-only | --dry-run]
                  [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>] [options]
```

## 说明

以当前账户（或 `--account`）调用注册表的 `register(string)`，该账户即成为此 Agent 的所有者。URI 必须指向一份由你自行构建并托管的注册文档；wallet-cli 不创建、也不校验它的内容。

URI 必须是 `https://`、`ipfs://` 或 base64 JSON 的 `data:` URI，最长 2048 个字符，且其中不得含有凭据。[`8004 show`](show.md) 只加载 `https://` 和 `http://` 的文档，因此用 `ipfs://` 或 `data:` URI 注册的 Agent 在那里不会显示注册详情；若希望能用 wallet-cli 读到这些内容，请优先使用 `https://`。

**Agent ID 由链分配。** 默认的提交回执里只有 `identity.uri`。加上 `--wait` 后，一旦能读到已确认的注册事件，回执就会补上 `identity.agentId`。不加 `--wait` 时，可事后从交易中读取：在 [`tx info`](../tx/info.md)` -o json` 中，`data.info.log` 的第一条就是注册表的 `Transfer` 事件，它的最后一个 topic 就是 hex 形式的 Agent ID（`…00aa` 即 Agent 170）。**不要为了拿 id 而重新注册**——那会再创建一个 Agent。

需要一个账户。只有会签名的模式才需要通过 `--password-stdin` 提供 master password。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `uri`——注册文档的 URI

## 选项

| 选项 | 说明 |
|---|---|
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥 |
| `--build-only` | 构建并估算，输出**未签名**的 hex，且不解锁钱包；与 `--dry-run` / `--sign-only` 互斥 |
| `--dry-run` | 只做估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--password-stdin` | 从 stdin 读取 master password |

仅限 TRON：

| 选项 | 说明 |
|---|---|
| `--fee-limit <sun>` | 允许燃烧的最高能量费用，单位 SUN（默认 100000000） |
| `--permission-id <n>` | 签名所用的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |

没有 EVM 侧的费用参数：在 EVM 上，gas 上限和费用均取自节点的估算，`--gas-limit` 之类会被当作未知选项拒绝。

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

在 Nile 上注册一个 Agent 并等待它的 ID。这里的注册文档是一个很小的 `data:` URI。 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
printf '%s' "$PW" | wallet-cli 8004 register "data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBmb3IgYSBjaXR5In0=" --network nile --wait --password-stdin
```

```console
✅ Called register
  Contract  TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
  Agent ID  173
  URI       data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBmb3IgYSBjaXR5In0=
  TxID      ee19cabbc6bfa4bc0201669c967c95f639a46128826f33b5fb27a9bb6de8a4c8
  Block     #71,015,894
  Energy    183,779
  Fee       18.8561 TRX
  Status    success
```

```bash
printf '%s' "$PW" | wallet-cli 8004 register "data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBmb3IgYSBjaXR5In0=" --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.register","data":{"kind":"contract-send","stage":"confirmed","txId":"6850f29e0eff687d0f0f41515a067fced277cd0fd0bbe2773371268cd14894ee","confirmed":true,"blockNumber":71015896,"feeSun":18884800,"energyUsed":183779,"energyFeeSun":18377800,"netFeeSun":507000,"result":"SUCCESS","failed":false,"method":"register(string)","contract":"TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5","identity":{"uri":"data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBmb3IgYSBjaXR5In0=","agentId":"173"}},"meta":{"durationMs":6869,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

新的 Agent ID 是 `173`——在 JSON 中对应 `data.identity.agentId`。`Fee` 是本次注册所消耗能量而燃烧掉的 TRX。

## 输出

`data` 随阶段而异：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-send"`、`stage: "submitted"`、`txId`、`method`、`contract`、`identity` |
| `--wait`（已确认/失败） | 同上，但 `stage` 为 `"confirmed"` 或 `"failed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际开销——TRON 上是 `feeSun` / `energyUsed` / `energyFeeSun` / `netFeeSun` / `result`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`、`signed`、`address`（签名者）、`txId`、`fee`、`method`、`contract`、`identity` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**）、`tx`、`fee`、`method`、`contract`、`identity` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`method`、`contract`，EVM 上另加 `nonce`，以及 `identity` |

`identity` 中有 `uri`；在 `--wait` 确认之后还会有 `agentId`（十进制字符串）。

## 退出码

`0` 已提交（提前退出的模式下则为已构建/已签名） · `1` 执行失败（`execution_reverted`——注册表在估算阶段拒绝了该调用，原始 revert 数据在 `error.details.revertData` 中；`auth_required`——签名模式下未给出 `--password-stdin`；`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`——超时后交易仍可能在途，请用 [`tx status`](../tx/status.md) 查询） · `2` 用法错误（`invalid_value`——id 或 URI 格式错误，或选项组合不当，例如 `--expiration` 没有配 `--sign-only` / `--build-only`；`family_mismatch`——地址属于另一个链家族；`invalid_option`——`--wait` 与提前退出的模式同用；`unsupported_network_capability`——所选网络上没有注册表）

## 另请参见

[`8004 show`](show.md) · [`8004 update`](update.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
