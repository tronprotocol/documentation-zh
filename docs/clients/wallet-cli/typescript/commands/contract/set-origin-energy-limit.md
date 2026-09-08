# wallet-cli contract set-origin-energy-limit

设置部署者为每次调用承担的能量上限。

## 用法

```
wallet-cli contract set-origin-energy-limit <address> <energy>
                                            [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                                            [--permission-id <n>] [options]
```

## 说明

设置 `origin_energy_limit`——即**部署者**愿意为对该合约的单次调用支付的能量上限。

它既不是合约的总能量限制，也不是调用方的能量上限。部署者实际承担的能量同时受三个因素约束：该上限、部署者通过质押获得的能量，以及 [`contract set-user-resource-percent`](set-user-resource-percent.md) 设定的调用方/部署者分摊比例。部署者无法承担的部分由调用方支付。在两种情况下，该设置不会产生实际效果：部署者没有质押能量（无论上限是多少，可补贴能量都为 0），或者用户承担比例为 100%（部署者份额为 0）。

`<energy>` 必须是**大于零**的整数——链会拒绝 0，因此本地就会拦下来，不会广播出去。

**仅限 TRON**——「部署者付能量」模型在 EVM 上没有对应物；该网络会以 `family_mismatch` 失败。

只有合约的部署者才能执行此操作；当前值见 [`contract info`](info.md)。设置在交易确认后立即生效。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

Ledger 的 TRON 应用无法解析这一治理类合约。Ledger 账户可以做试运行或构建，但签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `<address>` | **必填。** 要配置的合约；你必须是它的部署者 |
| `<energy>` | **必填。** 部署者为每次调用承担的能量，整数且 > 0 |
| `--dry-run` | 只构建和估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
echo "$PW" | wallet-cli contract set-origin-energy-limit TQ5nJ8mV...4wRe 50000000 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Origin energy limit set
  Contract      TQ5nJ8mV...4wRe
  Deployer      TQkXm4vN...5Zt7Uw (main)
  Energy limit  50,000,000
  TxID          3a9...
  Block         57,882,265
  Fee           0 TRX  (290 bandwidth)
  Status        success
```

```bash
echo "$PW" | wallet-cli contract set-origin-energy-limit TQ5nJ8mV...4wRe 50000000 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.set-origin-energy-limit","data":{"kind":"contract-set-origin-energy-limit","stage":"confirmed","txId":"3a9...","confirmed":true,"blockNumber":57882265,"failed":false,"contractAddress":"TQ5nJ8mV...","deployerAddress":"TQkXm4vN...","originEnergyLimit":50000000,"feeSun":0,"energyUsed":0,"netUsed":290,"energyFeeSun":0,"netFeeSun":0,"resource":{"netUsage":290,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0}},"meta":{"durationMs":6530,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-set-origin-energy-limit"`、`stage: "submitted"`、`txId`、`contractAddress`、`deployerAddress`、`originEnergyLimit` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理命令的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`），以及 `failed` |

`originEnergyLimit` 即当前生效的值。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`contract_not_found`——没有这个合约、`not_contract_deployer`、`watch_only_no_signer`、`ledger_unsupported`、`auth_failed`） · `2` 用法错误（`invalid_value`——地址格式非法，或能量不是大于 0 的整数）。

## 另请参见

[`contract set-user-resource-percent`](set-user-resource-percent.md) · [`contract info`](info.md) · [能量与带宽](../../concepts/energy-bandwidth.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
