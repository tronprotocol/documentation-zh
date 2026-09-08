# wallet-cli asset update

修改你所发行 TRC10 中的可变字段。

## 用法

```
wallet-cli asset update [--description <s>] [--url <url>]
                        [--free-net-per-account <n>] [--public-free-net <n>]
                        [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                        [--permission-id <n>] [options]
```

## 说明

本命令不接受 token 参数：它始终作用于签名账户所发行的那个 TRC10。没有发行过的账户会以 `not_an_issuer` 失败。

**永远只有四个字段可以修改**——描述、URL、每位持有人的免费带宽，以及共享的免费带宽池。供应量、精度、ICO 比率、ICO 窗口和冻结批次在发行时即固定，链上没有任何办法更改它们。

只需传入要修改的字段，但至少要指定一个。其他字段会从链上读取并保持原值，不会被意外清空。回执会
显示这四个字段更新后的值。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

Ledger 的 TRON 应用无法对 TRC10 发行类合约签名。Ledger 账户可以做试运行或构建未签名的 hex，但签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--description <s>` | 新的描述，≤ 200 字节（省略则保持不变） |
| `--url <url>` | 新的项目页面，非空，≤ 256 字节（省略则保持不变） |
| `--free-net-per-account <n>` | 每位持有人可用的免费带宽（省略则保持不变） |
| `--public-free-net <n>` | 持有人共享的免费带宽池（省略则保持不变） |
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
echo "$PW" | wallet-cli asset update --url https://mytoken.io/v2 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Asset updated
  Asset             MyToken  (id 1000123)
  Issuer            TQkXm4vN...5Zt7Uw
  Url               https://mytoken.io/v2
  Description       Demo TRC10
  Free net/account  0
  Public free net   0
  TxID              9e3...
  Block             #57,883,190
  Fee               0 TRX
  Status            success
```

```bash
echo "$PW" | wallet-cli asset update --url https://mytoken.io/v2 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"asset.update","data":{"kind":"asset-update","stage":"confirmed","txId":"9e3...","confirmed":true,"blockNumber":57883190,"feeSun":0,"netUsed":295,"netFeeSun":0,"failed":false,"assetId":"1000123","name":"MyToken","issuerAddress":"TQkXm4vN...","url":"https://mytoken.io/v2","description":"Demo TRC10","freeAssetNetLimit":0,"publicFreeAssetNetLimit":0},"meta":{"durationMs":6480,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "asset-update"`、`stage: "submitted"`、`txId`、`assetId`、`name`、`issuerAddress`，以及提交时的那四个字段 |
| `--wait`（已确认） | 以上内容，外加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、`failed` |

这四个字段是 `url`、`description`、`freeAssetNetLimit` 和 `publicFreeAssetNetLimit`——始终四个都在，包括那些原样读回、未做修改的字段。确认后的资源字段是扁平的；没有嵌套的 `resource` 对象。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`not_an_issuer`——该账户没有发行过 TRC10；`watch_only_no_signer`；`ledger_unsupported`；`auth_failed`） · `2` 用法错误（`invalid_value`——一个字段都没给，或者 URL / 描述过长；本命令没有必填参数，因此空调用报的是 `invalid_value`，而不是 `missing_option`）。

## 另请参见

[`asset issue`](issue.md) · [`asset info`](info.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
