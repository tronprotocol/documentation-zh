# wallet-cli backup

将账户的密钥导出到一个 0600 权限的文件，或查看历史导出记录。

## 用法

```
wallet-cli backup <account> [--keystore] [--out <path>] [--password-stdin] [options]
wallet-cli backup --records [<account>] [--from <datetime>] [--to <datetime>] [--limit <n>] [--offset <n>] [--account <ref>] [options]
```

## 说明

指定账户时，`backup` 会把该账户的密钥材料和元数据写入权限为 **0600** 的新文件，并且不会覆盖已有
文件。密钥只写入文件，不会输出到 stdout。仅观察账户和 Ledger 账户没有可导出的密钥，会返回
`not_exportable`；CLI 会先完成这项检查，再决定是否要求输入密码。

两种格式：

- **原生格式**——钱包自有的备份 JSON。种子账户导出的是它的助记词，因此整份种子会随之迁移。
- **`--keystore`**——标准的 Web3 keystore JSON，可被 TronLink 等导入，使用**你的 master password** 加密。keystore 只装**一把私钥**：HD 账户导出的只是它当前派生出的那把密钥，该密钥到了别处会成为一个独立账户，无法再从中派生任何东西。要迁移整份种子，请用原生格式。

不加 `--keystore` 时，在完全交互式的终端里会先询问要写出哪种格式，然后才提示输入密码：

```console
? Backup format (Up/Down, Enter)
> Native wallet backup (recovery phrase for the whole HD wallet)
  Web3 keystore (single TRON private key)
```

当密码来自 `--password-stdin`、或本次运行本来就是非交互式时，不会有任何询问，直接写出原生格式。

对 4.13.1 之前创建的钱包做原生备份时，可能会打印一条警告：它的部分 TRON 账户使用的是旧路径，导入助记词并不能把它们找回来。警告会逐个点名这些账户，并给出保存其密钥的 `--keystore` 命令。请在删除该钱包之前执行这些命令——参见[出现 `legacy_derivation` 后如何找回地址](../troubleshooting/legacy-derivation-recovery.md)。

一份种子在每个链家族下派生出不同的密钥，而 keystore 只装其中一把，因此由 `--network` 决定写出哪个家族的密钥——省略时回落到 `config.defaultNetwork`。回执中会写明它导出的是哪个家族，导出日志里也会记录。私钥账户只有一把密钥，会忽略该选择；原生格式则一次覆盖全部家族，因此既不需要选择，也不会报告家族。

默认情况下**文件写入当前工作目录**——`./<accountId>-<timestamp>.json`，使用 `--keystore` 时则为 `./<accountId>-<timestamp>.keystore.json`。`--out` 可覆盖该路径。

> 命令执行后，当前工作目录中会出现包含私钥或助记词的文件。不要在共享目录或 Git 仓库中执行该命令。
> CLI 只保证文件权限为 0600 且不覆盖已有文件，不会检查目录是否安全或是否受版本控制。请立即将导出
> 文件转移到安全存储位置，并按照私钥文件的安全等级进行保护。参见[安全](../concepts/security.md)。

使用 `--records` 且不指定账户时不会导出任何内容：命令转而列出**本地的历史导出审计日志**。每次 `backup` 和 `backup --keystore` 各占一行，最新的在前，记录了哪个账户的密钥被导出、何时导出，以及**导出到了哪个文件**。导入操作不记录——该日志的目的是留下密钥外流的痕迹。它保留最近 1000 条记录，超出部分丢弃最旧的。`Exported account` 是密钥被导出的那个账户，`--account` 即按它过滤。

**两种用法不能混用，CLI 会在两个方向上强制这一点：**

- `--keystore` 和 `--out` 描述的是导出行为，因此把其中任何一个与 `--records` 组合都会失败，而不是被静默忽略。
- `--from` / `--to` / `--limit` / `--offset` 用于过滤日志，因此**不带** `--records` 使用其中任何一个同样会失败。

