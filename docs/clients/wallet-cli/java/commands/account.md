# 账户命令

查询和更新链上账户、管理账户元数据，以及查看本地记录。

## 如何创建账户 {#how-to-create-account}

你可以通过向不存在的账户转账来创建账户，也可以用 **CreateAccount** 命令发起一笔交易来创建账户。
两种方式都会燃烧一笔由链参数 `getCreateNewAccountFeeInSystemContract` 决定的**账户激活费**。
除此之外，创建账户还会消耗**带宽**，而且只能使用质押获得或他人代理的带宽——每日免费带宽不能用于
创建账户。这类带宽不足时，会改为按链参数 `getCreateAccountFee` 燃烧 TRX 来抵扣；带宽充足时则不会
燃烧这一笔。两个参数都可以通过治理提案修改，因此请用
[`GetChainParameters`](chain-data.md#getchainparameters) 查询当前值，不要按固定数额估算。

## CreateAccount

用一个未激活的地址创建新账户，为此燃烧上述账户创建费。

```console
> CreateAccount [OwnerAddress] Address
```

示例：

```console
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

No.  Address                                    Name
1    TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB         TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB.json
2    TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew         TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew.json
3    TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7         TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7.json
4    TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe         Ledger-TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe.json
5    TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada         TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada.json
Please choose No. between 1 and 5, or enter search to search wallets
1
After sign transaction hex string is 0a84010a0291a422082bfcd3bb597f3d404083bd9cfae5325a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a15419d9c2bb5ee381a4396dd49ce42292e756b2e5e4b12154124764e4674179d4578cfc4c833c1ac1a09f6ce56708e8df6efe5321241ce53add4f75fe1838aa7e0a4e2411b3bbfce1d2164d68dac18507ed87e22ae503f65592a1161640834b3c0cef43c28f20b2d335120cc78b6f745a82ea95e451100
TxId is 26d6fcdfdc0018097ec4166eb140e19ebd597bea2212579d2f6d921b0ad6e56f
CreateAccount  successful !!
```

## GenerateAddress

生成一个地址，并打印出地址和私钥。

## GetAccount

根据地址获取账户信息。

```console
> GetAccount Address
```

## GetAccountById

通过账户 ID 获取账户详情。

```console
> GetAccountById accountId
```

## GetAccountNet

显示带宽的使用情况。

```console
> GetAccountNet Address
```

## GetAccountResource

显示带宽和能量的使用情况。

```console
> getAccountResource Address
```

## GetAddress

获取当前登录账户的地址。不带参数。

## GetBalance

获取当前登录账户的余额；如果给出 `Address`，则获取该地址的余额。

```console
> GetBalance [Address]
```

## SetAccountId

为账户设置自定义的唯一标识（Account ID）。

```console
> SetAccountId [owner_address] account_id
```

```console
> SetAccountId TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 100
```

## UpdateAccount

修改账户名称。

```console
> UpdateAccount [owner_address] account_name
```

```console
> UpdateAccount test-name
```

## ViewBackupRecords

查看备份记录。可以在 [`config.conf`](../reference/config.md) 中通过 `maxRecords` 设置最多保留多少条
记录；用于内部缓冲的记录不计入该上限。

```console
wallet> ViewBackupRecords

=== View Backup Records ===
1. View all records
2. Filter by time range
Choose an option (1-2): 1
```

## ViewTransactionHistory

查看交易历史。可以在 [`config.conf`](../reference/config.md) 中通过 `maxRecords` 设置最多保留多少条
记录；用于内部缓冲的记录不计入该上限。

```console
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

## ShowReceivingQrCode

为当前地址显示收款二维码。该命令要求终端上事先安装 `qrencode`：

- Debian/Ubuntu：`sudo apt install qrencode`
- CentOS：`sudo yum install qrencode`
- RHEL/Fedora：`sudo dnf install qrencode`
- macOS：`brew install qrencode`

```console
wallet> ShowReceivingQrCode
█████████████████████████████████████
████ ▄▄▄▄▄ ██▄▀▀ ▄ ▀▄▀ ▀▀█ ▄▄▄▄▄ ████
████ █   █ █▄  ▀▄  ▀▄▀▀███ █   █ ████
████ █▄▄▄█ ██▀▄██▀▄▀▄▀ ▀██ █▄▄▄█ ████
████▄▄▄▄▄▄▄█ ▀ █ ▀ ▀ ▀ ▀ █▄▄▄▄▄▄▄████
████▄  █▄▄▄▄▄█  ██  ▀▀██▀  ██▀▄▀▀████
████▄█▀▄█▀▄▀▄▄█▀█▄█▀▄ █▀██▄ █▄▄ ▄████
████ █▄█▄ ▄▄▄██▀ ▀█▀▄██▄█▄▄ █ █ ▄████
████ ▄▀▄▀▄▄▀ ▄█▄ ▀ ▀█  █ ██▀▀█▄▄▄████
████▄█▀ ██▄██ ▄ ██ ██ █   ▄▄▄   ▄████
████▄▀▀ ▀█▄█▀▄▀▀█▄█▄█▀ ▀▄▀█ ▄▄▄ ▄████
████▄██▄█▄▄▄▀ ▄▀ ▀██  ▄▄ ▄▄▄  ▄▄▄████
████ ▄▄▄▄▄ █ █▀▄ ▀ █▄▀▄  █▄█ ▄█▄ ████
████ █   █ █▄▀▀ ██ ▄▄  █  ▄ ▄▄▄██████
████ █▄▄▄█ █ ▀█▀█▄█▄▀▀█▄ ▄█  ██▀▄████
████▄▄▄▄▄▄▄█▄▄██▄██ ▀▀▄▄▄▄█   ▀  ████
█████████████████████████████████████
TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp
```

## 另请参见

- [wallet](wallet.md)——创建 / 导入 / 会话管理
- [chain-data](chain-data.md)——交易与区块查询
- [usdt](usdt.md)——token 余额与地址簿
