# Java-tron 快速入门

本指南将引导您完成一系列 `java-tron` 的基础操作。您将学习如何：
- 启动一个 `java-tron` 节点，将您的计算机接入 TRON 网络
- 使用命令行工具 `wallet-cli` 生成新账户并获取免费的测试币
- 学习通过 `wallet-cli` 或使用 `cURL` 直接调用 API 发起一笔转账，并根据交易 ID 查询链上结果

执行本教程中的操作前，请确保已安装 `java-tron` 及相关的开发工具。如果您尚未安装，请参考[部署](../using_javatron/installing_javatron.md)页面了解具体步骤。

## 核心概念

`java-tron` 是用 Java 语言编写的波场（TRON）网络客户端，运行 `java-tron` 会将您的计算机转变为一个 TRON 网络节点。TRON 网络是一个分布式网络，信息在节点之间共享，而非通过中心化服务器管理。当超级代表（Super Representative）的节点产出一个新区块后，会将其广播至网络中的其它节点。每个节点在接收到新区块时会对其进行校验，校验通过后便将其存入本地数据库。

`java-tron` 通过同步区块来持续更新其“状态”——即 TRON 网络上所有账户的实时余额。

TRON 网络上有两种主要类型的帐户:
- **外部账户 (Externally Owned Accounts)**: 由用户通过其**本地管理**的**公私钥对**来控制。每个外部账户都是一个公私密钥对，其中公钥用于派生出独一无二的账户地址，而私钥则用于保护帐户和安全地签署、授权交易。您在本教程中创建的便是这种类型的账户。
- **合约账户 (Contract Accounts)**: 当收到交易时，这类账户会执行其中包含的智能合约代码。

要开始与波场网络交互，您首先需要创建一个外部账户（以下简称“帐户”）。

## 创建并访问您的账户

虽然创建波场账户有多种方式，但本指南将演示如何使用 `wallet-cli` 这一便捷的命令行工具来完成。帐户是一对密钥（公钥和私钥）。

### 生成账户

首先，在您的终端中通过命令`java -jar wallet-cli.jar`启动一个 `wallet-cli`：

```
$ java -jar wallet-cli.jar

Welcome to TRON wallet-cli
Please type one of the following commands to proceed.
Login, RegisterWallet or ImportWallet
 
You may also use the Help command at anytime to display a full list of commands.
 
wallet> 
```
输入 `registerwallet` 命令，并根据提示设置一个安全的密码。此命令会生成一个新的 TRON 网络账户，并将其注册到 `wallet-cli`，即将其加密后的**私钥**存储在 `wallet-cli` 的本地密钥库中，以便后续使用该私钥对交易进行签名。

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
### 登录并查看账户详情

注册成功后，使用 `login` 命令登录 `wallet-cli`。
```
wallet> login
```
选择您希望登录的账户序号并输入密码。看到 `Login successful !!!` 提示即表示登录成功。

```
Please choose between 1 and 3
2
Please input your password.
password: 
Login successful !!!
wallet> 
```
登录后，使用 `getaddress` 命令查看您的账户地址。
```
wallet> getaddress
GetAddress successful !!
address = TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz
wallet> 
```
**重要提示**：我们建议您备份私钥，以保障资产安全。使用 `backupwallet` 命令，按提示输入密码即可查看账户的私钥。请务必将私钥存放在一个绝对安全的地方。


## 启动并运行一个 Java-tron 节点

现在，您需要启动一个 `java-tron` 节点以连接到 TRON 网络。本教程将连接到 TRON Nile 测试网。

请使用以下命令启动节点。其中 `-Xmx24g` 标志为 JVM 分配了 24GB 内存，您可以根据自己机器的配置进行调整。（提示：在运行此命令前，请确保您已根据引言部分的说明，完成了 `java-tron` 的安装。）

```
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c nile_net_config.conf
```

`java-tron` 节点启动后，您将在日志中看到类似以下的配置信息：

```
11:07:58.758 INFO  [main] [app](Args.java:1143) ************************ Net config ************************
11:07:58.758 INFO  [main] [app](Args.java:1144) P2P version: 201910292
11:07:58.758 INFO  [main] [app](Args.java:1145) Bind IP: 192.168.20.101
11:07:58.758 INFO  [main] [app](Args.java:1146) External IP: 203.12.203.3
11:07:58.758 INFO  [main] [app](Args.java:1147) Listen port: 18888
11:07:58.758 INFO  [main] [app](Args.java:1148) Discover enable: true
```

