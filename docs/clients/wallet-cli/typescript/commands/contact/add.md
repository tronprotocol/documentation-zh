# wallet-cli contact add

把一个收款方加入联系人簿。

## 用法

```
wallet-cli contact add <name> <address> [--note <text>]
```

## 说明

把一个收款方（名称 → 地址）保存到本地地址簿。此后凡是需要收款方的地方都可以用这个名称——[`tx send --to`](../tx/send.md) 和 [`gasfree transfer --to`](../gasfree/transfer.md)。地址校验和在本地验证；不访问节点。

名称必须为 1–64 个字符，且不能长得像地址（以免与直接写在 `--to` 里的地址混淆）。

一个联系人只属于一个链家族，家族由地址本身推断——本命令没有家族或网络选择器。格式错误的地址，或不属于任何受支持家族的地址，会以 `invalid_address` 被拒绝；家族是否匹配要等到链上命令用到该联系人时才检查。

## 选项

| 选项 | 说明 |
|---|---|
| `--note <text>` | 自由格式的备注（例如「交易所充值地址」），最长 128 个字符 |

此外还有[全局选项](../index.md#global-options-every-command)。 `name` 和 `address` 是位置参数。

## 示例

```bash
wallet-cli contact add alice TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c --note "Alice mainnet"
```

```console
✅ Contact added
  Name     alice
  Address  TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c
  Note     Alice mainnet
```

```bash
wallet-cli contact add alice TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c --note "Alice mainnet" -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contact.add","data":{"name":"alice","address":"TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c","note":"Alice mainnet"},"meta":{"durationMs":4,"warnings":[]}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | string | 联系人名称 |
| `address` | string | 收款方地址 |
| `note` | string \| null | 备注，未设置时为 `null` |

## 退出码

`0` 成功 · `1` 执行失败（`encoding_error`——本地地址簿无法解码；`insecure_permissions`——它是符号链接或对同组/其他用户可读，请对其执行 `chmod 600`） · `2` 用法错误（`already_exists`——名称或地址已被占用；`limit_exceeded`——地址簿已满；`invalid_address`——该地址对任何受支持的家族都不合法；`invalid_value`——名称或备注不合法）。

## 另请参见

[`contact list`](list.md) · [`contact remove`](remove.md) · [`tx send`](../tx/send.md)
