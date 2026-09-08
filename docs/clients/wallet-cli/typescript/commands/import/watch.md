# wallet-cli import watch

注册一个仅观察地址。不保存任何密钥。

## 用法

```
wallet-cli import watch --address <address> [--label <l>] [options]
```

## 选项

| 选项 | 说明 |
|---|---|
| `--address <string>` | **必填。** 要跟踪的仅观察地址——TRON base58（`T…`）或 EVM 十六进制（`0x…`）；链家族由地址本身识别 |
| `--label <string>` | 唯一的账户标签，1-64 个字符 |

此外还有[全局选项](../index.md)。

## 注意事项

无法签名——只能查询。适合监控冷存储余额。

仅观察账户属于**单一链家族**：它只记录导入时提供的地址，因此只会出现在该家族的网络中，也只能用于该家族。如需同时观察同一钱包在另一个家族中的地址，请将该地址另行导入。

## 示例

```bash
wallet-cli import watch --address TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --label cold
```

```console
✅ Added watch-only account "cold"
  TRON address  TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
  Note          read-only; signing operations will be rejected
```

EVM 地址的注册方式完全相同，会成为一个 `evm` 账户：

```bash
wallet-cli import watch --address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e --label cold-evm
```

```bash
wallet-cli import watch --address TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --label cold -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"import.watch","data":{"status":"created","accountId":"wlt_jsyq8fxe","label":"cold","type":"watch","index":null,"active":false,"addresses":{"tron":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ"},"family":"tron"},"meta":{"durationMs":36,"warnings":[]}}
```

## 输出

`data` 携带新注册的仅观察账户——只有地址，不含任何密钥。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | `"created"`；若同一个观察地址此前已注册过，则为 `"existing"` |
| `accountId` | string | 稳定的账户 id |
| `label` | string | 账户标签 |
| `type` | string | `"watch"`（只读，无法签名） |
| `index` | number \| null | 非 HD 账户，恒为 `null` |
| `active` | boolean | 该账户是否已经是当前账户。注册仅观察账户并不会自动选中它；请显式使用 [`use`](../use.md) |
| `addresses` | object | 唯一的那个地址，以其家族为键——`{"tron":"T…"}` 或 `{"evm":"0x…"}` |
| `family` | string | 由地址识别出的链家族——`tron` 或 `evm` |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../../machine-interface.md)。

## 另请参见

[`import ledger`](ledger.md) · [`account balance`](../account/balance.md)
