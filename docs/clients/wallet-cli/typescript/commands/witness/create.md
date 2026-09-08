# wallet-cli witness create

将账户注册为超级代表候选人。

## 用法

```
wallet-cli witness create --url <url>
                          [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                          [--permission-id <n>] [options]
```

## 说明

把执行操作的账户注册为 SR 候选人，使其可被投票，并在得票进入前 27 名后有资格出块。它同时让该账户成为治理意义上的见证人——[`proposal create`](../proposal/create.md) 和 [`proposal approve`](../proposal/approve.md) 都要求这一身份。

**注册会燃烧一笔费用——目前约 9,999 TRX——且不可退还。** 确切金额由链参数 `getAccountUpgradeCost` 决定（[`chain params`](../chain/params.md)），请在操作前查询；回执中的 `Fee` 行会报告实际燃烧的金额。注册后无法注销。

账户必须已经激活，且余额不低于注册费。`--url` 指定候选人信息页，即区块浏览器在该 SR 旁显示的网站；这也是链上为候选人保存的唯一业务字段，之后可用 [`witness update`](update.md) 修改。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

Ledger 的 TRON 应用无法对见证人类合约签名。Ledger 账户可以做试运行或构建，但签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--url <url>` | **必填。** 候选人信息页 |
| `--dry-run` | 只构建和估算，不签名/不广播；会报告注册费；与 `--sign-only` / `--build-only` 互斥 |
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
echo "$PW" | wallet-cli witness create --url https://sr.acme.io --network tron:3448148188 --wait --password-stdin
```

```console
✅ Witness registered
  Witness  TSRmq8kP...9dEf (main)
  Url      https://sr.acme.io
  TxID     d3a...
  Block    57,881,020
  Fee      9,999 TRX  (285 bandwidth)
  Status   success
```

```bash
echo "$PW" | wallet-cli witness create --url https://sr.acme.io --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"witness.create","data":{"kind":"witness-create","stage":"confirmed","txId":"d3a...","confirmed":true,"blockNumber":57881020,"failed":false,"witnessAddress":"TSRmq8kP...","url":"https://sr.acme.io","feeSun":"9999000000","energyUsed":0,"netUsed":285,"energyFeeSun":0,"netFeeSun":0,"registrationFeeSun":"9999000000","resource":{"netUsage":285,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0}},"meta":{"durationMs":6620,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "witness-create"`、`stage: "submitted"`、`txId`、`witnessAddress`、`url`、`feeSun`，以及 `registrationFeeSun` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理命令的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`）、`failed`，以及 `registrationFeeSun` |

`registrationFeeSun` 和 `feeSun` 都是十进制字符串，表示的是同一笔不可逆的注册燃烧费。本命令有意用这个具有经济意义的金额覆盖了节点回执中的带宽/能量费用；请不要把这两个字段相加。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`already_witness`、`account_not_active`、`insufficient_balance`——余额低于注册费、`watch_only_no_signer`、`ledger_unsupported`、`auth_failed`） · `2` 用法错误（`missing_option`——未提供 `--url`）。

## 另请参见

[`witness update`](update.md) · [`witness set-brokerage`](set-brokerage.md) · [`proposal create`](../proposal/create.md) · [`chain params`](../chain/params.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
