# Java-tron入门

本文主要说明如何启动Java-tron节点，并通过命令行工具wallet-cli执行基本命令与Java-tron节点进行交互。关于Java-tron的安装，您可以直接下载可运行文件，也可以通过源代码构建，具体步骤可以参考[安装和构建](../using_javatron/installing_javatron.md)页面。本教程是基于Java-tron和相关开发工具已经成功安装的基础上进行介绍的。

本文涵盖了使用Java-tron的基础，这包括生成帐户、加入TRON nile测试网络、在帐户之间发送TRX。文档中也使用了wallet-cli，wallet-cli是TRON网络的一个命令行工具，该工具提供用户交互式命令，使用它可以更方便的与Java-tron进行交互。


Java-tron是用Java编写的TRON网络客户端，这意味着运行Java-tron的计算机会变成一个TRON网络节点。TRON网络是一个分布式网络，信息在节点之间共享，而不是由中央服务器管理。超级代表的节点在生成新的区块后，会将区块发送给其它节点。每个节点在接收到一个新的区块时，都会对其进行校验，校验通过后将其添加到自己的数据库中。Java-tron使用每个区块提供的信息来更新其“状态”——TRON网络上每个账户的余额。TRON网络上有两种类型的帐户:外部拥有的帐户和合约帐户。合约帐户在收到交易时执行合约代码。外部账户是用户在本地管理的帐户，以便签署和提交交易，比如通过TronLink钱包创建的账户。每个外部账户都是一个公私密钥对，其中公钥用于为用户派生一个唯一的地址，而私钥用于保护帐户和安全签署消息。因此，为了使用TRON网络，首先需要生成外部账户(以下简称“帐户”)。本教程将指导用户如何创建一个帐户，存入TRX代币，并转账TRX。


# 生成账户
有多种方法来生成TRON网络帐户，这里将演示如何使用wallet-cli生成帐户, 参考[安装和部署](../clients/wallet-cli.md)章节。帐户是一对密钥(公钥和私钥)。

