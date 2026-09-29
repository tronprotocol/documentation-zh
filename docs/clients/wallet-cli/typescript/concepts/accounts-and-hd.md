# 账户与 HD 钱包

wallet-cli 如何组织你在 `list` 中看到的内容。

## 种子与账户 {#seeds-and-accounts}

一个**种子钱包**对应一条 BIP39 助记词；它可以派生出多个**账户**。id 正体现了这一点：

```
wlt_4473p34m        ← seedId (one mnemonic)
wlt_4473p34m.0      ← accountId = seedId.index (one account, one address per family)
wlt_4473p34m.1
```

`create` 创建一个新种子以及 0 号账户；`derive` 从同一条助记词追加下一个账户（或显式指定 `--index`）。它默认作用于当前账户所属的种子；要选另一个，可用 `--account`（该种子下的任意账户）或 `--seed-id`。在其他环境中恢复同一助记词会重新派生出相同的地址，因此助记词才是真正的备份，而 master password 只是本地保护。注意 `create` 不会打印助记词；执行 [`backup`](../commands/backup.md) 可以把它导出到离线文件。

## 一个账户，每个链家族一个地址

密钥本身并不绑定某一条链，因此**一个账户在每个[链家族](networks.md)下各有一个地址**——一个 TRON base58 地址和一个 EVM `0x` 地址——它们由同一份种子在不同的 BIP44 币种类型下派生而来：

```
m/44'/195'/0'/0/<index>   TRON
m/44'/60'/0'/0/<index>    EVM
```

两者只有币种类型不同；账户索引在两条路径上都是最后一级。因此账户 `.1` 对应的是 `m/44'/195'/0'/0/1` 和 `m/44'/60'/0'/0/1`。

两者都是真实且互相独立的地址：它们各自持有余额，给其中一个打钱不会让另一个多出一分。`list -o json` 和 `current -o json` 会把它们一起报告出来，放在按家族为键的 `addresses` 下。这两条命令不接收 master password，因此在不打开种子的情况下无法分辨旧 TRON 路径与当前路径；它们会刻意返回 `derivationPath: null`。而确实会打开种子的 `derive` 和 `backup`，则会报告每个地址经过校验的路径：

```json
{"accountId":"wlt_kwyjcwdh.0","label":"main","type":"seed","index":0,"active":false,"addresses":{"tron":"TEKbsrcsL74XyNWH6ju9zfjGDNok78dtTa","evm":"0xeb0a0D15e3B8f6E2FC4bc011Eb6644f1ce3E4fa2"},"seedId":"wlt_kwyjcwdh","derivationPath":null}
```

一条命令以哪个地址的身份执行，取决于**所选网络**，而不是账户上的某个设置：`--network nile` 用的是 TRON 地址，`--network sepolia` 用的是 EVM 地址。文本列表一次只显示一个家族，并会说明略去了多少个账户；JSON 则始终带上全部家族。

Ledger 账户用的是另一套模板：`import ledger --index <n>` 遵循 Ledger Live 的 `m/44'/<coin>'/<n>'/0/0`。两者只有在索引 0 上一致。参见 [`import ledger`](../commands/import/ledger.md)。

### 4.13.1 之前创建的账户 {#accounts-from-before-4131}

早先的版本按 `m/44'/195'/<index>'/0/0` 派生 TRON 账户。对 0 号账户来说这是同一条路径，因此毫无影响。1 号及之后的账户仍保留它们原来的 TRON 地址，但本版本不再用它签名：

- 以该 TRON 地址签名会以 `legacy_derivation` 失败。该账户的 EVM 地址、`--build-only` 以及各类查询仍然可用。
- `derive` 会以 `legacy_derivation` 拒绝向该种子添加新账户。
- 重新导入助记词并不会把旧的 TRON 地址找回来。

在删除任何东西之前，请先按[出现 `legacy_derivation` 后如何找回地址](../troubleshooting/legacy-derivation-recovery.md)操作。

并非每个账户都同时拥有两个地址。`watch` 或 `ledger` 账户只记录一个地址，即导入时提供的地址或设备应用派生的地址。因此，这类账户带有 `family` 字段，并且只能在对应家族的网络上使用；用于其他家族时会返回 `family_mismatch`。

## 账户类型 {#account-types}

| 类型 | 创建方式 | 本地是否保存密钥材料？ | 能否签名？ | 链家族 |
|---|---|---|---|---|
| `seed` | `create`、`import mnemonic`、`derive` | 加密的种子 | 能 | TRON + EVM |
| private-key | `import private-key`、`import keystore` | 加密的私钥；**无法派生** | 能 | TRON + EVM |
| ledger | `import ledger` | 无（仅观察条目） | 在设备上签名 | 由 `--app` 决定 |
| watch | `import watch` | 无 | 不能——只能查询 | 由地址本身决定 |

## 当前账户 {#the-active-account}

大多数与钱包绑定的命令都需要一个账户。解析顺序：

1. 命令上的 `--account <accountId|label|address>`；
2. 否则使用**当前**账户——用 `use <account>` 设置，由 `current` 显示，并在 `list` 中以 `(active)`
   标记。

标签唯一、1–64 个字符、可重命名（`rename`）——稳定的句柄始终是 `accountId`。

## 生命周期 {#lifecycle}

- `backup <account>` 把密钥材料和元数据导出到一个以 **0600** 权限创建、且不会覆盖的文件（默认位于当前工作目录）。请按照它所包含密钥的等级来对待该文件，并注意命令的执行目录，因为 CLI 不会检查该目录是否是共享目录或纳入了版本控制。原生格式携带的是种子或密钥本身，因此一次性覆盖全部家族；而 `backup --keystore` 携带的是**单个私钥**，因此由 `--network` 决定它装的是哪个家族的密钥。
- `delete` 删除账户；**删除 HD 钱包会从种子根开始级联**——该种子派生出的全部账户都会一并删除。链上资产不受影响。请先执行 `backup`，并留意它打印的任何警告——参见 [4.13.1 之前创建的账户](#accounts-from-before-4131)。
- 丢失 master password 在本地无法恢复；退路始终是助记词 → `import mnemonic`。

## 另请参见

[`list`](../commands/list.md) · [`create`](../commands/create.md) · [`import`](../commands/import/index.md) · [网络](networks.md) · [安全模型](security.md)
