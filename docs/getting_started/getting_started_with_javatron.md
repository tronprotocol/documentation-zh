# java-tron 快速入门

本指南将引导您完成一系列 `java-tron` 的基础操作。您将学习如何：
- 启动一个 `java-tron` 节点；
- 使用命令行工具 `wallet-cli` 与 `java-tron` 节点进行交互；
- 执行关键操作，例如创建账户和发送 TRX。

执行本教程中的操作前，请确保已安装 `java-tron` 及相关的开发工具。如果您尚未安装，请参考[安装和构建](../using_javatron/installing_javatron.md)页面，其中说明了如何直接下载可运行文件或通过源代码进行构建。

# 核心概念

`java-tron` 是用 Java 语言编写的波场（TRON）网络客户端，这意味着，运行 `java-tron` 会将您的计算机转变为一个 TRON 网络节点。TRON 网络是一个分布式网络，信息在节点之间共享，而非通过中心化服务器管理。当超级代表（Super Representative）的节点产出一个新区块后，会将其广播至网络中的其它节点。每个节点在接收到新区块时会对其进行校验，校验通过后便将其存入本地数据库。

`java-tron` 通过同步区块来持续更新其“状态”——即 TRON 网络上所有账户的实时余额。

TRON 网络上有两种主要类型的帐户:
- **外部账户 (Externally Owned Accounts)**: 由用户通过其**本地管理**的**公私钥对**来控制。每个外部账户都是一个公私密钥对，其中公钥用于派生出独一无二的账户地址，而私钥则用于保护帐户和安全地签署、授权交易。您在本教程中创建的便是这种类型的账户。
- **合约账户 (Contract Accounts)**: 当收到交易时，这类账户会执行其中包含的智能合约代码。

要开始与波场网络交互，您首先需要创建一个外部账户(以下简称“帐户”)。

## 第一步：创建并访问您的账户

虽然创建波场账户有多种方式，但本指南将演示如何使用 `wallet-cli` 这一便捷的命令行工具来完成。


有多种方法来生成TRON网络帐户，这里将演示如何使用wallet-cli生成帐户。帐户是一对密钥(公钥和私钥)。

在终端中通过命令`java -jar wallet-cli.jar`来启动一个wallet-cli：
```
$ java -jar wallet-cli.jar

Welcome to TRON wallet-cli
Please type one of the following commands to proceed.
Login, RegisterWallet or ImportWallet
 
You may also use the Help command at anytime to display a full list of commands.
 
wallet> 
```

输入命令：registerwallet，然后根据提示输入密码。该命令会生成TRON网络账户,并注册到wallet-cli，也就是wallet-cli会保存此账户的私钥，之后就可以使用该私钥对交易进行签名了。
```
wallet> registerwallet
Please input password.
password: 
user defined config file doesn't exists, use default config file in jar
WalletApi getRpcVsersion: 2
Please input password again.
password: 
Register a wallet successful, keystore file name is UTC--2022-07-04T06-35-35.304000000Z--TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz.json
wallet> 
```

## 登录wallet-cli
注册完成后，输入login命令登录wallet-cli。
```
wallet> login
```

选择要登录的账户，然后输入密码，密码输入正确后，会看到"Login successful !!!"字样，表示登录成功。

```
Please choose between 1 and 3
2
Please input your password.
password: 
Login successful !!!
wallet> 
```

登录后，可以通过getaddress命令查看登录的账户地址：
```
wallet> getaddress
GetAddress successful !!
address = TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz
wallet> 
```

然后可以通过backupwallet命令，根据提示输入密码后，查看账户的私钥，建议保存好私钥。


## 启动java-tron节点
java-tron是TRON网络客户端，它使计算机可以连接到TRON网络中。 本教程中的网络指的是TRON nile测试网。 要启动java-tron，请首先获取java-tron可执行文件，请参考[安装和部署](../using_javatron/installing_javatron.md)章节，然后通过如下命令，启动java-tron。
```
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c nile_net_config.conf
```
java-tron启动后，日志将包括以下内容：

```
11:07:58.758 INFO  [main] [app](Args.java:1143) ************************ Net config ************************
11:07:58.758 INFO  [main] [app](Args.java:1144) P2P version: 201910292
11:07:58.758 INFO  [main] [app](Args.java:1145) Bind IP: 192.168.20.101
11:07:58.758 INFO  [main] [app](Args.java:1146) External IP: 203.12.203.3
11:07:58.758 INFO  [main] [app](Args.java:1147) Listen port: 18888
11:07:58.758 INFO  [main] [app](Args.java:1148) Discover enable: true
```

