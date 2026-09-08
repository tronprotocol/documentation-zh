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

- **原生格式**（默认）——钱包自有的备份 JSON。种子账户导出的是助记词，因此整个 seed 会随之迁移。
- **`--keystore`**——标准的 Web3 keystore JSON，可被 TronLink 等钱包导入，用**你的 master password** 加密。keystore 只保存**单个私钥**：HD 账户仅导出当前派生出的那把密钥，该密钥到了别处只是一个独立账户，无法再从中派生出任何东西。要迁移整个 seed，请使用原生格式。

**每个 keystore 只保存一个链家族的密钥。** 种子账户会为 TRON（coin type 195）和 EVM（coin type 60）派生不同密钥，而单个 keystore 只能保存其中一把，因此由 `--network` 决定导出哪个家族；省略时使用 `config.defaultNetwork`。回执和导出日志都会记录实际导出的家族。私钥账户本身只有一把密钥，因此忽略该选择；原生备份一次覆盖全部家族，无需选择，也不会报告家族。

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
| `<account>` | 要导出的账户，可用 accountId、标签或地址指定。除非使用 `--records`，否则必填；**配合** `--records` 时它转为过滤日志，作用同 `--account` |
| `--keystore` | 导出为标准 Web3 keystore，而不是原生格式 |
| `--out <path>` | 输出文件路径；模式 0600，绝不覆盖（默认：当前目录，见上文） |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |
| `--network <id>` | 配合 `--keystore` 使用，决定导出哪个家族的密钥（`tron:3448148188` → TRON 密钥，`eip155:1` → EVM 密钥）。不会访问任何节点 |

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

以原生格式导出种子账户——导出的是助记词：

```bash
printf '%s' "$PW" | wallet-cli backup main --password-stdin
```

```console
⚠️ Backup written /home/you/wlt_d1qbj2fb.0-1783751611076.json
  Account ID  wlt_d1qbj2fb.0
  Secret      recovery phrase
  File mode   0600
  Bytes       277

⚠️ Secret material was written only to the backup file, never to stdout.
```

改为导出 keystore——单个私钥：

```bash
printf '%s' "$PW" | wallet-cli backup main --keystore --password-stdin
```

```console
⚠️ Keystore written /home/you/wlt_d1qbj2fb.0-1785930000.keystore.json
  Account ID  wlt_d1qbj2fb.0
  Family      tron
  Secret      private key
  File mode   0600
  Bytes       491

⚠️ Secret material was written only to the keystore file, never to stdout.
```

```bash
printf '%s' "$PW" | wallet-cli backup main --keystore --out ./main.keystore.json --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"backup","data":{"accountId":"wlt_d1qbj2fb.0","label":"main","type":"seed","index":0,"active":true,"addresses":{"tron":"TQkXm4vN...5Zt7Uw","evm":"0x86B3D0f2...f4106"},"seedId":"wlt_d1qbj2fb","derivationPath":{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"},"family":"tron","secretType":"privateKey","format":"keystore","out":"/home/you/main.keystore.json","fileMode":"0600","bytes":491},"meta":{"durationMs":1420,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

审计日志：

```bash
wallet-cli backup --records --limit 3
```

```console
Backup records (showing 3 of 12)
| Time (UTC)       | Exported account         | Operation         | File                                              |
| ---------------- | ------------------------ | ----------------- | ------------------------------------------------- |
| 2026-08-05 11:40 | TQkXm4vN...5Zt7Uw (main) | backup --keystore | /home/you/wlt_d1qbj2fb.0-1785930000.keystore.json |
| 2026-08-04 09:12 | TQkXm4vN...5Zt7Uw (main) | backup            | /home/you/wlt_d1qbj2fb.0-1785834720.json          |
| 2026-07-30 22:03 | TBeta9mR...8pLx          | backup            | /home/you/tbeta-seed.json                         |
```

```bash
wallet-cli backup --records --limit 3 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"backup.records","data":{"records":[{"operation":"backup --keystore","accountId":"wlt_d1qbj2fb.0","account":"TQkXm4vN...5Zt7Uw","family":"tron","label":"main","out":"/home/you/wlt_d1qbj2fb.0-1785930000.keystore.json","timestamp":"2026-08-05T11:40:00Z"},{"operation":"backup","accountId":"wlt_d1qbj2fb.0","account":"TQkXm4vN...5Zt7Uw","label":"main","out":"/home/you/wlt_d1qbj2fb.0-1785834720.json","timestamp":"2026-08-04T09:12:00Z"},{"operation":"backup","accountId":"wlt_9x3k2m7p.0","account":"TBeta9mR...8pLx","label":null,"out":"/home/you/tbeta-seed.json","timestamp":"2026-07-30T22:03:00Z"}]},"meta":{"durationMs":8,"warnings":[],"pagination":{"offset":0,"limit":3,"total":12}},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

## 输出

两种用法都在本地执行、不访问任何节点，但 `backup` 带有一个可选的网络显示选择器：所选网络（或默认网络）决定 `--keystore` 导出哪个家族。因此结果中包含 `chain` 块，`--records` 时也一样。两种用法的 `command` id 不同：导出为 `backup`，日志为 `backup.records`。

导出时的 `data` 是账户信息加上文件详情：

| 字段 | 类型 | 含义 |
|---|---|---|
| `accountId` | string | 账户 id |
| `label` | string | 账户标签 |
| `type` | string | 账户类型（可导出的类型：`seed` / `privateKey`） |
| `index` | number \| null | HD 派生索引；私钥账户为 `null` |
| `active` | boolean | 是否为当前账户 |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron` 和/或 `evm` |
| `derivationPath` | object \| null | `seed` 账户按家族给出的 BIP44 路径；`privateKey` 为 `null` |
| `family` | string | 使用 `--keystore` 时，实际写出的是哪个家族的密钥；原生备份覆盖全部家族，因此不含该字段 |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `secretType` | string | 导出的密钥种类——`mnemonic`，使用 `--keystore` 时为 `privateKey` |
| `format` | string | 使用了 `--keystore` 时为 `keystore` |
| `out` | string | 写入的**绝对**路径——相对的 `--out` 会先按工作目录解析，再据此报告 |
| `fileMode` | string | 文件权限，始终为 `0600` |
| `bytes` | number | 文件大小（字节） |

`--records` 时的 `data.records[]`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `operation` | string | `backup` 或 `backup --keystore` |
| `accountId` / `account` / `label` | string \| null | 密钥被导出的账户；未设置标签时 `label` 为 `null` |
| `out` | string | 密钥写入的文件，以**绝对**路径给出 |
| `timestamp` | string | 导出时间，UTC |

`meta.pagination` 包含 `offset`、`limit`（`null` = 不限）和 `total`。

## 退出码

`0` 成功 · `1` 执行失败（`account_not_found`——账户不存在；`not_exportable`——仅观察或 Ledger 账户；`auth_failed`；`io_error`——路径不可写）· `2` 用法错误（`output_exists`——目标文件已存在，且绝不覆盖；`invalid_value`——不带 `--records` 使用了记录过滤选项、`--keystore` / `--out` 与 `--records` 同用，或时间 / limit / offset 取值非法）。

## 另请参见

[安全模型](../concepts/security.md) · [`import keystore`](import/keystore.md) · [`delete`](delete.md)