两者都是退出码 `2` 的 `invalid_value`，错误信息会指明出问题的选项——例如 `invalid --offset: --offset filters the export log; it needs --records`。

位置参数 account 是个例外：它在两种用法下含义不同，而不是与 `--records` 冲突。`backup main` 导出 `main` 的密钥；`backup main --records` 列出 `main` 的历史导出记录，与 `--account main` 效果完全一致。

## 选项

| 选项 | 说明 |
|---|---|
| `<account>` | 要导出的账户，可用 accountId、标签或地址指定。除非使用 `--records`，否则必填；**配合** `--records` 时，它转而起到筛选日志的作用，用法同 `--account` |
| `--keystore` | 导出为标准 Web3 keystore，而不是原生格式。在交互式终端中省略它，会弹出选择提示 |
| `--out <path>` | 输出文件路径；权限 0600，绝不覆盖（默认写入当前目录，见上文） |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

使用 `--records` 时（不再指定账户）：

| 选项 | 说明 |
|---|---|
| `--records` | 列出历史导出记录，而不是执行导出 |
| `--from <datetime>` | 只返回该时间点及之后的记录，格式 `YYYY-MM-DD[ HH:mm:ss]`，UTC |
| `--to <datetime>` | 只返回该时间点及之前的记录，格式同上 |
| `--limit <number>` | 最多返回的记录数（默认：全部） |
| `--offset <number>` | 分页偏移（默认 `0`） |
| `--account <ref>` | 只看该账户的导出记录，可用 accountId / 标签 / 地址指定 |

