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

## 选项

仅[全局选项](index.md#global-options-every-command)。

## 示例

```bash
wallet-cli list --network tron:3448148188
```

```console
warning: 1 account(s) have no tron address and are not shown; use --network to switch, or --output json to see every family
HD  wlt_z259a1hq
└─ [0] main    TE9kPMtaMjfZN95CuPRsCHUQGWwx9EcJW8

watch-only
└─ watch-test  THdUXD3mZqT5aMnPQMtBSJX9ANGjaeUwQK
```

标签列的宽度按**实际显示出来的**最长标签对齐，因此过滤条件一变，同样这些账户的排布也会不同。切到 EVM 网络后，seed 账户以它的 EVM 地址重新出现，仅 TRON 的那条仅观察记录消失，仅 EVM 的那条则顶上来：

```bash
wallet-cli list --network eip155:11155111
```

```console
warning: 1 account(s) have no evm address and are not shown; use --network to switch, or --output json to see every family
HD  wlt_z259a1hq
└─ [0] main   0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C

watch-only
└─ watch_evm  0xe4aAd11792F7E74f1B5cbce65f9a1E207c952961  (active)
```

HD 账户按 seed 分组并带有 `[index]`；非 HD 条目（私钥 / 仅观察 / Ledger）按类型分组，没有 `[index]`。

```bash
wallet-cli list -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"list","data":[{"accountId":"wlt_z259a1hq.0","label":"main","type":"seed","index":0,"active":false,"addresses":{"tron":"TE9kPMtaMjfZN95CuPRsCHUQGWwx9EcJW8","evm":"0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C"},"seedId":"wlt_z259a1hq","derivationPath":{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"}},{"accountId":"wlt_whxjk6na","label":"watch-test","type":"watch","index":null,"active":false,"addresses":{"tron":"THdUXD3mZqT5aMnPQMtBSJX9ANGjaeUwQK"},"family":"tron","derivationPath":null},{"accountId":"wlt_n5v4r992","label":"watch_evm","type":"watch","index":null,"active":true,"addresses":{"evm":"0xe4aAd11792F7E74f1B5cbce65f9a1E207c952961"},"family":"evm","derivationPath":null}],"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

## 输出 {#output}

`data` 是一个数组，每个账户对应一项：

| 字段 | 类型 | 含义 |
|---|---|---|
| `accountId` | string | 稳定 id；HD 账户为 `<seedId>.<index>`，非 HD 账户为独立的 `wlt_…` |
| `label` | string | 可读标签（用 `rename` 修改） |
| `type` | string | `seed`（HD）、`privateKey`、`watch`、`ledger` |
| `index` | number \| null | 在该 seed 内的 HD 派生索引；非 HD 账户为 `null` |
| `active` | boolean | 是否为各命令默认使用的账户 |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `derivationPath` | object \| null | 每个地址背后的 BIP32 路径：`seed` 账户是全部家族（`{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"}`），`ledger` 账户是所选的那一条路径；`privateKey` 和 `watch` 从未派生过，因此为 `null` |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `family` | string | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）有此字段 |

`chain` 块回显的是用于显示的所选网络；命令本身不访问任何节点。

## 退出码

`0` 成功 · `2` 用法错误。参见 [machine-interface](../machine-interface.md#exit-codes)。

## 另请参见

`use` · `current` · [`create`](create.md) · [`account balance`](account/balance.md)
