# wallet-cli contact remove

删除一个联系人。

## 用法

```
wallet-cli contact remove <name>
```

## 说明

从本地地址簿中删除一个收款方。只影响本地记录——链上不受任何影响。纯本地操作，不访问节点。

## 选项

没有命令专属选项；`name` 是位置参数，此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli contact remove bob
```

```console
✅ Contact removed
  Name     bob
  Address  TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz
```

```bash
wallet-cli contact remove bob -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contact.remove","data":{"name":"bob","address":"TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz"},"meta":{"durationMs":3,"warnings":[]}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | string | 被删除联系人的名称 |
| `address` | string | 它的地址 |

## 退出码

`0` 成功 · `1` 执行失败（`encoding_error`、`insecure_permissions`） · `2` 用法错误（`contact_not_found`——不存在该名称的联系人；`invalid_value`）。

## 另请参见

[`contact add`](add.md) · [`contact list`](list.md)
