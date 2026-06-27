# 钱包管理

用于创建、导入、导出和选择本地钱包的命令，以及标准 CLI 的别名系统。

需要注意的几处模式差异：

- **REPL** 维持一个已登录的会话：用 `Login` / `LoginAll` 鉴权一次，钱包便保持解锁，直到
  `Logout`、`Lock` 或退出。
- **标准 CLI** 每次调用都是无状态的：不存在交互式登录。需要签名交易的命令从 `MASTER_PASSWORD`
  （或 `--password-stdin`）读取密码，并作用于**活动钱包**（`set-active-wallet`）或由 `--wallet`
  指定的钱包。
- 若干 REPL 钱包操作（私钥/助记词/Ledger 导入，助记词/keystore 导出，修改密码）没有标准 CLI
  等价命令，因为它们需要交互式输入密文。

## 创建钱包 —— `register-wallet` / `RegisterWallet`

创建一个全新钱包，生成新的助记词，并把加密 keystore 存入 `Wallet/`。

=== "标准 CLI"

    ```bash
    export MASTER_PASSWORD='your-wallet-password'
    java -jar build/libs/wallet-cli.jar --network nile register-wallet --name my-wallet --words 12
    ```

    - `--name`（必填）—— 钱包名称。
    - `--words`（可选）—— 助记词单词数，`12` 或 `24`（默认 `12`）。
    - keystore 用 `MASTER_PASSWORD` 加密。新创建的钱包会自动设为活动钱包。

=== "交互模式"

    ```
    RegisterWallet
    ```

    交互式提示输入密码（输入两次）和助记词单词数（12 或 24）。

## 生成子账户 —— `generate-sub-account` / `GenerateSubAccount`

从当前钱包的助记词在给定索引处派生一个额外账户。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile generate-sub-account --index 1 --name sub-1
    ```

    - `--index`（必填）—— 派生索引。
    - `--name`（必填）—— 子账户名称。需要鉴权。

=== "交互模式"

    ```
    GenerateSubAccount
    ```

    交互式提示输入派生索引和名称。

## 导入钱包（仅 REPL）

这些命令以交互方式接受密文，仅存在于 REPL 中。

```
ImportWallet                 # 从原始私钥导入（提示输入）
ImportWalletByMnemonic       # 从 12/24 词的 BIP39 助记词导入（提示输入）
ImportWalletByBase64         # 从 Base64 编码的私钥导入（提示输入）
ImportWalletByKeystore  tronlink <keystore-file>   # 从 TronLink keystore 文件导入
ImportWalletByLedger         # 从 Ledger 硬件钱包导入账户
```

- `ImportWalletByKeystore` 接受固定的 `tronlink` 通道关键字，后跟导出的 keystore JSON 文件路径。
  keystore 密码在提示时交互输入。
- `ImportWalletByLedger` 需要连接 Ledger 设备，并引导你完成账户选择。

## 生成独立地址 —— `GenerateAddress`（仅 REPL）

生成一个随机的 TRON 密钥对，打印地址和私钥，不存储 keystore。

```
GenerateAddress [isECKey]
```

- `isECKey`（可选）—— 默认生成 EC（secp256k1）密钥。

## 登录并选择钱包

=== "标准 CLI"

    标准 CLI 不进行交互式登录。它作用于**活动钱包**，或用全局选项 `--wallet <name|path>`
    在每条命令上单独选择钱包。

    ```bash
    # 列出钱包及其活动状态
    java -jar build/libs/wallet-cli.jar list-wallet

    # 按地址或名称设置活动钱包
    java -jar build/libs/wallet-cli.jar set-active-wallet --address TXyz...
    java -jar build/libs/wallet-cli.jar set-active-wallet --name my-wallet

    # 显示当前活动钱包
    java -jar build/libs/wallet-cli.jar get-active-wallet
    ```

    - `set-active-wallet` 接受 `--address` 或 `--name`（提供其一）。
    - 签名命令的鉴权使用 `MASTER_PASSWORD`（或 `--password-stdin`）。

=== "交互模式"

    ```
    Login           # 选择一个钱包并登录
    LoginAll        # 登录所有已存储的钱包
    SwitchWallet    # 在已登录的钱包之间切换活动钱包
    Logout          # 结束会话
    Lock            # 锁定钱包（使用前必须 Unlock）
    Unlock [durationSeconds]   # 解锁 N 秒（默认 300）
    ```

## 备份钱包（仅 REPL）

```
BackupWallet            # 打印钱包私钥（通过密码校验后）
BackupWallet2Base64     # 以 Base64 编码打印私钥
ExportWalletMnemonic    # 打印钱包的 BIP39 助记词（通过密码校验后）
ExportWalletKeystore  tronlink <directory>   # 把 keystore 文件导出到目录
ViewBackupRecords       # 列出本地备份历史
```

以上命令都需要钱包密码且为交互式，因此仅限 REPL。

## 从助记词派生私钥 —— `GetPrivateKeyByMnemonic`（仅 REPL）

提示输入 BIP39 助记词，并打印在默认路径 `m/44'/195'/0'/0/0` 派生出的私钥。它不会导入或存储钱包。