在终端中通过命令`java -jar wallet-cli.jar`来启动一个wallet-cli：
```
$ java -jar wallet-cli.jar

Welcome to Tron Wallet-Cli
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

# 登录wallet-cli
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


# 启动Java-tron节点
Java-tron是TRON网络客户端，它使计算机可以连接到TRON网络中。 本教程中的网络指的是TRON nile测试网。 要启动Java-tron，请首先获取Java-tron可执行文件，请参考[安装和部署](../using_javatron/installing_javatron.md)章节，然后通过如下命令，启动Java-tron。
```
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c nile_net_config.conf
```
Java-tron启动后，日志将包括以下内容：

```
11:07:58.758 INFO  [main] [app](Args.java:1143) ************************ Net config ************************
11:07:58.758 INFO  [main] [app](Args.java:1144) P2P version: 201910292
11:07:58.758 INFO  [main] [app](Args.java:1145) Bind IP: 192.168.20.101
11:07:58.758 INFO  [main] [app](Args.java:1146) External IP: 203.12.203.3
11:07:58.758 INFO  [main] [app](Args.java:1147) Listen port: 18888
11:07:58.758 INFO  [main] [app](Args.java:1148) Discover enable: true
```

上述日志表明Java-tron已经启动并连接到了nile测试网，然后它将寻找可以连接的对等节点。一旦它找到了对等节点，就可以向它们请求区块了，日志也证实了这一点：

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

这些日志表明Java-tron按照预期运行着。可以通过向此Java-tron节点发送如下http请求，来判断节点是否已经启动，以及查看节点的状态：
```
$ curl http://127.0.0.1:16887/wallet/getnodeinfo
```
如果节点日志中没有报告任何错误消息，则一切正常。为了让用户与TRON网络交互，Java-tron节点必须是运行着，并且处于同步正常的状态。节点是否与网络中其它节点保持同步，可以通过在Tronscan查询当前的区块高度，并与本地Java-tron节点`/wallet/getnowblock`的结果进行比较，如果相等，则说明本地节点的同步状态是正常的。

如果要关闭Java-tron，请通过`kill -15 进程id`来暂停节点。

# 获取Nile测试网TRX
为了能够发送交易，用户的账户中需要持有TRX。在TRON网络主网上，只能通过三种方式获得TRX:
1. 超级代表生产区块/为超级代表投票的奖励;
2. 另一个TRON网络账户向其转账TRX;
3. 从交易所获得。

在TRON测试网中，TRX没有实际价值, 可以通过 [水龙头](https://nileex.io/join/getJoinPage) 免费获得。

# 与Java-tron交互
如果本地不便运行节点，或者节点要长时间同步数据才能获取最新的数据，可以使用TronGrid。TronGrid提供负载均衡的，安全的，可靠的的节点访问API，参考[TronGrid](../clients/tron-grid.md)。
Nile测试网的TronGrid地址为 https://nile.trongrid.io。其他网络节点或者grpc连接参考[Networks](https://developers.tron.network/docs/networks)。

## 使用wallet-cli与Java-tron节点进行交互
Java-tron对外提供http接口和grpc接口，方便用户与TRON网络进行交互。wallet-cli使用的是grpc接口。
### 获取账户信息
在wallet-cli中输入getaccount命令后，它将向Java-tron节点请求账户信息数据，然后将结果展示到终端。
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
### 查询账户余额
通过getbalance命令查看一个账户的余额：
```
wallet> getbalance
Balance = 93642857919
wallet>
```

### 转账TRX
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

该命令返回转账TRX的交易，确认无误后，输入`y`确认，其它字母表示取消这个交易。如果输入`y`，则接下来根据提示，选择使用哪个账户的私钥进行签名，最后输入密码，完成对该交易的签名，wallet-cli最后会将签名后的交易发送到Java-tron节点，完成交易：
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

### 根据交易id查询交易
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


## 使用Curl与Java-tron节点进行交互
上文介绍了如何使用wallet-cli与Java-tron进行交互。与直接发送grpc/http命令相比，该工具提供更友好的交互式命令，使用户可以更方便的向Java-tron发送指令。但是，如何直接发送HTTP请求到Java-tron节点呢？ Curl是一个发送HTTP请求的命令行工具, 可以把curl命令复制到Postman工具里使用。本章节将说明如何通过Curl检查帐户余额，并发送交易。如果本地节点无法访问，请使用TranGrid API.

### 查询账户余额
可以通过节点HTTP接口`wallet/getaccount`来查询账户的TRX余额信息，返回结果中的balance即为TRX余额，以sun为单位。

访问本地节点，注意本地节点如果同步中则可能数据不准确:
```
curl --location 'http://127.0.0.1:16887/wallet/getaccount' \
--header 'Content-Type: application/json' \
--data '{
    "address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
    "visible": true
}'
```
参考返回结果数据：
```
{"account_name": "testacc2","address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM","balance": 1000000000000000,"account_resource": {}}
```

也可以通过TranGrid访问其他远端节点:
```
 curl --location 'https://nile.trongrid.io/wallet/getaccount' \
--header 'Content-Type: application/json' \
--data '{
    "address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
    "visible":"true"
}'
```


### 发送交易
通过http接口发送交易，总共需要三步：

1. 创建交易
2. 签名交易
3. 广播交易

下面以转账TRX为例来说明如何向Java-tron发送交易。

通过fullnode HTTP接口`wallet/createtransaction`创建一个未签名的TRX转账交易：
```
curl --location 'http://127.0.0.1:16887/wallet/createtransaction' \
--header 'Content-Type: application/json' \
--data '{
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
                        "owner_address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
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

最后，通过[`wallet/broadcasttransaction`](https://cn.developers.tron.network/reference/broadcasttransaction)接口将签名后的交易广播到Java-tron节点，完成TRX转账交易的发送。

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

### 根据交易id查询交易
通过http接口 `wallet/gettransactionbyid`来查询交易的内容：
```
curl --location 'http://127.0.0.1:16887/wallet/gettransactionbyid' \
--header 'Content-Type: application/json' \
--data '{
    "value": "f51f427344460ea484e92a90dc8701a4bbdb57f8b29ce1d7a7dca1bd74a5e1f2",
    "visible": true
}'
```
参考查询结果为：
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




