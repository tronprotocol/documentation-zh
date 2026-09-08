# wallet-cli address generate

在本地生成随机密钥对（不存入钱包）。

## 用法

```
wallet-cli address generate [--out <path>] [--print-secret]
```

## 说明

在本地生成一个随机密钥对（可离线工作），并打印它的 TRON 和 EVM 地址。私钥**不会**存入钱包，也不会进入 keystore。

默认情况下，私钥会写入权限为 `0600` 的文件，终端只显示地址和文件路径，避免密钥出现在屏幕、管道或
AI 会话中（与 [`backup`](../backup.md) 采用相同的保护方式）。使用 `--print-secret` 会改为将私钥输出到
stdout，仅适合离线抄录；此时 text 输出会附带 `!` 警告。

该命令生成的是独立私钥，适用于一次性地址、测试或导入其他系统。要创建可继续派生账户的普通 HD 钱包，请使用 [`create`](../create.md)。如需使用生成的密钥签名，请通过 [`import private-key`](../import/private-key.md) 将其导入钱包。

## 选项

| 选项 | 说明 |
|---|---|
| `--out <path>` | 写入密钥对的文件（权限 `0600`）；拒绝覆盖已存在的文件。默认：`<wallet-cli-root>/generated/keypair-<address>` |
| `--print-secret` | ⚠️ 把私钥打印到 stdout 而不是写入文件（请离线使用） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli address generate
```

```console
✅ Keypair generated (NOT stored in the wallet)
  TRON address  TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz
  EVM address   0x8a41C3b9E2d07f6A5B14c8D9e0F27a3B6c5D48E1
  Private key   written to <wallet-cli-root>/generated/keypair-TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz

! To sign with this key, import it: wallet-cli import private-key
```

私钥绝不会出现在 JSON 输出中（除非使用 `--print-secret`）：

```bash
wallet-cli address generate -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"address.generate","data":{"tron":"TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz","evm":"0x8a41C3b9E2d07f6A5B14c8D9e0F27a3B6c5D48E1","secretFile":"<wallet-cli-root>/generated/keypair-TNewAddr9k2fP7cW4bXm1sV8dRj6eL3aQz"},"meta":{"durationMs":8,"warnings":[]}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `tron` | string | TRON base58 地址 |
| `evm` | string | EVM `0x` 地址（EIP-55） |
| `secretFile` | string | 私钥写入的路径（使用 `--print-secret` 时不存在） |

## 退出码

`0` 成功 · `1` 执行失败（`io_error`；`entropy_failure`——系统 CSPRNG 不可用） · `2` 用法错误（`output_exists`——`--out` 目标已存在且绝不覆盖；`invalid_value`）。

## 另请参见

[`create`](../create.md) · [`import private-key`](../import/private-key.md) · [`encoding convert`](../encoding/convert.md)