上述日志表明java-tron已经启动并连接到了nile测试网，然后它将寻找可以连接的对等节点。一旦它找到了对等节点，就可以向它们请求区块了，日志也证实了这一点：

```
11:08:42.547 INFO  [TronJClientWorker-1] [net](Channel.java:116) Finish handshake with /123.56.3.74:18888.
11:08:42.547 INFO  [TronJClientWorker-1] [net](ChannelManager.java:161) Add active peer /123.56.3.74:18888 | fea80a0298b465a54fd332ff36819545d850115e77b327858b5306c9a58c6b8c2e7c08df76ab508a7594ed3577a8f4157727108442877077ab499b102b488467, total active peers: 1
11:08:42.549 INFO  [TronJClientWorker-1] [net](Channel.java:208) Peer /123.56.3.74:18888 status change to SYNCING.
11:08:42.566 INFO  [TronJClientWorker-1] [DB](Manager.java:1636) headNumber:23113867
11:08:42.566 INFO  [TronJClientWorker-1] [DB](Manager.java:1638) syncBeginNumber:23113867
11:08:42.567 INFO  [TronJClientWorker-1] [DB](Manager.java:1642) solidBlockNumber:23113849
11:08:42.567 INFO  [TronJClientWorker-1] [net](SyncService.java:179) Get block chain summary, low: 23113867, highNoFork: 23113867, high: 23113867, realHigh: 23113867
11:08:42.572 INFO  [TronJClientWorker-1] [net](MessageQueue.java:106) Send to /123.56.3.74:18888, type: SYNC_BLOCK_CHAIN
size: 1, start block: Num:23113867,ID:000000000160b08b510b6c501c980a2567bff1229eed62ca79874c9ca7828e9c 
11:08:42.631 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK_CHAIN_INVENTORY
size: 2001, first blockId: Num:23113867,ID:000000000160b08b510b6c501c980a2567bff1229eed62ca79874c9ca7828e9c, end blockId: Num:23115867,ID:000000000160b85b587ef18d00a1905d8022ec0a8fd174f3980b78f6aacf0ede

......

11:08:43.478 INFO  [pool-49-thread-1] [net](MessageQueue.java:106) Send to /123.56.3.74:18888, type: FETCH_INV_DATA
invType: BLOCK, size: 100, First hash: 000000000160b08c6eeba60eced4fb13d7c56e46a3c5220a67bb2801a05e5679, End hash: 000000000160b0efd90560e389d1f6e5b3c8d3877709ce375a8e063f5db73af9 
11:08:43.502 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK
Num:23113868,ID:000000000160b08c6eeba60eced4fb13d7c56e46a3c5220a67bb2801a05e5679, trx size: 1

11:08:43.504 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK
Num:23113869,ID:000000000160b08d231e450ae1993a72ba19eb8f3c748fa70d105dadd0c9fd5f, trx size: 0

11:08:43.504 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK
Num:23113870,ID:000000000160b08e37cb9951d31a4233f106c7e77e0535c597dbb6a16f163699, trx size: 0
```

这些日志表明java-tron按照预期运行着。可以通过向此java-tron节点发送如下http请求，来判断节点是否已经启动，以及查看节点的状态：
```
$ curl http://127.0.0.1:16887/wallet/getnodeinfo
```
如果节点日志中没有报告任何错误消息，则一切正常。为了让用户与TRON网络交互，java-tron节点必须是运行着，并且处于同步正常的状态。节点是否与网络中其它节点保持同步，可以通过在Tronscan查询当前的区块高度，并与本地java-tron节点`/wallet/getnowblock`的结果进行比较，如果相等，则说明本地节点的同步状态是正常的。

如果要关闭java-tron，请通过`kill -15 进程id`来暂停节点。

## 获取TRX
为了能够发送交易，用户的账户中需要持有TRX。在TRON网络主网上，只能通过三种方式获得TRX: 
1. 超级代表生产区块/为超级代表投票的奖励; 
2. 另一个TRON网络账户向其转账TRX; 
3. 从交易所获得。

