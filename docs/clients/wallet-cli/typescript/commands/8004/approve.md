# wallet-cli 8004 approve

为单个 Agent 批准一个操作者，或清除该批准。

## 用法

```
wallet-cli 8004 approve <id> <operator>
wallet-cli 8004 approve <id> --revoke
                  [--wait [--wait-timeout <ms>] | --sign-only | --build-only | --dry-run]
                  [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>] [options]
```

## 说明

调用注册表的 `approve(address,uint256)`。被批准的操作者可以管理**这一个** Agent——更新它的 URI 或转移它。每个 Agent 最多只有一个已批准的操作者，因此批准新的会替换掉旧的。该 Agent 被转移时，批准会被清除。

`--revoke` 通过批准零地址来清除批准；它不接收操作者参数。若想让某个操作者管理你的**全部** Agent，请改用 [`8004 add-operator`](add-operator.md)。

只有所有者，或所有者通过 [`8004 add-operator`](add-operator.md) 添加的操作者，才能执行批准。该 Agent 自身已批准的操作者**不能**批准他人，和其他任何人一样，会在手续费估算阶段、签名之前被以 `not_authorized` 拒绝。不存在的 Agent ID 会以 `agent_not_found` 失败。

需要一个账户。只有会签名的模式才需要通过 `--password-stdin` 提供 master password。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `id`——Agent ID，可选地带上它的规范网络 id 前缀（`<network-id>:<id>`，例如 `tron:3448148188:172`；不接受 `nile:172` 这样的别名形式）
- `operator`——要批准的地址；除非使用 `--revoke`，否则必填，且不能与 `--revoke` 同用

## 选项

| 选项 | 说明 |
|---|---|
| `--revoke` | 清除当前的批准 |
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

让 `TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH` 可以管理 Agent 173。 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
printf '%s' "$PW" | wallet-cli 8004 approve 173 TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin
```

```console
✅ Called approve
  Contract  TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
  Agent ID  173
  Operator  TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
  TxID      aae465db71a0d35aeaa7d9818c71f52f52dfcc1d2efc7245656710c2bb525635
  Block     #71,015,912
  Energy    22,778
  Fee       2.6227 TRX
  Status    success
```

```bash
printf '%s' "$PW" | wallet-cli 8004 approve 173 TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.approve","data":{"kind":"contract-send","stage":"confirmed","txId":"50ac14a81ef8959d3c7bb1eb8ce20d528ceaf8e289e577738725d58e80eef164","confirmed":true,"blockNumber":71015914,"feeSun":2622700,"energyUsed":22778,"energyFeeSun":2277700,"netFeeSun":345000,"result":"SUCCESS","failed":false,"identity":{"operator":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","agentId":"173"},"method":"approve(address,uint256)","contract":"TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5"},"meta":{"durationMs":6841,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

日后要清除该批准，执行 `8004 approve 173 --revoke`；其回执中的操作者会显示为零地址。

## 输出

`data` 随阶段而异：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-send"`、`stage: "submitted"`、`txId`、`method`、`contract`、`identity` |
| `--wait`（已确认/失败） | 同上，但 `stage` 为 `"confirmed"` 或 `"failed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际开销——TRON 上是 `feeSun` / `energyUsed` / `energyFeeSun` / `netFeeSun` / `result`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`、`signed`、`address`（签名者）、`txId`、`fee`、`method`、`contract`、`identity` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**）、`tx`、`fee`、`method`、`contract`、`identity` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`method`、`contract`，EVM 上另加 `nonce`，以及 `identity` |

`identity` 中有 `agentId` 和 `operator`——使用 `--revoke` 时为零地址。

## 退出码

`0` 已提交（提前退出的模式下则为已构建/已签名） · `1` execution failure (`not_authorized`——该账户无权对本 Agent 执行此操作；`agent_not_found`——不存在该 id 的 Agent；`execution_reverted`——注册表因其他原因拒绝了该调用，原始 revert 数据在 `error.details.revertData` 中；`auth_required`——签名模式下未给出 `--password-stdin`；`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`——超时后交易仍可能在途，请用 [`tx status`](../tx/status.md) 查询） · `2` 用法错误（`invalid_value`——id 或 URI 格式错误，或选项组合不当，例如 `--expiration` 没有配 `--sign-only` / `--build-only`；`family_mismatch`——地址属于另一个链家族；`invalid_option`——`--wait` 与提前退出的模式同用；`unsupported_network_capability`——所选网络上没有注册表）

## 另请参见

[`8004 show`](show.md) · [`8004 add-operator`](add-operator.md)
