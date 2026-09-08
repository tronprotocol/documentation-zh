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
wallet-cli rename main --label primary
```

```console
✅ Renamed account
  Old label  main
  New label  primary
```

```bash
wallet-cli rename main-1 --label hot-hd -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"rename","data":{"previousLabel":"main-1","accountId":"wlt_0y2z0gvr.1","label":"hot-hd","type":"seed","index":1,"active":true,"addresses":{"tron":"TRzaAZWRvPCcmqNETTWvmMLDi6cKwM3gbR","evm":"0x94f2e5cbb4BcA39A3F6c252217a0F30A0D23660b"},"seedId":"wlt_0y2z0gvr","derivationPath":{"tron":"m/44'/195'/1'/0/0","evm":"m/44'/60'/0'/0/1"}},"meta":{"durationMs":14,"warnings":[]}}
```

## 输出

`data` 是重命名后的账户，外加 `previousLabel`。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `previousLabel` | string | 重命名前的旧标签 |
| `accountId` | string | 稳定的账户 id（重命名不会改变它） |
| `label` | string | 新标签 |
| `type` | string | `seed` / `privateKey` / `watch` / `ledger` |
| `index` | number \| null | HD 派生索引；非 HD 账户为 `null` |
| `active` | boolean | 是否为当前账户 |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `derivationPath` | object \| null | 派生类账户按家族给出的 BIP44 路径；`watch` / `privateKey` 从未派生过，因此为 `null` |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `family` | string | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）有此字段 |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`list`](list.md) · [`use`](use.md)
