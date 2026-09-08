# wallet-cli contract clear-abi

清除合约存储在链上的 ABI。

## 用法

```
wallet-cli contract clear-abi <address>
                              [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                              [--permission-id <n>] [options]
```

## 说明

移除合约保存在链上的 ABI。**此操作无法撤销**——ABI 从链上消失后，所有靠读取它来解码调用的工具（区块浏览器、SDK、[`contract call`](call.md)）此后都必须自行提供 ABI。

它**不会**动到的东西：`bytecode` 和合约状态都不受影响，合约照样可以像之前一样被调用。ABI 只是附带的元数据，并不参与执行。

**仅限 TRON**——EVM 链上没有链上 ABI 可清除，该网络会以 `family_mismatch` 失败。

只有合约的部署者才能执行此操作——即链上记录为该合约 `origin` 的地址，可在 [`contract info`](info.md) 中查看。其他账户会以 `not_contract_deployer` 失败。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

Ledger 的 TRON 应用无法解析这一治理类合约。Ledger 账户可以做试运行或构建，但签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `<address>` | **必填。** 要清除 ABI 的合约 |
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
echo "$PW" | wallet-cli contract clear-abi TQ5nJ8mV...4wRe --network tron:3448148188 --wait --password-stdin
```

```console
✅ ABI cleared
  Contract  TQ5nJ8mV...4wRe
  Deployer  TQkXm4vN...5Zt7Uw (main)
  TxID      3f7...
  Block     57,882,140
  Fee       0 TRX  (287 bandwidth)
  Status    success
```

```bash
echo "$PW" | wallet-cli contract clear-abi TQ5nJ8mV...4wRe --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.clear-abi","data":{"kind":"contract-clear-abi","stage":"confirmed","txId":"3f7...","confirmed":true,"blockNumber":57882140,"failed":false,"contractAddress":"TQ5nJ8mV...","deployerAddress":"TQkXm4vN...","feeSun":0,"energyUsed":0,"netUsed":287,"energyFeeSun":0,"netFeeSun":0,"resource":{"netUsage":287,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0}},"meta":{"durationMs":6510,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-clear-abi"`, `stage: "submitted"`, `txId`, `contractAddress`, `deployerAddress` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理命令的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`），以及 `failed` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`contract_not_found`——没有这个合约、`not_contract_deployer`、`watch_only_no_signer`、`ledger_unsupported`、`auth_failed`） · `2` 用法错误（`invalid_value`——地址格式非法）。

## 另请参见

[`contract info`](info.md) · [`contract deploy`](deploy.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
