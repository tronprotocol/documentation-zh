# wallet-cli
## 简介
wallet-cli是一个支持TRON网络的交互式命令行钱包，用于在安全的本地环境中签名和广播交易，也可以获取链上数据。wallet-cli支持密钥管理，您可以将私钥导入钱包中，wallet-cli会使用对称加密算法加密您的私钥，并存储到一个keystore文件中。wallet-cli本地不存储链上数据，它采用gRPC的方式与某一个java-tron节点进行通信，您需要在配置文件中配置需要链接的java-tron节点，下图是使用wallet-cli签名和广播TRX转账交易的流程：
![](https://i.imgur.com/NRKmZmE.png)

用户首先运行`Login`命令解锁钱包，然后运行`SendCoin`命令发送TRX，wallet-cli会本地构建和签名交易，然后将调用java-tron节点的BroadcastTransaction gRPC API将交易广播的网络中，广播成功后java-tron节点会返回交易hash给wallet-cli，wallet-cli将交易hash展示给用户。

安装和运行: [wallet-cli](https://github.com/tronprotocol/wallet-cli)

## 命令
下面是wallet-cli钱包支持的命令分类:

- [密钥管理](#_3)
- [链上账户](#_4)
- [账户资源](#_5)
- [交易](#_6)
- [查询链上数据](#_7)
- [智能合约](#_8)
- [TRC-10资产](#trc-10)
- [治理](#_9)
- [去中心化交易所](#_10)
### 密钥管理
下面是账户地址相关命令：

- [RegisterWallet](#registerwallet)
- [Login](#login)
- [BackupWallet](#backupwallet)
- [BackupWallet2Base64](#backupwallet2base64)
- [ChangePassword](#changepassword)
- [ImportWallet](#importwallet)
- [ImportWalletByBase64](#importwalletbybase64)

#### RegisterWallet
注册时，需要先为账户设置密码，之后带有账户信息的json文件将会生成在`wallet-cli/wallet`路径中。账户地址即是文件名中base58格式的部分，如下面示例中的“TWyDBTHsWJFhgywWkTNW7vh7jSUxeBaiAw”：
```shell
wallet> RegisterWallet 
Please input password.
password: 
Please input password again.
password: 
Register a wallet successful, keystore file name is UTC--2022-06-27T07-37-47.601000000Z--TWyDBTHsWJFhgywWkTNW7vh7jSUxeBaiAw.json
```
#### Login
当钱包注册完成后，可以使用Login命令登陆钱包。选择你想要登陆的钱包地址，再输入密码完成登陆。
```shell
wallet> login
use user defined config file in current dir
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-06-22T08-31-57.735000000Z--TBnPDbw99BLzPUZuW8Rrcc3RGGQT3cnSfF.json
The 4th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 5th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 5
4
Please input your password.
password: 
Login successful !!!
```
#### BackupWallet
备份钱包时需要输入秘密，成功后将会导出你的私钥, 如下面示例中的
```
721d63b0...e5076545
```

```shell
wallet> backupwallet
Please input your password.
password: 
BackupWallet successful !!
721d63b0...e5076545
```
#### BackupWallet2Base64
备份钱包时需要输入秘密，成功后将会以base64格式导出你的私钥, 如下面示例中的
```
ch1j...ZUU=
```

```shell
wallet> backupwallet
Please input your password.
password: 
BackupWallet successful !!
ch1j...ZUU=
```
#### ChangePassword
使用本命令来更改密码
```shell
wallet> changepassword
Please input old password.
password: 
Please input new password.
Please input password.
password: 
Please input password again.
password: 
The 1th keystore file name is .DS_Store
The 2th keystore file name is UTC--2022-06-27T10-58-59.306000000Z--TBnPDbw99BLzPUZuW8Rrcc3RGGQT3cnSfF.json
Please choose between 1 and 2
2
ChangePassword successful !!
```


#### ImportWallet
在导入钱包时，需先为即将导入的私钥设置一个密码，之后再导入私钥，提示成功后，将会在`wallet-cli/wallet`路径下生成一个记录该钱包的json文件，请看示例：
```shell
wallet> importwallet
Please input password.
password: 
Please input password again.
password: 
Please input private key. Max retry time:3
bd1ff0f4...42a1fb5b
Import a wallet successful, keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
```
#### ImportWalletByBase64
在导入钱包时，需先为即将倒入的私钥设置一个密码，之后再导入base64格式的私钥，提示成功后，将会在`wallet-cli/wallet`路径下生成一个记录该钱包的json文件。
```shell
wallet> importwalletbybase64
Please input password.
password: 
Please input password again.
password: 
Please input private key by base64. Max retry time:3
...your private key...  
Import a wallet successful, keystore file name is UTC--2022-06-28T06-51-56.154000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json

```


### 链上账户
下面是账户地址相关命令：

- [GenerateAddress](#generateaddress)
- [GetAccount](#getaccount)
- [GetAddress](#getaddress)
- [GetBalance](#getbalance)
- [UpdateAccountPermission](#updateaccountpermission)

#### GenerateAddress
使用该命令生成一个新的钱包地址和它的私钥
```shell
wallet> generateaddress
{
	"address": "TQAvi6bemLa1t1irdV1KuaSC5vKc2EswTj",
	"privateKey": "610a8a80...642c297e"
}
```
**注意：** 生成的地址及其私钥不会被保存，如需使用请单独留存。
#### GetAccount
使用地址获得账户相关信息，可以查询账户余额，创建时间及分配权限的情况等
```shell
wallet> getaccount [address]
```
示例：
```shell
wallet> getaccount TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
{
	"address": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
	"balance": 2665198240,
	"create_time": 1650363711000,
	"latest_opration_time": 1653578769000,
	"latest_consume_free_time": 1651228080000,
	"account_resource": {
		"latest_consume_time_for_energy": 1653578769000
	},
	"owner_permission": {
		"permission_name": "owner",
		"threshold": 1,
		"keys": [
			{
				"address": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
				"weight": 1
			}
		]
	},
	"active_permission": [
		{
			"type": "Active",
			"id": 2,
			"permission_name": "active",
			"threshold": 1,
			"operations": "7fff1fc0033e3b00000000000000000000000000000000000000000000000000",
			"keys": [
				{
					"address": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
					"weight": 1
				}
			]
		}
	]
}

```
#### GetAddress

使用该命令立即获得当前登陆账户的地址
```shell
wallet> getaddress
GetAddress successful !!
address = TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
```

#### GetBalance
使用该命令查询当前登陆账户的余额
```shell
wallet> getbalance
Balance = 2665198240
```

#### UpdateAccountPermission
该命令用于管理账户权限，为其他账户赋予当前账户的部分权限，让其他账户可以在该发起账户下完成多种操作以便实现更复杂的功能及更好的管理账户。
```shell
wallet>UpdateAccountPermission [ownerAddress] [permissions]
```

权限分为如下三种： 

* `owner`: 拥有账户的所有权限。
* `active`: 可以获得账户中的特定权限，如果是witness权限则不包括出块权利。
* `witness`: 只用于超级代表, 出块的权利将会被授予其他账户。

**注意** 参数`Permission` 必须按json格式传入且不能换行。如果owner账户不是超级代表，则不要授权witness权限给其他账户。

示例：
```shell
wallet> updateaccountpermission TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8 {"owner_permission":{"keys":[{"address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8","weight":1}],"threshold":1,"type":0,"permission_name":"owner"},"active_permissions":[{"operations":"7fff1fc0033e0000000000000000000000000000000000000000000000000000","keys":[{"address":"TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej","weight":1},{"address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE","weight":1}],"threshold":2,"type":2,"permission_name":"active12323"}]}
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"owner":{
							"keys":[
								{
									"address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
									"weight":1
								}
							],
							"threshold":1,
							"permission_name":"owner"
						},
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
						"actives":[
							{
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
								"type":"Active",
								"permission_name":"active12323"
							}
						]
					},
					"type_url":"type.googleapis.com/protocol.AccountPermissionUpdateContract"
				},
				"type":"AccountPermissionUpdateContract"
			}
		],
		"ref_block_bytes":"4e88",
		"ref_block_hash":"11a47859be13f689",
		"expiration":1656423231000,
		"timestamp":1656423171818
	},
	"raw_data_hex":"0a024e88220811a47859be13f6894098dc92d49a305aee01082e12e9010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e747261637412a8010a1541babecec4d9f58f0df77f0728b9c53abb1f21d68412241a056f776e657220013a190a1541babecec4d9f58f0df77f0728b9c53abb1f21d6841001226908021a0b6163746976653132333233200232207fff1fc0033e00000000000000000000000000000000000000000000000000003a190a15410cfaec7164cbfe78dbb8d8fba7e23b4d745ed81310013a190a1541e8bd653015895947cec33d1670a88cf67ab277b9100170ea8d8fd49a30"
}
before sign transaction hex string is 0a8d020a024e88220811a47859be13f6894098dc92d49a305aee01082e12e9010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e747261637412a8010a1541babecec4d9f58f0df77f0728b9c53abb1f21d68412241a056f776e657220013a190a1541babecec4d9f58f0df77f0728b9c53abb1f21d6841001226908021a0b6163746976653132333233200232207fff1fc0033e00000000000000000000000000000000000000000000000000003a190a15410cfaec7164cbfe78dbb8d8fba7e23b4d745ed81310013a190a1541e8bd653015895947cec33d1670a88cf67ab277b9100170ea8d8fd49a30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
3
Please input your password.
password: 
after sign transaction hex string is 0a8d020a024e88220811a47859be13f6894096bcb5de9a305aee01082e12e9010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e747261637412a8010a1541babecec4d9f58f0df77f0728b9c53abb1f21d68412241a056f776e657220013a190a1541babecec4d9f58f0df77f0728b9c53abb1f21d6841001226908021a0b6163746976653132333233200232207fff1fc0033e00000000000000000000000000000000000000000000000000003a190a15410cfaec7164cbfe78dbb8d8fba7e23b4d745ed81310013a190a1541e8bd653015895947cec33d1670a88cf67ab277b9100170ea8d8fd49a301241881b00f8e8828d9347469fcbcec730093841c2363561243b7162a9669439266049ab82f20f97a136adc88feff0a4d5aa57b11f762eaa7e05105d27ec5d55a33900
txid is 3dce7f18f6cf6962c38904678947b3b32f9e94ba6460874679d8ed063bb1c0eb
UpdateAccountPermission successful !!!
```


### 账户资源
下面是账户地址相关命令：

- [FreezeBalance](#freezebalance)
- [UnfreezeBalance](#unfreezebalance)
- [GetDelegatedResource](#getdelegatedresource)
- [FreezeBalanceV2](#freezebalancev2)
- [UnfreezeBalanceV2](#unfreezebalancev2)
- [DelegateResource](#delegateresource)
- [UndelegateResource](#undelegateresource)
- [WithdrawExpireUnfreeze](#withdrawexpireunfreeze)
- [GetAvailableUnfreezeCount](#getavailableunfreezecount)
- [GetCanWithdrawUnfreezeAmount](#getcanwithdrawunfreezeamount)
- [GetCanDelegatedMaxsize](#getcandelegatedmaxsize)
- [GetDelegatedResourceV2](#getdelegatedresourcev2)
- [GetDelegatedResourceAccountIndexV2](#getdelegatedresourceaccountindexv2)
- [GetAccountNet](#getaccountnet)
- [GetAccountResource](#getaccountresource)
#### FreezeBalance
通过质押一定数量的TRX可以获得`带宽`，`能量`以及`TRON Power`（投票权）。用户同样也可以通过质押TRX来为别人提供`带宽`和`能量`。质押资产的单位是sun。该接口已废弃，请使用freezeBalanceV2接口质押TRX。
```shell
wallet> freezeBalance [OwnerAddress] [frozen_balance] [frozen_duration] [ResourceCode:0 BANDWIDTH, 1 ENERGY] [receiverAddress]
```

* `OwnerAddress` 是交易发起人的地址，为选填，不填则默认为当前登录账户地址。
* `frozen_balance` 是所冻结TRX的数值,单位为`sun`, 最小冻结值为1000000sun。
* `frozen_duration` 冻结天数, 目前只能设置为3天, 就是说3天之后才可解冻。
* `ResourceCode` 用来指示所冻结资源的种类，0为`带宽`，1为`能量`。 
* `receiverAddress` 为资源接受人的地址。

`ResourceCode` 与 `receiverAddress`  为选填， `ResourceCode` 如若不填，默认值为0，即选择类型为`带宽`，`receiverAddress` 如若不填，则默认为`OwnerAddress` 使用。

示例:
```shell
wallet> freezeBalance TWyDBTHsWJFhgywWkTNW7vh7jSUxeBaiAw 1000000 3 1 TCrkRWJuHP4VgQF3xwLNBAjVVXvxRRGpbA
{
	"raw_data":{
		...
	},
	"raw_data_hex":"0a02a9b822081db2070d39d2316640c095dda19a305a70080b126c0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e6365436f6e747261637412360a1541e65aca838a9e15dd81bd9532d2ad61300e58cf7110c0843d180350017a15411fafb1e96dfe4f609e2259bfaf8c77b60c535b9370c6c8d9a19a30"
}
before sign transaction hex string is 0a8e010a02a9b822081db2070d39d2316640c095dda19a305a70080b126c0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e6365436f6e747261637412360a1541e65aca838a9e15dd81bd9532d2ad61300e58cf7110c0843d180350017a15411fafb1e96dfe4f609e2259bfaf8c77b60c535b9370c6c8d9a19a30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-22T08-21-05.158000000Z--TDQgNvjrE6RH749f8aFGyJqEEGyhV4BDEU.json
The 2th keystore file name is UTC--2022-06-27T07-37-47.601000000Z--TWyDBTHsWJFhgywWkTNW7vh7jSUxeBaiAw.json
Please choose between 1 and 2
2
Please input your password.
password: 
after sign transaction hex string is 0a8e010a02a9b822081db2070d39d2316640e0f7ffab9a305a70080b126c0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e6365436f6e747261637412360a1541e65aca838a9e15dd81bd9532d2ad61300e58cf7110c0843d180350017a15411fafb1e96dfe4f609e2259bfaf8c77b60c535b9370c6c8d9a19a301241c45742648e6970e01b242c9b6eca2549c8721b860ced71abd331b9fe925f3c0f184768e0d2e3b580ce787cc6f67d186a0d583226fdb69c2cc8cfc6ec42e389f600
txid is f45cb5ae425796a492d4a9ecac8d60fd48bf78dbcdbe1d92725047c5dfbffba2
FreezeBalance successful !!!
```


#### UnfreezeBalance
```shell
wallet>unfreezeBalance [OwnerAddress] ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER) [receiverAddress]
```

* `OwnerAddress` 是交易发起人的地址。
* `ResourceCode` 用来指示所冻结资源的种类，0为`带宽`，1为`能量`。 
* `receiverAddress` 为资源接受人的地址。

示例：

```shell
wallet> unfreezebalance TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8 1 TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"resource":"ENERGY",
						"receiver_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8"
					},
					"type_url":"type.googleapis.com/protocol.UnfreezeBalanceContract"
				},
				"type":"UnfreezeBalanceContract"
			}
		],
		"ref_block_bytes":"c8b7",
		"ref_block_hash":"8842722f2845274d",
		"expiration":1656915213000,
		"timestamp":1656915154748
	},
	"raw_data_hex":"0a02c8b722088842722f2845274d40c8f5debe9c305a6c080c12680a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e6365436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d68450017a1541e8bd653015895947cec33d1670a88cf67ab277b970bcaedbbe9c30"
}
before sign transaction hex string is 0a8a010a02c8b722088842722f2845274d40c8f5debe9c305a6c080c12680a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e6365436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d68450017a1541e8bd653015895947cec33d1670a88cf67ab277b970bcaedbbe9c30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y               
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
3
Please input your password.
password: 
after sign transaction hex string is 0a8a010a02c8b722088842722f2845274d40e8dd81c99c305a6c080c12680a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e6365436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d68450017a1541e8bd653015895947cec33d1670a88cf67ab277b970bcaedbbe9c301241593a94650274df29619a6a6946258ea32a22f24a33445f943e3d72cd7d9b8ce7234d188f4bf3a6f0c90cb60af36fc77dc8d376afac9ed840f36dfd68c429fb7e00
txid is 3ea58b3ac2cb05868e70d40f58916312d927c40fd1e4c549554dc3e520c1efde
UnfreezeBalance successful !!!
```
#### GetDelegatedResource 
```shell
wallet>getdelegatedresource [fromAddress] [toAddress]
```
该命令用于查询账户资源质押的情况。`fromAddress` 为资源所有方地址，`toAddress` 为受益方地址。

```shell
wallet> getdelegatedresource TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8 TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE
{
	"delegatedResource": [
		{
			"from": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
			"to": "TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
			"frozen_balance_for_energy": 1000000,
			"expire_time_for_energy": 1656660447000
		}
	]
}
```

#### FreezeBalanceV2
Stake 2.0质押接口，通过质押一定数量的TRX可以获得`带宽`或者`能量`以及`TRON Power`（投票权）。质押资产的单位是sun。
```shell
wallet> freezeBalanceV2 [OwnerAddress] frozen_balance ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER)
```

* `OwnerAddress` 是交易发起人的地址，为选填，不填则默认为当前登录账户地址。
* `frozen_balance` 是所冻结TRX的数值,单位为`sun`, 最小冻结值为1000000sun。。
* `ResourceCode` 用来指示要获取资源的类型, 0为`带宽`，1为`能量`。

示例:
```shell
wallet> freezeBalanceV2 1000000 1
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"resource":"ENERGY",
						"frozen_balance":1000000,
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM"
					},
					"type_url":"type.googleapis.com/protocol.FreezeBalanceV2Contract"
				},
				"type":"FreezeBalanceV2Contract"
			}
		],
		"ref_block_bytes":"00bb",
		"ref_block_hash":"0c237850e9e3c216",
		"expiration":1676620524000,
		"timestamp":1676620465372
	},
	"raw_data_hex":"0a0200bb22080c237850e9e3c21640e0d3fbf2e5305a59083612550a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d180170dc89f8f2e530"
}
before sign transaction hex string is 0a770a0200bb22080c237850e9e3c21640e0d3fbf2e5305a59083612550a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d180170dc89f8f2e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a770a0200bb22080c237850e9e3c21640dbb89efde5305a59083612550a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d180170dc89f8f2e53012419e46cc7b6706ee6a14a541df5f9c518fae9a71ac7a7cc484c48386eb0997a8ab10c41e09feb905c5cc370fe1d15968d22cec2fd2cdc5916adfd3a78c52f8d47000
txid is 1743aa098f5e10ac8b68ccbf0ca6b5f1364a63485e442e6cb03fd33e3331e3fb
freezeBalanceV2 successful !!!
```

#### UnfreezeBalanceV2
Stake2.0 解质押API：解锁质押的TRX, 释放所相应数量的带宽和能量，同时回收相应数量的投票权(TP)。

```shell
wallet> unfreezeBalanceV2 [OwnerAddress] unfreezeBalance ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER)
```

* `OwnerAddress` 是交易发起人的地址。可选，默认为wallet-cli登录地址。
* `unfreezeBalance` 解质押TRX数量。
* `ResourceCode` 用来指示所冻结资源的种类，0为`带宽`，1为`能量`。 


示例：

```shell
wallet> unfreezeBalanceV2 1000000  1
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"resource":"ENERGY",
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
						"unfreeze_balance":1000000
					},
					"type_url":"type.googleapis.com/protocol.UnfreezeBalanceV2Contract"
				},
				"type":"UnfreezeBalanceV2Contract"
			}
		],
		"ref_block_bytes":"0132",
		"ref_block_hash":"0772c1a1727e2ef0",
		"expiration":1676620887000,
		"timestamp":1676620829314
	},
	"raw_data_hex":"0a02013222080772c1a1727e2ef040d8e791f3e5305a5b083712570a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d18017082a58ef3e530"
}
before sign transaction hex string is 0a790a02013222080772c1a1727e2ef040d8e791f3e5305a5b083712570a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d18017082a58ef3e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a790a02013222080772c1a1727e2ef040ecd2b4fde5305a5b083712570a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d18017082a58ef3e530124111bac22e9bc35e1a78c13796893e9f2b81dc99eb26d9ce7a95d0c6a0a9b5588739c52b999acd370b255d178f57bf2abef8881891f23e042ddf83c3551b8bd98e01
txid is f9e114347ea89c5d722d20226817bc41c8a39ea36be756ba216cf450ab3f1fb3
unfreezeBalanceV2 successful !!!
```

#### DelegateResource
Stake 2.0 资源代理API：将带宽或者能量资源代理给其它账户。
```shell
wallet> delegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress [lock]
```

* `OwnerAddress` 是交易发起人的地址。可选，默认为wallet-cli登录地址。
* `balance` 代理的TRX数量。
* `ResourceCode` 用来指示代理资源的种类，0为`带宽`，1为`能量`。 
* `ReceiverAddress` 资源接收者地址。 
* `lock` 用来指示是否将该资源代理锁定三天，可选，默认值为0，0为不锁定，1为锁定。 


示例：

```shell
wallet> delegateResource 1000000  1 TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g 0
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"balance":1000000,
						"resource":"ENERGY",
						"receiver_address":"TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM"
					},
					"type_url":"type.googleapis.com/protocol.DelegateResourceContract"
				},
				"type":"DelegateResourceContract"
			}
		],
		"ref_block_bytes":"020c",
		"ref_block_hash":"54e32e95d11894f8",
		"expiration":1676621547000,
		"timestamp":1676621487525
	},
	"raw_data_hex":"0a02020c220854e32e95d11894f840f88bbaf3e5305a710839126d0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e70a5bbb6f3e530"
}
before sign transaction hex string is 0a8f010a02020c220854e32e95d11894f840f88bbaf3e5305a710839126d0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e70a5bbb6f3e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a8f010a02020c220854e32e95d11894f84093e9dcfde5305a710839126d0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e70a5bbb6f3e5301241414de060e9c104bb45d745e22b7b7a30b4a89a2635c62aab152fff5d2f10b7443023a9aa487be86652b74974ff6a7d82d3dbf94cea9ac1e0a7e48e682175e3f601
txid is 0917002d0068dde7ad4ffe46e75303d11192e17bfa78934a5f867c5ae20720ec
delegateResource successful !!!
```

#### UndelegateResource
Stake 2.0 取消资源代理API：取消为目标地址代理的带宽或者能量。
```shell
wallet> unDelegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress
```

* `OwnerAddress` 是交易发起人的地址。可选，默认为wallet-cli登录地址。
* `balance` 解代理的TRX数量。
* `ResourceCode` 用来指示解除代理资源的种类，0为`带宽`，1为`能量`。 
* `ReceiverAddress` 资源接收者地址。 


示例：

```shell
wallet> unDelegateResource 1000000  1 TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"balance":1000000,
						"resource":"ENERGY",
						"receiver_address":"TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM"
					},
					"type_url":"type.googleapis.com/protocol.UnDelegateResourceContract"
				},
				"type":"UnDelegateResourceContract"
			}
		],
		"ref_block_bytes":"0251",
		"ref_block_hash":"68ac15256c213e71",
		"expiration":1676621754000,
		"timestamp":1676621695001
	},
	"raw_data_hex":"0a020251220868ac15256c213e714090ddc6f3e5305a73083a126f0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e709990c3f3e530"
}
before sign transaction hex string is 0a91010a020251220868ac15256c213e714090ddc6f3e5305a73083a126f0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e709990c3f3e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a91010a020251220868ac15256c213e7140febde9fde5305a73083a126f0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e709990c3f3e530124102ebde16d1abaccd976f8ead4b5acf92b05f7d9796c28ca6a26b4e51442e638e5e33e598bb03732da24dc761a39b9d307c045b55323128dc9b07510ffc48933a01
txid is 537a3f4461ab55c705b77503bc42f469bfc22c0cb8588b8f3641ab40117ebfd8
unDelegateResource successful !!!
```
#### WithdrawExpireUnfreeze
Stake 2.0 提取质押本金API：提取已过锁定期的解质押的本金。

```shell
wallet> withdrawExpireUnfreeze [OwnerAddress]
```

* `OwnerAddress` 是交易发起人的地址。可选，默认为wallet-cli登录地址。


示例：

```shell
wallet> withdrawExpireUnfreeze 
```

#### GetAvailableUnfreezeCount
Stake 2.0 API: 查询当下解质押剩余次数。

```shell
wallet> getavailableunfreezecount [OwnerAddress]
```

* `OwnerAddress` 是交易发起人的地址。可选，默认为wallet-cli登录地址。


示例：

```shell
wallet> GetAvailableUnfreezeCount
{
	"count": 30
}
```
#### GetCanWithdrawUnfreezeAmount
Stake 2.0 API: 查询在某时间点可以提取的解质押本金数量。

```shell
wallet> getcanwithdrawunfreezeamount ownerAddress timestamp
```

* `OwnerAddress` 是交易发起人的地址。可选，默认为wallet-cli登录地址。
* `timestamp` 查询的提现时间戳，以毫秒为单位。

示例：

```shell
wallet> getcanwithdrawunfreezeamount 1776621695001
{
	"amount": 4000000
}
```

#### GetCanDelegatedMaxsize
Stake 2.0 API: 查询在某时间点可以提取的解质押本金数量。

```shell
wallet> getcandelegatedmaxsize ownerAddress type
```

* `OwnerAddress` 是交易发起人的地址。可选，默认为wallet-cli登录地址。
* `type` 查询的资源类型，0为带宽，1为能量。

示例：

```shell
wallet> getcandelegatedmaxsize 1
{
	"max_size": 11000000
}
```
#### GetDelegatedResourceV2
Stake 2.0 API：查询某地址代理给目标地址的资源情况。

```shell
wallet> getdelegatedresourcev2 fromAddress toAddress
```

* `fromAddress` 资源代理地址。
* `toAddress` 资源接收地址。

示例：

```shell
wallet> getdelegatedresourcev2  TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g
{
	"delegatedResource": [
		{
			"from": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
			"to": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
			"frozen_balance_for_bandwidth": 7000000,
			"frozen_balance_for_energy": 3000000
		}
	]
}
```
#### GetDelegatedResourceAccountIndexV2
Stake 2.0 API：查询某地址的资源委托索引。返回两个列表，一个是该帐户将资源委托给的地址列表(toAddress)，另一个是将资源委托给该帐户的地址列表(fromAddress)

```shell
wallet> getdelegatedresourceaccountindexv2 ownerAddress
```

* `OwnerAddress` 查询的地址。

示例：

```shell
wallet> getdelegatedresourceaccountindexv2 TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
{
	"account": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
	"fromAccounts": [
		"TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
	],
	"toAccounts": [
		"TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"
	]
}
```

#### GetAccountNet
该命令用于查询账户内的带宽使用情况

示例：
```shell
wallet> getaccountnet TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
{
	"freeNetUsed": 262,
	"freeNetLimit": 1500,
	"TotalNetLimit": 43200000000,
	"TotalNetWeight": 8725123062
}
```

#### GetAccountResource
该命令用于查询账户的带宽和能量使用情况

示例：
```shell
wallet> getaccountresource TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
{
	"freeNetUsed": 262,
	"freeNetLimit": 1500,
	"TotalNetLimit": 43200000000,
	"TotalNetWeight": 8725123062,
	"tronPowerLimit": 1,
	"TotalEnergyLimit": 90000000000,
	"TotalEnergyWeight": 328098231
}
```


### 交易
下面是账户地址相关命令：

- [SendCoin](#sendcoin)
- [AddTransactionSign](#addtransactionsign)
- [BroadcastTransaction](#broadcasttransaction)
- [GetTransactionApprovedList](#gettransactionapprovedlist)

#### SendCoin
```
> sendcoin [toAddress] [amount]
```
`toAddress`为目标地址，`amount` 为转账数额。下面是一个多签交易例子，其中的签名各账户的授权情况为[UpdateAccountPermission](#updateaccountpermission)部分的例子中实际的授权情况,请参考：
```shell
wallet> sendcoin TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE 10
{
	"raw_data":{
		"contract":[
	···
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
		"result":{
			"result":true
		},
		"txid":"ece603ec8ad11578450dc8adf29dd9d9833e733c313fe16a947c8c768f1e4483",
		"transaction":{
			"signature":[
				"990001e909e638bbaa5de9b392121971d25cabde1391f5e164cd8a14608812df01a273e867c2329b8adb233599c5d353c435e789c777fd3e0b9fe83f0737a91101"
			],
			"txID":"ece603ec8ad11578450dc8adf29dd9d9833e733c313fe16a947c8c768f1e4483",
			"raw_data":···,
			"raw_data_hex":"0a029ca12208432ed1fe1357ff7f40a2b3a7fb9a305a67080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a2802708a8481f19a30"
		}
	}
}
Please confirm if continue add signature enter y or Y, else any other
y
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
4
Please input your password.
password: 
after sign transaction hex string is 0a85010a029ca12208432ed1fe1357ff7f40a2b3a7fb9a305a67080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a2802708a8481f19a301241990001e909e638bbaa5de9b392121971d25cabde1391f5e164cd8a14608812df01a273e867c2329b8adb233599c5d353c435e789c777fd3e0b9fe83f0737a91101124141ba3ffe9c7bb1ed184df8bf635d8c987982b2f4b22c447666ac82726f4a97cb2ef4d3fabd64137b8d59239bd7173c74264733ed140ccd04934a88c438de1cab00
txid is ece603ec8ad11578450dc8adf29dd9d9833e733c313fe16a947c8c768f1e4483
Send 10 Sun to TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE successful !!
```
在转账过程中，需要输入`permission_id`，其默认值为0，此时表示该笔交易只需发起人签名即可。 在上面的例子中，我们输入了“2”，表示需要具有ID为2的权限的账户来签名完成此笔交易，此时需要拥有`actives` 权限的两个账户都签名才能完成交易，请参照[UpdateAccountPermission](#updateaccountpermission) 部分的例子，首先由`TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej` 完成签名，此时系统会询问是否继续签名，输入“y”之后，再由`TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE` 完成签名。

两个账户的权重各为1，完成多签的权重阀值为2，此时签名条件达成，交易成功。这个例子为使用同一客户端时如何完成多重签名交易。当使用多个客户端时，请参考下面这个命令。

#### AddTransactionSign
当有多个客户端时，可以使用该命令为交易添加签名，此时需要交易本体的hex string。

示例：
```shell
wallet> addtransactionsign 0a83010a0241aa2208b2d2c13c86e8bd884098acb1cf9a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a30
Please input permission id.
0
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
3
Please input your password.
password: 
{
	"signature":[
		"dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201"
	],
	"txID":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"amount":10,
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
						"to_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE"
					},
					"type_url":"type.googleapis.com/protocol.TransferContract"
				},
				"type":"TransferContract"
			}
		],
		"ref_block_bytes":"41aa",
		"ref_block_hash":"b2d2c13c86e8bd88",
		"expiration":1656434882649,
		"timestamp":1656413188328
	},
	"raw_data_hex":"0a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a30"
}
Transaction hex string is 0a83010a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a301241dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201
```


**注意** 签名后，各方需要使用下面的命令手动完成交易广播。

#### BroadcastTransaction

要使用交易本体hex string完成交易广播时，请使用本命令。
```shell
wallet> broadcasttransaction 0a83010a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a301241dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201
BroadcastTransaction successful !!!
```

#### GetTransactionApprovedList
通过交易本体hex string使用本命令可以查看签名列表

示例：
```shell
wallet> getTransactionApprovedList
0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101
{
	"result":{
		
	},
	"approved_list":[
		"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8"
	],
	"transaction":{
		"result":{
			"result":true
		},
		"txid":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
		"transaction":{
			"signature":[
				"dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201"
			],
			"txID":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
			"raw_data":{
				"contract":[
					{
						"parameter":{
							"value":{
								"amount":10,
								"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
								"to_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE"
							},
							"type_url":"type.googleapis.com/protocol.TransferContract"
						},
						"type":"TransferContract"
					}
				],
				"ref_block_bytes":"41aa",
				"ref_block_hash":"b2d2c13c86e8bd88",
				"expiration":1656434882649,
				"timestamp":1656413188328
			},
			"raw_data_hex":"0a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a30"
		}
	}
}

```




### 查询链上数据
下面是账户地址相关命令：

- [GetNextMaintenanceTime](#getnextmaintenancetime)
- [ListNodes](#listnodes)
- [GetBlock](#getblock)
- [GetBlockById](#getblockbyid)
- [GetBlockByLatestNum](#getblockbylatestnum)
- [GetBlockByLimitNext](#getblockbylimitnext)
- [GetTransactionById](#gettransactionbyid)
- [GetTransactionCountByBlockNum](#gettransactioncountbyblocknum)
- [GetTransactionInfoById](#gettransactioninfobyid)
- [GetTransactionInfoByBlockNum](#gettransactioninfobyblocknum)
- [GetTransactionSignWeight](#gettransactionsignweight)



#### GetNextMaintenanceTime

使用该命令查询下一个维护时间
```
wallet> GetNextMaintenanceTime
Next maintenance time is : 2022-06-29 16:40:00
```
#### ListNodes

使用该命令列出其他节点的地址和端口信息
```
wallet> listnodes
IP::1.23.456.789
Port::12345
IP::2.345.67.89
Port::12345
IP::345.678.901.234
Port::12345
···
```
#### GetBlock

使用该命令通过区块高度查询区块，如不输入区块高度，则默认查询最新区块。
```shell
wallet> getblock
Get current block !!!
{
	"block_header":{
		"raw_data":{
			"number":27774469,
			"txTrieRoot":"0000000000000000000000000000000000000000000000000000000000000000",
			"witness_address":"TQuzjxWcqHSh1xDUw4wmMFmCcLjz4wSCBp",
			"parentHash":"0000000001a7ce048eb88d7c3c5e9c5f8e93a6cc568f47140e243d00d0f9280a",
			"version":24,
			"timestamp":1656919215000
		},
		"witness_signature":"3af25276891b1cf7f9f72e63ad956b50e5819fb3fa6f0b6393ed092e53a90a5438620b92b5d499e0068c6775b723e3c90677157b3e9f7b8933d1e863716145f500"
	}
}
```
#### GetBlockById

通过区块哈希查询区块信息
```
wallet> getblockbyid [blockID]
```
示例：
```shell
wallet> getblockbyid 0000000001a7cd54ee2b302cfd443cccec78e55a31902d2e7ea47e737c1a5ede
{
	"block_header":{
		"raw_data":{
			"number":27774292,
			"txTrieRoot":"a60f8cb160d06d5279cb463925274e18fec37f0414c4d8fdc4fb2299ccb0a8bf",
			"witness_address":"TGsdxpHNJaxsVNFFdb4R6Rib1TsKGon2Wp",
			"parentHash":"0000000001a7cd53685867286b17fa0f2389e1d3026bea0a0019c5fc37f873cb",
			"version":24,
			"timestamp":1656918678000
		},
		"witness_signature":"a93db1a8d989c6637d587369de2872a008f14d1df8f0aaeda8a54c324a44c269367ea31daf623834fd6a4ef3f6150ab8d370adff1df6c0e8c96af9cf34408d5600"
	},
	···

```
#### GetBlockByLatestNum

获取最近的n个区块的信息，n 必须满足 0 < n < 100。
```
wallet> getblockbylatestnum [n]
```
#### GetBlockByLimitNext

通过区块高度查询区间内的区块信息。`startBlock`为区间开始的区块高度，`endBLock`为区间结束的区块高度。
```
wallet> GetBlockByLimitNext [startBlock, endBlock]
```
示例：
```shell
wallet> getblockbylimitnext 27774670 27774674
[
	{
		"block_header":{
			"raw_data":{
				"number":27774670,
				"txTrieRoot":"0eb9ba48deda22fafa613c0aefa6d3e0b21261ad82a126ce99a6b80e8b68045c",
				"witness_address":"TVKfvNUMcZdZbxhPLb2CkQ4nyUUhvwhv1b",
				"parentHash":"0000000001a7cecd7a2cdc58fdfd2edbfeaeb530958879bf1a299cc30043cd0b",
				"version":24,
				"timestamp":1656919824000
			},
			"witness_signature":"ee6653289e24edd24d70f4975e12934573d6e798a2a5c5e26e0b13bc6d25138c49a0f55fb0e9a5c503622b5877811403577a5e278528293d05c5f0b9d5d5542401"
		},
···
```
#### GetTransactionById

通过交易哈希查询交易信息。

```shell
wallet> GetTransactionById [transactionID]
```
`transactionID`是交易哈希，示例如下：
```shell
wallet> gettransactionbyid 86f09e0152cae9424685411439601c93f9a0ee484ab6e4184cb02294e85cdf89
{
	"ret":[
		{
			"contractRet":"SUCCESS"
		}
	],
	"signature":[
		"26b70d14ca08de644c4b1d8b71952ff57078a36719497bb188040ba589a808c7c896deb82fadcaad7d68be3d1d02bd2e490227ca90cc8b050f750aa10df6105300"
	],
	"txID":"86f09e0152cae9424685411439601c93f9a0ee484ab6e4184cb02294e85cdf89",
	"raw_data":{
···
```
#### GetTransactionCountByBlockNum

通过区块高度查询该区块内有多少笔交易。比如下例中，区块高度为27633562。
```
wallet> gettransactioncountbyblocknum 27633562
The block contains 4 transactions
```

#### GetTransactionInfoById

使用该命令通过交易哈希获取交易详情，通常用于查看智能合约的触发情况。

示例：
```shell
wallet> gettransactioninfobyid 6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87
{
	"id": "6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
	"blockNumber": 27609041,
	"blockTimeStamp": 1656417906000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 265
	}
}
```

#### GetTransactionInfoByBlockNum

通过区块高度查询该区块内交易的详情，`blockNum`为区块高度。
```
wallet> gettransactioninfobyblocknum [blockNum]
```
示例：
```shell
wallet> gettransactioninfobyblocknum 27775479
[
	{
		"result":"FAILED",
		"packingFee":882440,
		"fee":882440,
		"blockNumber":27775479,
		"contractResult":[
			"08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002173746172742074696d65206265666f726520626c6f636b2e74696d657374616d7000000000000000000000000000000000000000000000000000000000000000"
		],
		···
		"result":"FAILED",
		"packingFee":345000,
		"fee":345000,
		"blockNumber":27775479,
		"contractResult":[
			"08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002345524332303a207472616e7366657220746f20746865207a65726f20616464726573730000000000000000000000000000000000000000000000000000000000"
		],
		"blockTimeStamp":1656922275000,
		"resMessage":"REVERT opcode executed",
		"receipt":{
			"result":"REVERT",
			"net_fee":345000,
			"energy_usage_total":647,
			"origin_energy_usage":647
		},
		"id":"13d1e01639edd3f5200789b2fe4d3fdeb765f0bbe4548a1fb69583da85cf7980",
		"contract_address":"TBLfSzQo8TGtCotPD5JZntpZfQqPFLehTE"
	}
]

```
#### GetTransactionSignWeight
通过交易本体hex string获取签名信息

示例：
```shell
wallet>getTransactionSignWeight 
0a83010a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a301241dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201
{
	"result":{
		
	},
	"approved_list":[
		"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8"
	],
	"permission":{
		"keys":[
			{
				"address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
				"weight":1
			}
		],
		"threshold":1,
		"permission_name":"owner"
	},
	"current_weight":1,
	"transaction":{
		"result":{
			"result":true
		},
		"txid":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
		"transaction":{
			"signature":[
				"dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201"
			],
			···
		}
	}
}
```




### 智能合约
本节为所有与智能合约相关的命令:

- [DeployContract](#deploycontract)
- [TriggerContract](#triggercontract)
- [TriggerConstantContract](#triggerconstantcontract)
- [EstimateEnergy](#estimateenergy)
- [GetContract](#getcontract)
- [UpdateEnergyLimit](#updateenergylimit)
- [UpdateSetting](#updatesetting)
- [UnfreezeAsset](#unfreezeasset)
#### DeployContract
使用该命令部署智能合约
```
wallet> DeployContract [ownerAddress] [contractName] [ABI] [byteCode] [constructor] [params] [isHex] [fee_limit] [consume_user_resource_percent] [origin_energy_limit] [value] [token_value] [token_id](e.g: TRXTOKEN, use # if don't provided) <library:address,library:address,...> <lib_compiler_version(e.g:v5)> library:address,...>
```

* `OwnerAddress`为发起人地址，如若不填，则默认为当前登陆账户地址。
* `contractName` 为智能合约的名称。
* `ABI` 为编译时生成的ABI码。
* `byteCode` 为编译时生成的bytecode。
* `constructor`, `params`, `isHex` 这三个参数定义了bytecode的格式，也就决定了从参数来解析bytecode的方式。
* `fee_limit` 用来设置单笔交易所能消耗的TRX的上限。
* `consume_user_resource_percent` 为用户调用合约时消耗TRX所占的比例，为百分数[0, 100%]。
* `origin_energy_limit` 为触发一次合约开发者所消耗TRX的上限。
* `value` 为转入到合约地址中的TRX的数额。
* `token_value` 为合约中TRC-10 token的数量。
* `token_id` 为TRC-10 的ID。

示例:
```shell
wallet> deployContract normalcontract544 [{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name": "findArgsByIndexTest","outputs":[{"name":"z","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]
608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029 # # false 1000000000 75 50000 0 0 #
```
可以使用`getTransactionInfoById`来查看合约的执行结果，示例如下:
```shell
wallet> getTransactionInfoById 4978dc64ff746ca208e51780cce93237ee444f598b24d5e9ce0da885fb3a3eb9
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

#### TriggerContract
该命令用于触发智能合约
```
wallet> TriggerContract [ownerAddress] [contractAddress] [method] [args] [isHex] [fee_limit] [value] [token_value] [token_id]
```

* `OwnerAddress` 调用者地址，如若不填，则默认为当前登陆账户地址。
* `ContractAddress` 为智能合约地址。
* `method` 为调用函数或者参数的名称，请参考下面的例子。
* `args` 为一个占位参数, 可以传入'#'代替如若`method` 不需要额外的参数。
* `isHex` 决定了`method`和`args`的格式是否是hex string。
* `fee_limit` 用来设置单笔交易所能消耗的TRX的上限。
* `value` 传入的TRX的数额.
* `token_value` 为TRC-10 token的数额.
* `token_id` 为TRC-10 token的ID, 如果没有, 可以传入‘#’代替.

示例：
```shell
wallet> triggerContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG findArgsByIndexTest(uint256) 0 false
1000000000 0 0 #
```
可以使用`getTransactionInfoById`来查看合约的执行结果，示例如下:
```shell
wallet> getTransactionInfoById 7d9c4e765ea53cf6749d8a89ac07d577141b93f83adc4015f0b266d8f5c2dec4
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
#### TriggerConstantContract
既可以调用合约只读函数(view 或 pure修饰的函数)，用于合约数据查询；也可以调用合约非只读函数，用于预判交易是否可以执行成功或者预估交易的能量消耗。

```
wallet> TriggerConstantContract ownerAddress(use # if you own) contractAddress method args isHex [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]

```

* `ownerAddress` 调用者地址，如是当前登陆账户地址，请输入#。
* `contractAddress` 智能合约地址。
* `method` 调用的合约函数。
* `args` 合约调用传入的参数, 如若`method` 不需要额外的参数，请输入#。
* `isHex` `args`的格式是否是hex string。
* `value` 传入的TRX的数额. 可选，如果没有, 可以传入‘#’代替。
* `token_value` 为TRC-10 token的数额。可选，如果没有, 可以传入‘#’代替。
* `token_id` 为TRC-10 token的ID, 可选，如果没有, 可以传入‘#’代替。

示例：
```shell
wallet> TriggerConstantContract TTGhREx2pDSxFX555NWz1YwGpiBVPvQA7e  TVSvjZdyDSNocHm7dP3jvCmMNsCnMTPa5W transfer(address,uint256) 0000000000000000000000002ce5de57373427f799cc0a3dd03b841322514a8c00000000000000000000000000000000000000000000000000038d7ea4c68000 true

transfer(address,uint256):a9059cbb
Execution result = {
	"constant_result": [
		"0000000000000000000000000000000000000000000000000000000000000001"
	],
	"result": {
		"result": true
	},
	"energy_used": 13253,
	"logs": [
		{
			"address": "LUijWGF4iFrT7hV37Q2Q45DU5TUBvVZb7",
			"topics": [
				"ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
				"000000000000000000000000bdc8ee51fdd1b1e01d71f836481828f88463c838",
				"0000000000000000000000002ce5de57373427f799cc0a3dd03b841322514a8c"
			],
			"data": "00000000000000000000000000000000000000000000000000038d7ea4c68000"
		}
	]
}
```
#### EstimateEnergy
为智能合约交易预估能量消耗。 estimateEnergy 是可选接口, 有些 FullNode 节点可能没有开启该接口，因此，如若调用 estimateEnergy 接口时捕获到节点不支持此功能的错误信息 (this node does not support estimate energy)，建议继续使用 triggerconstantcontract 接口预估能量消耗。

```
wallet> EstimateEnergy ownerAddress contractAddress method args isHex [value token_value token_id]
```

* `ownerAddress` 调用者地址，如是当前登陆账户地址，请输入#。
* `contractAddress` 智能合约地址。
* `method` 调用的合约函数。
* `args` 合约调用传入的参数, 如若`method` 不需要额外的参数，请输入#。
* `isHex` `args`的格式是否是hex string。
* `value` 传入的TRX的数额. 可选，如果没有, 可以传入‘#’代替。
* `token_value` 为TRC-10 token的数额。可选，如果没有, 可以传入‘#’代替。
* `token_id` 为TRC-10 token的ID, 可选，如果没有, 可以传入‘#’代替。

示例：
```shell
wallet> EstimateEnergy TTGhREx2pDSxFX555NWz1YwGpiBVPvQA7e  TVSvjZdyDSNocHm7dP3jvCmMNsCnMTPa5W transfer(address,uint256) 0000000000000000000000002ce5de57373427f799cc0a3dd03b841322514a8c00000000000000000000000000000000000000000000000000038d7ea4c68000 true

transfer(address,uint256):a9059cbb
Estimate energy result = {
	"result": {
		"result": true
	},
	"energy_required": 14910
}
```

#### GetContract
用合约地址调出合约信息
```
wallet> GetContract [contractAddress]
```

示例:
```shell
wallet> GetContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
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

#### UpdateEnergyLimit
该命令用于修改合约中能量消耗的上限,参数定义请参考上面的命令。
```
wallet> UpdateEnergyLimit [ownerAddress] [contract_address] [energy_limit]
```
示例:
```shell
wallet> updateenergylimit TY7CMEBRMgtFeNzkVJACh9L7TdMKENFkeq 8000000
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
						"origin_energy_limit":8000000,
						"contract_address":"TY7CMEBRMgtFeNzkVJACh9L7TdMKENFkeq"
					},
					"type_url":"type.googleapis.com/protocol.UpdateEnergyLimitContract"
				},
				"type":"UpdateEnergyLimitContract"
			}
		],
		"ref_block_bytes":"2d56",
		"ref_block_hash":"3e8f88e2de6bb637",
		"expiration":1656993270000,
		"timestamp":1656993210227
	},
	···
UpdateSetting for origin_energy_limit successful !!!
```
#### UpdateSetting
该命令用于修改合约中用户能量消耗的比例,参数定义请参考上面的命令。
```
wallet> UpdateSetting [ownerAddress] [contract_address] [consume_user_resource_percent]
```
示例:
```shell
wallet> updateenergylimit TY7CMEBRMgtFeNzkVJACh9L7TdMKENFkeq 35
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
						"origin_energy_limit":35,
						"contract_address":"TY7CMEBRMgtFeNzkVJACh9L7TdMKENFkeq"
					},
					"type_url":"type.googleapis.com/protocol.UpdateEnergyLimitContract"
				},
				"type":"UpdateEnergyLimitContract"
			}
		],
		"ref_block_bytes":"2d9f",
		"ref_block_hash":"c25a5c8ba398aa8f",
		"expiration":1656993489000,
		"timestamp":1656993430923
	},
	···
UpdateSetting for origin_energy_limit successful !!!
```


### TRC-10资产
下面是账户地址相关命令：

- [AssetIssue](#assetissue)
- [UpdateAsset](#updateasset)
- [TransferAsset](#transferasset)
- [ParticipateAssetissue](#participateassetissue)
- [ListAssetIssue](#listassetissue)
- [GetAssetIssueByAccount](#getassetissuebyaccount)
- [GetAssetIssueById](#getassetissuebyid)
- [GetAssetIssueByName](#getassetissuebyname)
- [GetAssetIssueListByName](#getassetissuelistbyname)
#### AssetIssue
发行TRC10代币，每个账户地址智能发行一种TRC-10 token。

```
wallet> AssetIssue [OwnerAddress] [AssetName] [AbbrName] [TotalSupply] [TrxNum] [AssetNum] [Precision] [StartDate] [EndDate] [Description Url] [FreeNetLimitPerAccount] [PublicFreeNetLimit] [FrozenAmount0] [FrozenDays0] [...] [FrozenAmountN] [FrozenDaysN]
```

* `OwnerAddress` 为交易发起人地址，如若不填，默认为当前登陆地址。
* `AssetName` 为发行的TRC-10 token的名称。
* `AbbrName` 为发行的TRC-10 token名称缩写。
* `TotalSupply` 为该TRC-10 token的总量。
    * TotalSupply = Account Balance of Issuer + All Frozen Token Amount 
* Account Balance Of Issuer: 发行时发行人的该币余额
* All Frozen Token Amount: 该币在转账和发行前的数额
* `TrxNum`, `AssetNum` 这两个参数决定了该币发行时交易率是多少。
    * Exchange Rate = TrxNum / AssetNum 
* `AssetNum`: 该币的单位
* `TrxNum`: 单位为sun (0.000001 TRX)
* `Precision` 小数点后的位数。
* `FreeNetLimitPerAccount` 为每个账户可以使用的最大带宽。发行人可以质押TRX获得带宽。(仅限于`TransferAsset`)
* `PublicFreeNetLimit` 为所有账户可用的最大带宽。 发行人可以质押TRX获得带宽。(仅限于`TransferAsset`)
* `StartDate`, `EndDate` 为发行起始和终止日期。 在该日期内，其他用户可以参与到新币发行中。
* `FrozenAmount0`, `FrozenDays0` 决定了会有多少新币冻结多久。`FrozenAmount0`需大于0. `FrozenDays0`: 必须字1到3652之间。

示例:
```shell
wallet> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
wallet> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # View published information
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
#### UpdateAsset
使用该命来修改已发布资产的部分参数
```
wallet> UpdateAsset [OwnerAddress] [newLimit] [newPublicLimit] [description url]
```
参数定义与AssetIssue相同。

示例:
```shell
wallet> UpdateAsset 1000 1000000 "change description" www.changetest.com
wallet> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # to check the modified information
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
#### TransferAsset
该命令用于转移资产
```
> TransferAsset [OwnerAddress] [ToAddress] [AssertID] [Amount]
```
这其中`OwnerAddress` 为发起人地址，如若不填，默认为当前登陆地址，`ToAddress` 为接收地址，`AssertName` 为代币的名称，`Amount` 本次转账的数额。

示例:
```shell
wallet> TransferAsset TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz 1000001 1000
wallet> getaccount TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz  # to check target account information after the transfer
address: TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz
    assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```
#### ParticipateAssetissue
使用该命令参与代币的发行
```
> ParticipateAssetIssue [OwnerAddress] [ToAddress] [AssetID] [Amount]
```
`OwnerAddress` 为发起人地址，如若不填，默认为当前登陆地址。`ToAddress` 为接收地址，`AssertName` 为代币的名称，`Amount`为本次转账的数额。

参与发行必须发生在TRC10代币的发行过程中，否则会报错。

示例:
```shell
wallet> ParticipateAssetIssue TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 1000001 1000
wallet> getaccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  # View remaining balance
address: TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```
#### UnfreezeAsset

解冻一个地址下已经超过冻结时间的待解冻TRC-10代币。 
```
wallet> unfreezeasset [OwnerAddress]
```
#### ListAssetIssue

列出所有已发行TRC-10代币及详情
```shell
wallet> listassetissue
{
	"assetIssue": [
		{
			"owner_address": "TMWXhuxiT1KczhBxCseCDDsrhmpYGUcoA9",
			"name": "tronlink_token",
			"abbr": "tronlink_token",
			"total_supply": 1000000000000000,
			"frozen_supply": [
				{
					"frozen_amount": 1,
					"frozen_days": 1
				}
			],
			"trx_num": 1,
			"precision": 6,
			"num": 1,
			"start_time": 1574757000000,
			"end_time": 1757595000000,
			"description": "Description",
			"url": "https://blog.csdn.net/u010270891/article/details/82978260",
			"free_asset_net_limit": 1000,
			"public_free_asset_net_limit": 2000,
			"id": "1000001"
		},
···
```
#### GetAssetIssueByAccount

列出发行人地址下所有已发行TRC-10代币及详情。
```
wallet> getassetissuebyaccount [owneraddress]
```
示例：
```shell
wallet> getassetissuebyaccount TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN
{
	"assetIssue": [
		{
			"owner_address": "TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN",
			"name": "h00966",
			"abbr": "h00966",
			"total_supply": 100000000000,
			"trx_num": 1000000,
			"precision": 6,
			"num": 1000000,
			"start_time": 1656374400000,
			"end_time": 1656460800000,
			"description": "Automated gaming platform. 
TRC10 token h0966.
More info on website.  TRC10 token h0966.
More info on website.  More info on website.",
			"url": "https://h00966.com",
			"id": "1004901"
		}
	]
}
```

#### GetAssetIssueById

根据代币ID获取其详细信息

示例：
```shell
wallet> GetAssetIssueById 1004901
{
	"owner_address": "TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN",
	"name": "h00966",
	"abbr": "h00966",
	"total_supply": 100000000000,
	"trx_num": 1000000,
	"precision": 6,
	"num": 1000000,
	"start_time": 1656374400000,
	"end_time": 1656460800000,
	"description": "Automated gaming platform. 
TRC10 token h0966.
More info on website.TRC10 token h0966.
More info on website.More info on website.",
	"url": "https://h00966.com",
	"id": "1004901"
}
```

#### GetAssetIssueByName

根据代币名称获取其详细信息

示例：
```shell
wallet> GetAssetIssueByname h00966
{
	"owner_address": "TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN",
	"name": "h00966",
	"abbr": "h00966",
	"total_supply": 100000000000,
	"trx_num": 1000000,
	"precision": 6,
	"num": 1000000,
	"start_time": 1656374400000,
	"end_time": 1656460800000,
	"description": "Automated gaming platform. 
TRC10 token h0966.
More info on website.TRC10 token h0966.
More info on website.More info on website.",
	"url": "https://h00966.com",
	"id": "1004901"
}
```

#### GetAssetIssueListByName

根据代币名称获取其详细信息
```shell
wallet> GetAssetIssueListByName ROFLOTOKEN
{
	"assetIssue": [
		{
			"owner_address": "TLvQSVH9Hm7kxLFtTP228fN6pCrHmtVjpb",
			"name": "ROFLOTOKEN",
			"abbr": "roflotoken",
			"total_supply": 10000000000000000,
			"trx_num": 1000000,
			"precision": 6,
			"num": 100000000,
			"start_time": 1656349200000,
			"end_time": 1656435600000,
			"description": "roflotoken.com",
			"url": "https://haxibaibo.com/",
			"id": "1004898"
		}
	]
}
```



### 治理
任何关于proposal的操作，除了查看类的以外，都需要委员会成员来完成。

下面是账户地址相关命令：

 - [CreatProposal](#creatproposal)
 - [ApproveProposal](#approveproposal)
 - [Deleteproposal](#deleteproposal)
 - [ListProposals](#listproposals)
 - [ListProposalsPaginated](#listproposalspaginated)
 - [GetProposal](#getproposal)
 - [Votewitness](#votewitness)
 - [GetBrokerage](#getbrokerage)
 - [GetReward](#getreward)
 - [UpdateBrokerage](#updatebrokerage)

#### CreatProposal
发起一项新的proposal。
```
wallet> createProposal [OwnerAddress] [id0] [value0] ... [idN] [valueN]
```
`OwnerAddress` 为发起人地址，如若不填，默认为当前登陆地址。
`id0` 是TRON Network Parameter的序列号。其中的每个参数都定义好的提议内容，同时对应一个序列号，请参考 [https://tronscan.org/#/sr/committee](https://tronscan.org/#/sr/committee)。`Value0` 为提议修改的值。在下面的例子中，proposal建议将No.4(修改发行费用)的费用改为 1000TRX，
```shell
wallet> createProposal 4 1000
wallet> listproposals  # to check initiated proposal
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
该proposal的对应ID为1。

#### ApproveProposal
使用该命令同意或否决一项proposal。
```
wallet> approveProposal [OwnerAddress] [id] [is_or_not_add_approval]
```
`OwnerAddress` 为发起人地址，如若不填，默认为当前登陆地址。`id` 为proposal的ID。`is_or_not_add_approval` 填入“true”为同意，填入“false”为否决。

示例:
```shell
wallet> ApproveProposal 1 true  # in favor of the offer
wallet> ApproveProposal 1 false  # Cancel the approved proposal
```
#### Deleteproposal
取消一个proposal。
```
wallet> deleteProposal [OwnerAddress] [proposalId]
```
 `OwnerAddress` 为发起人地址，如若不填，默认为当前登陆地址。`proposalId` 为proposal对应的ID。只有发起该propsal的超级代表才能取消自己发起的proposal。

示例：
```shell
wallet> DeleteProposal 1
```

#### ListProposals
查看已发起的proposal。
```shell
wallet> listproposals
{
	"proposals": [
		{
			"proposal_id": 12732,
			"proposer_address": "TQ4eBJna51sew13DBLd7YjEHHHW7fkNzc2",
			"parameters": [
				{
					"key": 65,
					"value": 1
				},
				{
					"key": 66,
					"value": 1
				},
				{
					"key": 62,
					"value": 432000000
				}
			],
			"expiration_time": 1656491400000,
			"create_time": 1656490794000,
			"approvals": [
				"TQ4eBJna51sew13DBLd7YjEHHHW7fkNzc2"
			],
			"state": "DISAPPROVED"
		},
		{
···
```
#### ListProposalsPaginated
用分段的方式查看已发起的proposal。
```
wallet> ListProposalsPaginated [offset] [limit] 
```
`offset` 是需要跳过的proposal的ID，如输入20，则从proposal_ID=21 开始查看。`limit` 是要查看的proposal数量，如输入10，则查看`offset`的值之后的10个proposal。默认情况下，该命令将会列出所有的proposal。

下面的示例中，传参的意义为跳过ID为33及之前的proposal，查看其之后2个proposal，即34和35的两个proposal：

```shell
wallet> listproposalspaginated 33 2
{
	"proposals": [
		{
			"proposal_id": 34,
			"proposer_address": "TEDguVMSsFw3HSizQXFK1BsrGWeuRMNN7t",
			"parameters": [
				{
					"key": 1,
					"value": 9997000000
				}
			],
			"expiration_time": 1582381200000,
			"create_time": 1582380477000,
			"state": "DISAPPROVED"
		},
		{
			"proposal_id": 35,
			"proposer_address": "TDkSQtBhZx7Ua8qvenM4zuH52u2BsYTwzc",
			"parameters": [
				{
					"key": 1,
					"value": 9997000000
				}
			],
			"expiration_time": 1582381200000,
			"create_time": 1582380498000,
			"state": "DISAPPROVED"
		}
	]
}
```
#### GetProposal

通过proposal ID查看proposal详情。
```shell
wallet> getproposal 34
{
	"proposal_id": 34,
	"proposer_address": "TEDguVMSsFw3HSizQXFK1BsrGWeuRMNN7t",
	"parameters": [
		{
			"key": 1,
			"value": 9997000000
		}
	],
	"expiration_time": 1582381200000,
	"create_time": 1582380477000,
	"state": "DISAPPROVED"
}
```

#### Votewitness
使用该命令为超级代表投票。投票需要相应的投票权, 即`TRON Power`，可以通过质押资产来获得。第一个参数为超级代表的地址，第二个参数为该超级代表投票的数量。
```
wallet> votewitness [SR address] [TRON Power Amount]

* TRON Power计算规则: 每冻结 1 TRX获得一个单位的TRON Power。
* 资产解冻后, 所有之前的投票即作废。可以重复冻结资产避免这种情况。

**注意** TRON 只会记录你的最后一次投票，新的投票会覆盖之前的投票。

示例：
```shell
wallet> freezeBalance 100000000 3 1 address  # 冻结 10TRX，获得10个单位的TRON Power。

wallet> votewitness [SR1] 4 [SR2] 6  # 为SR1投4票，同时再为SR2投6票

wallet> votewitness [SR1] 10  # 为SR1投10票
```
示例中的结果为SR1获得10票，SR2获得0票。

#### ListWitnesses

列出所有超级代表的信息。
```shell
wallet> listwitnesses
{
	"witnesses": [
		{
			"address": "TPffmvjxEcvZefQqS7QYvL1Der3uiguikE",
			"voteCount": 324999518,
			"url": "http://sr-26.com",
			"totalProduced": 414028,
			"totalMissed": 20,
			"latestBlockNum": 27638663,
			"latestSlotNum": 552169224,
			"isJobs": true
		},
		{
			"address": "TFFLWM7tmKiwGtbh2mcz2rBssoFjHjSShG",
			"voteCount": 324759460,
			"url": "http://sr-27.com",
			"totalProduced": 414144,
			"totalMissed": 16,
			"latestBlockNum": 27638664,
			"latestSlotNum": 552169225,
			"isJobs": true
		},
···
```

#### GetBrokerage
使用该命令，可以查看超级代表的出块分成比例。

在为超级代表投票后，会收到相应的奖励。超级代表可以调整出块收益的分成比例，默认比例为20%，即收益的20%归该超级代表所有，剩余80%按投票数分配给投票者。

`OwnerAddress` 为超级代表的地址，base58格式。

示例中，出块奖励的分成为20%，即80%的收益会按权重分配给投票者：
```shell
wallet> getbrokerage TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
The brokerage is : 20
```

#### GetReward
查询未领取的奖励。

`OwnerAddress` 为超级代表的地址，base58格式。示例如下：
```shell
wallet> getreward TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
The reward is : 0
``` 


#### UpdateBrokerage
该命令由超级代表发起，调整出块收益的分成比例。
```
wallet> updateBrokerage [OwnerAddress] [brokerage]
```
`OwnerAddress`  为超级代表的地址，base58格式。`brokerage` 为要改成的比例，0-100之间。

示例：
```shell
wallet> updateBrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h 30
```


### 去中心化交易所
交易对的价格浮动和交易情况遵循[Bancor Agreement](https://cryptopapers.info/assets/pdf/bancor.pdf)。

下面是账户地址相关命令：

- [ExchangeCreate](#exchangecreate)
- [ExchangeInject](#exchangeinject)
- [ExchangeTransaction](#exchangetransaction)
- [ExchangeWithdraw](#exchangewithdraw)
- [ListExchanges](#listexchanges)
- [ListExchangesPaginated](#listexchangespaginated)
- [MarketSellAsset](#marketsellasset)
- [MarketCancelOrder](#marketcancelorder)
- [GetMarketOrderByAccount](#getmarketorderbyaccount)
- [GetMarketOrderById](#getmarketorderbyid)
- [GetMarketPairList](#getmarketpairlist)
- [GetMarketOrderListByPair](#getmarketorderlistbypair)
- [GetMarketPriceByPair](#getmarketpricebypair)

#### ExchangeCreate
创建一个交易对
```
wallet> exchangeCreate [OwnerAddress][first_token_id] [first_token_balance] [second_token_id] [second_token_balance]
```
`OwnerAddress` 为发起人地址，如若不填则默认为当前登陆地址。`First_token_id`, `first_token_balance`为交易对中第一个代币的ID和金额。`second_token_id`, `second_token_balance` 为交易对中第二代币的ID和金额。如果是TRX, 则ID为""，额度必须在0到1,000,000,000,000,000之间，不包括头尾。

示例:
```shell
wallet> exchangeCreate 1000001 10000 _ 10000
# Create trading pairs with the IDs of 1000001 and TRX, with amount 10000 for both.
```
#### ExchangeInject
将资金注入交易对
```
wallet> exchangeInject [OwnerAddress] [exchange_id] [token_id] [quant]
```
`OwnerAddress` 为发起人地址，如若不填则默认为当前登陆地址。`exchange_id` 为交易对的ID。`token_id, quant` 为要注入的代币ID和金额。

当要向交易对注入资金时，交易对中的代币会从本账户中取走，注入到交易对中。根据不同的代币余额情况，同种数额的同种代币会有变化。

#### ExchangeTransaction
发起一笔交易对交易
```
wallet> exchangeTransaction [OwnerAddress] [exchange_id] [token_id] [quant] [expected]
```
`OwnerAddress` 为发起人地址，如若不填则默认为当前登陆地址。`exchange_id` 为交易对的ID。`token_id`, `quant` 为要卖出的代币的ID和数额。`expected` 为预期买入的代币数额，该数额必须小于`quant`，否则会报错。

示例：
```shell
wallet> ExchangeTransaction 1 1000001 100 80
```
示例的含义为，想要通过ID为1的交易对，用100个单位的ID为1000001的代币来交易80个TRX。(亦可理解为在交易对1中，通过卖出100个1000001代币来买入80个TRX。).

#### ExchangeWithdraw
提取交易对中的资金
```
wallet> exchangeWithdraw [OwnerAddress] [exchange_id] [token_id] [quant]
```
`OwnerAddress` 为发起人地址，如若不填则默认为当前登陆地址。`Exchange_id` 为交易对ID。`Token_id`, `quant` 为要从交易对中取出的代币的ID和数额。

当要向交易对提取资金时，交易对中的代币会被提取到账户地址中。根据不同的代币余额情况，同种数额的同种代币会有变化。

可以通过下面的`ListExchanges`命令来获取所有的交易对信息。

#### ListExchanges
列出所有交易对及详情
```shell
wallet> listexchanges
{
	"exchanges": [
		{
			"exchange_id": 14,
			"creator_address": "TCjuQbm5yab7ENTYb7tbdAKaiNa9Lrj4mo",
			"create_time": 1654154880000,
			"first_token_id": "1004852",
			"first_token_balance": 91,
			"second_token_id": "_",
			"second_token_balance": 110000000
		},
		{
			"exchange_id": 13,
			"creator_address": "TBpbKyKVUB1YLULrbhawUws69Gv33cmKDL",
			"create_time": 1648004214000,
			"first_token_id": "1000575",
			"first_token_balance": 991,
			"second_token_id": "1000184",
			"second_token_balance": 1010
		},
···
```

#### ListExchangesPaginated

列出选段中的交易对
```shell
wallet> ListExchangesPaginated [offset] [limit]
```
`offset` 为想要跳过的交易对ID。默认从1开始列出交易对，如此处输入值为15，则从交易对ID为16开始列出。`limit` 为想要列出的交易对数量。

下面示例的含义为从id为4的交易对开始列出信息，一共列出2组信息，即列出交易对ID为4，5的信息,请参考:
```shell
wallet> listexchangespaginated 3 2
{
	"exchanges": [
		{
			"exchange_id": 4,
			"creator_address": "TXmHTj3t5LXGvqGkr4jRNw7nf9GjquQ5yf",
			"create_time": 1601458377000,
			"first_token_id": "1000088",
			"first_token_balance": 1,
			"second_token_id": "_",
			"second_token_balance": 1
		},
		{
			"exchange_id": 5,
			"creator_address": "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS",
			"create_time": 1602578613000,
			"first_token_id": "1000091",
			"first_token_balance": 456125,
			"second_token_id": "_",
			"second_token_balance": 106968111
		}
	]
}
```
#### MarketSellAsset
创建一个售出订单
```
wallet> MarketSellAsset [owner_address] [sell_token_id] [sell_token_quantity] [buy_token_id] [buy_token_quantity]
```
`OwnerAddress` 为发起人地址，如若不填则默认为当前登陆地址。`sell_token_id` and `sell_token_quantity` 为要售出的代币ID和数额。`buy_token_id`, `buy_token_quantity` 为想要买入的代币ID和数额。

示例：
```shell
wallet> MarketSellAsset TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  1000001 200 _ 100    
```
如上创建订单后，我们用`getTransactionInfoById`来查看结果,
```shell
wallet> getTransactionInfoById 10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374   

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
#### MarketCancelOrder
使用该命令可以取消订单
```
wallet> MarketCancelOrder [owner_address] [order_id]
```
`owner_address` 为发起人地址，如若不填则默认为当前登陆账户地址。`order_id` 为订单的ID。

示例:
```shell
wallet> MarketCancelOrder TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0  
```
通过`getTransactionInfoById`来查看结果，
```shell
wallet> getTransactionInfoById b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27   
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
#### GetMarketOrderByAccount
使用该命令可查看该账户创建的活跃订单
```
wallet> GetMarketOrderByAccount [ownerAddress]
```
`ownerAddress` 为可查看的地址。

示例:
```shell
wallet> GetMarketOrderByAccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW   
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
#### GetMarketOrderById
通过订单ID查看订单信息
```
wallet> GetMarketOrderById [orderId]
```
示例:
```shell
wallet> GetMarketOrderById fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0   
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
#### GetMarketPairList
列出当前活跃的交易对
```shell
wallet> getmarketpairlist
{
	"orderPair": [
		{
			"sell_token_id": "1000012",
			"buy_token_id": "_"
		},
		{
			"sell_token_id": "1000094",
			"buy_token_id": "1000095"
		},
		{
			"sell_token_id": "1000099",
			"buy_token_id": "1000100"
		},
···
```
#### GetMarketOrderListByPair
通过代币ID查看当前活跃订单
```
wallet> GetMarketOrderListByPair [sell_token_id] [buy_token_id]
```
`sell_token_id` 为要售出的代币ID。`buy_token_id` 为要买入的代币ID。

示例:
```shell
wallet> GetMarketOrderListByPair _ 1000001   
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
#### GetMarketPriceByPair
通过代币ID获取当前市场价格
```
wallet> GetMarketPriceByPair [sell_token_id] [buy_token_id]
```
`sell_token_id` 为要售出的代币ID，`buy_token_id` 为要买入的代币ID。

示例:
```shell
wallet> GetMarketPriceByPair _ 1000001   
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
