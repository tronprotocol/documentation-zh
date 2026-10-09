# java-tron 快速入门

本指南将引导您完成一系列 java-tron 的基础操作。我们建议按以下顺序学习：

- [**创建 TRON 账户**](#create-account)：
    - 获得您在区块链世界的数字身份。学习如何安全地生成和管理您的地址与私钥，这是您持有 TRX 资产、发送交易以及与智能合约交互的唯一凭证。
- [**启动并运行一个 java-tron 节点**](#start-node)（可选）：
    - 搭建您与 TRON 网络连接的专用网关。将您的计算机接入 TRON 网络，使其成为网络的一部分。这对于希望成为网络维护者或需要本地、高可用 API 服务的开发者至关重要。
- [**使用 java-tron 节点与 TRON 网络交互**](#interact-with-tron)：
    - 学习如何通过客户端工具（如 `wallet-cli` 或 `cURL`）发送交易、查询链上数据（此技能不要求您自己运行节点，您可以使用公共节点服务完成操作）。


## 核心概念

java-tron 是用 Java 语言编写的 TRON 网络客户端，运行 java-tron 会将您的计算机转变为一个 TRON 网络节点。TRON 网络是一个分布式网络，信息在节点之间共享，而非通过中心化服务器管理。当超级代表（Super Representative）的节点产出一个新区块后，会将其广播至网络中的其它节点。每个节点在接收到新区块时会对其进行校验，校验通过后便将其存入本地数据库。java-tron 通过同步区块来持续更新其“状态”——即 TRON 网络上所有账户的实时余额。

与任何区块链交互的第一步都是连接到正确的网络。TRON 网络主要分为：

- Mainnet (主网)：用于处理真实资产交易的生产环境。
- Nile/Shasta Testnet (测试网)：供开发者免费测试应用和智能合约的公共环境。

对于开发和学习，我们必须使用测试网，以避免任何实际的资产损失。本指南使用的网络是 TRON [Nile 测试网](https://nileex.io/)。


## 技能一：创建 TRON 账户 { #create-account }

TRON 网络上有两种主要类型的帐户:

- **外部账户 (Externally Owned Accounts)**: 由用户通过其**本地管理**的**公私钥对**来控制。每个外部账户都是一个公私密钥对，其中公钥用于派生出独一无二的账户地址，而私钥则用于保护帐户和安全地签署、授权交易。您在本教程中创建的便是这种类型的账户。
- **合约账户 (Contract Accounts)**: 当收到交易时，这类账户会执行其中包含的智能合约代码。

要开始与 TRON 网络交互，您需要创建一个外部账户（以下简称“帐户”）。创建 TRON 账户有多种方式，例如通过软件开发工具包 (SDK) (如 [Trident-java](https://tronprotocol.github.io/trident/)，[TronWeb](https://tronweb.network/)) 或各类钱包应用（如浏览器插件钱包 [TronLink](https://www.tronlink.org/)）。

在本指南中，我们将使用 `wallet-cli` 来创建您的 TRON 账户。

> **关于 `wallet-cli`**
> 
>`wallet-cli` 提供 Java 和 TypeScript 两种实现：Java 版采用交互式命令行，通过 gRPC 连接节点；TypeScript 版通过 npm 安装，面向脚本和自动化，通过 FullNode HTTP 接口访问节点。两者都可以在本地管理钱包、签名和广播交易，以及查询链上数据。本指南使用 Java 版。
>
> 在继续之前，请务必完成 `wallet-cli` 的下载与编译。本指南仅引用 `wallet-cli` 的几个基础命令作为示例，完整说明参见 [Java CLI 环境准备](../clients/wallet-cli/java/index.md#setup)。


现在，请按顺序完成以下三个准备步骤。

### 步骤 A：启动工具并配置网络


**1. 启动 `wallet-cli`**

在您的终端中通过命令 `java -jar wallet-cli.jar` 启动一个 `wallet-cli` 实例：

```bash
java -jar wallet-cli.jar

Welcome to TRON wallet-cli
Please type one of the following commands to proceed.
Login, RegisterWallet or ImportWallet

You may also use the Help command at anytime to display a full list of commands.

wallet> 
```

**2. 配置网络**

`wallet-cli` 默认的工作环境是 TRON 主网 (Mainnet)。请先将环境切换至 Nile 测试网，以避免在本指南的后续操作中与真实资产交互。

您可使用 `switchnetwork` 命令切换网络，并用 `currentnetwork` 命令验证网络状态。当提示选择网络时，输入 `2` 选择 `NILE`。

```text
wallet> switchnetwork
Please select network：
1. MAIN
2. NILE
3. SHASTA
Enter numbers to select a network (1-3): 2
Now, current network is : NILE
SwitchNetwork successful !!!
wallet> currentnetwork
currentNetwork: NILE
```

### 步骤 B：创建账户

**1. 注册新账户**

在提示符后输入 `registerwallet` 命令，并根据提示设置一个安全的密码。此命令会生成一对公钥和私钥，并从公钥派生出账户地址。它会将加密后的私钥保存在本地，以便后续对交易进行签名，但不会激活链上账户。步骤 C 将介绍如何通过接收 TRX 转账，在主网或 Nile 测试网上为地址充值并激活账户。

```text
wallet> registerwallet
Please input password.
password: 
Please input password again.
Please enter the number of mnemonic words 
        Default: 12 mnemonic words, 
        Enter 24 to use 24 mnemonic words
        Press Enter to use the default (12). 
        Valid inputs are "12" or "24"
mnemonic file : ./Mnemonic/(your wallet address).json
Please name your wallet: 
register a wallet successful, keystore file : ./Wallet/(your wallet address).json
(Note: If you delete an account, make sure to delete the wallet file and mnemonic file) 
wallet> 
```

**2. 登录并查看地址**：

首先，在 `wallet-cli` 中使用 `login` 命令。系统会列出当前已有的账户供您选择。

```text
wallet> login
```

如您有多个账户，请根据提示，输入您希望登录的账户所对应的序号（例如 `2`），然后输入该账户的密码。

```text
Please choose between 1 and 3
2
Please input your password.
password: 
Login successful !!!
wallet> 
```

看到 `Login successful !!!` 提示即表示登录成功。您可使用 `getaddress` 命令查看当前账户的地址。

```text
wallet> getaddress
GetAddress successful !!
address = TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz
wallet> 
```

**3. 备份私钥 (重要)**：

我们强烈建议您在完成账户创建后立即备份私钥，并将其存放在绝对安全的地方。使用 `backupwallet` 命令，并按提示输入密码，即可查看账户的私钥。


### 步骤 C：为账户充值 TRX 并激活账户

新地址接收 TRX 转账时，会在转账所在的网络上创建链上账户记录并激活账户。主网和 Nile 的账户记录相互独立：在一个网络上激活地址，不会激活另一个网络上的同一地址。

链上交易会消耗带宽，智能合约执行还会消耗能量。账户的免费额度可用于支付带宽消耗，额外的带宽和能量可通过质押或接收他人代理的资源获得。可用资源不足时，可能需要燃烧 TRX 来支付费用。发送交易前，请确保有足够的资源，以及足以支付转账金额和相关费用的 TRX。本教程使用测试 TRX 激活地址并完成示例转账。TRX 的获取方式因网络而异：

- **在 TRON 网络主网 (Mainnet)**，TRX 是真实资产，主要通过以下方式获得：
    - 作为超级代表获得出块奖励，或通过为超级代表投票获得奖励
    - 从其他的 TRON 网络账户接收 TRX 转账
    - 从加密货币交易所购买

    要激活主网上新生成的地址，请让一个已有的主网账户向该地址转入 TRX。

- **在 Nile 测试网 (Testnet)**，TRX 没有实际价值。您可以通过访问 [水龙头 (Faucet)](https://nileex.io/join/getJoinPage) 免费获取。详细流程可参考 [如何获取测试币](https://developers.tron.network/docs/getting-testnet-tokens-on-tron)。

    接收水龙头的 TRX 转账会激活您在 Nile 上的地址。您也可以通过接收已有 Nile 账户的 TRX 转账来激活地址。

完成以上所有准备工作后，您现在拥有了一个配置正确、网络环境安全且持有测试币的 TRON 账户。

## 技能二：启动并运行一个 java-tron 节点 { #start-node }

本模块为可选步骤。如果您使用公共节点，可以跳过节点部署，直接进入[技能三：使用 java-tron 节点与 TRON 网络交互](#interact-with-tron)。

本模块将指导您启动一个 java-tron 节点。运行自己的节点可让您自行管理 API 访问和限流设置。java-tron 提供可配置的 API 限流，您可以在运行自己的节点时进行管理。本模块使用 TRON 的 [Nile 测试网](https://nileex.io/)。

> 提示：
> 
> - 执行本教程中的操作前，请确保已安装 java-tron 及相关的开发工具。如果您尚未安装，请参考 [部署](../using_javatron/installing_javatron.md) 页面了解具体步骤。
> - 教程中的启动命令仅为基础演示。关于更详细的部署与配置，请参考 [Nile 官方节点部署指南](https://nileex.io/run/getRunPage)。
> - Nile 测试网不支持从创世区块（区块 0）开始同步数据。为快速启动节点，请下载官方提供的数据快照。具体操作可参阅 [使用数据快照部署节点](../using_javatron/backup_restore.md) 指南。

### **1. 启动节点**

启动命令请参考[启动全节点连接 Nile 测试网](../using_javatron/installing_javatron.md#starting-a-fullnode-on-the-nile-test-network)。

### 2. 验证节点状态

**2.1 查看启动与同步日志**

启动过程中，java-tron 会打印网络配置。以下日志展示了 Nile 使用的配置值，但不能证明节点已完成启动或已连接到其他节点。日志中的类名、内容和行号可能因版本而异：

```text
11:07:58.758 INFO  [main] [app](Args.java:1143) ************************ Net config ************************
11:07:58.758 INFO  [main] [app](Args.java:1144) P2P version: 201910292
11:07:58.758 INFO  [main] [app](Args.java:1145) Bind IP: 192.168.20.101
11:07:58.758 INFO  [main] [app](Args.java:1146) External IP: 203.12.203.3
11:07:58.758 INFO  [main] [app](Args.java:1147) Listen port: 18888
11:07:58.758 INFO  [main] [app](Args.java:1148) Discover enable: true
```

接下来，节点会寻找对等节点并请求缺失的区块，以更新本地区块链数据。以下日志展示了对等节点握手后开始同步区块的过程；日志内容可能因版本而异：

```text
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

接收消息中的区块号持续增长，说明区块数据正在到达，但不能仅凭这一点证明区块已通过验证并应用到本地区块链。请检查 `/wallet/getnowblock` 返回的本地最新区块高度是否持续增长。如果网络仍在出块，而本地最新区块高度长时间不再增长，或日志反复出现错误，请检查节点的连接和同步状态。

**2.2 使用 API 确认同步状态**

要与 TRON 网络进行交互，您的 java-tron 节点必须保持运行，并处于同步正常的状态。

您可向 java-tron 节点发送如下 HTTP 请求，来验证其是否已成功启动，并查看当前状态：

- 通过 `/wallet/getnodeinfo` API 获取节点概况: 
`curl http://127.0.0.1:8090/wallet/getnodeinfo`
- 通过 `/wallet/getnowblock` API 获取当前区块高度: 
`curl http://127.0.0.1:8090/wallet/getnowblock`

将本地节点的区块高度与 [Nile Tronscan 区块浏览器](https://nile.tronscan.org/) 上的最新高度进行比较。请使用与节点属于同一网络的区块浏览器。两次查询之间可能产生新区块，因此暂时出现较小的高度差是正常的。请多次检查，确认本地最新区块高度持续增长并接近网络最新高度；单次高度相同不足以证明同步状态正常。

### 3. 关闭节点

如果要关闭 java-tron，请通过`kill -15 <进程ID>`来停止节点。


## 技能三：使用 java-tron 节点与 TRON 网络交互 { #interact-with-tron }

本模块的核心是学习如何使用 java-tron 节点提供的 API 接口与 TRON 网络进行通信。java-tron 节点是您与区块链交互的网关，它通过开放强大的 HTTP 和 gRPC 接口，让任何客户端应用都能够查询链上数据或广播交易。

在开始交互前，您可以选择两种节点连接方式：

- **使用公共节点**（推荐新手）：无需等待同步，立即开始体验
- **使用自有节点**（如已完成技能二）：自行管理 API 访问，并配置限流

`wallet-cli` 示例使用技能一中选择的**公共 Nile 节点**。cURL 示例使用位于 `http://127.0.0.1:8090` 的**本地 Nile 全节点**，需要先完成技能二的部署。如果您跳过了节点部署，可以继续使用 `wallet-cli`，或将 HTTP 示例中的基础 URL 替换为所选公共 Nile 节点服务的地址。

### 方式一：使用 `wallet-cli` (推荐)

#### 查询账户信息

您可以使用 `getaccount <地址>` 命令查询指定地址的详细信息。执行该命令时，`wallet-cli` 会在后台向 java-tron 节点发送请求，然后将获取到的账户数据呈现在终端界面。

```text
wallet> getaccount TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
```

返回结果如下：

```json
{
	"address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
	"balance": 5,
	"create_time": 1663487574000,
	"net_window_size": 28800000,
	"net_window_optimized": true,
	"account_resource": {
		"energy_window_size": 28800000
        "energy_window_optimized": true
	},
    
        ......
}

```

#### 查询账户余额

使用 `getbalance` 命令可快速查看当前登录账户的 TRX 余额。

```text
wallet> getbalance
Balance = 93642857919
wallet> 
```

#### 转账 TRX

使用 `sendcoin <接收方地址> <转账金额>` 命令发起一笔 TRX 转账。金额单位为 sun（1 TRX = 1,000,000 sun）。

```text
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
Please confirm and input your permission id, if input y/Y means default 0, other non-numeric characters will cancel transaction.
```

此命令会返回一笔未签名的交易。请按以下步骤完成签名和广播：

1. 确认交易：核对交易详情无误后，输入 `y` 或 `Y`，使用默认权限 ID `0`。
2. 选择签名账户：选择发送方账户的钱包来签名交易。本教程使用账户的默认权限。
3. 输入密码授权：输入所选钱包的密码，`wallet-cli` 会对交易签名并将其广播至 java-tron 节点。广播成功不代表交易已被打包进区块或已确认，请按照下文查询交易状态。

```text
Please confirm and input your permission id, if input y/Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.

No.  Address                  Name
1    (your wallet address)
2    (your wallet address)
3    (your wallet address)
Please choose between 1 and 3, or enter search to search wallets
3
Please input your password.
password: 
after sign transaction hex string is 0a85010a02cbc322088581ae7e29258a5240dbfc91ca9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c301241241a3ce4797ccc2fedf49ae41af28b49df1e15a476e4948af4df5aadf23a1e940ad5cc2133f501c08f2bab6a2231cdc82a745fed0fc6a012dc19310532d9138600
txid is 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
Send 1000000 Sun to TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf successful !!
wallet> 
```

#### 根据交易 ID 查询交易详情

当您发送一笔交易后，`wallet-cli` 终端会返回一个唯一的交易ID（`txid`）。通过这个 `txid`，您可以查询到关于这笔交易的所有信息。

1. 使用 `gettransactionbyid <txid>` 查看交易的原始内容：

```text
  wallet> gettransactionbyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
```

返回的 JSON 数据包含合约类型（`TransferContract`）、转账金额、发送方和接收方地址等交易详情。`"contractRet":"SUCCESS"` 表示交易执行成功。

```json
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

```text
  wallet> gettransactioninfobyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
```

`blockNumber` 字段表示包含该交易的区块高度。交易入块本身不能证明执行成功或已固化确认：执行失败的智能合约交易也可能被打包进区块。请检查执行结果和回执，并通过本指南末尾介绍的固化状态查询方式检查确认状态。`receipt` 对象还记录了带宽（`net_usage`）等资源消耗。

```json
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

### 方式二：使用 `cURL`（直接调用 HTTP API）

虽然 `wallet-cli` 提供了友好的交互式命令，但对于更进阶的开发者或在自动化脚本场景中，直接通过 HTTP API 与 java-tron 节点交互会更加灵活高效。本章节将展示如何使用 `cURL` (一个发送 HTTP 请求的命令行工具)，调用 java-tron 节点的 HTTP API, 来实现查询账户余额、发送交易等核心功能。

与 `wallet-cli` 自动完成签名和广播不同，直接调用 API 发送一笔交易，需要您手动完成一个标准的“三步走”流程：**创建 -> 签名 -> 广播**。本章节将向您展示如何执行这个流程。

#### 准备工作：查询账户余额

在发送交易前，我们先用通过节点 HTTP 接口 `wallet/getaccount` 来查询一个账户的 TRX 余额。

本地 Nile 全节点启动并完成同步后，向其 `8090` 端口发送一个 `POST` 请求，请求体中包含您要查询的地址。

```bash
 curl -X POST http://127.0.0.1:8090/wallet/getaccount \
     -H 'Content-Type: application/json' \
     -d '{"address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
       "visible": true
     }'
```

返回的 JSON 数据中，`balance` 字段即为该地址的 TRX 余额，单位为 sun (1 TRX = 1,000,000 sun)。

```json
{
    "account_name": "testacc2",
    "address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
    "balance": 1000000000000000,"account_resource": {}
}
```

#### 发送交易的三步流程

现在，让我们以 TRX 转账为例说明如何向 java-tron 发送交易，完整地演示“创建-签名-广播”这三个步骤。

**第一步 - 创建一笔交易**

  通过 FullNode HTTP 的 `wallet/createtransaction` 接口，创建一笔未签名的 TRX 转账交易。在请求体中，指明发送方 (`owner_address`)、接收方 (`to_address`) 和金额 (`amount`)。
  
  ```bash
  curl -X POST http://127.0.0.1:8090/wallet/createtransaction \
      -H 'Content-Type: application/json' \
      -d '{
          "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf", 
          "owner_address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
          "amount": 10000000,
          "visible":true
      }'
  ```

  节点会返回一个未签名的 TRX 转账交易。请记下其中的 `txid` 和 `raw_data_hex`，它们将在后续步骤中使用。

  ```json
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

**第二步 - 对交易进行签名**

  使用发送方账户的私钥，对交易 ID（`txID`）进行签名。`txID` 是序列化后的 `raw_data` 的 SHA-256 哈希。
  
  **重要提示**: 
  
- 为保障私钥安全，请在本地或安全的服务器环境中，使用 `TronWeb` 或 `Trident-java` 等 TRON SDK 完成签名。
- `cURL` 无法执行签名操作。此步骤仅作流程说明。
  
  已签名交易的 `signature` 数组中包含十六进制编码的签名。

**第三步 - 广播交易**

  调用 [`wallet/broadcasttransaction`](../api/http/tx-build-and-broadcast/broadcasttransaction.md) 接口，并传入第二步得到的已签名交易对象。节点会验证交易（包括签名），并尝试将其传播给对等节点。成功响应表示节点已接受广播，不代表交易已入块、链上执行成功或已固化确认。广播后请分别查询这些状态。
  
  ```bash
  curl --location --request POST 'http://127.0.0.1:8090/wallet/broadcasttransaction' \
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

  ```json
  {
      "result": true,
      "txid": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
  }
  ```

#### 根据交易 ID 查询交易

通过 HTTP API 查询已广播的交易，原理与 `wallet-cli` 相同。

**`wallet/gettransactionbyid`**

当交易已被打包进节点已知的区块后，可通过 HTTP 接口 `wallet/gettransactionbyid` 获取交易数据。刚广播的交易可能暂时查不到，请在入块后重试。在请求体中，通过 `value` 字段传入要查询的交易 ID：

  ```bash
  curl --location --request POST 'http://127.0.0.1:8090/wallet/gettransactionbyid' \
  --header 'Content-Type: application/json' \
  --data-raw '{
       "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
  }'
  ```

  返回结果的数据结构与 `wallet-cli` 的 `gettransactionbyid` 命令基本一致：

  ```json
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

**`wallet/gettransactioninfobyid`**

通过 HTTP 接口 `wallet/gettransactioninfobyid` 查看交易的处理结果和回执信息（即交易是否已经被打包进区块，执行的结果和资源消耗情况）。

  在请求体中传入目标 `txid`：
  
  ```bash
  curl --location --request POST 'http://127.0.0.1:8090/wallet/gettransactioninfobyid' \
  --header 'Content-Type: application/json' \
  --data-raw '{
       "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
  }'
  ```

  `blockNumber` 字段表示包含该交易的区块高度。要检查执行是否成功，请使用上文的 `wallet/gettransactionbyid`：`ret` 数组中的 `"contractRet":"SUCCESS"` 表示执行成功。交易入块不代表已固化确认。`receipt` 字段记录带宽用量（`net_usage`）等资源消耗。

  要检查固化确认状态，请使用同一个交易 ID 查询 `/walletsolidity/gettransactionbyid`。此接口读取固化状态。本地节点启用 Solidity HTTP 服务后，其默认端口为 `8091`；公共节点服务可能在与其他 API 相同的基础 URL 下提供此路径。接口返回交易后，请检查 `ret` 数组中的 `contractRet` 是否为 `SUCCESS`，以确认执行成功。

  ```json
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

## 总结与展望

恭喜您完成了 java-tron 的入门之旅！您已经亲手操作并掌握了运行节点、创建账户和发送交易等核心技能，为深入探索 TRON 生态打下了坚实的基础。



