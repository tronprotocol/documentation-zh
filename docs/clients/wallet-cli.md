# wallet-cli

## 简介

**wallet-cli** 是一个专为 **TRON** 网络设计的交互式命令行钱包。它使您能够在安全的本地环境中对交易进行签名和广播，并查询链上数据。

**wallet-cli** 支持密钥管理，它会使用对称加密算法对您的私钥进行加密，并将其存储在本地的 Keystore 文件中。由于 **wallet-cli** 不存储链上数据，它通过 gRPC 与您配置的 **java-tron** 节点通信。下图展示了使用 **wallet-cli** 签名和广播 TRX 转账交易的流程：

![avatar](https://i.imgur.com/NRKmZmE.png)

1. 首先，运行 `Login` 命令解锁钱包。
2. 然后，运行 `SendCoin` 命令发送 TRX。
3. **wallet-cli** 会在本地构建和签署交易。
4. 接下来，它会调用 **java-tron** 节点的 `BroadcastTransaction` gRPC API，将交易广播到网络中。
5. 广播成功后，**java-tron** 节点会返回交易成功的结果，以及包含交易哈希的对象。
6. 最后，**wallet-cli** 将交易哈希展示给用户。

有关安装和运行的详细说明，请访问：[GitHub 代码库](https://github.com/tronprotocol/wallet-cli)

## 命令行操作流程示例

```
$ cd wallet-cli
$ ./gradlew build
$ ./gradlew run
> RegisterWallet 123456      (password = 123456)
> login 123456
> getAddress
address = TRfwwLDpr4excH4V4QzghLEsdYwkapTxnm'  # 备份它！
> BackupWallet 123456
priKey = 1234567890123456789012345678901234567890123456789012345678901234  # 备份它！ (BackupWallet2Base64 option)
> getbalance
Balance = 0
> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
> getaccount TRfwwLDpr4excH4V4QzghLEsdYwkapTxnm
(打印余额: 9999900000
"assetV2": [
    {
        "key": "1000001",
        "value": 74999999999980000
    }
],)
  # (发行资产（assetIssue）花费了1000 trx)
  # (您可以查询任何账户的trx余额和其他资产余额)
> TransferAsset TWzrEZYtwzkAxXJ8PatVrGuoSNsexejRiM 1000001 10000
```

<a id="top"></a>
## 命令

**wallet-cli** 支持以下几类命令：

- [密钥管理](#private_key)
- [链上账户](#account)
- [账户资源](#resource)
- [交易](#transaction)
- [查询链上数据](#query_chain_data)
- [智能合约](#contract)
- [TRC-10 资产](#trc-10)
- [治理](#governance)
- [去中心化交易所](#defi)
- [GasFree 支持](#gasfree)
- [其他实用命令](#other)

<a id="private_key"></a>
### 密钥管理

#### 退出登录 - `Logout`
> 登出当前钱包账户。

示例：
```
wallet> Logout
Logout successful !!!
```

#### 统一登录所有账户 - `LoginAll`
> 多个 keystore 账户可以使用一个统一密码登录。

示例：
```
wallet> loginall
Please input your password.
password:
Use user defined config file in current dir
WalletApi getRpcVsersion: 2
[========================================] 100%
The 1th keystore file name is TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB.json
The 2th keystore file name is TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew.json
The 3th keystore file name is TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7.json
The 4th keystore file name is Ledger-TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe.json
The 5th keystore file name is TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada.json
Please choose between 1 and 5
5
LoginAll successful !!!
```

#### 锁定账户 - `Lock`
> 要使用登录账户的锁定功能，需要在 `config.conf` 中配置 `lockAccount = true`。
> 当前登录账户被锁定，这意味着不允许进行签名和交易。

示例：
```
wallet> lock
lock successful !!!
```

#### 解锁账户 - `Unlock`
> 要使用登录账户的解锁功能，需要在 `config.conf` 中配置 `lockAccount = true`。
> 当前登录账户被锁定后可以解锁。默认情况下，它将在 300 秒后再次锁定。解锁时可以指定秒数参数。

示例：
```
wallet> unlock 60
Please input your password.
password:
unlock successful !!!
```

#### 生成账户 - `GenerateAddress`
> 生成一个地址并打印出地址和 private key。

#### 生成子账户 - `GenerateSubAccount`
> 使用钱包中的助记词生成子账户。

示例：
```
wallet> GenerateSubAccount
Please input your password.
password:

=== Sub Account Generator ===
-----------------------------
Default Address: TYEhEg7b7tXm92UDbRDXPtJNU6T9xVGbbo
Default Path: m/44'/195'/0'/0/1
-----------------------------

1. Generate Default Path
2. Change Account
3. Custom Path

Enter your choice (1-3): 1
mnemonic file : ./Mnemonic/TYEhEg7b7tXm92UDbRDXPtJNU6T9xVGbbo.json
Generate a sub account successful, keystore file name is TYEhEg7b7tXm92UDbRDXPtJNU6T9xVGbbo.json
generateSubAccount successful.
```

#### 重置钱包 - `ResetWallet`
> 使用此命令可以删除所有本地钱包的 Keystore 文件和助记词文件，并引导您重新注册或导入钱包。

示例：
```
wallet> resetwallet
User defined config file doesn't exists, use default config file in jar

Warning: Dangerous operation!
This operation will permanently delete the Wallet&Mnemonic files
Warning: The private key and mnemonic words will be permanently lost and cannot be recovered!
Continue? (y/Y to proceed, c/C to cancel):
y

Final confirmation:
Please enter: 'DELETE' to confirm the delete operation:
Confirm: (DELETE): DELETE
resetWallet successful !!!
Now, you can RegisterWallet or ImportWallet again. Or import the wallet through other means.
```

#### 注册钱包 - `RegisterWallet`
> 注册您的钱包，您需要设置钱包密码并生成地址和 private key。

#### 修改账户密码 - `ChangePassword`
> 修改账户的密码。

#### 修改钱包名称 - `ModifyWalletName new_wallet_name`
> 修改钱包的名称。

示例：
```
wallet> ModifyWalletName new-name
Modify Wallet Name successful !!
```

#### 导入钱包 - `ImportWallet`
> 导入钱包，您需要设置密码和 hex String 格式的 private key。

#### 导入Base64格式的钱包 - `ImportWalletByBase64`
> 导入钱包，您需要设置密码和 base64 格式的 private key。

#### 导入助记词 - `ImportWalletByMnemonic`
> 导入钱包，需要设置密码和助记词。

示例：
```
wallet> ImportWalletByMnemonic
Please input password.
password:
Please input password again.
password:
Please enter 12 words (separated by spaces) [Attempt 1/3]:
```

#### 导出助记词 - `ExportWalletMnemonic`
> 导出钱包中地址的助记词。

示例：
```
wallet> ExportWalletMnemonic
Please input your password.
password:
exportWalletMnemonic successful !!
a*ert tw*st co*rect mat*er pa*s g*ther p*t p*sition s*op em*ty coc*nut aband*n
```

#### 导出钱包 keystore - `ExportWalletKeystore`
> 将钱包 keystore 导出为 TronLink 钱包格式。

示例：
```
wallet> ExportWalletKeystore tronlink /tmp
Please input your password.
password:
exported keystore file : /tmp/TYdhEg8b7tXm92UDbRDXPtJNU6T9xVGbbo.json
exportWalletKeystore successful !!
```

#### 导入钱包 keystore - `ImportWalletByKeystore`
> 将 TronLink 钱包的 keystore 文件导入到 wallet-cli。

示例：
```
wallet> ImportWalletByKeystore tronlink /tmp/tronlink.json
Please input password.
password:
Please input password again.
password:
fileName = TYQq6zp51unQDNELmT4xKMWh5WLcwpCDZJ.json
importWalletByKeystore successful !!
```

#### 通过 Ledger 导入钱包 - `ImportWalletByLedger`
> 将 Ledger 的派生账户导入到 wallet-cli。

示例：
```
wallet> ImportWalletByLedger
((Note:This will pair Ledger to user your hardward wallet)
Only one Ledger device is supported. If you have multiple devices, please ensure only one is connected.
Ledger device found: Nano X
Please input password.
password:
Please input password again.
password:
-------------------------------------------------
Default Account Address: TAT1dA8F9HXGqmhvMCjxCKAD29YxDRw81y
Default Path: m/44'/195'/0'/0/0
-------------------------------------------------
1. Import Default Account
2. Change Path
3. Custom Path
Select an option: 1
Import a wallet by Ledger successful, keystore file : ./Wallet/Ledger-TAT1dA8F9HXGqmhvMCjxCKAD29YxDRw81y.json
You are now logged in, and you can perform operations using this account.
```

#### 备份钱包 - `BackupWallet`
> 备份您的钱包，您需要输入钱包密码并导出 hex string 格式的 private key。
> 例如：`1234567890123456789012345678901234567890123456789012345678901234`

#### 备份钱包（Base64）- `BackupWallet2Base64`
> 备份您的钱包，您需要输入钱包密码并导出 base64 格式的 private key。
> 例如：ch1jsHTxjUHBR+BMlS7JNGd3ejC28WdFvEeo6uUHZUU=

#### 清除钱包 keystore - `ClearWalletKeystore`
> 清除登录账户的钱包 keystore 文件。

示例：
```
wallet> ClearWalletKeystore

Warning: Dangerous operation!
This operation will permanently delete the Wallet&Mnemonic files of the Address: TABWx7yFhWrvZHbwKcCmFLyPLWjd2dZ2Rq
Warning: The private key and mnemonic words will be permanently lost and cannot be recovered!
Continue? (y/Y to proceed):y

Final confirmation:
Please enter: 'DELETE' to confirm the delete operation:
Confirm: (DELETE): DELETE

File deleted successfully:
- /wallet-cli/Wallet/TABWx8yFhWrvZHbwKcCmFLyPLWjd2dZ2Rq.json
- /wallet-cli/Mnemonic/TABWx8yFhWrvZHbwKcCmFLyPLWjd2dZ2Rq.json
ClearWalletKeystore successful !!!
```

<a id="account"></a>
### 链上账户

#### 创建账户 - `CreateAccount`
> 该命令可以创建一个新的非活跃地址账户，并为其燃烧 1 trx 作为手续费。

示例：
```
wallet> createaccount TDJ13zZzT3w91WMBm98gC3mwL7NbA6sQPA
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"owner_address":"TQLaB7L8o3ikjRVcN7tTjMZsRYPJ23XZbd",
						"account_address":"TDJ13zZzT3w91WMBm98gC3mwL7NbA6sQPA"
					},
					"type_url":"type.googleapis.com/protocol.AccountCreateContract"
				},
				"type":"AccountCreateContract"
			}
		],
		"ref_block_bytes":"91a4",
		"ref_block_hash":"2bfcd3bb597f3d40",
		"expiration":1745333676000,
		"timestamp":1745333618318
	},
	"raw_data_hex":"0a0291a422082bfcd3bb597f3d4040e0cff9efe5325a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a15419d9c2bb5ee381a4396dd49ce42292e756b2e5e4b12154124764e4674179d4578cfc4c833c1ac1a09f6ce56708e8df6efe532"
}
Before sign transaction hex string is 0a84010a0291a422082bfcd3bb597f3d4040e0cff9efe5325a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a15419d9c2bb5ee381a4396dd49ce42292e756b2e5e4b12154124764e4674179d4578cfc4c833c1ac1a09f6ce56708e8df6efe532
Please confirm and input your permission id, if input y/Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB.json
The 2th keystore file name is TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew.json
The 3th keystore file name is TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7.json
The 4th keystore file name is Ledger-TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe.json
The 5th keystore file name is TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada.json
Please choose between 1 and 5
1
After sign transaction hex string is 0a84010a0291a422082bfcd3bb597f3d404083bd9cfae5325a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a15419d9c2bb5ee381a4396dd49ce42292e756b2e5e4b12154124764e4674179d4578cfc4c833c1ac1a09f6ce56708e8df6efe5321241ce53add4f75fe1838aa7e0a4e2411b3bbfce1d2164d68dac18507ed87e22ae503f65592a1161640834b3c0cef43c28f20b2d335120cc78b6f745a82ea95e451100
TxId is 26d6fcdfdc0018097ec4166eb140e19ebd597bea2212579d2f6d921b0ad6e56f
CreateAccount successful !!
```

#### 设置账户 ID - `SetAccountId [owner_address] account_id`

> 为账户设置一个自定义的唯一标识符（Account ID）。

示例：

```
> SetAccountId TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 100
```

#### 更新账户 - `UpdateAccount [owner_address] account_name`

> 修改账户名称。

示例：

```
> UpdateAccount test-name
```

#### 获取账户信息 - `GetAccount`
> 根据地址获取账户信息。

#### 获取账户地址 - `GetAddress`
> 获取当前登录账户的地址。

#### 获取账户余额 - `GetBalance`
> 获取当前登录账户的余额。

#### 修改账户权限

##### 如何使用 `wallet-cli` 的账户权限管理功能？

账户权限管理功能允许其他用户访问账户，以便更好地管理账户。有三种访问类型：

* `owner`：账户所有者的访问权限
* `active`：账户的其他功能访问权限，以及授权特定功能的访问权限。如果用于 SR，不包括区块生产授权。
* `witness`：仅用于 SR，将授予其中一个用户区块生产授权。

其余用户将被授予权限

```
> Updateaccountpermission TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 
{
  "owner_permission": {
    "type": 0,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      {
        "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
        "weight": 1
      }
    ]
  },
  "witness_permission": {
    "type": 1,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      {
        "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
        "weight": 1
      }
    ]
  },
  "active_permissions": [
    {
      "type": 2,
      "permission_name": "active12323",
      "threshold": 2,
      "operations": "7fff1fc0033e0000000000000000000000000000000000000000000000000000",
      "keys": [
        {
          "address": "TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR",
          "weight": 1
        },
        {
          "address": "TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP",
          "weight": 1
        }
      ]
    }
  ]
}
```

账户 `TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ` 授予自身 Owner 访问权限，以及授予 `TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR` 和 `TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP` Active 访问权限。Active 访问需要两个账户的签名才能生效。

如果账户不是超级代表（Super Representative, 简称 SR），则无需设置 `witness_permission`，否则将报错。

<a id="resource"></a>
### 账户资源

#### 如何冻结/解冻余额

资金冻结后，将获得相应数量的 Tron Power（TP） 和 Bandwidth（或 Energy）。TP 可用于投票，Bandwidth 可用于交易。

本文稍后将介绍 TP 和 Bandwidth 的使用和计算规则。

**冻结操作如下：**

##### `freezev2` 资源

```
freezeBalanceV2 [OwnerAddress] frozen_balance [ResourceCode:0 BANDWIDTH,1 ENERGY,2 TRON_POWER]
```
- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址
- `frozen_balance` - 冻结的金额，单位为最小单位 sun，最小值为 1,000,000 sun
- `ResourceCode` - 0 代表 BANDWIDTH；1 代表 ENERGY

示例：
```
wallet> FreezeBalanceV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 1000000000000000 0
txid is 82244829971b4235d98a9f09ba67ddb09690ac2f879ad93e09ba3ec1ab29177d
wallet> GetTransactionById 82244829971b4235d98a9f09ba67ddb09690ac2f879ad93e09ba3ec1ab29177d
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "4faa3772fa3d3e4792e8126cafed2dc2c5c069cd09c29532f0119bc982bf356004772e16fad86e401f5818c35b96d214d693efab06997ca2f07044d4494f12fd01"
    ],
    "txID":"82244829971b4235d98a9f09ba67ddb09690ac2f879ad93e09ba3ec1ab29177d",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "frozen_balance":1000000000000000,
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.FreezeBalanceV2Contract"
                },
                "type":"FreezeBalanceV2Contract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671109891800,
        "timestamp":1671088291796
    },
    "raw_data_hex":"0a020000220819b59068c6058ff440d8ada5afd1305a5c083612580a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e747261637412200a154159e3741a68ec3e1ebba80ad809d5ccd31674236e1080809aa6eaafe30170d4fffea4d130"
}
```

冻结操作后，冻结的资金将从“账户余额”（Account Balance）转移到“冻结”（Frozen），

您可以从您的账户信息中查看冻结的资金。

解冻后，资金将由“冻结”（Frozen）转回“余额”（Balance），冻结的资金不能用于交易。

当需要临时获得更多 TP 或 Bandwidth 时，可以额外冻结资金以获得额外的 TP 和 Bandwidth。
解冻时间将推迟到最后一次冻结操作后的 14 天。

冻结时间到期后，资金可以解冻。

**解冻操作如下：**

##### `unfreezev2` 资源

```
unfreezeBalanceV2 [OwnerAddress] unfreezeBalance ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER)
```

- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址。
- `unfreezeBalance` - 解冻的金额，单位为最小单位 sun
- `ResourceCode` - 0 代表 Bandwidth；1 代表 Energy

示例：
```
wallet> UnFreezeBalanceV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 9000000 0
txid is dcfea1d92fc928d24c88f7f71a03ae8105d0b5b112d6d48be93d3b9c73bea634
wallet> GetTransactionById dcfea1d92fc928d24c88f7f71a03ae8105d0b5b112d6d48be93d3b9c73bea634
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "f73a278f742c11e8e5ede693ca09b0447a804fcb28ea2bfdfd8545bb05da7be44bd08cfaa92bd4d159178f763fcf753f28d5296bd0c3d4557532cce3b256b9da00"
    ],
    "txID":"dcfea1d92fc928d24c88f7f71a03ae8105d0b5b112d6d48be93d3b9c73bea634",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e",
                        "unfreeze_balance":9000000
                    },
                    "type_url":"type.googleapis.com/protocol.UnfreezeBalanceV2Contract"
                },
                "type":"UnfreezeBalanceV2Contract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671119916913,
        "timestamp":1671098316907
    },
    "raw_data_hex":"0a020000220819b59068c6058ff440f19e89b4d1305a5a083712560a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121c0a154159e3741a68ec3e1ebba80ad809d5ccd31674236e10c0a8a50470ebf0e2a9d130"
}
```

**注意：目前质押只允许使用v2接口。如果仍有未解冻的v1资产，请使用下面的方法尽快解冻**

```
> unfreezeBalance [OwnerAddress] ResourceCode(0 BANDWIDTH, 1 CPU) [receiverAddress]
```


#### 提取过期解冻金额 - `withdrawExpireUnfreeze [OwnerAddress]`

- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址。

示例：
```
wallet> withdrawexpireunfreeze TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
txid is e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
wallet> GetTransactionById e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "f8f02b5aa634b8666862a6d2ed68fcfd90afc616d14062952b0b09f0404d9bca6c4d3dc6dab082784950ff1ded235a07dab0d738c8a202be9451d5ca92b8eece01"
    ],
    "txID":"e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.WithdrawExpireUnfreezeContract"
                },
                "type":"WithdrawExpireUnfreezeContract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671122055318,
        "timestamp":1671100455315
    },
    "raw_data_hex":"0a020000220819b59068c6058ff44096e18bb5d1305a5a083812560a3b747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5769746864726177457870697265556e667265657a65436f6e747261637412170a154159e3741a68ec3e1ebba80ad809d5ccd31674236e7093b3e5aad130"
}
```

#### 取消所有解质押 - `cancelAllUnfreezeV2 [OwnerAddress]`

- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址。

示例：
```
wallet> cancelAllUnfreezeV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
txid is e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
wallet> GetTransactionById e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "f8f02b5aa634b8666862a6d2ed68fcfd90afc616d14062952b0b09f0404d9bca6c4d3dc6dab082784950ff1ded235a07dab0d738c8a202be9451d5ca92b8eece01"
    ],
    "txID":"e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.CancelAllUnfreezeV2"
                },
                "type":"CancelAllUnfreezeV2Contract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671122055318,
        "timestamp":1671100455315
    },
    "raw_data_hex":"0a020000220819b59068c6058ff44096e18bb5d1305a5a083812560a3b747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5769746864726177457870697265556e667265657a65436f6e747261637412170a154159e3741a68ec3e1ebba80ad809d5ccd31674236e7093b3e5aad130"
}
```

#### 如何代理资源

##### 代理资源

```
delegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress [lock]
```

- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址
- `balance` - 代理的金额，单位为最小单位 sun，最小值为 1000000 sun
- `ResourceCode` - 0 代表 Bandwidth；1 代表 Energy
- `ReceiverAddress` - 账户地址
- `lock` - 默认为 `false`，如果需要锁定代理 3 天则设为 `true`
- `lock_period` - 最大代理锁定期限，可以锁定 (0, 86400] 之间的任何时间，单位是区块个数

示例：
```
wallet> DelegateResource TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 10000000 0 TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3 true 10000
txid is 363ac0b82b6ad3e0d3cad90f7d72b3eceafe36585432a3e013389db36152b6ed
wallet> GetTransactionById 363ac0b82b6ad3e0d3cad90f7d72b3eceafe36585432a3e013389db36152b6ed
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "1f57fd78456136faadc5091b47f5fd27a8e1181621e49129df6a4062499429fb48ee72e5f9a9ff5bfb7f2575f01f4076f7d4b89ca382d36af46a6fa4bc749f4301"
    ],
    "txID":"363ac0b82b6ad3e0d3cad90f7d72b3eceafe36585432a3e013389db36152b6ed",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "balance":10000000,
                        "receiver_address":"419a9afe56e155ef0ff3f680d00ecf19deff60bdca",
                        "lock":true,
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e",
                        "lock_period":80000
                    },
                    "type_url":"type.googleapis.com/protocol.DelegateResourceContract"
                },
                "type":"DelegateResourceContract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671120059226,
        "timestamp":1671098459216
    },
    "raw_data_hex":"0a020000220819b59068c6058ff440daf691b4d1305a720839126e0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412350a154159e3741a68ec3e1ebba80ad809d5ccd31674236e1880ade2042215419a9afe56e155ef0ff3f680d00ecf19deff60bdca280170d0c8eba9d130"
}
```
##### 取消代理资源

```
unDelegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress
```
- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址
- `balance` - 取消代理的金额，单位为最小单位 sun
- `ResourceCode` - 0 代表 Bandwidth；1 代表 Energy
- `ReceiverAddress` - 账户地址

示例：
```
wallet> UnDelegateResource TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 1000000 0 TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3
txid is feb334794cf361fd351728026ccf7319e6ae90eba622b9eb53c626cdcae4965c
wallet> GetTransactionById feb334794cf361fd351728026ccf7319e6ae90eba622b9eb53c626cdcae4965c
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "85a41a4e44780ffbe0841a44fd71cf621f129d98e84984cfca68e03364f781aa7f9d44177af0b40d82da052feec9f47a399ed6e51be66c5db07cb13477dcde8c01"
    ],
    "txID":"feb334794cf361fd351728026ccf7319e6ae90eba622b9eb53c626cdcae4965c",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "balance":1000000,
                        "receiver_address":"419a9afe56e155ef0ff3f680d00ecf19deff60bdca",
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.UnDelegateResourceContract"
                },
                "type":"UnDelegateResourceContract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671120342283,
        "timestamp":1671098742280
    },
    "raw_data_hex":"0a020000220819b59068c6058ff4408b9aa3b4d1305a71083a126d0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412320a154159e3741a68ec3e1ebba80ad809d5ccd31674236e18c0843d2215419a9afe56e155ef0ff3f680d00ecf19deff60bdca7088ecfca9d130"
}
```

#### 获取账户带宽 - `GetAccountNet`
> 获取带宽的使用情况。

#### 获取账户资源 - `GetAccountResource`
> 获取带宽和能量的使用情况。

#### 获取资源代理信息

##### `getDelegatedResource fromAddress toAddress`
> 获取从 `fromAddress` 到 `toAddress` 的资源代理信息。

##### `getDelegatedResourceAccountIndex address`
> 获取该 `address` 代理给其他账户的资源信息。

#### 使用 v2 API 获取资源代理信息 - `getDelegatedResourceV2 fromAddress toAddress`
> 使用 v2 API 获取从 `fromAddress` 到 `toAddress` 的资源代理信息。
- `fromAddress` - 发起代理的账户地址
- `toAddress` - 接收代理的账户地址

示例：
```
wallet> getDelegatedResourceV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3
{
	"delegatedResource": [
		{
			"from": "TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh",
			"to": "TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3",
			"frozen_balance_for_bandwidth": 10000000
		}
	]
}
```

`getDelegatedResourceAccountIndexV2 address`
> 使用 v2 API 获取该 `address` 代理给其他账户的资源信息。

- `address` - 发起代理或接收代理的账户地址。

示例：
```
wallet> getDelegatedResourceAccountIndexV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
{
	"account": "TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh",
	"toAccounts": [
		"TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3"
	]
}
```

`getcandelegatedmaxsize ownerAddress type`
- `ownerAddress` - 发起代理的账户地址，可选，默认为登录账户的地址。
    > 获取 `ownerAddress` 可以代理的最大数量（使用 `delegateResource`）。
- `type` - 0 代表 Bandwidth，1 代表 Energy。

示例：
```
wallet> getCanDelegatedMaxSize TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 0
{
	"max_size": 999999978708334
}
```

`getavailableunfreezecount ownerAddress`
- `ownerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址
    > 获取 `ownerAddress` 可以调用 `unfreezeBalanceV2` 的可用解冻次数。


示例：
```
wallet> getAvailableUnfreezeCount TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
{
	"count": 31
}
```

`getcanwithdrawunfreezeamount ownerAddress timestamp`

*获取 `ownerAddress` 通过 `withdrawexpireunfreeze` 可以提取的解冻金额。*

- `ownerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址
- `timestamp` - 获取在此时间戳之前可提取的解冻金额

示例：
```
wallet> getCanWithdrawUnfreezeAmount TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 1671100335000
{
	"amount": 9000000
}
```
<a id="transaction"></a>
### 交易

#### 签名交易

> SendCoin TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW 10000000000000000

以下是一个使用账户权限管理功能的交易示例。其中，签名账户的授权情况请参考 修改账户权限 部分的示例。

```
wallet> sendcoin TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE 10
{
	"raw_data":{
		"contract":[
	...
	"raw_data_hex":"0a029ca12208432ed1fe1357ff7f40c0c484f19a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a708a8481f19a30"
}
before sign transaction hex string is 0a83010a029ca12208432ed1fe1357ff7f40c0c484f19a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a708a8481f19a30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
2
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
1
Please input your password.
password: 
Current signWeight is:
{
	"result":{
		"code":"NOT_ENOUGH_PERMISSION"
	},
	"approved_list":[
		"TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej"
	],
	"permission":{
		"operations":"7fff1fc0033e0000000000000000000000000000000000000000000000000000",
		"keys":[
			{
				"address":"TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej",
				"weight":1
			},
			{
				"address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
				"weight":1
			}
		],
		"threshold":2,
		"id":2,
		"type":"Active",
		"permission_name":"active12323"
	},
	"current_weight":1,
	"transaction":{
		"raw_data":{
			"contract":[
				{
					"parameter":{
						"value":{
							"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
							"to_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
							"amount":10
						},
						"type_url":"type.googleapis.com/protocol.TransferContract"
					},
					"type":"TransferContract"
				}
			],
			"ref_block_bytes":"9ca1",
			"ref_block_hash":"432ed1fe1357ff7f",
			"expiration":1656403217000,
			"timestamp":1656403157297
		},
		"signature":[
			"a32b906a5b6f00f023d5a4208a0d2445c75463f822a16d56f6c0f836f3325e6488d57d76a08605330e2f3d532a849f2b389ed94819d9b4b0051e5052994f0e0d01"
		]
	},
	"permission_id":2
}
...
```



#### 广播交易 - `BroadcastTransaction`
> 广播交易，其中交易是 HexString 格式。

#### 根据交易获取权重信息 - `getTransactionSignWeight`
> 0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101

信息显示如下：

```json
{
    "result":{
        "code":"PERMISSION_ERROR",
        "message":"Signature count is 2 more than key counts of permission : 1"
    },
    "permission":{
        "operations":"7fff1fc0033e0100000000000000000000000000000000000000000000000000",
        "keys":[
            {
                "address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                "weight":1
            }
        ],
        "threshold":1,
        "id":2,
        "type":"Active",
        "permission_name":"active"
    },
    "transaction":{
        "result":{
            "result":true
        },
        "txid":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
        "transaction":{
            "signature":[
                "c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b01",
                "3d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101"
            ],
            "txID":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
            "raw_data":{
                "contract":[
                    {
                        "parameter":{
                            "value":{
                                "amount":10000000000000000,
                                "owner_address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                                "to_address":"TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                            },
                            "type_url":"type.googleapis.com/protocol.TransferContract"
                        },
                        "type":"TransferContract",
                        "Permission_id":2
                    }
                ],
                "ref_block_bytes":"0318",
                "ref_block_hash":"60e195d3609c8661",
                "expiration":1554123306262,
                "timestamp":1554101706260
            },
            "raw_data_hex":"0a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d"
        }
    }
}
```

#### 根据交易获取签名信息 - `getTransactionApprovedList`
> 0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101

```json
{
    "result":{

    },
    "approved_list":[
        "TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP",
        "TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR"
    ],
    "transaction":{
        "result":{
            "result":true
        },
        "txid":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
        "transaction":{
            "signature":[
                "c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b01",
                "3d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101"
            ],
            "txID":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
            "raw_data":{
                "contract":[
                    {
                        "parameter":{
                            "value":{
                                "amount":10000000000000000,
                                "owner_address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                                "to_address":"TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                            },
                            "type_url":"type.googleapis.com/protocol.TransferContract"
                        },
                        "type":"TransferContract",
                        "Permission_id":2
                    }
                ],
                "ref_block_bytes":"0318",
                "ref_block_hash":"60e195d3609c8661",
                "expiration":1554123306262,
                "timestamp":1554101706260
            },
            "raw_data_hex":"0a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d"
        }
    }
}
```
<a id="query_chain_data"></a>
### 查询链上数据

#### 查看本地交易历史 - `ViewTransactionHistory`

> 查看本地wallet-cli的交易历史。您可以配置 `config.conf` 中的 `maxRecords` 来保留的最大记录数，不包括缓冲区记录。

示例：
```
wallet> ViewTransactionHistory
====================================
        TRANSACTION VIEWER
====================================

MAIN MENU:
1. View all transactions
2. Filter by time range
3. Help
4. Exit
Select option: 1
```

#### 如何获取交易信息
`GetTransactionById`
> 根据 transaction ID 获取交易信息。

`GetTransactionCountByBlockNum`
> 根据 block height 获取区块中的交易数量。

`GetTransactionInfoById`
> 根据 transaction ID 获取 transaction-info，通常用于检查智能合约触发的结果。

`GetTransactionInfoByBlockNum`
> 根据 block height 获取区块中的交易信息列表。

#### 获取链上参数 - `GetChainParameters`
> 展示区块链委员会可以设置的所有参数。


#### 获取资源价格和 memo fee 
`getbandwidthprices`
> 获取 Bandwidth 的历史单价。

示例：
```
wallet> getBandwidthPrices
{
    "prices": "0:10,1606537680000:40,1614238080000:140,1626581880000:1000,1626925680000:140,1627731480000:1000"
}
```

`getenergyprices`
> 获取 Energy 的历史单价。

示例：
```
wallet> getEnergyPrices
{
    "prices": "0:100,1575871200000:10,1606537680000:40,1614238080000:140,1635739080000:280,1681895880000:420"
}
```

`getmemofee`
> 获取 memo fee。

示例：
```
wallet> getMemoFee
{
    "prices": "0:0,1675492680000:1000000"
}
```

#### 如何获取区块信息

`GetBlock`
> 根据 block number 获取区块；如果您不传递参数，则获取最新区块。

`GetBlockById`
> 根据 blockID 获取区块。

`GetBlockByIdOrNum`
> 根据 ID 或 block height 获取区块。如果不传递参数，则获取 header block。

`GetBlockByLatestNum n`
> 获取最新的 n 个区块，其中 0 < n < 100。

`GetBlockByLimitNext startBlockId endBlockId`
> 获取范围 [startBlockId, endBlockId) 内的区块。

#### 其他链上数据相关命令

`GetNextMaintenanceTime`
> 获取下一个维护期的开始时间。

`ListNodes`
> 获取其他 peer 信息。

`ListWitnesses`
> 获取所有 miner node 信息。

#### 当前网络 - `CurrentNetwork`
> 查看当前网络。

示例：
```
wallet> currentnetwork
currentNetwork: NILE
```
```
wallet> currentnetwork
current network: CUSTOM
fullNode: EMPTY, solidityNode: localhost:50052
```
<a id="contract"></a>
### 智能合约

#### 部署智能合约

```
DeployContract [ownerAddress] contractName ABI byteCode constructor params isHex fee_limit consume_user_resource_percent origin_energy_limit value token_value token_id(e.g: TRXTOKEN, use # if don't provided) <library:address,library:address,...> <lib_compiler_version(e.g:v5)> library:address,...>
```

- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址
- `contractName` - 智能合约名称
- `ABI` - 编译生成的 ABI 代码
- `byteCode` - 编译生成的字节码
- `constructor`, `params`, `isHex` - 定义字节码的格式，决定从参数解析字节码的方式
- `fee_limit` - 交易允许消耗的最大TRX
- `consume_user_resource_percent` - 用户资源消耗的百分比，范围在 [0, 100]
- `origin_energy_limit` - 触发合约一次开发者消耗的最大 Energy 量
- `value` - 转移到合约账户的 TRX 数量
- `token_value` - TRX-10 数量
- `token_id` - TRX-10 ID

示例：

```
> deployContract normalcontract544 [{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name": "findArgsByIndexTest","outputs":[{"name":"z","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]
608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029 # # false 1000000000 75 50000 0 0 #
```

使用 `getTransactionInfoById` 命令获取合约执行结果：

```
> getTransactionInfoById 4978dc64ff746ca208e51780cce93237ee444f598b24d5e9ce0da885fb3a3eb9
{
    "id": "8c1f57a5e53b15bb0a0a0a0d4740eda9c31fbdb6a63bc429ec2113a92e8ff361",
    "fee": 6170500,
    "blockNumber": 1867,
    "blockTimeStamp": 1567499757000,
    "contractResult": [
        "6080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029"
    ],
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "receipt": {
        "energy_fee": 6170500,
        "energy_usage_total": 61705,
        "net_usage": 704,
        "result": "SUCCESS"
    }
}
```

#### 触发智能合约 
```
TriggerContract [ownerAddress] contractAddress method args isHex fee_limit value token_value token_id
```
- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址
- `contractAddress` - 智能合约地址
- `method` - 函数名称和参数，请参考示例
- `args` - 参数值，如果要调用 `receive`，请传入'#'
- `isHex` - 参数 `method` 和 `args` 的格式，是否为十六进制字符串
- `fee_limit` - 允许消耗的最大 TRX 数量
- `token_value` - TRX-10数量
- `token_id` - TRC-10 ID，如果没有，请使用'#'代替

示例：

```
> triggerContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG findArgsByIndexTest(uint256) 0 false
1000000000 0 0 #
# 使用getTransactionInfoById命令获取合约执行结果
> getTransactionInfoById 7d9c4e765ea53cf6749d8a89ac07d577141b93f83adc4015f0b266d8f5c2dec4
{
    "id": "de289f255aa2cdda95fbd430caf8fde3f9c989c544c4917cf1285a088115d0e8",
    "fee": 8500,
    "blockNumber": 2076,
    "blockTimeStamp": 1567500396000,
    "contractResult": [
        ""
    ],
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "receipt": {
        "energy_fee": 8500,
        "energy_usage_total": 85,
        "net_usage": 314,
        "result": "REVERT"
    },
    "result": "FAILED",
    "resMessage": "REVERT opcode executed"
}
```

#### 触发常量合约

```
TriggerConstantContract [ownerAddress] contractAddress method args isHex fee_limit value token_value token_id
```
- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址。
- `contractAddress` - 智能合约地址
- `method` - 函数名称和参数，请参考示例
- `args` - 参数值，如果要调用 `receive`，请传入 `#`
- `isHex` - 参数 `method` 和 `args` 的格式，是否为十六进制字符串
- `fee_limit` - 允许消耗的最大 TRX 数量
- `token_value` - TRX-10 数量
- `token_id` - TRC-10 ID，如果没有，请使用 `#` 代替

示例：

```
> TriggerConstantContract TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs "balanceOf(address)" 000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c true
```

#### 预测合约地址 - `Create2 address code salt`

>预测部署合约后生成的合约地址。其中，`address` 是执行 `create2` 指令的合约地址，`code` 是待部署合约的字节码，`salt` 是一个随机的 `salt` 值。

示例：
```
> Create2 TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 5f805460ff1916600190811790915560649055606319600255 > 2132
```

#### 能量消耗估算

```
EstimateEnergy owner_address(use # if you own) contract_address method args isHex [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]
```

> 估计智能合约交易成功执行所需的 Energy（已确认状态）。

示例：

```
> EstimateEnergy TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs "balanceOf(address)" 000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c true
```

#### 清除合约 ABI - `ClearContractABI [ownerAddress] contractAddress`
- `OwnerAddress` - 发起交易的账户地址，可选，默认为登录账户的地址。
- `contractAddress` - 合约地址

示例：
```
> ClearContractABI TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs
```

#### 获取智能合约详情 - `GetContract contractAddress`

- `contractAddress` - 智能合约地址

示例：
```
> GetContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
{
    "origin_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "abi": {
        "entrys": [
            {
                "name": "findArgsByIndexTest",
                "inputs": [
                    {
                        "name": "i",
                        "type": "uint256"
                    }
                ],
                "outputs": [
                    {
                        "name": "z",
                        "type": "uint256"
                    }
                ],
                "type": "Function",
                "stateMutability": "Nonpayable"
            }
        ]
    },
    "bytecode": "608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029",
    "consume_user_resource_percent": 75,
    "name": "normalcontract544",
    "origin_energy_limit": 50000,
    "code_hash": "23423cece3b4866263c15357b358e5ac261c218693b862bcdb90fa792d5714e6"
}
```

#### 获取智能合约信息 - `GetContractInfo contractAddress`

- `contractAddress` - 智能合约地址

示例：

```
> GetContractInfo TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
```

#### 更新智能合约参数

```
UpdateEnergyLimit [ownerAddress] contract_address energy_limit  # 更新参数energy_limit
> UpdateSetting [ownerAddress] contract_address consume_user_resource_percent  # 更新参数consume_user_resource_percent
```


<a id="trc-10"></a>
### TRC-10 资产

#### 如何发行 TRC-10 代币

每个账户只能发行**一个** TRC-10 代币。

##### 发行 TRC-10 代币

```
AssetIssue [OwnerAddress] AssetName AbbrName TotalSupply TrxNum AssetNum Precision StartDate EndDate Description Url FreeNetLimitPerAccount PublicFreeNetLimit FrozenAmount0 FrozenDays0 [...] FrozenAmountN FrozenDaysN
```

- `OwnerAddress` (可选) - 发起交易的账户地址。默认为登录账户的地址。
- `AssetName` - 发行的 TRC-10 代币名称
- `AbbrName` - TRC-10 代币的缩写
- `TotalSupply`
    > `TotalSupply` = 发行者的账户余额 + 所有冻结的代币数量
    > `TotalSupply`：总发行量
    > 发行者的账户余额：在发行时
    > 所有冻结的代币数量：在资产转移和发行之前
- `TrxNum`, `AssetNum`
    > 这两个参数决定了代币发行时的兑换率。
    > 兑换率 = `TrxNum` / `AssetNum`
    > `AssetNum`：发行的代币的单位，以基础单位计
    > `TrxNum`：单位为 sun（0.000001 TRX）
- `Precision` - 精确到小数点后几位
- `FreeNetLimitPerAccount` - 每个账户允许使用的最大 Bandwidth 量。代币发行者可以冻结 TRX 来获取 Bandwidth（仅限于 `TransferAssetContract`）
- `PublicFreeNetLimit` - 允许所有账户使用的最大 Bandwidth 总量。代币发行者可以冻结 TRX 来获取 Bandwidth（仅限于 `TransferAssetContract`）
- `StartDate`, `EndDate` - 代币发行的开始和结束日期。在此期间，其他用户可以参与代币发行。
- `FrozenAmount0`, `FrozenDays0`
    > 代币冻结的数量和天数。
    > `FrozenAmount0`：必须大于 0
    > `FrozenDays0`：必须在 1 到 3653 之间。

示例：

```
> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # 查看已发布的信息
{
    "assetIssue": [
        {
            "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "name": "TestTRX",
            "abbr": "TRX",
            "total_supply": 75000000000000000,
            "frozen_supply": [
                {
                    "frozen_amount": 10000,
                    "frozen_days": 1
                },
                {
                    "frozen_amount": 10000,
                    "frozen_days": 10
                }
            ],
            "trx_num": 1,
            "precision": 2,
            "num": 1,
            "start_time": 1570000200000,
            "end_time": 1594396800000,
            "description": "just for test121212",
            "url": "www.test.com",
            "free_asset_net_limit": 100,
            "public_free_asset_net_limit": 100000,
            "id": "1000001"
        }
    ]
}
```

##### 更新 TRC-10 代币的参数
```
UpdateAsset [OwnerAddress] newLimit newPublicLimit description url
```
- 参数的具体含义与 `AssetIssue` 相同。

示例：

```
> UpdateAsset 1000 1000000 "change description" www.changetest.com
> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # 查看已修改的信息
{
    "assetIssue": [
        {
            "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "name": "TestTRX",
            "abbr": "TRX",
            "total_supply": 75000000000000000,
            "frozen_supply": [
                {
                    "frozen_amount": 10000,
                    "frozen_days": 1
                },
                {
                    "frozen_amount": 10000,
                    "frozen_days": 10
                }
            ],
            "trx_num": 1,
            "precision": 2,
            "num": 1,
            "start_time": 1570000200000,
            "end_time": 1594396800000,
            "description": "change description",
            "url": "www.changetest.com",
            "free_asset_net_limit": 1000,
            "public_free_asset_net_limit": 1000000,
            "id": "1000001"
        }
    ]
}
```

#### 参与 TRC-10 代币发行
```
ParticipateAssetIssue [OwnerAddress] ToAddress AssetID Amount
```

- `OwnerAddress` (可选) - 发起交易的账户地址。默认：登录账户的地址
- `ToAddress` - TRC-10 发行者的账户地址
- `AssertName` - TRC-10 代币 ID。示例：1000001
- `Amount` - 转移的 TRC-10 代币数量

> 参与过程必须在 TRC-10 发行期间进行，否则可能会发生错误。

示例：

```
> ParticipateAssetIssue TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 1000001 1000
> getaccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  # 查看剩余余额
address: TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```

#### 解冻 TRC-10 代币 - `unfreezeasset [OwnerAddress]`

> 用于解冻所有在冻结期后本应解冻的 TRC-10 代币。

#### TRC-10 代币转账 - `TransferAsset [OwnerAddress] ToAddress AssertID Amount`

- `OwnerAddress` (可选) - 发起交易的账户地址。默认：登录账户的地址
- `ToAddress` - 目标账户的地址
- `AssertName` - TRC-10 代币 ID。示例：1000001
- `Amount` - 要转移的 TRC-10 代币数量

示例：

```
> TransferAsset TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz 1000001 1000
> getaccount TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz  # 查看转账后的目标账户信息
address: TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz
    assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```

#### 如何获取 TRC-10 代币信息

`ListAssetIssue`
> 获取所有已发布的 TRC-10 代币信息

`GetAssetIssueByAccount`
> 根据发行地址获取 TRC-10 代币信息

`GetAssetIssueById`
> 根据 ID 获取 TRC-10 代币信息

`GetAssetIssueByName`
> 根据名称获取 TRC-10 代币信息

`GetAssetIssueListByName`
> 根据名称获取 TRC-10 代币信息列表

#### 分页列出资产发行 - `ListAssetIssuePaginated address code salt`

> 按分页查询所有代币列表。返回从偏移量位置成功后的代币列表。

示例：

```
> ListAssetIssuePaginated 0 1
```

-----

<a id="governance"></a>
### 治理

#### 如何投票

投票需要 Share。Share 可以通过冻结资金获得。

* Share 计算方法是：每冻结 **1 TRX**，可获得 **1** 单位的 Share。
* 解冻后，先前的投票将失效。您可以通过重新冻结和投票来避免投票失效。

**注意** TRON 网络只记录您最后一次的投票状态，这意味着您的每一次投票都将覆盖所有先前的投票结果。

示例：

```
> freezeBalance 100000000 3 1 address  # 冻结 10 TRX 并获得 10 单位的 Shares
> votewitness 123455 witness1 4 witness2 6  # 同时为 SR1 投 4 票，为 SR2 投 6 票
> votewitness 123455 witness1 10  # 为 witness1 投 10 票
```

上述命令的最终结果是为 SR1 投了 10  票，为 SR2 投了 0 票。

#### 代理（Brokerage）

投票给 SR 后，您将获得奖励。SR 有权决定代理的比例（brokerage）。默认比例为 20%，SR 可以进行调整。

默认情况下，如果一个 SR 获得奖励，他将获得全部奖励的20%，80%的奖励将分配给他的投票者。

##### 查看 SR 的代理比例（brokerage） - `getbrokerage OwnerAddress`
- `OwnerAddress` - SR 账户的地址，是 base58check 类型的地址。

##### 查询未领取的奖励 - getreward OwnerAddress

- `OwnerAddress` - 投票者账户的地址，是 base58check 类型的地址。

##### 更新代理比例 - `updateBrokerage OwnerAddress brokerage`

> 此命令通常由 SR 账户使用。

- `OwnerAddress` - witness账户的地址，是base58check类型的地址。
- `brokerage` - 您想要更新的代理比例（brokerage），范围从 0 到 100。如果输入 10，则表示总奖励的 10% 将分配给 SR，其余部分（本例中为 90%）将奖励给所有投票者。

示例：

```
> getbrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h  
> getreward  TNfu3u8jo1LDWerHGbzs2Pv88Biqd85wEY
> updateBrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h 30
```

##### 提取投票或区块奖励 - WithdrawBalance [owner_address]

示例：

```
> WithdrawBalance TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp
```

#### 如何创建超级代表（SR）

申请成为 SR 账户需要消耗 100_000 TRX。这部分资金将被直接销毁（burned）。

##### 创建 SR - `CreateWitness [owner_address] url`
> 申请成为超级代表候选人。

示例：
```
> CreateWitness TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 007570646174654e616d6531353330363038383733343633
```

##### 更新 SR - `UpdateWitness`
> 编辑SR官网的URL。

示例：
```
> UpdateWitness TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 007570646174654e616d6531353330363038383733343633
```

#### 如何提取余额

每个区块产生后，区块奖励会发送到账户的 allowance，并且每**24小时**允许从 allowance 提取一次到 balance。allowance 中的资金不能被锁定或交易。

#### 如何操作提案

任何与提案相关的操作（查看操作除外），都必须由委员会成员执行。

##### 发起提案 - `createProposal [OwnerAddress] id0 value0 ... idN valueN`

- OwnerAddress (可选) - 发起交易的账户地址。默认：登录账户的地址
- `id0` - 参数的序列号。TRON 网络的每个参数都有一个序列号。请参考 http://tronscan.org/#/sr/committee
- `Value0` - 修改后的值

在本例中，修改第4号（修改代币发行费用）的成本为 1000 TRX，如下所示：

```
> createProposal 4 1000
> listproposals  # 查看已发起的提案
{
    "proposals": [
        {
            "proposal_id": 1,
            "proposer_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "parameters": [
                {
                    "key": 4,
                    "value": 1000
                }
            ],
            "expiration_time": 1567498800000,
            "create_time": 1567498308000
        }
    ]
}
```

相应的 id 是 1。

##### 批准/不批准提案 - `approveProposal [OwnerAddress] id is_or_not_add_approval`

- `OwnerAddress` (可选) - 发起交易的账户地址。默认：登录账户的地址。
- `id` - 已发起提案的 ID。示例：1
- `is_or_not_add_approval` - `true` 表示批准；`false` 表示不批准

示例：

```
> ApproveProposal 1 true  # 赞成该提案
> ApproveProposal 1 false  # 取消已批准的提案
```

##### 删除现有提案- -`deleteProposal [OwnerAddress] proposalId`

- `proposalId` - 已发起提案的 ID。示例：1

> 提案必须由发起该提案的超级节点取消。

示例：

> DeleteProposal 1

##### 获取提案信息

`ListProposals`
> 获取已发起提案的列表

`ListProposalsPaginated`
> 使用分页模式获取已发起的提案

`GetProposal`
> 根据提案 ID 获取提案信息


<a id="defi"></a>
### 去中心化交易所

交易对的交易和价格波动遵循 Bancor 协议，可在 TRON 代码库的 [相关文档](https://tronprotocol.github.io/documentation-en/clients/wallet-cli-command/#dex) 中找到。

#### 创建交易对
```
exchangeCreate [OwnerAddress] first_token_id first_token_balance second_token_id second_token_balance
```

- `OwnerAddress` (可选) - 发起交易的账户地址。默认：登录账户的地址。
- `First_token_id`, `first_token_balance` - 第一个代币的ID和数量
- `second_token_id`, `second_token_balance` - 第二个代币的ID和数量
    > ID 是已发行的 TRC-10 代币的 ID。
    > 如果是 TRX，ID 为 “_”。
    > 数量必须大于 0，且小于 1,000,000,000,000,000。

示例：

```
exchangeCreate 1000001 10000 _ 10000
# 创建ID为1000001和TRX的交易对，两者数量均为10000。
```

#### 根据 id 获取交易所信息 - `getExchange`

> 根据 id 查询交易对（已确认状态）。

示例：

```
> getExchange 1
```

#### 注资 - `exchangeInject [OwnerAddress] exchange_id token_id quant`

- `OwnerAddress` (可选) - 发起交易的账户地址。默认：登录账户的地址。
- `exchange_id` - 要注资的交易对的ID
- `token_id`, `quant` - 注资的代币ID和数量（单位以基础单位计）

> 进行注资时，根据其数量（quant），交易对中每个代币的一部分将从账户中提取，并注入到交易对中。根据交易余额的差异，同一代币的相同数量的资金也会有所不同。

#### 交易 - `exchangeTransaction [OwnerAddress] exchange_id token_id quant expected`

- `OwnerAddress` (可选) - 发起交易的账户地址。默认：登录账户的地址。
- `exchange_id` - 交易对的ID
- `token_id`, `quant` - 要交易的代币ID和数量，相当于卖出
- `expected` - 另一个代币的预期数量。
    > expected 必须小于 quant，否则将报错。

示例：

> ExchangeTransaction 1 1000001 100 80

预期通过将交易对 ID 为 1 的 1000001 代币中的 100 个，以 80 TRX 的价格换取 80 TRX。（相当于在 ID 为 1 的交易对中，以 80 TRX 的价格卖出 100 个 ID 为 1000001 的代币）。

#### 撤资 - `exchangeWithdraw [OwnerAddress] exchange_id token_id quant`

- `OwnerAddress` (可选) - 发起交易的账户地址。默认：登录账户的地址。
- `exchange_id` - 要撤资的交易对的 ID
- `token_id`, `quant` - 撤资的代币 ID 和数量（单位以基础单位计）

> 进行撤资时，根据其数量（quant），交易对中每个代币的一部分将从交易对中提取，并注入到账户中。根据交易余额的差异，同一代币的相同数量的资金也会有所不同。

#### 获取交易对信息

`ListExchanges`
> 列出交易对

`ListExchangesPaginated`
> 按页列出交易对

#### 如何使用 tron-dex 出售资产

##### 创建一个卖出资产的订单
```
MarketSellAsset owner_address sell_token_id sell_token_quantity buy_token_id buy_token_quantity
```
- `ownerAddress` - 发起交易的账户地址。
- `sell_token_id`, `sell_token_quantity` - 想要卖出的 token ID 和数量。
- `buy_token_id`, `buy_token_quantity` - 想要买入的 token ID 和数量。

示例：

```
MarketSellAsset TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  1000001 200 _ 100

使用 getTransactionInfoById 命令获取合约执行结果：
getTransactionInfoById 10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374

{
	"id": "10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374",
	"blockNumber": 669,
	"blockTimeStamp": 1578983493000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 264
	}
}
```

##### 获取账户创建的订单（仅包含 active 状态）- `GetMarketOrderByAccount ownerAddress`
- `ownerAddress` - 创建市场订单的账户地址。

示例：

```
GetMarketOrderByAccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
{
	"orders": [
		{
			"order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
			"owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
			"create_time": 1578983490000,
			"sell_token_id": "_",
			"sell_token_quantity": 100,
			"buy_token_id": "1000001",
			"buy_token_quantity": 200,
			"sell_token_quantity_remain": 100
		}
	]
}
```

##### 根据 `order_id` 获取特定订单 - `GetMarketOrderById orderId`

示例：

```
GetMarketOrderById fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0
{
	"order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
	"owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
	"create_time": 1578983490000,
	"sell_token_id": "_",
	"sell_token_quantity": 100,
	"buy_token_id": "1000001",
	"buy_token_quantity": 200,
}
```

##### 获取市场交易对列表 - `GetMarketPairList`

示例：

```
GetMarketPairList
{
	"orderPair": [
		{
			"sell_token_id": "_",
			"buy_token_id": "1000001"
		}
	]
}
```

##### 根据交易对获取订单列表 - `GetMarketOrderListByPair sell_token_id buy_token_id`

- `sell_token_id` - 想要卖出的 token ID。
- `buy_token_id` - 想要买入的 token ID。

示例：

```
GetMarketOrderListByPair _ 1000001
{
	"orders": [
		{
			"order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
			"owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
			"create_time": 1578983490000,
			"sell_token_id": "_",
			"sell_token_quantity": 100,
			"buy_token_id": "1000001",
			"buy_token_quantity": 200,
			"sell_token_quantity_remain": 100
		}
	]
}
```

##### 根据交易对获取市场价格 - `GetMarketPriceByPair sell_token_id buy_token_id`
- `sell_token_id` - 想要卖出的 token ID。
- `buy_token_id` - 想要买入的 token ID。

示例：

```
GetMarketPriceByPair _ 1000001
{
	"sell_token_id": "_",
	"buy_token_id": "1000001",
	"prices": [
		{
			"sell_token_quantity": 100,
			"buy_token_quantity": 200
		}
	]
}
```

##### 取消订单 - `MarketCancelOrder owner_address order_id`
- `owner_address` - 创建订单的账户地址。
- `order_id`- 想要取消的 order ID。

示例：

```
MarketCancelOrder TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0
```

使用 `getTransactionInfoById` 命令获取合约执行结果：
```
getTransactionInfoById b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27
{
	"id": "b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27",
	"blockNumber": 1582,
	"blockTimeStamp": 1578986232000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 283
	}
}
```


<a id="gasfree"></a>
### GasFree 支持

`wallet-cli` 现在支持 **GasFree** 集成。本指南解释了新的命令并提供了如何使用它们的说明。

有关更多详细信息，请参阅 [GasFree Documentation](https://gasfree.io/specification) 和 [TronLink User Guide For GasFree](https://support.tronlink.org/hc/en-us/articles/38903684778393-GasFree-User-Guide)。

前提条件
API Credentials: 用户必须从 **GasFree** 获取 API Key 和 API Secret 以进行身份验证。请参阅官方 [application form](https://docs.google.com/forms/d/e/1FAIpQLSc5EB1X8JN7LA4SAVAG99VziXEY6Kv6JxmlBry9rUBlwI-GaQ/viewform) 以获取设置 API 身份验证的说明。


#### 查询 GasFree 信息 - `GasFreeInfo`
> 查询 GasFree 信息。
> 功能：检索基本信息，包括与当前钱包地址关联的 **GasFree** 地址。
> 注意：GasFree 地址在首次转账时自动激活，可能会产生激活费用。

示例：
```
wallet> gasfreeinfo
balanceOf(address):70a08231
{
	"gasFreeAddress":"TCtSt8fCkZcVdrGpaVHUr6P8EmdjysswMF",
	"active":true,
	"tokenBalance":998696000,
	"activateFee":0,
	"transferFee":2000,
	"maxTransferValue":998694000
}
gasFreeInfo: successful !!
```
```
wallet> gasfreeinfo TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe
balanceOf(address):70a08231
{
	"gasFreeAddress":"TCtSt8fCkZcVdrGpaVHUr6P8EmdjysswMF",
	"active":true,
	"tokenBalance":998696000,
	"activateFee":0,
	"transferFee":2000,
	"maxTransferValue":998694000
}
gasFreeInfo: successful !!
```

#### 提交 **GasFree** 转账 - `GasFreeTransfer`
> 功能：提交一笔 gasfree 代币转账请求。

示例：
```
wallet> gasfreetransfer TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT 100000

GasFreeTransfer result: {
	"code":200,
	"data":{
		"amount":100000,
		"providerAddress":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E",
		"apiKey":"",
		"accountAddress":"TUUSMd58eC3fKx3fn7whxJyr1FR56tgaP8",
		"signature":"",
		"targetAddress":"TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT",
		"maxFee":2000000,
		"version":1,
		"nonce":8,
		"tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf",
		"createdAt":1747909635678,
		"expiredAt":1747909695000,
		"estimatedTransferFee":2000,
		"id":"6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0",
		"state":"WAITING",
		"estimatedActivateFee":0,
		"gasFreeAddress":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER",
		"updatedAt":1747909635678
	}
}
GasFreeTransfer successful !!!
```

#### 追踪转账状态 - `GasFreeTrace`
> 功能：使用从 `GasFreeTransfer` 获取的 traceId 检查 GasFree 转账的进度。

示例：
```
wallet> gasfreetrace 6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0
GasFreeTrace result: {
	"code":200,
	"data":{
		"amount":100000,
		"providerAddress":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E",
		"txnTotalCost":102000,
		"accountAddress":"TUUSMd58eC3fKx3fn7whxJyr1FR56tgaP8",
		"txnActivateFee":0,
		"estimatedTotalCost":102000,
		"targetAddress":"TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT",
		"txnBlockTimestamp":1747909638000,
		"txnTotalFee":2000,
		"nonce":8,
		"estimatedTotalFee":2000,
		"tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf",
		"txnHash":"858f9a00776163b1f8a34467b9c5727657f8971a9f4e9d492f0a247fac0384f9",
		"txnBlockNum":57175988,
		"createdAt":1747909635678,
		"expiredAt":1747909695000,
		"estimatedTransferFee":2000,
		"txnState":"ON_CHAIN",
		"id":"6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0",
		"state":"CONFIRMING",
		"estimatedActivateFee":0,
		"gasFreeAddress":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER",
		"txnTransferFee":2000,
		"txnAmount":100000
	}
}
GasFreeTrace: successful!!
```


<a id="other"></a>
### 其他实用命令

#### 切换网络 - `SwitchNetwork`
> 此命令允许随时灵活切换网络。
> `switchnetwork local` 将切换到在本地 config.conf 中配置的网络。

示例：

```
wallet> switchnetwork
Please select network：
1. MAIN
2. NILE
3. SHASTA
Enter numbers to select a network (1-3):1
Now, current network is : MAIN
SwitchNetwork successful !!!
```

```
wallet> switchnetwork main
Now, current network is : MAIN
SwitchNetwork successful !!!
```

```
wallet> switchnetwork empty localhost:50052
Now, current network is : CUSTOM
SwitchNetwork successful !!!
```

#### 切换钱包 - `SwitchWallet`
> 在使用 **LoginAll** 命令登录后，可以切换钱包。

示例：
```
wallet> switchwallet
The 1th keystore file name is TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB.json
The 2th keystore file name is TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew.json
The 3th keystore file name is TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7.json
The 4th keystore file name is Ledger-TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe.json
The 5th keystore file name is TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada.json
Please choose between 1 and 5
5
SwitchWallet successful !!!
```

#### 查看备份记录 - `ViewBackupRecords`

>查看备份记录。您可以配置 `config.conf` 中的 `maxRecords` 来保留的最大记录数，不包括缓冲区记录。

示例：
```
wallet> ViewBackupRecords

=== View Backup Records ===
1. View all records
2. Filter by time range
Choose an option (1-2): 1
```


