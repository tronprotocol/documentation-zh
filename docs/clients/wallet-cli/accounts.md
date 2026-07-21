# 账户

链上账户操作：创建和更新账户、读取余额和账户数据、管理账户权限。

在 REPL 中，构建交易的命令可带一个**可选的首参 `[OwnerAddress]`**。若省略，则使用当前已登录账户；
若提供，则该命令会按该 owner 准备成一笔多签交易。标准 CLI 的等价写法是 `--owner` 配合 `--multi`。

## 创建账户 —— `create-account` / `CreateAccount`

为给定地址创建一个链上账户。（一个地址只有被激活后才成为链上账户，例如收到 TRX，或通过本命令。）

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile create-account --address TXyz...
    ```

    - `--address`（必填）—— 要激活的地址。
    - `--owner`（可选）、`--multi`（可选）。需要鉴权。

=== "交互模式"

    ```
    CreateAccount [OwnerAddress] Address
    ```

## 更新账户名称 —— `update-account` / `UpdateAccount`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-account --name "my account"
    ```

    - `--name`（必填）—— 新的账户名称。
    - `--owner`（可选）、`--multi`（可选）。需要鉴权。

=== "交互模式"

    ```
    UpdateAccount [OwnerAddress] AccountName
    ```

## 设置账户 ID —— `set-account-id` / `SetAccountId`

为账户设置一个唯一、可读的账户 ID。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile set-account-id --id myaccountid
    ```

    - `--id`（必填）—— 要设置的账户 ID。
    - `--owner`（可选）。需要鉴权。

=== "交互模式"

    ```
    SetAccountId [OwnerAddress] account_id
    ```

## 读取账户数据

### 查询账户信息 —— `get-account` / `GetAccount`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account --address TXyz...
    ```

    - `--address`（必填）。无需鉴权。

=== "交互模式"

    ```
    GetAccount Address
    ```

### 按 ID 查询账户 —— `get-account-by-id` / `GetAccountById`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account-by-id --id myaccountid
    ```

    - `--id`（必填）。无需鉴权。

=== "交互模式"

    ```
    GetAccountById account_id
    ```

### 查询当前地址 —— `get-address` / `GetAddress`

打印活动/已登录钱包的地址。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar get-address
    ```

    需要鉴权（它上报活动钱包的地址）。

=== "交互模式"

    ```
    GetAddress
    ```

### 查询 TRX 余额 —— `get-balance` / `GetBalance`

=== "标准 CLI"

    ```bash
    # 查询某个显式地址的余额（无需鉴权）
    java -jar build/libs/wallet-cli.jar --network nile get-balance --address TXyz...

    # 查询活动钱包的余额（需要鉴权）
    java -jar build/libs/wallet-cli.jar --network nile get-balance
    ```

    - `--address`（可选）。若提供则无需鉴权；若省略则读取活动钱包余额，需要鉴权。

=== "交互模式"

    ```
    GetBalance [Address]
    ```

    省略地址即读取当前账户余额。

### 显示收款二维码 —— `ShowReceivingQrCode`（仅 REPL）

```
ShowReceivingQrCode
```

渲染当前地址的二维码，用于收款。

## 账户权限 —— `update-account-permission` / `UpdateAccountPermission`

TRON 账户支持灵活的权限模型（一个 owner 权限、一个可选的 witness 权限，以及多个 active 权限），
从而实现多签控制。本命令用你提供的权限集替换账户当前的整套权限。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-account-permission \
      --owner TXyz... --permissions '<permission-json>'
    ```

    - `--owner`（必填）—— 要更新权限的账户。
    - `--permissions`（必填）—— 完整权限集，以 JSON 字符串形式给出。
    - `--multi`（可选）。需要鉴权。

=== "交互模式"

    ```
    UpdateAccountPermission [ownerAddress] [permissions]
    ```

    不带参数（或只带一个 owner 地址）时，交互式构建器会引导你编辑权限。带两个参数时，第二个是
    权限集的 JSON 字符串。

权限 JSON 的结构如下（键、阈值，以及带权重的签名者列表）：

```json
{
  "owner_permission": {
    "type": 0,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      { "address": "TXyz...", "weight": 1 }
    ]
  },
  "witness_permission": {
    "type": 1,
    "permission_name": "witness",
    "threshold": 1,
    "keys": [
      { "address": "TXyz...", "weight": 1 }
    ]
  },
  "active_permissions": [
    {
      "type": 2,
      "permission_name": "active",
      "threshold": 2,
      "operations": "7fff1fc0033ef30f000000000000000000000000000000000000000000000000",
      "keys": [
        { "address": "TAbc...", "weight": 1 },
        { "address": "TDef...", "weight": 1 }
      ]
    }
  ]
}
```

- `threshold` 是该权限授权一个操作所需的签名者总权重。
- `operations`（仅 active 权限）是一个 32 字节的十六进制位图，用于选择该权限可执行哪些合约/操作类型。
  上面的示例匹配 4.9.7 的默认 active 权限位图：它排除了已禁用的操作 51
  （`ShieldedTransferContract`），同时保留 49、52 等 active 操作。
- `witness_permission` 仅对超级代表账户有意义。