```
GetPrivateKeyByMnemonic
```

## 修改钱包密码 —— `ChangePassword`（仅 REPL）

```
ChangePassword
```

提示输入当前密码和新密码。

## 重命名钱包 —— `modify-wallet-name` / `ModifyWalletName`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar modify-wallet-name --name new-name
    ```

    - `--name`（必填）—— 新的钱包名称。需要鉴权。

=== "交互模式"

    ```
    ModifyWalletName new_wallet_name
    ```

## 清除 keystore —— `clear-wallet-keystore` / `ClearWalletKeystore`

从本地存储中删除钱包的加密 keystore 文件。此操作具有破坏性。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar clear-wallet-keystore --force
    ```

    - `--force` 在语法上是可选的，但在标准 CLI 模式下执行这一破坏性操作时必须提供 —— 不带它命令会
      以用法错误失败。需要鉴权。

=== "交互模式"

    ```
    ClearWalletKeystore
    ```

## 重置钱包 —— `reset-wallet` / `ResetWallet`

把本地钱包状态清回初始状态。此操作具有破坏性。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar reset-wallet --confirm delete-all-wallets
    ```

    - `--confirm` 必须传入确切的值 `delete-all-wallets` 才会执行重置。不带 `--confirm` 运行
      `reset-wallet` 是一次试运行（列出将被删除的文件）；传入其他任何值都是用法错误。

=== "交互模式"

    ```
    ResetWallet
    ```

## 地址簿 —— `AddressBook`（仅 REPL）

打开交互式的本地地址簿，可在其中为常用地址存储和管理友好名称。它会提示输入，而非接受参数。

```
AddressBook
```

## 查看交易历史 —— `ViewTransactionHistory`（仅 REPL）

列出当前钱包在本地记录的交易历史。

```
ViewTransactionHistory
```

## 别名（仅标准 CLI）

标准 CLI 支持**别名** —— 为账户和代币起的友好名称 —— 这样你可以写 `--to my-friend` 而不是原始的
Base58 地址。别名按网络隔离，来自两层：一组**内置**别名（只读）和你的**用户**别名。

别名解析作用于**地址**字段，而非数字 ID：

- **账户别名**（`--type ACCOUNT`）作用于诸如 `--to`、`--from`、`--owner`、`--receiver`、
  `--address` 等地址字段。
- **代币别名**（`--type TOKEN`）作用于合约地址字段 —— 合约 `--contract` 选项，以及
  `get-contract` / `get-contract-info` 的 `--address`。

它们**不**作用于 TRC-10 资产 ID（`--asset`）或 `--token-id`，这些按数字 ID 原样读取。当别名被
解析时，解析结果会在 JSON 模式下以 `meta.resolved` 上报。

```bash
# 添加账户别名
java -jar build/libs/wallet-cli.jar --network nile alias-add \
  --name treasury --type ACCOUNT --address TXyz... --note "team treasury"

# 添加代币别名（带精度）
java -jar build/libs/wallet-cli.jar --network nile alias-add \
  --name usdt --type TOKEN --address TR7NHq... --decimals 6

# 列出别名（可按类型过滤）
java -jar build/libs/wallet-cli.jar --network nile alias-list --type ACCOUNT

# 把别名或地址解析为其规范形式
java -jar build/libs/wallet-cli.jar --network nile alias-resolve --name treasury

# 删除用户别名
java -jar build/libs/wallet-cli.jar --network nile alias-remove --name treasury
```

选项说明：

- `alias-add`：`--name`、`--type`（`ACCOUNT` 或 `TOKEN`）、`--address` 为必填。`--decimals` 仅对
  `TOKEN` 有效；`--note` 仅对 `ACCOUNT` 有效。
- 内置别名不可覆盖或删除。要替换某个用户别名，先 `alias-remove`，再重新 `alias-add`。
- `alias-list` 和 `alias-resolve` 接受可选的 `--type` 过滤。
