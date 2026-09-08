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
  TRON address  TRs9HgTuY3dT3yDasdFdP9WQHqL37891Ax
  EVM address   0xf3ec542047Fe61E0b753a7EBca95B27a672F9cbe
```

也可以用 accountId 或地址来指定：`wallet-cli use wlt_758891fa.1` / `wallet-cli use TRs9Hg…`。

```bash
wallet-cli use main-1 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"use","data":{"previous":"wlt_758891fa.0","accountId":"wlt_758891fa.1","label":"main-1","type":"seed","index":1,"active":true,"addresses":{"tron":"TRs9HgTuY3dT3yDasdFdP9WQHqL37891Ax","evm":"0xf3ec542047Fe61E0b753a7EBca95B27a672F9cbe"},"seedId":"wlt_758891fa","derivationPath":{"tron":"m/44'/195'/1'/0/0","evm":"m/44'/60'/0'/0/1"}},"meta":{"durationMs":14,"warnings":[]}}
```

## 输出

`data` 是切换到的账户，外加 `previous`（切换前的当前账户）。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `previous` | string | 切换前的当前账户 id |
| `accountId` | string | 现在的当前账户 id |
| `label` | string | 账户标签 |
| `type` | string | `seed` / `privateKey` / `watch` / `ledger` |
| `index` | number \| null | HD 派生索引；非 HD 账户为 `null` |
| `active` | boolean | 始终为 `true`（刚被设为当前账户） |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `derivationPath` | object \| null | 派生类账户按家族给出的 BIP44 路径；`watch` / `privateKey` 从未派生过，因此为 `null` |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `family` | string | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）有此字段 |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`current`](current.md) · [`list`](list.md)
