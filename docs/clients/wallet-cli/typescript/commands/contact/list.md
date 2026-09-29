# wallet-cli contact list

列出联系人簿中的全部收款方。

## 用法

```
wallet-cli contact list
```

## 说明

列出本地地址簿中的每一个收款方——名称、完整地址和备注。地址簿为空时返回空列表（而不是报错）。纯本地操作，不访问节点。

## 选项

仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli contact list
```

```console
| Name  | Address                            | Note          |
| ----- | ---------------------------------- | ------------- |
| alice | TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c | Alice mainnet |
| bob   | TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP | —             |
```

```bash
wallet-cli contact list -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contact.list","data":{"contacts":[{"name":"alice","address":"TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c","note":"Alice mainnet"},{"name":"bob","address":"TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP","note":null}]},"meta":{"durationMs":3,"warnings":[]}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `contacts[]` | array | 收款方列表，每项为 `{name, address, note}`——未设置备注时 `note` 为 `null` |

## 退出码

`0` 成功（包括空列表） · `1` 执行失败（`encoding_error`、`insecure_permissions`——地址簿是符号链接或对同组/其他用户可读，请 `chmod 600`） · `2` 用法错误。

## 另请参见

[`contact add`](add.md) · [`contact remove`](remove.md) · [`tx send`](../tx/send.md)
