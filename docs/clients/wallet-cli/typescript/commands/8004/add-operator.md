# wallet-cli 8004 add-operator

允许某个操作者管理本账户拥有的全部 Agent。

## 用法

```
wallet-cli 8004 add-operator <operator>
                  [--wait [--wait-timeout <ms>] | --sign-only | --build-only | --dry-run]
                  [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>] [options]
```

## 说明

以当前账户（或 `--account`）调用注册表的 `setApprovalForAll(operator, true)`。此后，该操作者可以对本账户拥有的任何 Agent 执行更新、转移或批准操作者，**包括日后才收到的 Agent**，直到 [`8004 remove-operator`](remove-operator.md) 收回该权限为止。

若只想为单个 Agent 批准操作者，请用 [`8004 approve`](approve.md)。结果可用 [`8004 operator-check`](operator-check.md) 查验。

需要一个账户。只有会签名的模式才需要通过 `--password-stdin` 提供 master password。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `operator`——要授予该权限的地址

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

让 `TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH` 可以管理当前账户的全部 Agent。 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
printf '%s' "$PW" | wallet-cli 8004 add-operator TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin
```

```console
✅ Called setApprovalForAll
  Contract  TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
  Operator  TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
  TxID      1275606774d2f7d51d9e534f919a16fa99d452d1545a43ac4a18792696cd8531
  Block     #71,039,806
  Energy    22,934
  Fee       2.1681 TRX
  Status    success
```

```bash
printf '%s' "$PW" | wallet-cli 8004 add-operator TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.add-operator","data":{"kind":"contract-send","stage":"confirmed","txId":"0320dea652e7e0899d7b64fc2d1f02e642c902d37f5de1321f07edbf853deaea","confirmed":true,"blockNumber":71039808,"feeSun":1138300,"energyUsed":7934,"energyFeeSun":793300,"netFeeSun":345000,"result":"SUCCESS","failed":false,"method":"setApprovalForAll(address,bool)","contract":"TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5","identity":{"operator":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","requestedApproval":true,"approved":true}},"meta":{"durationMs":6158,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

`Operator`（JSON 中的 `identity.operator`）是获得该权限的地址。`identity.approved: true` 是确认之后从注册表读回的权限状态，因此不必再单独执行一次 [`8004 operator-check`](operator-check.md)。

## 输出

`data` 随阶段而异：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-send"`、`stage: "submitted"`、`txId`、`method`、`contract`、`identity` |
| `--wait`（已确认/失败） | 同上，但 `stage` 为 `"confirmed"` 或 `"failed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际开销——TRON 上是 `feeSun` / `energyUsed` / `energyFeeSun` / `netFeeSun` / `result`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`、`signed`、`address`（签名者）、`txId`、`fee`、`method`、`contract`、`identity` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**）、`tx`、`fee`、`method`、`contract`、`identity` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`method`、`contract`，EVM 上另加 `nonce`，以及 `identity` |

`identity` 中有 `operator` 和 `requestedApproval`（本命令下为 `true`）。在 `--wait` 确认之后，它会补上 `approved`——从注册表读回的权限状态，应当与 `requestedApproval` 一致。若这次读取失败，你会得到一条警告；**不要**因此重发交易。

## 退出码

`0` 已提交（提前退出的模式下则为已构建/已签名） · `1` execution failure (`execution_reverted`——注册表在估算阶段拒绝了该调用，原始 revert 数据在 `error.details.revertData` 中；`auth_required`——签名模式下未给出 `--password-stdin`；`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`——超时后交易仍可能在途，请用 [`tx status`](../tx/status.md) 查询） · `2` 用法错误（`invalid_value`——id 或 URI 格式错误，或选项组合不当，例如 `--expiration` 没有配 `--sign-only` / `--build-only`；`family_mismatch`——地址属于另一个链家族；`invalid_option`——`--wait` 与提前退出的模式同用；`unsupported_network_capability`——所选网络上没有注册表）

## 另请参见

[`8004 remove-operator`](remove-operator.md) · [`8004 operator-check`](operator-check.md) · [`8004 approve`](approve.md)