上述日志表明 `java-tron` 已经启动并连接到了 Nile 测试网。接下来，节点会开始寻找网络中可连接的其他对等节点（peer），并通过持续向它们请求区块来同步整个链上数据。成功连接上的对等节点即为“活跃对等节点” (active peer)。以下日志表明节点已成功连接并开始同步数据：

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

您可通过向此 `java-tron` 节点发送如下 HTTP 请求，来验证节点是否已成功启动，并查看其当前状态：
```
$ curl http://127.0.0.1:16887/wallet/getnodeinfo
```

要与 TRON 网络进行交互，您的 `java-tron` 节点必须保持运行，并处于同步正常的状态。您可以分两步来验证节点是否正常：
- 基础检查：确认节点日志中没有持续报错。
- 同步验证：要确保您的节点已与网络完全同步，可将您本地节点的区块高度（通过 `/wallet/getnowblock` API 获取）与 [Tronscan](https://tronscan.org/) 区块浏览器上查询的最新区块高度进行比较。如果两者一致，则表示您本地节点的同步状态正常。

如果要关闭 `java-tron`，请通过`kill -15 <进程ID>`来暂停节点。

## 为您的账户充值 TRX
为了能在 TRON 网络上发送交易，您的账户中需要持有 TRX。
- 在 TRON 网络主网上，您可通过以下三种方式获取 TRX:
  1. 作为超级代表获得出块奖励，或通过为超级代表投票获得奖励;
  2. 从其他的 TRON 网络账户接收 TRX 转账;
  3. 从加密货币交易所获得。
- 在 Nile 测试网中，TRX 没有实际价值, 您可以通过 [水龙头](https://nileex.io/join/getJoinPage) 免费获取。

## 与 TRON 网络交互

您的 `java-tron` 节点是您与 TRON 网络交互的窗口，它通过 HTTP 和 gRPC 提供了强大的 API 接口。本章节将介绍如何通过 `wallet-cli` 和 `cURL` 这两种工具，向您的节点发送指令来完成链上操作。

### 方式一：使用 wallet-cli (推荐)

`wallet-cli` 封装了 gRPC 接口，提供了对开发者更友好的交互式命令。

#### 查询账户信息
您可以使用 `getaccount <地址>` 命令查询指定地址的详细信息。执行该命令时，`wallet-cli` 会在后台向 `java-tron` 节点发送请求，然后将获取到的账户数据呈现在终端界面。

```
wallet> getaccount TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
```
返回结果如下：
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
使用 `getbalance` 命令可快速查看当前登录账户的 TRX 余额。
```
wallet> getbalance
Balance = 93642857919
wallet> 
```

#### 转账 TRX
使用 `sendcoin <接收方地址> <转账金额>` 命令发起一笔 TRX 转账。金额单位为 sun（1 TRX = 1,000,000 sun）。
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
此命令会返回一个待确认的交易。请按以下步骤完成签名和广播：
1. 确认交易: 核对交易详情无误后，输入 `y` 并按回车键（输入其他任意字符则会取消交易）。
2. 选择签名账户: 根据界面提示，选择用于给这笔交易签名的账户（即扣款账户）。
3. 输入密码授权: 输入所选账户的密码，`wallet-cli` 将会完成签名，并将交易广播至 `java-tron` 节点，完成交易。

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

#### 根据交易 ID 查询交易详情

当您发送一笔交易后，`wallet-cli` 终端会返回一个唯一的交易ID（txid）。通过这个 `txid`，您可以查询到关于这笔交易的所有信息。

1. 使用 `gettransactionbyid <txid>` 查看交易的原始内容：
```
wallet> gettransactionbyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
```
返回的 JSON 数据包含了交易的所有细节，例如合约类型 (`TransferContract`)、转账金额、发送方和接收方地址等。`"contractRet":"SUCCESS"` 表示这笔交易的合约在语法上是正确的。

```
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
2. 使用 `gettransactioninfobyid <txid>` 查看交易的处理结果和回执信息（即交易是否已经被打包进区块，执行的结果和资源消耗情况）：
```
wallet> gettransactioninfobyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
```
在返回的结果中，最重要的字段是 `blockNumber`，它表示交易在哪一个区块高度被确认。如果这个值存在，说明交易已成功上链。此外，`receipt` 对象则记录了该交易消耗的带宽（`net_usage`）等资源。
```
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

### 方式二：使用 cURL（直接调用 HTTP API）

虽然 `wallet-cli` 提供了友好的交互式命令，但对于更进阶的开发者或在自动化脚本场景中，直接通过 HTTP API 与 `java-tron` 节点交互会更加灵活高效。本章节将展示如何使用 `cURL` (一个发送 HTTP 请求的命令行工具)，调用 `java-tron` 节点的 HTTP API, 来实现查询账户余额、发送交易等核心功能。

与 `wallet-cli` 自动完成签名和广播不同，直接调用 API 发送一笔交易，需要您手动完成一个标准的“三步走”流程：**创建 -> 签名 -> 广播**。本章节将向您展示如何执行这个流程。

#### 准备工作：查询账户余额

在发送交易前，我们先用通过节点 HTTP 接口 `wallet/getaccount` 来查询一个账户的 TRX 余额。

向节点的 `16887` 端口发送一个 POST 请求，请求体中包含您要查询的地址。

```
 curl -X POST http://127.0.0.1:16887/wallet/getaccount -d 
     '{"address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
       "visible": true
     }'
```
返回的 JSON 数据中，`balance` 字段即为该地址的 TRX 余额，单位为 sun (1 TRX = 1,000,000 sun)。
```
{
    "account_name": "testacc2",
    "address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
    "balance": 1000000000000000,"account_resource": {}
}
```

#### 发送交易的三步流程

现在，让我们以 TRX 转账为例说明如何向 `java-tron` 发送交易，完整地演示“创建-签名-广播”这三个步骤。

1. 创建一笔交易

通过 fullnode HTTP 的 `wallet/createtransaction` 接口，创建一笔未签名的 TRX 转账交易。在请求体中，指明发送方 (`owner_address`)、接收方 (`to_address`) 和金额 (`amount`)。

```
curl -X POST  http://127.0.0.1:16887/wallet/createtransaction -d 
    '{
        "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf", 
        "owner_address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM", 
        "amount": 10000000,
        "visible":true
    }'
```
节点会返回一个未签名的 TRX 转账交易。请记下其中的 `txID` 和 `raw_data_hex`，它们将在后续步骤中使用。
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
2. 对交易进行签名

使用发送方账户的私钥，对上一步生成的交易数据 (`raw_data_hex` 或 `txID`) 进行签名，以证明您对该账户的所有权。

**重要提示**: 
- 为保障私钥安全，建议您始终在本地或安全的服务器环境中，并使用 TRON 官方提供的 SDK (如 `TronWeb`, `java-tron-sdk` 等) 完成所有签名操作。
- `cURL` 无法执行签名操作。此步骤仅作流程说明。

签名后，您会得到一个长字符串，即交易的签名哈希 (Signature Hash)。

3. 广播交易

最后一步，我们将已签名的交易广播出去。调用  [`wallet/broadcasttransaction`](https://cn.developers.tron.network/reference/broadcasttransaction) 接口，并在其请求体中填入第一步获取的交易对象和第二步生成的签名哈希。提交后，节点会验证签名，然后将交易广播至整个 TRON 网络等待打包确认，至此便完成了整个转账流程。

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
如果返回结果中的 `"result": true`，则代表您的交易已成功广播:
```
{
    "result": true,
    "txid": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}
```

#### 根据交易 ID 查询交易

通过 HTTP API 查询已广播的交易，原理与 `wallet-cli` 相同。

1. 通过 HTTP 接口 `wallet/gettransactionbyid` 获取已广播交易的完整数据。在请求体中，通过 `value` 字段传入您要查询的 `txid`：

```
curl --location --request POST 'http://127.0.0.1:16887/wallet/gettransactionbyid' \
--header 'Content-Type: application/json' \
--data-raw '{
     "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}'
```
返回结果的数据结构与 `wallet-cli` 的 `gettransactionbyid` 命令基本一致：
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
2. 通过 http 接口 `wallet/gettransactioninfobyid` 查看交易的处理结果和回执信息（即交易是否已经被打包进区块，执行的结果和资源消耗情况）。在请求体中传入目标 `txid`：

```
curl --location --request POST 'http://127.0.0.1:16887/wallet/gettransactioninfobyid' \
--header 'Content-Type: application/json' \
--data-raw '{
     "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}'
```
返回结果中的 `blockNumber` 字段是交易成功的关键凭证，只要这个字段有值，就代表您的交易已成功上链且不可逆转。而 `receipt` 字段则提供了详细的执行回执。
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
恭喜您完成了 `java-tron` 的入门之旅！您已经亲手操作并掌握了创建账户、运行节点和发送交易等核心技能。

这仅仅是一个开始。基于今天所学，您可以继续探索更高级的主题，例如：
- 深入了解波场的[资源模型](..mechanism-algorithm/resource/.md)
- 探索完整的 [API 参考文档](api/http)，发现更多可能性

