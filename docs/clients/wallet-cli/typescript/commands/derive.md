# wallet-cli derive

从种子钱包派生下一个 HD 账户（通过 --seed-id 指定）。

## 用法

```
wallet-cli derive --seed-id <wlt_…> [--index <n>] [--label <l>] [options]
```

## 选项

| 选项 | 说明 |
|---|---|
| `--seed-id <string>` | 要从中派生的 HD 钱包的 seed id——即 `list` 输出中 HD 分组的标题  [必填] |
| `--index <number>` | 显式指定 HD 账户索引；省略则使用下一个空闲索引。已存在的索引不会被重新派生——对应账户会被切换为当前账户，`status` 返回 `"existing"` |
| `--label <string>` | 新账户的标签，1–64 个字符；省略则自动生成 |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

此外还有[全局选项](index.md)。

## 注意事项

私钥账户和 Ledger 账户没有 seed，无法派生。参见[账户与 HD](../concepts/accounts-and-hd.md)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
printf '%s' "$PW" | wallet-cli derive --seed-id wlt_y8cz6xda --password-stdin
```

```console
✅ Derived sub-account "main-1"
  Account ID    wlt_y8cz6xda.1
  Index         1
  TRON address  TWCa1W6BkcXZnRGxeZZw9jh8eNgULDVGzj
  EVM address   0x2395227A93465175c6D6EAF2B9d37c2cC0BaB60c
  Active        yes
  Note          shares master mnemonic; no separate backup needed
```

```bash
printf '%s' "$PW" | wallet-cli derive --seed-id wlt_y8cz6xda --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"derive","data":{"status":"created","accountId":"wlt_y8cz6xda.1","label":"main-1","type":"seed","index":1,"active":true,"addresses":{"tron":"TWCa1W6BkcXZnRGxeZZw9jh8eNgULDVGzj","evm":"0x2395227A93465175c6D6EAF2B9d37c2cC0BaB60c"},"seedId":"wlt_y8cz6xda","derivationPath":{"tron":"m/44'/195'/1'/0/0","evm":"m/44'/60'/0'/0/1"}},"meta":{"durationMs":1013,"warnings":[]}}
```

## 输出

`data` 是新派生出的账户（始终是 HD `seed` 账户）。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | 新派生出的索引为 `"created"`；`--index` 指到该钱包已有的索引时为 `"existing"`——这种情况下只是把该账户重新设为当前账户，不会派生任何新密钥 |
| `accountId` | string | 稳定 id `<seedId>.<index>` |
| `label` | string | 账户标签（默认为 `<wallet-name>-<index>`，例如 `main-1`） |
| `type` | string | 始终为 `"seed"` |
| `index` | number | HD 派生索引 |
| `active` | boolean | 始终为 `true`（新账户会被设为当前账户） |
| `addresses` | object | 该账户能产生的每个家族各一个地址：`tron`（base58）和 `evm`（`0x`，EIP-55 校验和格式） |
| `derivationPath` | object | 每个地址各自来自的 BIP44 路径：`{"tron":"m/44'/195'/<index>'/0/0","evm":"m/44'/60'/0'/0/<index>"}` |
| `seedId` | string | 所属种子钱包 id |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`create`](create.md) · [`list`](list.md)
