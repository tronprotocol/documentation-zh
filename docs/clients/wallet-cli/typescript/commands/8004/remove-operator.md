# wallet-cli 8004 remove-operator

收回某个操作者管理本账户全部 Agent 的权限。

## 用法

```
wallet-cli 8004 remove-operator <operator>
                  [--wait [--wait-timeout <ms>] | --sign-only | --build-only | --dry-run]
                  [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>] [options]
```

## 说明

调用注册表的 `setApprovalForAll(operator, false)`，撤销 [`8004 add-operator`](add-operator.md) 的效果。由 [`8004 approve`](approve.md) 给出的、针对单个 Agent 的批准不受影响——那些需要用 `8004 approve <id> --revoke` 单独清除。

需要一个账户。只有会签名的模式才需要通过 `--password-stdin` 提供 master password。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `operator`——要收回权限的地址

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

取消 `TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH` 作为当前账户全部 Agent 的操作者。 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
printf '%s' "$PW" | wallet-cli 8004 remove-operator TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin
```

```console
✅ Called setApprovalForAll
  Contract  TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
  Operator  TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
  TxID      5f62b3cfba3da2859104add9ef36eb4bae4bc96f1480c67fd9c1eaf440e12c59
  Block     #71,039,810
  Energy    7,934
  Fee       1.1383 TRX
  Status    success
```

```bash
printf '%s' "$PW" | wallet-cli 8004 remove-operator TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.remove-operator","data":{"kind":"contract-send","stage":"confirmed","txId":"9311d9aeec938ba6c640f45ebb699421037d687580c017892e22e96cfff5db0c","confirmed":true,"blockNumber":71039812,"feeSun":1138300,"energyUsed":7934,"energyFeeSun":793300,"netFeeSun":345000,"result":"SUCCESS","failed":false,"method":"setApprovalForAll(address,bool)","contract":"TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5","identity":{"operator":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","requestedApproval":false,"approved":false}},"meta":{"durationMs":5058,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

`Operator`（JSON 中的 `identity.operator`）是被收回权限的地址。`identity.approved: false` 是确认之后从注册表读回的权限状态；对这一对所有者与操作者执行 [`8004 operator-check`](operator-check.md) 会得到相同结果。

## 输出

`data` 随阶段而异：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-send"`、`stage: "submitted"`、`txId`、`method`、`contract`、`identity` |
| `--wait`（已确认/失败） | 同上，但 `stage` 为 `"confirmed"` 或 `"failed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际开销——TRON 上是 `feeSun` / `energyUsed` / `energyFeeSun` / `netFeeSun` / `result`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`、`signed`、`address`（签名者）、`txId`、`fee`、`method`、`contract`、`identity` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**）、`tx`、`fee`、`method`、`contract`、`identity` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`method`、`contract`，EVM 上另加 `nonce`，以及 `identity` |

`identity` 中有 `operator` 和 `requestedApproval`（本命令下为 `false`）。在 `--wait` 确认之后，它会补上 `approved`——从注册表读回的权限状态，应当与 `requestedApproval` 一致。若这次读取失败，你会得到一条警告；**不要**因此重发交易。

## 退出码

`0` 已提交（提前退出的模式下则为已构建/已签名） · `1` execution failure (`execution_reverted`——注册表在估算阶段拒绝了该调用，原始 revert 数据在 `error.details.revertData` 中；`auth_required`——签名模式下未给出 `--password-stdin`；`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`——超时后交易仍可能在途，请用 [`tx status`](../tx/status.md) 查询） · `2` 用法错误（`invalid_value`——id 或 URI 格式错误，或选项组合不当，例如 `--expiration` 没有配 `--sign-only` / `--build-only`；`family_mismatch`——地址属于另一个链家族；`invalid_option`——`--wait` 与提前退出的模式同用；`unsupported_network_capability`——所选网络上没有注册表）

## 另请参见

[`8004 add-operator`](add-operator.md) · [`8004 operator-check`](operator-check.md)