此外还有[全局选项](index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

种子账户的原生导出——即助记词，写入当前工作目录：

```bash
printf '%s' "$PW" | wallet-cli backup main --password-stdin
```

```console
⚠️ Backup written /home/you/wlt_kwyjcwdh.0-1789571843395.json
  Account ID  wlt_kwyjcwdh.0
  Secret      recovery phrase
  File mode   0600
  Bytes       325

⚠️ Secret material was written only to the backup file, never to stdout.
```

```bash
printf '%s' "$PW" | wallet-cli backup main --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"backup","data":{"accountId":"wlt_kwyjcwdh.0","label":"main","type":"seed","index":0,"active":true,"addresses":{"tron":"TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa","evm":"0xeb0a0D15e3B8f6E2FC4bc011Eb6644f1ce3E4fa2"},"seedId":"wlt_kwyjcwdh","derivationPath":{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"},"secretType":"mnemonic","format":"native","out":"/home/you/wlt_kwyjcwdh.0-1789571843395.json","fileMode":"0600","bytes":325},"meta":{"durationMs":2187,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

改为导出 keystore——只含一把私钥，这里是默认网络对应的 TRON 私钥：

```bash
printf '%s' "$PW" | wallet-cli backup main --keystore --out ./main.keystore.json --password-stdin
```

```console
⚠️ Keystore written /home/you/main.keystore.json
  Account ID  wlt_kwyjcwdh.0
  Family      tron
  Secret      private key
  File mode   0600
  Bytes       608

⚠️ Secret material was written only to the keystore file, never to stdout.
```

```bash
printf '%s' "$PW" | wallet-cli backup main --keystore --out ./main.keystore.json --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"backup","data":{"accountId":"wlt_kwyjcwdh.0","label":"main","type":"seed","index":0,"active":true,"addresses":{"tron":"TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa","evm":"0xeb0a0D15e3B8f6E2FC4bc011Eb6644f1ce3E4fa2"},"seedId":"wlt_kwyjcwdh","derivationPath":{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"},"family":"tron","secretType":"privateKey","format":"keystore","out":"/home/you/main.keystore.json","fileMode":"0600","bytes":608},"meta":{"durationMs":1858,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

历次导出的审计日志，最新的在前：

```bash
wallet-cli backup --records --limit 3
```

```console
Backup records (showing 3 of 4)
| Time (UTC)       | Exported account             | Operation         | File                                        |
| ---------------- | ---------------------------- | ----------------- | ------------------------------------------- |
| 2026-09-16 15:17 | TEKbsrcsL7...ok78dtTa (main) | backup --keystore | /home/you/main-2.keystore.json              |
| 2026-09-16 15:17 | TEKbsrcsL7...ok78dtTa (main) | backup --keystore | /home/you/main.keystore.json                |
| 2026-09-16 15:17 | TEKbsrcsL7...ok78dtTa (main) | backup            | /home/you/wlt_kwyjcwdh.0-1789571843395.json |
```

```bash
wallet-cli backup --records --limit 3 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"backup.records","data":{"records":[{"operation":"backup --keystore","accountId":"wlt_kwyjcwdh.0","account":"TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa","family":"tron","label":"main","out":"/home/you/main-2.keystore.json","timestamp":"2026-09-16T15:17:27Z"},{"operation":"backup --keystore","accountId":"wlt_kwyjcwdh.0","account":"TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa","family":"tron","label":"main","out":"/home/you/main.keystore.json","timestamp":"2026-09-16T15:17:25Z"},{"operation":"backup","accountId":"wlt_kwyjcwdh.0","account":"TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa","label":"main","out":"/home/you/wlt_kwyjcwdh.0-1789571843395.json","timestamp":"2026-09-16T15:17:23Z"}]},"meta":{"durationMs":17,"warnings":[],"pagination":{"offset":0,"limit":3,"total":4}},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

## 输出

两种形式都是本地操作、不访问节点，但 `backup` 有一个可选的网络显示选择器：所选网络或默认网络决定 `--keystore` 导出哪个家族的密钥。因此响应中带有 `chain` 块，`--records` 也不例外。两种形式的 `command` id 不同：导出为 `backup`，查日志为 `backup.records`。

导出时的 `data` 是账户信息加上文件详情：

| 字段 | 类型 | 含义 |
|---|---|---|
| `accountId` | string | 账户 id |
| `label` | string | 账户标签 |
| `type` | string | 账户类型（可导出的为 `seed` / `privateKey`） |
| `index` | number \| null | HD 派生索引；私钥账户为 `null` |
| `active` | boolean | 是否为当前账户 |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`） |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `derivationPath` | object \| null | 每个地址背后经过校验的路径，从种子读出——对旧账户来说，这里是它实际使用的 4.13.1 之前的 TRON 路径。私钥账户为 `null` |
| `family` | string | 使用 `--keystore` 时，写出的是哪个家族的密钥；原生备份没有该字段，因为它覆盖全部家族 |
| `secretType` | string | 导出的密钥种类——`mnemonic`，或使用 `--keystore` 时为 `privateKey` |
| `format` | string | `native` 或 `keystore` |
| `out` | string | 写入的**绝对**路径——相对形式的 `--out` 会先按工作目录解析，再报告出来 |
| `fileMode` | string | 文件权限，恒为 `0600` |
| `bytes` | number | 文件大小，单位字节 |

`--records` 时的 `data.records[]`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `operation` | string | `backup` 或 `backup --keystore` |
| `family` | string | 对 `backup --keystore` 而言，导出的是哪个家族的密钥；原生备份没有该字段 |
| `accountId` / `account` / `label` | string \| null | 被导出密钥的那个账户；未设置标签时 `label` 为 `null` |
| `out` | string | 密钥写入的文件，以**绝对**路径给出 |
| `timestamp` | string | 导出时间，UTC |

`meta.pagination` 包含 `offset`、`limit`（`null` = 不限）和 `total`。

## 退出码

`0` 成功 · `1` 执行失败（`not_exportable`——仅观察或 Ledger 账户；`auth_failed`；`io_error`——路径不可写） · `2` 用法错误（`account_not_found`——没有该账户；`output_exists`——目标文件已存在，且绝不会被覆盖；`invalid_value`——用了记录筛选却没加 `--records`、`--keystore` / `--out` 与 `--records` 同用，或时间 / limit / offset 取值有误）。

## 另请参见

[安全模型](../concepts/security.md) · [`import keystore`](import/keystore.md) · [`delete`](delete.md)
