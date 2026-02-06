# 事件订阅

TRON 提供了强大的事件订阅机制，使开发者能够实时捕获链上关键事件，例如交易状态、合约调用和区块生成，从而构建功能丰富的去中心化应用（DApps）。

TRON 支持两种事件订阅方式，开发者可根据不同的使用场景进行选择：

* [本地事件插件订阅](#_2)
* [内置消息队列（ZeroMQ）订阅](#zeromq)

## 本地事件插件订阅（推荐）

该方式基于可扩展的插件架构，可将链上事件实时或批量持久化到外部系统，如 **MongoDB** 数据库或 **Kafka** 消息队列。此方案专为对事件可靠性、持久化和数据分析有较高要求的生产环境而设计。

这种方式有如下优势：

  - **多样化的插件支持：** 目前支持 Kafka 和 MongoDB。
  - **丰富的数据类型：** 可订阅区块、交易、智能合约事件及日志。
  - **支持复杂过滤：** 可根据特定条件过滤事件。
  - **历史事件回溯：** V2.0 框架支持从指定区块高度开始同步历史事件。
  - **生产级可靠性：** 推荐用于需要数据完整性和可靠性的场景。

### 事件服务框架

Java-tron 当前支持两个事件服务框架版本：`V1.0` 和 `V2.0`。

  - **V1.0：** 仅支持新区块产生时的实时事件推送。
  - **V2.0：** **推荐使用**，新增了历史事件回溯功能，允许从任意区块高度开始同步。

详细对比与选择建议请参考：[事件服务框架 V2.0 介绍](https://medium.com/tronnetwork/event-service-framework-v2-0-0622f2f07249)。

**事件服务工作流程：**

1.  **事件采集：** TRON 节点从链上区块中获取事件信息。
2.  **事件入队：** 将事件封装并写入事件缓存队列。
3.  **插件消费：** 事件插件异步消费队列数据。
4.  **事件推送：** 插件将数据推送到目标系统（例如 Kafka 或 MongoDB）。
5.  **业务处理：** 外部业务应用持续消费这些事件数据。


#### 如何迁移至新版事件服务（V2.0）

新版 `V2.0` 事件服务框架引入了历史事件回溯功能，并对事件推送机制进行了全面优化。以下是迁移至 `V2.0` 的操作步骤。

**迁移前评估**

在迁移之前，请考虑以下因素：

  - 内部交易日志支持： `V2.0` 暂不支持内部交易日志（`internalTransactionList` 字段为空）。如果您的业务依赖此字段，请继续使用 `V1.0`。
  - 插件版本： 建议将事件插件同步升级至最新版，以避免在处理大量历史数据时可能出现的性能问题。

**迁移操作步骤**

##### 步骤 1：获取新版事件插件

你可以从 GitHub 获取源码并自行构建，或直接下载官方发布的版本。

* 通过源码构建

```
git clone git@github.com:tronprotocol/event-plugin.git
cd event-plugin
git checkout master
./gradlew build
```
构建完成后，生成的 `.zip` 文件即为插件包。

* 直接下载官方发布版本

访问 [event-plugin Releases 页面](https://github.com/tronprotocol/event-plugin/releases) 下载最新插件包。

##### 步骤 2：修改 FullNode 配置

在 `config.conf` 文件中，将事件服务版本修改为使用`V2.0`，值为 1 。

```
event.subscribe.version = 1 # 1 表示 V2.0，0 表示 V1.0
```

##### 步骤 3：配置事件插件

新版插件的配置方式与旧版基本一致，你可以参考如下文档进行部署：

  - [事件插件部署(MongoDB)](#use-mongodb)
  - [事件插件部署(Kafka)](#use-kafka)

##### 步骤 4（可选）：配置历史事件同步起点

如果你需要从指定区块高度开始同步历史事件，请在配置文件中加入以下配置。

```
event.subscribe.startSyncBlockNum = <block_height>
```

##### 步骤 5：启动 FullNode 和插件

完成上述配置后，使用以下命令启动 `FullNode` 并加载事件插件。

```
java -jar FullNode.jar -c config.conf --es
```
<a id="use-kafka"></a>
### Kafka 事件订阅插件部署与使用指南

本指南旨在帮助开发者高效搭建并运行 TRON Kafka 事件订阅插件，用以监听 TRON 链上事件。我们将从环境准备讲起，一步步带您完成部署、配置和最终验证。主要步骤包括：

- [检查系统配置](#checking-system-configuration-1)
- [编译事件插件](#compiling-the-event-plugin-1)
- [部署并运行 Kafka](#deploying-and-running-kafka)
- [配置事件订阅规则](#configuring-event-subscription-rules)
- [创建 Kafka 订阅 Topic](#creating-the-kafka-subscription-topic)
- [启动事件订阅节点](#start-the-node)

<a id="checking-system-configuration-1"></a> 
#### 推荐系统配置

为确保 TRON 节点和事件订阅服务的稳定运行，建议采用以下系统配置：

*   **CPU**：16 核或更高
*   **RAM**：32 GB 或更高
*   **SSD**：2.5 TB 或更大存储空间
*   **操作系统**：Linux 或 macOS

<a id="compiling-the-event-plugin-1"></a> 
#### 编译 Kafka 事件订阅插件

首先，您需要从 GitHub 仓库克隆 `event-plugin` 项目，并进行编译以生成插件的 `.zip` 文件。请按照以下步骤操作：

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```

编译成功后，您将在 `event-plugin/build/plugins/` 目录下找到生成的 `.zip` 插件文件，例如 `plugin-kafka-1.0.0.zip`。

<a id="deploying-and-running-kafka"></a> 
#### 部署并运行 Kafka

##### 步骤 1：安装 Kafka

在 Linux 环境下，请按照以下步骤安装 Kafka：

```
cd /usr/local
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar -xzf kafka_2.13-2.8.0.tgz
```

##### 步骤 2：运行 Kafka

在 Linux 环境下，请按照以下步骤启动 ZooKeeper 服务和 Kafka Broker 服务：

```
cd /usr/local/kafka_2.13-2.8.0
# 启动 ZooKeeper 服务
bin/zookeeper-server-start.sh config/zookeeper.properties &
# 启动 Kafka Broker 服务
bin/kafka-server-start.sh config/server.properties &
```

<a id="configuring-event-subscription-rules"></a> 
#### 配置事件订阅

为了支持 Kafka 事件订阅，您需要修改 Fullnode 节点的配置文件 (`config.conf`)，配置 `event.subscribe` 配置项。

```
event.subscribe = {
  version = 1 
  startSyncBlockNum = 0 

  native = {
    useNativeQueue = false 
  }

  path = "" 
  server = "" 
  dbconfig = "" 
  contractParse = true
  topics = []
  filter = {}
}
```

**字段解析**：

*   `version`：事件服务框架版本。`1` 表示使用 V2.0 版本，`0` 表示使用 V1.0 版本。若未配置，默认使用 V1.0。
*   `startSyncBlockNum`：V2.0 版本新增功能，支持从本地历史区块处理并推送事件，满足历史数据订阅需求。
    *   当 `startSyncBlockNum <= 0` 时，表示关闭历史事件同步功能；
    *   当 `startSyncBlockNum > 0` 时，表示开启该功能，并从指定区块高度开始同步历史事件。**注意**：启用该功能时建议使用最新版本的事件插件。
*   `native.useNativeQueue`：是否使用内置消息队列（ZeroMQ）订阅事件。如果需要支持 Kafka 事件订阅，请确保此字段为 `false`，否则 Kafka 事件订阅将无法生效。
*   `path`：`plugin-kafka-1.0.0.zip` 的本地绝对路径，请确保路径正确，否则无法加载。
*   `server`：Kafka 服务器地址，使用 `ip:port` 的格式。Kafka 默认端口号是 `9092`，请确保端口号正确，并确保 Kafka 服务可访问。
*   `dbconfig`：此配置项仅针对 MongoDB 插件，对于 Kafka 插件请忽略。
*   `topics`：配置订阅的事件，详情请参看接下来的[事件类型](#event-types)章节。
*   `filter`：过滤参数，详情请参看接下来的[事件类型](#event-types)章节。


<a id="event-types"></a>
###### 事件类型

TRON 事件订阅支持 `block`、`transaction`、`contractevent`、`contractlog`、`solidity`、`soliditytevent`、`soliditylog` 7 种类型的事件订阅。开发者需要根据业务需求进行配置，**建议只订阅 1-2 种事件类型，如果开启过多触发器，会导致性能下降。**

**1. 交易事件**

用于订阅交易相关的事件信息。

配置示例：

```
event.subscribe.topics = [
  {
    triggerName = "transaction"
    enable = false
    topic = "transaction"
    solidified = false
    ethCompatible = false
  }
]
```

参数说明：

  - `triggerName`: 事件类型标识，交易事件固定为 `"transaction"`。
  - `enable`: 是否订阅此类型的事件。
  - `topic`: 在 MongoDB 或 Kafka 中接收此类型事件的主题名，该参数值需与 MongoDB 或 Kafka 的配置保持一致。
  - `solidified`: 如果设为 `true`，则仅订阅已固化的交易事件。
  - `ethCompatible`: 如果设为 `true`，将包含 ETH 兼容字段（如 `transactionIndex`, `logList`）。

交易事件中包含的主要字段：

  - `transactionId`: 交易哈希。
  - `blockNumber`: 区块高度。
  - `energyUsage`: 此次调用中消耗的能量(Energy) 总量。
  - `energyFee`: 此次调用中消耗的 TRX 数量（以 `sun` 为单位）。

更多字段请参考 [TransactionLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/TransactionLogTrigger.java)。

**2. 区块事件**

用于订阅区块生成信息。

配置示例：

```
event.subscribe.topics = [
  {
    triggerName = "block"
    enable = false
    topic = "block"
    solidified = false
  }
]
```

区块事件中包含的主要字段：

  - `blockHash`: 区块哈希。
  - `blockNumber`: 区块高度。
  - `transactionSize`: 区块中包含的交易数量。
  - `latestSolidifiedBlockNumber`: 最新的固化块的高度
  - `transactionList`: 交易哈希列表

更多字段请参考 [BlockLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/BlockLogTrigger.java)。

**3. 合约事件与日志**

用于订阅智能合约事件和日志。

配置示例：

```
event.subscribe.topics = [
  {
    triggerName = "contractevent"
    enable = false
    topic = "contractevent"
  },
  {
    triggerName = "contractlog"
    enable = false
    topic = "contractlog"
  },
  {
    triggerName = "solidityevent"
    enable = false
    topic = "solidityevent"
  },
  {
    triggerName = "soliditylog"
    enable = false
    topic = "soliditylog"
  }
]
```

  - `contractevent`: 订阅所有合约事件。
  - `contractlog`: 订阅所有合约日志。
  - `solidityevent`: 仅订阅固化块中的合约事件。
  - `soliditylog`: 仅订阅固化块中的合约日志。

合约事件中包含的主要字段：

  - `transactionId`: 交易哈希。
  - `contractAddress`: 合约地址。
  - `blockNumber`: 合约事件所在的区块高度。

更多字段请参考 [ContractEventTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractEventTrigger.java) 和  [ContractLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractLogTrigger.java)。

> **注意**：`合约事件`与`合约日志事件`订阅支持通过`filter` 字段对事件进行过滤，可以指定区块范围 (`fromblock` - `toblock`)、特定合约地址 (`contractAddress`) 或特定合约主题 (`contractTopic`)，为开发者提供更高效、更精准的事件订阅服务。：
> ```
> filter = {
>   fromblock = "" // 查询范围的起始区块号，可以是空字符串、"earliest" 或指定的区块号。
>   toblock = "" // 查询范围的结束区块号，可以是空字符串、"latest" 或指定的区块号。
>   contractAddress = [
>     "" // 您希望订阅的合约地址。如果设置为空字符串，将接收所有合约地址的日志/事件。
>   ]
>
>   contractTopic = [
>     "" // 您希望订阅的合约主题。如果设置为空字符串，将接收所有合约主题的日志/事件。
>   ]
> }
> ```



**4. 固化块通知事件**

用于实时获取最新固化块高度，适用于需要同步最新固化状态的场景。

配置示例：

```
event.subscribe.topics = [
  {
    triggerName = "solidity"
    enable = true
    topic = "solidity"
  }
]
```

固化快通知事件中包含的主要字段：

  - `latestSolidifiedBlockNumber`: 最新固化块高度。
  - `timestamp`: 区块时间戳。

更多字段请参考 [SolidityTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/SolidityTrigger.java)。



<a id="creating-the-kafka-subscription-topic"></a> 
#### 创建 Kafka 订阅 Topic

Kafka 订阅 Topic 的名称必须与 `event.subscribe` 配置中 `topics` 字段的 `topic` 配置项一致。例如，如果开发者需要订阅 `block` 事件，并在 `block` 触发器中填写 `topic` 字段为 `"block"`，则需要在 Kafka 中创建名为 `"block"` 的 Topic，用于接收区块事件。

在 Linux 环境下，创建 Kafka Topic 的命令如下：

```
bin/kafka-topics.sh --create --topic block --bootstrap-server localhost:9092
```

<a id="start-the-node"></a> 
#### 启动事件订阅节点

完成上述配置后，启动 Fullnode 节点时需要添加 `--es` 参数，以启用事件订阅功能。

```
java -jar FullNode.jar -c config.conf --es
```

##### 验证插件加载

您可以通过查看 Fullnode 日志来验证 Kafka 事件插件是否成功加载：

```
grep -i eventplugin logs/tron.log
```

如果日志中出现类似以下字样，则表明事件订阅插件已成功加载：

```
[o.t.c.l.EventPluginLoader] 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

##### 验证事件订阅

执行 `kafka-console-consumer.sh` 脚本，获取 Kafka 中 Topic 为 `"block"` 的消息，以验证事件订阅是否成功。

在 Linux 环境下，命令如下：

```
bin/kafka-console-consumer.sh --topic block --from-beginning --bootstrap-server localhost:9092
```

如果控制台出现类似以下 JSON 格式的输出，则表明事件订阅成功：

```
{
	"timeStamp": 1539973125000,
	"triggerName": "blockTrigger",
	"blockNumber": 3341315,
	"blockHash": "000000000032fc03440362c3d42eb05e79e8a1aef77fe31c7879d23a750f2a31",
	"transactionSize": 16,
	"latestSolidifiedBlockNumber": 3341297,
	"transactionList": ["8757f846e541b51b5692a2370327f4b8031125f4557f8ad4b1037d4452616d39", "f6adab7814b34e5e756170f93a31a0c3393c5d99eff11e30271916375adc7467", ..., "89bcbcd063a48ef4a5678a033acf5edbb6b17419a3c91eb0479a3c8598774b43"]
}
```

<a id="use-mongodb"></a>
### MongoDB 事件订阅插件部署与使用指南

本指南旨在帮助开发者快速部署和使用 TRON MongoDB 事件订阅插件，实现链上事件的实时数据采集、持久化存储与查询。我们将从环境准备讲起，一步步带您完成部署、配置和使用，主要流程包括：

- [检查系统配置](#checking-system-configuration-2)
- [了解系统架构](#understanding-system-architecture)
- [部署事件订阅插件](#deploying-the-event-plugin)
- [安装并配置 MongoDB](#deploying-the-mongodb)
- [部署事件查询服务](#deploying-the-event-query-service)
- [启动服务并验证数据](#starting-and-verifing)
- [调用 API 查询事件](#using-the-tron-event-query-service-api)


<a id="checking-system-configuration-2"></a> 
#### 推荐系统配置

为了确保 TRON 节点与事件服务的高效稳定运行，推荐以下配置：

*   **CPU**：16 核及以上
*   **RAM**：32 GB 或更高
*   **SSD**：2.5 TB 以上
*   **操作系统**：Linux 或 macOS

<a id="understanding-system-architecture"></a> 
#### 系统架构与工作机制
TRON MongoDB 事件订阅系统包含三大核心模块：

1. 事件订阅插件：连接 TRON 节点，捕获事件数据，然后写入 MongoDB。
2. MongoDB 数据库：事件数据持久化存储层。
3. 事件查询服务：提供 HTTP API，供外部查询事件数据。

<a id="deploying-the-event-plugin"></a> 
#### 部署事件订阅插件

##### 1. 构建插件

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```
构建完成后，生成的插件文件：
```
event-plugin/build/plugins/plugin-mongodb-*.zip
```

##### 2. FullNode 节点配置

在 FullNode 配置文件 `config.conf` 中添加如下内容：

```javascript
event.subscribe = {
  version = 1  
  startSyncBlockNum = 0 

  native = {
    useNativeQueue = false 
  }
  path = "/deploy/fullnode/event-plugin/build/plugins/plugin-mongodb-1.0.0.zip" 
  server = "127.0.0.1:27017" 
  dbconfig = "eventlog|tron|123456" 
  topics = [
    {
      triggerName = "block" 
      enable = false
      topic = "block" 
      solidified = false 
    },
    {
      triggerName = "transaction"
      enable = false
      topic = "transaction"
      solidified = false
      ethCompatible = false 
    },
    {
      triggerName = "contractevent"
      enable = false
      topic = "contractevent"
    },
    {
      triggerName = "contractlog"
      enable = false
      topic = "contractlog"
      redundancy = false 
    },
    {
      triggerName = "solidity"
      enable = true  
      topic = "solidity"
    },
    {
      triggerName = "solidityevent"
      enable = false
      topic = "solidityevent"
    },
    {
      triggerName = "soliditylog"
      enable = false
      topic = "soliditylog"
      redundancy = false 
    }
  ]

  filter = {
    fromblock = "" 
    toblock = "" 
    contractAddress = ["" ]
    contractTopic = [""]
  }
}
```

**字段解析**：

*   `version`：事件服务框架版本。`1` 表示使用 V2.0 版本，`0` 表示使用 V1.0 版本。若未配置，默认使用 V1.0。
*   `startSyncBlockNum`：V2.0 版本新增支持从本地历史区块中处理并推送事件，可满足用户对历史数据的订阅需求。当 `startSyncBlockNum <= 0` 时，表示关闭历史事件同步功能；当 `startSyncBlockNum > 0` 时，表示开启该功能，并从指定区块高度开始同步历史事件。**注意**：启用该功能时建议使用最新版本的事件插件。
*   `native.useNativeQueue`：是否使用内置消息队列（ZeroMQ）订阅事件。`true` 表示使用内置消息队列，`false` 表示使用插件订阅事件。这里需设置成 `false`。
*   `path`：插件的绝对路径，例如 `"/deploy/fullnode/event-plugin/build/plugins/plugin-mongodb-1.0.0.zip"`。
*   `server`：目标服务器地址，即MongoDB 的地址和端口，例如 `"127.0.0.1:27017"`。
*   `dbconfig`：MongoDB 数据库配置，格式为：`数据库名|用户名|密码`，例如 `"eventlog|tron|123456"`。
*   `topics`：目前支持七种事件类型：`block`、`transaction`、`contractevent`、 `contractlog`、`solidity`、`solidityevent` 和 `soliditylog`。详细信息请参考 [事件类型](#event-types) 章节。
    *   `triggerName`：触发器名称，不可修改。
    *   `enable`：是否启用该事件订阅。`true` 为开启，`false` 为禁用。
    *   `topic`：MongoDB 中接收事件的集合名称，可修改。
*   `filter`：事件过滤条件。
    *   `fromblock`：查询范围的起始区块号，可以是""、`"earliest"` （从创世区块开始查询） 或指定的区块号。
    *   `toblock`：查询范围的结束区块号，可以是""、`"latest"` （最新区块） 或指定的区块号。
    *   `contractAddress`：您希望订阅的合约地址列表。如果设置为空字符串，将接收所有合约地址的日志/事件。
    *   `contractTopic`：您希望订阅的合约主题列表。如果设置为空字符串，将接收所有合约主题的日志/事件。

<a id="deploying-the-mongodb"></a> 
#### 安装与配置 MongoDB

MongoDB 将用于存储 TRON 事件数据。请按照以下步骤安装和配置 MongoDB：

##### 1. 安装 MongoDB

首先，创建 MongoDB 的安装目录，并下载、解压 MongoDB 安装包：

```
mkdir /home/java-tron
cd /home/java-tron
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.4.tgz
tar zxvf mongodb-linux-x86_64-4.0.4.tgz
mv mongodb-linux-x86_64-4.0.4 mongodb
```

##### 2. 设置环境变量

为了便于后续操作，请设置 MongoDB 的环境变量：

```
export MONGOPATH=/home/java-tron/mongodb/
export PATH=$PATH:$MONGOPATH/bin
```

##### 3. 配置 MongoDB

创建 MongoDB 的日志和数据目录，并创建配置文件 `mgdb.conf`：

```
mkdir -p /home/java-tron/mongodb/{log,data}
cd /home/java-tron/mongodb/log/ && touch mongodb.log && cd -
vim /home/java-tron/mongodb/mgdb.conf
```

将以下内容写入 `mgdb.conf` 文件中，请确保 `dbpath` 和 `logpath` 使用绝对路径：

```
dbpath=/home/java-tron/mongodb/data
logpath=/home/java-tron/mongodb/log/mongodb.log
port=27017
logappend=true
fork=true
bind_ip=0.0.0.0
auth=true
wiredTigerCacheSizeGB=2
```

重要配置说明：

*   `bind_ip=0.0.0.0`：必须配置为 `0.0.0.0`，否则将拒绝远程连接。
*   `wiredTigerCacheSizeGB`：必须配置此参数以防止内存溢出 (OOM) 问题。

##### 4. 启动 MongoDB

使用配置文件启动 MongoDB 服务：

```
mongod --config /home/java-tron/mongodb/mgdb.conf &
```

##### 5. 创建管理员用户和数据库用户

连接到 MongoDB 并创建管理员用户，然后创建用于事件订阅的数据库和用户：

```
mongo
use admin
db.createUser({user:"root",pwd:"admin",roles:[{role:"root",db:"admin"}]})

db.auth("root", "admin")
use eventlog
db.createUser({user:"tron",pwd:"123456",roles:[{role:"dbOwner",db:"eventlog"}]})
```

<a id="deploying-the-event-query-service"></a> 
#### 部署事件查询服务（Event Query Service）

事件查询服务提供 HTTP 接口，用于查询 MongoDB 中存储的事件数据。该服务依赖 Java 环境。

**注意**：x86_64架构上请使用Oracle JDK 8，arm64架构上请使用JDK 17

##### 步骤 1：下载源码

克隆 `tron-eventquery` 项目源码：

```
git clone https://github.com/tronprotocol/tron-eventquery.git
cd tron-eventquery
```

##### 步骤 2：构建服务

下载 Maven 并使用 Maven 构建 `tron-eventquery` 服务：

```
wget https://mirrors.cnnic.cn/apache/maven/maven-3/3.5.4/binaries/apache-maven-3.5.4-bin.tar.gz --no-check-certificate
tar zxvf apache-maven-3.5.4-bin.tar.gz
export M2_HOME=$HOME/maven/apache-maven-3.5.4
export PATH=$PATH:$M2_HOME/bin
mvn --version
mvn package
```

命令执行成功后，将在 `tron-eventquery/target` 目录下生成 JAR 包，并在 `tron-eventquery/`目录下生成配置文件`config.conf`。配置文件内容示例如下：

```
mongo.host=IP
mongo.port=27017
mongo.dbname=eventlog
mongo.username=tron
mongo.password=123456
mongo.connectionsPerHost=8
mongo.threadsAllowedToBlockForConnectionMultiplier=4
```

请根据您的 MongoDB 配置修改 `mongo.host`、`mongo.port`、`mongo.dbname`、`mongo.username` 和 `mongo.password`。

##### 步骤 3：启动 TRON Event Query Service

启动 `tron-eventquery` 服务并插入索引：

```
sh deploy.sh
sh insertIndex.sh
```

**注意**：默认端口为 `8080`。如需修改，请编辑 `deploy.sh` 脚本，例如：

```
nohup java -jar -Dserver.port=8081 target/troneventquery-1.0.0-SNAPSHOT.jar 2>&1 &
```

<a id="starting-and-verifing"></a> 
#### 启动服务与验证数据

完成上述部署步骤后，您可以启动 TRON FullNode 节点并验证事件订阅服务是否正常工作。

##### 启动 FullNode 节点

**重要提示**：在启动 FullNode 节点之前，请确保 MongoDB 服务已成功启动。

启动 FullNode 节点的命令如下：

```
java -jar FullNode.jar -c config.conf --es
```

有关 FullNode 节点的安装，请参考 [部署 FullNode](https://tronprotocol.github.io/documentation-zh/using_javatron/installing_javatron/) 文档。

##### 验证插件加载

您可以通过查看 FullNode 日志来验证事件插件是否成功加载：

```
tail -f logs/tron.log | grep -i eventplugin
```

如果看到类似以下字样，则表示插件已成功加载：

```text
o.t.c.l.EventPluginLoader 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

##### 验证数据是否存入 MongoDB

连接到 MongoDB 并查询数据，以验证事件数据是否已从节点获取并通过事件订阅存储到 MongoDB 中：

```
mongo 47.90.245.68:27017
use eventlog
db.auth("tron", "123456")
show collections
db.block.find()
```

如果有返回信息，则说明数据已成功存储。否则，请查看 FullNode 日志逐步排查问题。


<a id="using-the-tron-event-query-service-api"></a> 
#### 调用 API 查询事件

TRON Event Query Service 提供了一系列 HTTP API 接口，用于查询 MongoDB 中存储的事件数据。具体 API 及其用法请参考[Event Query Service HTTP API](https://github.com/tronprotocol/tron-eventquery?tab=readme-ov-file#main-http-service)。



## 内置消息队列订阅（ZeroMQ）

Java-tron 节点内置 **ZeroMQ** 消息队列，提供轻量级的事件推送能力。这种方式无需部署额外插件，适用于对实时性要求较高，但不需要存储或回溯事件的简单场景，例如快速开发和测试。

这种方式有如下优势：

  - **无需部署插件：** 直接连接 TRON 节点即可订阅。
  - **高实时性：** 专为实时事件推送而设计。
  - **轻量级：** 适合快速原型开发和测试环境。

因此，当您希望以最小成本、快速接入事件流，并不依赖持久化能力时，使用 **内置 ZeroMQ 消息队列** 将是更轻便、直接的选择。本指南将详细介绍如何通过 Java-tron 内置的消息队列来订阅事件。


### 配置节点
要通过 Java-tron 内置的 ZeroMQ 实现事件订阅，需在节点的配置文件中启用内置消息队列功能。具体操作如下：

```
event.subscribe = {
  native = {
    useNativeQueue = true 
    bindport = 5555 
    sendqueuelength = 1000 
  }

  ......
 
  topics = [
    {
      triggerName = "block" 
      enable = true
      topic = "block" 
    },
    ......
  ]
}
```

* `native.useNativeQueue`: `true` 为使用内置消息队列，`false` 为使用事件插件
* `native.bindport`: ZeroMQ 发布者绑定端口。本例中为 `5555`，所以订阅者应连接的发布者地址为`"tcp://127.0.0.1:5555"`
* `native.sendqueuelength`: 发送队列的长度，即当订阅者接收消息较慢的情况下，TCP 缓冲区最多容纳的发布者发布的消息数量，超过则丢弃
* `topics`: 订阅的 [事件类型](#event-types)，包括区块类型、交易类型等

### 启动节点
事件订阅服务默认为关闭状态，需要通过配置命令行参数 `--es` 的方式来启用。开启事件订阅服务的节点的启动命令如下：
```
$ java -jar FullNode.jar --es
```

### 准备事件订阅脚本

本文以 Node.js 为例来说明如何订阅事件。

首先，下载 `ZeroMQ` 库：
```
$ npm install zeromq@5
```
然后，编写订阅者代码：
```
// subscriber.js
var zmq = require("zeromq"),
var sock = zmq.socket("sub");

sock.connect("tcp://127.0.0.1:5555");
sock.subscribe("block");
console.log("Subscriber connected to port 5555");

sock.on("message", function(topic, message) {
  console.log(
    "received a message related to:",
    Buffer.from(topic).toString(),
    ", containing message:",
    Buffer.from(message).toString()
  );
});
```
本示例将订阅者连接到了节点事件发布者，并订阅了 `block` 事件。

### 启动订阅者

Node.js 启动命令如下：
```
$ node subscriber.js

> Subscriber connected to port 5555
```
当节点有新的区块时，该订阅者将收到区块事件，输出信息如下：
```
received a message related to: blockTrigger, containing message: {"timeStamp":1678343709000,"triggerName":"blockTrigger","blockNumber":1361,"blockHash":"00000000000005519b3995cd638753a862c812d1bda11de14bbfaa5ad3383280","transactionSize":0,"latestSolidifiedBlockNumber":1361,"transactionList":[]}
received a message related to: blockTrigger, containing message: {"timeStamp":1678343712000,"triggerName":"blockTrigger","blockNumber":1362,"blockHash":"0000000000000552d53d1bdd9929e4533a983f14df8931ee9b3bf6d6c74a47b0","transactionSize":0,"latestSolidifiedBlockNumber":1362,"transactionList":[]}
```


