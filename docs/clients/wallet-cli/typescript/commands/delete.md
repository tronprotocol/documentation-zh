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

删除 HD 钱包会从种子根开始级联——所有派生账户一并删除。链上资产不受影响；重新导入助记词即可恢复访问。请先做好备份。该操作只涉及元数据——不需要 master password。

## 示例

不带 `--yes` 时，删除会要求确认——你必须一字不差地输入账户标签：

```bash
wallet-cli delete solo
```

```console
? Delete solo? Type the exact label "solo" to confirm: solo
✅ Deleted wallet wlt_p7cg790g
  Secret removed  yes
```

删除 HD 根会级联到整个钱包（所有派生账户 + 密钥）：

```bash
wallet-cli delete main --yes
```

```console
✅ Deleted wallet wlt_teh9fafq
  Secret removed  yes
```

删除单个 HD 子账户只会移除该账户，保留种子密钥（之后仍可再次 `derive`）；JSON 输出会给出删除范围、密钥是否一并被移除，以及删除后的当前账户：

```bash
wallet-cli delete main-1 --yes -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"delete","data":{"accountId":"wlt_teh9fafq.1","scope":"account","secretRemoved":false,"newActive":"wlt_teh9fafq.0"},"meta":{"durationMs":14,"warnings":[]}}
```

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
