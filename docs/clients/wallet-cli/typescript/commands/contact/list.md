# wallet-cli contact list

列出全部联系人。

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
| alice | TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub | Alice mainnet |
| bob   | TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz | —             |
```

```bash
wallet-cli contact list -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contact.list","data":{"contacts":[{"name":"alice","address":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","note":"Alice mainnet"},{"name":"bob","address":"TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz","note":null}]},"meta":{"durationMs":3,"warnings":[]}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `contacts[]` | array | 收款方列表，每项为 `{name, address, note}`——`note` 未设置时为 `null`。链家族属于内部路由细节，不会返回 |

## 退出码

`0` 成功（包括空列表） · `1` 执行失败（`encoding_error`、`insecure_permissions`——地址簿是符号链接或对同组/其他用户可读，请 `chmod 600`） · `2` 用法错误。

## 另请参见

[`contact add`](add.md) · [`contact remove`](remove.md) · [`tx send`](../tx/send.md)
