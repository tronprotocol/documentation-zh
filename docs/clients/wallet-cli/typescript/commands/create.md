# wallet-cli create

创建新的 HD 钱包（BIP39 种子）。

## 用法

```
wallet-cli create [options]
```

## 说明

生成一个新的 BIP39 种子，派生出 #0 号账户，用你的 master password 加密全部内容并保存在本地。助记词**不会被打印**——种子在静态存储时始终是加密的；执行 [`backup`](backup.md) 可把助记词导出到一个 `0600` 权限的文件。之后还可以用 [`derive`](derive.md) 从同一个 seed 派生更多账户。

需要 **master password**：非交互场景用 `--password-stdin` 传入，或在 TTY 提示处输入。密码至少 8 个字符，且必须包含大写字母、小写字母、数字和特殊字符（`!@#$%^&*()-_=+[]{};:,.?`）各一个；强度不足会以 `weak_password` 失败（退出码 2）。

## 选项

| 选项 | 说明 |
|---|---|
| `--label <string>` | 便于识别的唯一账户标签，1–64 个字符；省略则自动生成 |
| `--password-stdin` | 从 stdin（fd 0）读取 master password；每次运行只能有一个 `*-stdin` 选项占用 stdin |

此外还有[全局选项](index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

交互式——先提示输入 master password，然后显示新账户：

```bash
wallet-cli create --label main
```

```console
? Set master password (hidden):
? Confirm master password:
✅ Created wallet "main"
  Account ID    wlt_2dbv24de.0
  Type          HD
  TRON address  TTVdGTBXY5mmY3nJFGUp7Vo898kUJ6gtFQ
  EVM address   0x5c8e1b04A7f39d62C0B3e85A1d47F9028b6ce713
  Active        yes

⚠️ Recovery phrase is encrypted locally and was not printed.
⚠️ Run `backup` soon and store the file offline.
```

非交互式（密码通过管道从 stdin 传入）：

```bash
printf '%s' "$PW" | wallet-cli create --label main --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"create","data":{"status":"created","accountId":"wlt_2dbv24de.0","label":"main","type":"seed","index":0,"active":true,"addresses":{"tron":"TTVdGTBXY5mmY3nJFGUp7Vo898kUJ6gtFQ","evm":"0x5c8e1b04A7f39d62C0B3e85A1d47F9028b6ce713"},"seedId":"wlt_2dbv24de","derivationPath":{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"}},"meta":{"durationMs":38,"warnings":[]}}
```

## 输出

`data` 描述所创建的账户（本地命令——没有 `chain` 块）。返回结果中永远不会包含助记词字段。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | `"created"` |
| `accountId` | string | 稳定 id `<seedId>.<index>` |
| `label` | string | 账户标签 |
| `type` | string | `"seed"`（HD 派生） |
| `index` | number | HD 派生索引（首个账户为 0） |
| `active` | boolean | 是否成为了当前账户 |
| `addresses` | object | 该账户能产生的每个家族各一个地址：`tron`（base58）和 `evm`（`0x`，EIP-55 校验和格式） |
| `derivationPath` | object | 每个地址各自来自的 BIP44 路径：`{"tron":"m/44'/195'/<index>'/0/0","evm":"m/44'/60'/0'/0/<index>"}` |
| `seedId` | string | 所属种子钱包 id |

## 退出码

`0` 创建成功 · `1` 执行失败 · `2` 用法错误（例如标签已被占用 / 非法，或 `weak_password`）。参见 [machine-interface](../machine-interface.md#exit-codes)。

## 另请参见

[`import mnemonic`](import/mnemonic.md) · [`list`](list.md) · [`derive`](derive.md) · [`backup`](backup.md) · [快速上手](../guide/getting-started.md)
