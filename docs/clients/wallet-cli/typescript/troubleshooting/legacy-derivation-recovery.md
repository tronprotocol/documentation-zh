# 出现 `legacy_derivation` 后如何找回地址

在 4.13.1 之前，wallet-cli 按 `m/44'/195'/<index>'/0/0` 派生 TRON 账户。现在改用 `m/44'/195'/0'/0/<index>`，与 EVM 的布局一致。0 号账户在两种方式下相同，EVM 路径也从未改变。**旧钱包中 1 号及之后的 TRON 账户仍保留它们原来的地址**，本版本对它们的处理如下：

| 你的操作 | 结果 |
|---|---|
| 以该 TRON 地址签名（`tx send`、`message sign` 等） | `legacy_derivation`（退出码 1） |
| 在该钱包中 `derive` 新账户 | `legacy_derivation`（退出码 1） |
| 使用同一账户的 EVM 地址 | 正常 |
| 查询余额、`--build-only`、`list`、`use` | 正常 |
| 用助记词执行 `import mnemonic` | 1 号及之后的账户会以**新的** TRON 地址回来 |

旧密钥并没有丢——助记词在旧路径上仍然能派生出它。下面的步骤会把每一把旧 TRON 密钥迁到独立账户中，然后在新路径上重建钱包。全过程只改动本地数据，链上没有任何变动。

## 这个错误长什么样

```console
error [legacy_derivation]: account "main-1" was derived at m/44'/195'/1'/0/0, a TRON path this version no longer produces, so it cannot be signed here. Follow the complete recovery procedure before deleting anything:
  https://github.com/tronprotocol/wallet-cli/blob/wallet-cli-4.13.1/ts/docs/troubleshooting/legacy-derivation-recovery.md
```

## 开始之前

示例钱包中有一个受影响的账户 `main-1`：

```bash
wallet-cli list --network tron:728126428
```

```console
HD  wlt_n5g8s27j
├─ [0] main    TRTEhBEhyiXfRxG2kRbZ3KgenwpcZ4yUJA
└─ [1] main-1  TXyPxeWda1vGTj7mS5eF7gqSmbQ6p3PDKP  (active)
```

先保存账户列表，以及该钱包的原生备份：

```bash
wallet-cli list -o json > ./accounts-before.json
```

```bash
wallet-cli backup main --out ./main-mnemonic.json
```

在提示处选择 **Native wallet backup**。备份中会列出所有需要执行第 1 步的账户，并给出对应的命令：

```console
warning: this version's default mnemonic recovery will NOT recreate wlt_n5g8s27j.1 (m/44'/195'/1'/0/0) — that account was derived at a TRON path this version no longer produces, but the recovery phrase can still derive that key at the listed path. Export it separately before deleting anything:
  wallet-cli backup wlt_n5g8s27j.1 --keystore --network tron:728126428 --password-stdin
```

这两个文件都要妥善保管，不要纳入版本控制。

## 1. 保住旧的 TRON 地址

把列出的每个账户的 TRON 密钥导出为 keystore：

```bash
wallet-cli backup main-1 --keystore --network tron:728126428 --out ./main-1-tron.keystore.json
```

把它作为独立账户导入。先输入 master password，再输入 keystore 密码——后者就是导出该 keystore 时所用的 master password：

```bash
wallet-cli import keystore ./main-1-tron.keystore.json --label main-1-legacy-tron
```

```console
✅ Imported wallet "main-1-legacy-tron"
  Account ID    wlt_pafmpa51
  Type          private key
  TRON address  TXyPxeWda1vGTj7mS5eF7gqSmbQ6p3PDKP
  EVM address   0xF15BeA353364D1022BCAa2f3F0A318ca2676A440
  Active        yes
```

这里的 TRON 地址与原来一致，且可以正常签名。EVM 地址是由同一把私钥推出来的，它**不是**钱包中 `main-1` 的那个 EVM 地址——除非你确实要用它，否则请忽略。

确认每个旧 TRON 地址现在也出现在 `private key` 之下：

```bash
wallet-cli list --network tron:728126428
```

```console
HD  wlt_n5g8s27j
├─ [0] main            TRTEhBEhyiXfRxG2kRbZ3KgenwpcZ4yUJA
└─ [1] main-1          TXyPxeWda1vGTj7mS5eF7gqSmbQ6p3PDKP

private key
└─ main-1-legacy-tron  TXyPxeWda1vGTj7mS5eF7gqSmbQ6p3PDKP  (active)
```

在确认之前不要继续往下做。如果你确定某个旧 TRON 地址不再需要，可以跳过它。

## 2. 重建钱包

删除该 HD 钱包。这会移除它的全部账户，但不会影响第 1 步中建立的独立账户：

```bash
wallet-cli delete main --yes
```

用 `main-mnemonic.json` 中的助记词导入。这会恢复 0 号账户：

```bash
wallet-cli import mnemonic --label main
```

## 3. 重新派生其余账户

`import mnemonic` 只恢复索引 0。你原先有哪些索引，就逐个重新派生（`derive` 只从 stdin 接收 master password；`$PW` 中存放着它）：

```bash
printf '%s' "$PW" | wallet-cli derive --account main --index 1 --label main-1 --password-stdin
```

与 `accounts-before.json` 对照：

```bash
wallet-cli list --network eip155:1
```

```console
private key
└─ main-1-legacy-tron  0xF15BeA353364D1022BCAa2f3F0A318ca2676A440

HD  wlt_6xzxsmj5
├─ [0] main            0x811Bae29A75A3e283cC9B1ae4b7D7280429BD316
└─ [1] main-1          0x6F63D9e65070319885d1B46D3df31D6f1dB042e1  (active)
```

- 每个索引上的 EVM 地址都与之前一致。
- 0 号账户的 TRON 地址与之前一致。
- 1 号及之后的账户是新的 TRON 地址。旧地址及其上的资金，在第 1 步建立的那些 `private key` 账户里。

全部核对无误后，请把备份文件和 keystore 文件转移到安全的存储位置。

## `derivation_mismatch`

这是另一种错误：`wallets.json` 中存放的某个地址，与其种子的任何派生路径都对不上，也就是钱包文件与加密保险库互相矛盾——通常是因为该文件被手工编辑过，或是从别的钱包拷贝过来的。以该账户签名、以及从其钱包派生，都会返回这个错误码。请用你自己的副本恢复这些文件，或用助记词重建该钱包。

## 另请参见

[账户与 HD 钱包](../concepts/accounts-and-hd.md) · [`backup`](../commands/backup.md) · [`derive`](../commands/derive.md) · [`import keystore`](../commands/import/keystore.md)
