# wallet-cli rename

重命名账户标签。

## 用法

```
wallet-cli rename <account> --label <new> [options]
```

## 参数

- `account`——要重命名的账户，可用 accountId、当前标签或地址指定

## 选项

| 选项 | 说明 |
|---|---|
| `--label <string>` | 新的唯一标签，1–64 个字符  [必填] |

此外还有[全局选项](index.md)。

## 注意事项

稳定的引用句柄始终是 `accountId`，改变的只是标签。该操作只涉及元数据——不需要 master password。

## 示例

```bash
wallet-cli rename main-1 --label hot-hd
```

```console
✅ Renamed account
  Old label  main-1
  New label  hot-hd
```

```bash
wallet-cli rename main-1 --label hot-hd -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"rename","data":{"previousLabel":"main-1","accountId":"wlt_kwyjcwdh.1","label":"hot-hd","type":"seed","index":1,"active":true,"addresses":{"tron":"TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ","evm":"0xEA4A61822322c695F5A9eB7920b843054CbDaA83"},"seedId":"wlt_kwyjcwdh","derivationPath":null},"meta":{"durationMs":26,"warnings":[]}}
```

## 输出

`data` 是重命名后的账户，外加 `previousLabel`。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `previousLabel` | string | 重命名前的旧标签 |
| `accountId` | string | 稳定的账户 id (unchanged by rename) |
| `label` | string | 新标签 |
| `type` | string | `seed` / `privateKey` / `watch` / `ledger` |
| `index` | number \| null | HD 派生索引；非 HD 账户为 `null` |
| `active` | boolean | 是否为当前账户 |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `derivationPath` | null | 恒为 `null`，这是刻意为之——`rename` 不接收 master password，因此在不打开种子的情况下无法分辨旧 TRON 路径与当前路径；`derive` 和 `backup` 会报告经过校验的路径 |
| `family` | string | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）有此字段 |
| `path` | string | 该账户在设备上的派生路径（仅 `ledger` 账户） |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`list`](list.md) · [`use`](use.md)
