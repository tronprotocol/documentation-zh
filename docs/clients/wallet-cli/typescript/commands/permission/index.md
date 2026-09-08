# wallet-cli permission

查看和更新账户权限——TRON 多签的基础。

`show` 用于只读查看当前权限，建议在修改前执行；`update` 通过一笔链上交易替换整个权限结构，并燃烧
100 TRX。

**仅限 TRON。** 多密钥权限模型是 TRON 的协议特性；本组两条子命令在 EVM 网络上都会以 `family_mismatch` 失败。

## 用法

```
wallet-cli permission COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `permission show` | [show.md](show.md) | 显示账户的权限结构 |
| `permission update` | [update.md](update.md) | 替换账户的权限结构（燃烧 100 TRX） |

## 权限模型 {#the-permission-model}

每个 TRON 账户都有：

- **一个 owner 权限**（id `0`）——完全控制权，包括修改权限本身的能力；
- **最多 8 个 active 权限**（id `2`–`9`）——每个都限定了它可以执行的一组操作类型；
- **一个 witness 权限**（id `1`）——仅超级代表使用，用于出块签名。

每个权限组最多可包含 **5 个密钥**（地址及权重）和一个**阈值**。当交易的签名权重之和**≥ 阈值**时，
该交易才满足此权限组的授权条件。典型配置是使用多密钥阈值保护 owner 组，并通过限制了操作范围的
active 组执行日常操作。

> ⚠️ **owner 权限配置错误会导致账户永久无法操作。** 如果新的 owner 密钥中不含任何你能签名的地址，或者你持有的密钥权重未达到阈值，交易仍可能成功，而且链上没有任何补救手段。`permission update` 会以警告形式提示此风险，但**不会**阻止提交。警告码有：`owner_lockout`（本地密钥在 owner 组中没有任何权重）、`owner_lockout_partial`（权重低于阈值，因此必须有联署人）、`active_can_update_permission`（某个 active 组可以改写权限本身）和 `active_unknown_operations`（某个组设置了当前版本无法识别的操作位）。

## 另请参见

[`permission show`](show.md) · [`permission update`](update.md) · [`tx sign`](../tx/sign.md) · [安全](../../concepts/security.md)
