# wallet-cli change-password

修改 master password（重新加密所有软件钱包的 keystore）。

## 用法

```
wallet-cli change-password [--yes]
```

## 说明

master password 用于解密**每一个软件钱包**的 keystore，因此修改它意味着：验证旧密码、设置新密码，然后原子地把每个软件 keystore 解密并重新加密。Ledger 和仅观察账户不持有密钥，不受影响。

**仅支持交互式**：旧密码、新密码和确认输入全部通过隐藏回显的 TTY 提示完成。没有 stdin 或 argv 通道——该命令一次性处理两个高价值密钥且极少运行，因此任何内容都不允许经过管道、shell 历史或进程列表。没有 TTY 时以 `tty_required` 失败。

流程：

1. **验证**——输入当前 master password；它必须能解密一个已有的 keystore（否则 `auth_failed`，不做任何改动）。
2. **设置**——输入两次新密码。不一致或不满足强度策略都会在提示处被拒绝并要求重新输入。
3. **确认**——命令会列出将被重新加密的软件钱包数量；`[y/N]`（使用 `--yes` 时跳过）。拒绝则中止，不做任何改动。
4. **原子重新加密**——对每个 keystore：用旧密码解密 → 用新密码加密 → 写入临时文件 → fsync；只有*全部*成功后，文件才会被重命名到位。任何失败都会整体回滚并报告 `io_error`——旧的 keystore 仍然有效。

## 选项

| 选项 | 说明 |
|---|---|
| `--yes` | 跳过最后的确认提示（第 3 步） |

此外还有[全局选项](index.md#global-options-every-command)。

## 示例

```bash
wallet-cli change-password
```

```console
? Master password (hidden):
? New master password (hidden):
? Confirm new password:
? Re-encrypt 3 software wallet(s) with the new password? [y/N]: y
✅ Master password changed — re-encrypted 3 software wallet(s)
  Wallets  wallet1, wallet2, imported-1
  Note     Ledger / watch-only accounts are unaffected
```

## 输出

该命令是交互式的。text 模式下，回执会列出被重新加密的软件钱包，且绝不包含任何密钥材料。JSON 模式下，`data.wallets` 给出这些钱包的标签/id，`data.count` 给出数量。本地命令——没有 `chain` 块。

## 退出码

`0` 修改成功 · `1` 执行失败（`auth_failed`；`no_software_wallet`——没有可重新加密的对象；`invalid_value`——引用到的某个加密钱包数据缺失；`io_error`——写入失败，已回滚）· `2` 用法错误（`tty_required`——没有可用于交互输入的 TTY；`invalid_value`——新密码与当前密码相同；`aborted`——确认被拒绝）。

## 另请参见

[`backup`](backup.md) · [安全模型](../concepts/security.md) · [machine-interface → 敏感信息处理](../machine-interface.md#secret-handling)
