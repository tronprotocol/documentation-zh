# wallet-cli contact add

向地址簿中添加一个收款方。

## 用法

```
wallet-cli contact add <name> <address> [--note <text>]
```

## 说明

把一个收款方（名称 → 地址）保存到本地地址簿。之后凡是需要填收款方的地方都可以使用这个名称——[`tx send --to`](../tx/send.md) 和 [`gasfree transfer --to`](../gasfree/transfer.md)。地址会在本地按它所属的链家族做校验（`T…` = TRON，`0x…` = EVM），这个家族也会记录在该条目上；不访问节点。

一个联系人只属于**一个链家族**，直接由它的地址推断得出；本命令没有家族或网络选择器。地址格式错误，或不属于任何受支持的家族，都会以 `invalid_address` 被拒绝。家族是否匹配，要等到链上命令实际使用该联系人时才检查。

名称必须由 1–64 个安全字符组成（不含控制字符或格式字符），且不能与地址格式相似。该检测会有意扩大匹配范围，包括校验和错误一个字符或粘贴时被截断的地址，从而避免错误地址被当作联系人名称解析，并将资金发送给同名联系人。比较名称时，CLI 会先执行 Unicode NFKC 归一化，再忽略大小写。

## 选项

| 选项 | 说明 |
|---|---|
| `--note <text>` | 自由格式备注（例如“交易所充值地址”），最多 128 个安全字符 |

此外还有[全局选项](../index.md#global-options-every-command)。 `name` 和 `address` 是位置参数。

## 示例

```bash
wallet-cli contact add alice TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub --note "Alice mainnet"
```

```console
✅ Contact added
  Name     alice
  Address  TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Note     Alice mainnet
```

EVM 地址的登记方式完全相同。链家族只在内部用于路由，不会出现在对外的联系人对象里：

```bash
wallet-cli contact add alice-eth 0x742d35Cc6634C0532925a3b844Bc454e4438f44e --note "Alice mainnet"
```

```bash
wallet-cli contact add alice TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub --note "Alice mainnet" -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contact.add","data":{"name":"alice","address":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","note":"Alice mainnet"},"meta":{"durationMs":4,"warnings":[]}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | string | 联系人名称 |
| `address` | string | 收款方地址 |
| `note` | string \| null | 备注，未设置时为 `null` |

## 退出码

`0` 成功 · `1` 执行失败（`encoding_error`——本地地址簿无法解码；`insecure_permissions`——它是符号链接或对同组/其他用户可读，请执行 `chmod 600`） · `2` 用法错误（`already_exists`——名称或地址已被占用；`limit_exceeded`——地址簿已满；`invalid_address`——该地址对任何受支持的家族都不合法；`invalid_value`——名称或备注不合法）。

## 另请参见

[`contact list`](list.md) · [`contact remove`](remove.md) · [`tx send`](../tx/send.md)
