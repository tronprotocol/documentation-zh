# wallet-cli list

列出钱包/账户（无需解锁）。

## 用法

```
wallet-cli list [options]
```

## 说明

枚举本地存储的全部账户，涵盖所有种子钱包和导入的账户：HD 账户按 seed 分组，其余按类型分组（私钥 / 仅观察 / Ledger），并标出当前账户。只读取元数据——不需要 master password，也不访问任何节点。

一个账户在其支持的**每个链家族下各有一个地址**：seed 账户和私钥账户同时拥有 TRON 与 EVM 地址，
仅观察账户和 Ledger 账户则只绑定到注册时选择的链家族。

这里的 `--network` 是一个**显示选择器**，而不是操作目标：它决定文本列表打印哪个家族的地址。在该家族下没有地址的账户会被略去，并由一条警告说明略去了几个。JSON 输出不做过滤——它始终列出每个账户及其全部地址。

如果某个账户所用的钱包格式本版本无法识别——也就是注册表由更新版本的 wallet-cli 写下——它会被**跳过而不是导致失败**：列表仍会显示所有能读取的账户，并给出警告点名被略过的钱包 id（`… use a wallet format this version does not understand and were skipped: wlt_… . Upgrade wallet-cli to use them.`）。而在其他任何命令上指名这样的账户，都会是硬性的 `encoding_error`（退出码 1），且在操作开始之前就抛出。

## 选项

仅[全局选项](index.md#global-options-every-command)。

## 示例

```bash
wallet-cli list --network nile
```

```console
warning: 1 account(s) have no tron address and are not shown; use --network to switch, or --output json to see every family
HD  wlt_kwyjcwdh
├─ [0] main    TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa
├─ [1] main-1  TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ
└─ [2] main-2  TA6CYVzW9rskb54mv4mwMM7tu42ZXvfpnz  (active)

watch-only
└─ cold        TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
```

HD 账户按种子分组，并带有 `[索引]`；非 HD 条目（私钥 / 仅观察 / Ledger）则按类型分组。文本一次只显示一个家族：仅限 EVM 的仅观察账户 `cold-evm` 在 Nile 上会被略去（警告里会说明），换成 `--network sepolia` 这类 EVM 网络时才会出现。

```bash
wallet-cli list -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"list","data":[{"accountId":"wlt_kwyjcwdh.0","label":"main","type":"seed","index":0,"active":false,"addresses":{"tron":"TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa","evm":"0xeb0a0D15e3B8f6E2FC4bc011Eb6644f1ce3E4fa2"},"seedId":"wlt_kwyjcwdh","derivationPath":null},{"accountId":"wlt_kwyjcwdh.1","label":"main-1","type":"seed","index":1,"active":false,"addresses":{"tron":"TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ","evm":"0xEA4A61822322c695F5A9eB7920b843054CbDaA83"},"seedId":"wlt_kwyjcwdh","derivationPath":null},{"accountId":"wlt_kwyjcwdh.2","label":"main-2","type":"seed","index":2,"active":true,"addresses":{"tron":"TA6CYVzW9rskb54mv4mwMM7tu42ZXvfpnz","evm":"0xbdFFbe9F40522E2DB8B32692E9fB0d2b63D83304"},"seedId":"wlt_kwyjcwdh","derivationPath":null},{"accountId":"wlt_h10w1nm0","label":"cold","type":"watch","index":null,"active":false,"addresses":{"tron":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ"},"family":"tron","derivationPath":null},{"accountId":"wlt_x771mz6t","label":"cold-evm","type":"watch","index":null,"active":false,"addresses":{"evm":"0x742d35Cc6634C0532925a3b844Bc454e4438f44e"},"family":"evm","derivationPath":null}],"meta":{"durationMs":16,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

无论选的是哪个网络，JSON 都会列出每个账户及其全部地址。

## 输出 {#output}

`data` 是一个数组，每个账户对应一项：

| 字段 | 类型 | 含义 |
| ---------------- | -------------- | ----------------------------------------------------------------------------------------------------- |
| `accountId`      | string         | 稳定的 id；HD 账户为 `<seedId>.<index>`，非 HD 账户为独立的 `wlt_…`                        |
| `label`          | string         | 供人阅读的标签（可用 `rename` 修改）                                                                    |
| `type`           | string         | `seed` (HD), `privateKey`, `watch`, `ledger`                                                          |
| `index`          | number \| null | 该种子内的 HD 派生索引；非 HD 账户为 `null`                                       |
| `active`         | boolean        | 各命令是否默认作用于该账户                                                       |
| `addresses`      | object         | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `seedId`         | string         | 所属种子钱包 id（仅 `seed` 账户）                                                          |
| `derivationPath` | null | 恒为 `null`，这是刻意为之——`list` 不接收 master password，因此在不打开种子的情况下无法分辨旧 TRON 路径与当前路径；`derive` 和 `backup` 会报告经过校验的路径 |
| `family`         | string         | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）才有    |
| `path`           | string         | 该账户在设备上的派生路径（仅 `ledger` 账户）                                  |

`chain` 块回显的是用于显示的所选网络；命令本身不访问任何节点。

## 退出码

`0` 成功 · `2` 用法错误。参见 [machine-interface](../machine-interface.md#exit-codes)。

## 另请参见

`use` · `current` · [`create`](create.md) · [`account balance`](account/balance.md)
