# wallet-cli 8004 transfer

把某个 Agent 转移给新的所有者。

## 用法

```
wallet-cli 8004 transfer <id> <newOwner>
                  [--wait [--wait-timeout <ms>] | --sign-only | --build-only | --dry-run]
                  [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>] [options]
```

## 说明

调用注册表的 `transferFrom(address,address,uint256)`，把该 Agent 从当前所有者转移给 `newOwner`。签名账户必须是所有者、该 Agent 已批准的操作者，或所有者通过 [`8004 add-operator`](add-operator.md) 添加的操作者；否则该调用会在手续费估算阶段、签名之前被以 `not_authorized` 拒绝。不存在的 Agent ID 会以 `agent_not_found` 失败，而 `newOwner` 不得为零地址（否则 `invalid_address`）。

**转移不可撤销**——完成之后，只有新的所有者才能更新、批准或再次转移该 Agent。发送前请核对 `newOwner`。

回执中会给出转移前读到的所有者（`oldOwner`）和你请求的那个。加上 `--wait` 时，它会在确认之后再读一次所有者并补上 `newOwner`；若这次读取失败，则给出一条警告。

需要一个账户。只有会签名的模式才需要通过 `--password-stdin` 提供 master password。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `id`——Agent ID，可选地带上它的规范网络 id 前缀（`<network-id>:<id>`，例如 `tron:3448148188:172`；不接受 `nile:172` 这样的别名形式）
- `newOwner`——新所有者的地址，须属于所选网络的链家族

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

把 Agent 173 转移给 `TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH`。 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
printf '%s' "$PW" | wallet-cli 8004 transfer 173 TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin
```

```console
✅ Called transferFrom
  Contract         TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
  Agent ID         173
  Previous owner   TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
  Requested owner  TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
  Current owner    TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
  TxID             2aa501c87a95185515098b2e333600f8e51a1277ad8b0ff8c8bf2ded59df3a57
  Block            #71,015,932
  Energy           31,998
  Fee              3.5777 TRX
  Status           success
```

```bash
printf '%s' "$PW" | wallet-cli 8004 transfer 173 TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.transfer","data":{"kind":"contract-send","stage":"confirmed","txId":"ca42c4fe2d6246178042bbb205ff3359a821c6f260f776bb267aa7c73072ba44","confirmed":true,"blockNumber":71015936,"feeSun":3577700,"energyUsed":31998,"energyFeeSun":3199700,"netFeeSun":378000,"result":"SUCCESS","failed":false,"method":"transferFrom(address,address,uint256)","contract":"TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5","identity":{"agentId":"173","oldOwner":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","requestedOwner":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","newOwner":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH"}},"meta":{"durationMs":12076,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

`Current owner` 是确认之后读回来的，与请求的所有者一致，说明转移已经生效。

## 输出

`data` 随阶段而异：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-send"`、`stage: "submitted"`、`txId`、`method`、`contract`、`identity` |
| `--wait`（已确认/失败） | 同上，但 `stage` 为 `"confirmed"` 或 `"failed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际开销——TRON 上是 `feeSun` / `energyUsed` / `energyFeeSun` / `netFeeSun` / `result`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`、`signed`、`address`（签名者）、`txId`、`fee`、`method`、`contract`、`identity` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**）、`tx`、`fee`、`method`、`contract`、`identity` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`method`、`contract`，EVM 上另加 `nonce`，以及 `identity` |

`identity` 中有 `agentId`、`oldOwner` 和 `requestedOwner`；在 `--wait` 确认之后还会有 `newOwner`。

## 退出码

`0` 已提交（提前退出的模式下则为已构建/已签名） · `1` execution failure (`not_authorized`——该账户无权对本 Agent 执行此操作；`agent_not_found`——不存在该 id 的 Agent；`execution_reverted`——注册表因其他原因拒绝了该调用，原始 revert 数据在 `error.details.revertData` 中；`auth_required`——签名模式下未给出 `--password-stdin`；`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`——超时后交易仍可能在途，请用 [`tx status`](../tx/status.md) 查询） · `2` 用法错误（`invalid_address`——`newOwner` 不是合法地址，或是零地址；`invalid_value`——id 或 URI 格式错误，或选项组合不当，例如 `--expiration` 没有配 `--sign-only` / `--build-only`；`family_mismatch`——地址属于另一个链家族；`invalid_option`——`--wait` 与提前退出的模式同用；`unsupported_network_capability`——所选网络上没有注册表）

## 另请参见

[`8004 show`](show.md) · [`8004 approve`](approve.md)
