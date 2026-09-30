# wallet-cli delete

删除钱包/账户，并清理失效的标签。

## 用法

```
wallet-cli delete <account> [--yes] [options]
```

## 参数

- `account`——要删除的账户或钱包，可用 accountId、标签或地址指定

## 选项

| 选项 | 说明 |
|---|---|
| `--yes` | 跳过交互式确认；在非 TTY 环境下删除时必须使用 |

此外还有[全局选项](index.md)。

## 注意事项

删除 HD 钱包会从种子根开始级联——全部派生账户都会一并删除。链上资产不受影响。请先执行 [`backup`](backup.md)，并按它打印的任何警告处理。仅涉及元数据——不需要 master password。

**从含有 TRON 子账户（索引 1 或更高）的 HD 钱包中删除**时，总会在确认之前先打印一条警告。在没有密码的情况下，`delete` 无法判断这些地址是由哪条派生路径生成的；如果它们来自更早的版本，重新导入助记词并不能把它们重建出来。请先备份并核验它们的密钥——参见[出现 `legacy_derivation` 后如何找回地址](../troubleshooting/legacy-derivation-recovery.md)。该警告不会阻止删除。

## 示例

删除 HD 子账户只会移除该账户并保留种子，因此之后还可以再 `derive` 回来。由于该钱包存在 TRON 子账户，会先打印旧派生路径的警告：

```bash
wallet-cli delete main-2 --yes
```

```console
warning: This HD wallet contains TRON sub-accounts. If created with an older derivation path, default mnemonic recovery may not recreate them. Back up and verify their keys before deleting. https://github.com/tronprotocol/wallet-cli/blob/wallet-cli-4.13.1/ts/docs/troubleshooting/legacy-derivation-recovery.md
✅ Deleted account wlt_kwyjcwdh.2
  Secret removed  no
  New active      wlt_kwyjcwdh.0
```

```bash
wallet-cli delete main-2 --yes -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"delete","data":{"accountId":"wlt_kwyjcwdh.2","scope":"account","secretRemoved":false,"newActive":"wlt_kwyjcwdh.0"},"meta":{"durationMs":26,"warnings":["This HD wallet contains TRON sub-accounts. If created with an older derivation path, default mnemonic recovery may not recreate them. Back up and verify their keys before deleting. https://github.com/tronprotocol/wallet-cli/blob/wallet-cli-4.13.1/ts/docs/troubleshooting/legacy-derivation-recovery.md"]}}
```

删除钱包的根账户会移除整个钱包——包括全部派生账户和种子：

```bash
wallet-cli delete main --yes
```

```console
warning: This HD wallet contains TRON sub-accounts. If created with an older derivation path, default mnemonic recovery may not recreate them. Back up and verify their keys before deleting. https://github.com/tronprotocol/wallet-cli/blob/wallet-cli-4.13.1/ts/docs/troubleshooting/legacy-derivation-recovery.md
✅ Deleted wallet wlt_kwyjcwdh
  Secret removed  yes
  New active      wlt_h10w1nm0
```

```bash
wallet-cli delete main --yes -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"delete","data":{"accountId":"wlt_kwyjcwdh","scope":"wallet","secretRemoved":true,"newActive":"wlt_h10w1nm0"},"meta":{"durationMs":53,"warnings":["This HD wallet contains TRON sub-accounts. If created with an older derivation path, default mnemonic recovery may not recreate them. Back up and verify their keys before deleting. https://github.com/tronprotocol/wallet-cli/blob/wallet-cli-4.13.1/ts/docs/troubleshooting/legacy-derivation-recovery.md"]}}
```

不加 `--yes` 时，命令会要求你输入该账户的标签以确认，并且需要交互式终端。

## 输出

`data` 描述删除结果。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `accountId` | string | 被删除的账户/钱包 id（子账户为 `wlt_….N`，整个钱包则为钱包 id `wlt_…`） |
| `scope` | string | `account`（仅该账户）或 `wallet`（级联删除整个钱包） |
| `secretRemoved` | boolean | 是否移除了加密的密钥材料。删除 HD 子账户会保留 seed，因此为 `false`。删除钱包时，它报告的是该钱包本身是否持有密钥：seed 钱包和私钥钱包为 `true`，Ledger 和仅观察钱包从未保存过密钥，因此为 `false` |
| `newActive` | string \| null | 删除后新的当前账户 id；若已无剩余账户则为 `null` |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`backup`](backup.md) · [账户与 HD](../concepts/accounts-and-hd.md)
