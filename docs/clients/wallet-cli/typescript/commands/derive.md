# wallet-cli derive

从种子钱包派生下一个 HD 账户。

## 用法

```
wallet-cli derive [--seed-id <wlt_…>] [--account <account>] [--index <n>] [--label <l>] [options]
```

## 选项

| 选项 | 说明 |
|---|---|
| `--seed-id <string>` | 要从中派生的 HD 钱包的 seed id——即 `list` 中 HD 分组的标题。与 `--account` 同时给出时以它为准 |
| `--account <string>` | 该 HD 钱包中任意一个账户的 accountId、标签或地址；默认取当前账户 |
| `--index <number>` | 显式指定 HD 账户索引；省略则使用下一个空闲索引。已存在的索引不会被重新派生——该账户会被设为当前账户，`status` 返回 `"existing"`，文本输出的标题也变成 `Selected existing account` 而不是 `Derived sub-account` |
| `--label <string>` | 新账户的标签，1-64 个字符；省略则自动生成 |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

此外还有[全局选项](index.md)。

## 注意事项

不给 `--seed-id` 或 `--account` 时，`derive` 使用当前账户所属的种子。用该钱包的任意一个账户都能选中它，不限于索引 0。

每个新账户在 TRON 上取 `m/44'/195'/0'/0/<index>`，在 EVM 上取 `m/44'/60'/0'/0/<index>`。

私钥账户、Ledger 账户和仅观察账户没有种子，无法派生；选中它们会以 `seed_not_found` 失败（退出码 2）。参见[账户与 HD 钱包](../concepts/accounts-and-hd.md)。

4.13.1 之前创建的钱包，其 TRON 账户可能位于旧路径上。从这类钱包派生新账户会以 `legacy_derivation` 失败。用 `--index` 指名其中已有的账户仍然可行——它会被设为当前账户，并给出一条警告。参见[出现 `legacy_derivation` 后如何找回地址](../troubleshooting/legacy-derivation-recovery.md)。

如果存储的某个地址与种子对不上，`derive` 会以 `derivation_mismatch` 失败。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

从当前账户所属钱包派生下一个账户：

```bash
printf '%s' "$PW" | wallet-cli derive --password-stdin
```

```console
✅ Derived sub-account "main-1"
  Account ID    wlt_kwyjcwdh.1
  Index         1
  TRON address  TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ
  EVM address   0xEA4A61822322c695F5A9eB7920b843054CbDaA83
  Active        yes
  Note          shares the wallet's recovery phrase
```

```bash
printf '%s' "$PW" | wallet-cli derive --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"derive","data":{"status":"created","accountId":"wlt_kwyjcwdh.1","label":"main-1","type":"seed","index":1,"active":true,"addresses":{"tron":"TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ","evm":"0xEA4A61822322c695F5A9eB7920b843054CbDaA83"},"seedId":"wlt_kwyjcwdh","derivationPath":{"tron":"m/44'/195'/0'/0/1","evm":"m/44'/60'/0'/0/1"}},"meta":{"durationMs":1784,"warnings":[]}}
```

要从另一个钱包派生，用 `--account` 指定它的任意一个账户，或用 `--seed-id` 指定它的种子。

## 输出

`data` 是派生出的账户（必定是 HD 的 `seed` 账户）。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | 新派生出的索引为 `"created"`；`--index` 指向该钱包已有的索引时为 `"existing"`——此时只是把该账户重新设为当前账户，不会派生新密钥 |
| `accountId` | string | 稳定的 id，形如 `<seedId>.<index>` |
| `label` | string | 账户标签（默认为 `<钱包名>-<索引>`，例如 `main-1`） |
| `type` | string | 恒为 `"seed"` |
| `index` | number | HD 派生索引 |
| `active` | boolean | 恒为 `true`（该账户会被设为当前账户） |
| `addresses` | object | 该账户能产生的每个家族各一个地址：`tron`（base58）和 `evm`（`0x`，EIP-55 校验和格式） |
| `derivationPath` | object | 每个地址经过校验的路径。新账户为 `{"tron":"m/44'/195'/0'/0/<index>","evm":"m/44'/60'/0'/0/<index>"}`；`"existing"` 的账户则报告它实际使用的路径，那可能是旧的 TRON 路径 |
| `seedId` | string | 所属种子钱包 id |

## 退出码

`0` 成功 · `1` 执行失败，含 `legacy_derivation` 和 `derivation_mismatch` · `2` 用法错误，含 `seed_not_found`。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`create`](create.md) · [`list`](list.md) · [账户与 HD 钱包](../concepts/accounts-and-hd.md)
