# wallet-cli use

设置当前账户。

## 用法

```
wallet-cli use <account> [options]
```

## 参数

- `account`——要设为当前账户的 accountId、标签或地址

## 选项

仅[全局选项](index.md)。

## 示例

```bash
wallet-cli use main-1
```

```console
✅ Active account: main-1
  TRON address  TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ
  EVM address   0xEA4A61822322c695F5A9eB7920b843054CbDaA83
```

也可以用 accountId 或地址来选择：`wallet-cli use wlt_kwyjcwdh.1` / `wallet-cli use TVz38F…`。

```bash
wallet-cli use main-1 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"use","data":{"previous":"wlt_kwyjcwdh.2","accountId":"wlt_kwyjcwdh.1","label":"main-1","type":"seed","index":1,"active":true,"addresses":{"tron":"TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ","evm":"0xEA4A61822322c695F5A9eB7920b843054CbDaA83"},"seedId":"wlt_kwyjcwdh","derivationPath":null},"meta":{"durationMs":27,"warnings":[]}}
```

## 输出

`data` 是切换到的账户，外加 `previous`（切换前的当前账户）。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `previous` | string | 此前处于当前状态的账户 id |
| `accountId` | string | 现在成为当前账户的 id |
| `label` | string | 账户标签 |
| `type` | string | `seed` / `privateKey` / `watch` / `ledger` |
| `index` | number \| null | HD 派生索引；非 HD 账户为 `null` |
| `active` | boolean | 恒为 `true`（刚刚被设为当前账户） |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `derivationPath` | null | 恒为 `null`，这是刻意为之——`use` 不接收 master password，因此在不打开种子的情况下无法分辨旧 TRON 路径与当前路径；`derive` 和 `backup` 会报告经过校验的路径 |
| `family` | string | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）有此字段 |
| `path` | string | 该账户在设备上的派生路径（仅 `ledger` 账户） |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`current`](current.md) · [`list`](list.md)