在TRON测试网中，TRX没有实际价值, 可以通过 [水龙头](https://nileex.io/join/getJoinPage) 免费获得。

## 与java-tron交互

### 使用wallet-cli与java-tron节点进行交互
java-tron对外提供http接口和grpc接口，方便用户与TRON网络进行交互。wallet-cli使用的是grpc接口。
#### 获取账户信息
在wallet-cli中输入getaccount命令后，它将向java-tron节点请求账户信息数据，然后将结果展示到终端。
```
wallet> getaccount TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
```
结果为：
```
{
	"address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
	"balance": 93643857919,
	"create_time": 1619681898000,
	"latest_opration_time": 1655358327000,
	"is_witness": true,
	"asset_issued_name": "TestTRC10T",
	"latest_consume_free_time": 1652948766000,
	"account_resource": {
		"latest_consume_time_for_energy": 1655358327000
	},
    
        ......
}

```
#### 查询账户余额
通过getbalance命令查看一个账户的余额：
```
wallet> getbalance
Balance = 93642857919
wallet> 
```

#### 转账TRX
通过sendcoin命令来转账TRX，输入转入地址，及金额：
```
wallet> sendcoin TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf 1000000
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"amount":1000000,
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
						"to_address":"TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
					},
					"type_url":"type.googleapis.com/protocol.TransferContract"
				},
				"type":"TransferContract"
			}
		],
		"ref_block_bytes":"cbc3",
		"ref_block_hash":"8581ae7e29258a52",
		"expiration":1656917577000,
		"timestamp":1656917518232
	},
	"raw_data_hex":"0a02cbc322088581ae7e29258a5240a89aefbf9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c30"
}
before sign transaction hex string is 0a85010a02cbc322088581ae7e29258a5240a89aefbf9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
```

该命令返回转账TRX的交易，确认无误后，输入`y`确认，其它字母表示取消这个交易。如果输入`y`，则接下来根据提示，选择使用哪个账户的私钥进行签名，最后输入密码，完成对该交易的签名，wallet-cli最后会将签名后的交易发送到java-tron节点，完成交易：
```
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is .DS_Store
The 2th keystore file name is UTC--2022-07-04T06-35-35.304000000Z--TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz.json
The 3th keystore file name is UTC--2022-06-21T09-51-26.367000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 3
3
Please input your password.
password: 
after sign transaction hex string is 0a85010a02cbc322088581ae7e29258a5240dbfc91ca9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c301241241a3ce4797ccc2fedf49ae41af28b49df1e15a476e4948af4df5aadf23a1e940ad5cc2133f501c08f2bab6a2231cdc82a745fed0fc6a012dc19310532d9138600
txid is 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
Send 1000000 Sun to TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf successful !!
wallet> 
```

#### 根据交易id查询交易
上面通过sendcoin命令发送了一条转账TRX的交易，在wallet-cli终端打印出了交易的id：`0e28724f0963dff35c6c76149524d3ee1073463c6dd0ceb03a592bf2c1b37122`，接下来可以通过gettransactionbyid查询交易，也可以通过gettransactioninfobyid查询交易的结果。

```
wallet> gettransactionbyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
{
	"ret":[
		{
			"contractRet":"SUCCESS"
		}
	],
	"signature":[
		"241a3ce4797ccc2fedf49ae41af28b49df1e15a476e4948af4df5aadf23a1e940ad5cc2133f501c08f2bab6a2231cdc82a745fed0fc6a012dc19310532d9138600"
	],
	"txID":"21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4",
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"amount":1000000,
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
						"to_address":"TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
					},
					"type_url":"type.googleapis.com/protocol.TransferContract"
				},
				"type":"TransferContract"
			}
		],
		"ref_block_bytes":"cbc3",
		"ref_block_hash":"8581ae7e29258a52",
		"expiration":1656939118171,
		"timestamp":1656917518232
	},
	"raw_data_hex":"0a02cbc322088581ae7e29258a5240dbfc91ca9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c30"
}
wallet> 

```

```
wallet> gettransactioninfobyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
{
	"id": "21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4",
	"blockNumber": 27773932,
	"blockTimeStamp": 1656917586000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 267
	}
}
wallet> 
```


### 使用Curl与java-tron节点进行交互
上文介绍了如何使用wallet-cli与java-tron进行交互。与直接发送grpc/http命令相比，该工具提供更友好的交互式命令，使用户可以更方便的向java-tron发送指令。但是，如何直接发送HTTP请求到java-tron节点呢？ Curl是一个发送HTTP请求的命令行工具。本章节将说明如何通过Curl检查帐户余额，并发送交易。

#### 查询账户余额
可以通过节点HTTP接口`wallet/getaccount`来查询账户的TRX余额信息，返回结果中的balance即为TRX余额，以sun为单位：
```
 curl -X POST http://127.0.0.1:16887/wallet/getaccount -d 
     '{"address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
       "visible": true
     }'
```
结果为：
```
{"account_name": "testacc2","address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM","balance": 1000000000000000,"account_resource": {}}
```

#### 发送交易
通过http接口发送交易，总共需要三步：

1. 创建交易
2. 签名交易
3. 广播交易

下面以转账TRX为例来说明如何向java-tron发送交易。

通过fullnode HTTP接口`wallet/createtransaction`创建一个未签名的TRX转账交易：
```
curl -X POST  http://127.0.0.1:16887/wallet/createtransaction -d 
    '{
        "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf", 
        "owner_address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM", 
        "amount": 10000000,
        "visible":true
    }'
```
返回一个未签名的TRX转账交易：
```
{
    "visible": true,
    "txID": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "raw_data": {
        "contract": [
            {
                "parameter": {
                    "value": {
                        "amount": 10000000,
                        "owner_address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
                        "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
                    },
                    "type_url": "type.googleapis.com/protocol.TransferContract"
                },
                "type": "TransferContract"
            }
        ],
        "ref_block_bytes": "193b",
        "ref_block_hash": "aaecd88e4e0e7528",
        "expiration": 1656580476000,
        "timestamp": 1656580418228
    },
    "raw_data_hex": "0a02193b2208aaecd88e4e0e752840e098909f9b305a68080112640a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412330a154198927ffb9f554dc4a453c64b2e553a02d6df514b121541d0b69631440f0a494bb51f7eee68ff5c593c00f01880ade20470b4d58c9f9b30"
}
```
然后使用SDK对该交易进行签名。

最后，通过[`wallet/broadcasttransaction`](https://cn.developers.tron.network/reference/broadcasttransaction)接口将签名后的交易广播到java-tron节点，完成TRX转账交易的发送。

```
curl --location --request POST 'http://127.0.0.1:16887/wallet/broadcasttransaction' \
--header 'Content-Type: application/json' \
--data-raw '{
    "visible": true,
    "signature": [
        "e12996cfaf52f8b49e64400987f9158a87b1aa809a11a75e01bb230722db97a26204334aea945b1ece0851a89c96459872e56229b0bd725c4f6a0577bfe331c301"
    ],
    "txID": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "raw_data": {
        "contract": [
            {
                "parameter": {
                    "value": {
                        "amount": 10000000,
                        "owner_address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
                        "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
                    },
                    "type_url": "type.googleapis.com/protocol.TransferContract"
                },
                "type": "TransferContract"
            }
        ],
        "ref_block_bytes": "193b",
        "ref_block_hash": "aaecd88e4e0e7528",
        "expiration": 1656580476000,
        "timestamp": 1656580418228
    },
    "raw_data_hex": "0a02193b2208aaecd88e4e0e752840e098909f9b305a68080112640a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412330a154198927ffb9f554dc4a453c64b2e553a02d6df514b121541d0b69631440f0a494bb51f7eee68ff5c593c00f01880ade20470b4d58c9f9b30"
}'
```
执行结果为：

```
{
    "result": true,
    "txid": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}
```
结果返回true，表示交易广播成功。

#### 根据交易id查询交易
通过http接口 `wallet/gettransactionbyid`来查询交易的内容：
```
curl --location --request POST 'http://127.0.0.1:16887/wallet/gettransactionbyid' \
--header 'Content-Type: application/json' \
--data-raw '{
     "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}'
```
查询结果为：

```
{
    "ret": [
        {
            "contractRet": "SUCCESS"
        }
    ],
    "signature": [
        "e12996cfaf52f8b49e64400987f9158a87b1aa809a11a75e01bb230722db97a26204334aea945b1ece0851a89c96459872e56229b0bd725c4f6a0577bfe331c301"
    ],
    "txID": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "raw_data": {
        "contract": [
            {
                "parameter": {
                    "value": {
                        "amount": 10000000,
                        "owner_address": "4198927ffb9f554dc4a453c64b2e553a02d6df514b",
                        "to_address": "41d0b69631440f0a494bb51f7eee68ff5c593c00f0"
                    },
                    "type_url": "type.googleapis.com/protocol.TransferContract"
                },
                "type": "TransferContract"
            }
        ],
        "ref_block_bytes": "193b",
        "ref_block_hash": "aaecd88e4e0e7528",
        "expiration": 1656580476000,
        "timestamp": 1656580418228
    },
    "raw_data_hex": "0a02193b2208aaecd88e4e0e752840e098909f9b305a68080112640a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412330a154198927ffb9f554dc4a453c64b2e553a02d6df514b121541d0b69631440f0a494bb51f7eee68ff5c593c00f01880ade20470b4d58c9f9b30"
}
```


通过http接口 `wallet/gettransactioninfobyid`来查询交易结果及交易回执：

```
curl --location --request POST 'http://127.0.0.1:16887/wallet/gettransactioninfobyid' \
--header 'Content-Type: application/json' \
--data-raw '{
     "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}'
```
查询结果为：
```
{
    "id": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "blockNumber": 27662687,
    "blockTimeStamp": 1656580470000,
    "contractResult": [
        ""
    ],
    "receipt": {
        "net_usage": 268
    }
}
```




