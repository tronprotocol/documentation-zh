# TRON Kafka 事件订阅插件：部署与使用指南

本指南旨在帮助开发者高效搭建并运行 TRON Kafka 事件订阅插件，用以监听 TRON 链上事件。我们将从环境准备讲起，一步步带您完成部署、配置和最终验证。主要步骤包括：

- [检查系统配置](#1)
- [编译事件插件](#2)
- [部署并运行 Kafka](#3)
- [配置事件订阅规则](#4)
- [创建 Kafka 订阅 Topic](#5)
- [启动事件订阅节点](#6)

<a id="1"></a> 
## 推荐系统配置

为确保 TRON 节点和事件订阅服务的稳定运行，建议采用以下系统配置：

*   **CPU**：16 核或更高
*   **RAM**：32 GB 或更高
*   **SSD**：2.5 TB 或更大存储空间
*   **操作系统**：Linux 或 macOS

<a id="2"></a> 
## 编译 Kafka 事件订阅插件

首先，您需要从 GitHub 仓库克隆 `event-plugin` 项目，并进行编译以生成插件的 `.zip` 文件。请按照以下步骤操作：

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```

编译成功后，您将在 `event-plugin/build/plugins/` 目录下找到生成的 `.zip` 插件文件，例如 `plugin-kafka-1.0.0.zip`。

<a id="3"></a> 
## 部署并运行 Kafka

### 步骤 1：安装 Kafka

在 Linux 环境下，请按照以下步骤安装 Kafka：

```
cd /usr/local
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar -xzf kafka_2.13-2.8.0.tgz
```

### 步骤 2：运行 Kafka

在 Linux 环境下，请按照以下步骤启动 ZooKeeper 服务和 Kafka Broker 服务：

```
cd /usr/local/kafka_2.13-2.8.0
# 启动 ZooKeeper 服务
bin/zookeeper-server-start.sh config/zookeeper.properties &
# 启动 Kafka Broker 服务
bin/kafka-server-start.sh config/server.properties &
```

<a id="4"></a> 
## 配置事件订阅

为了支持 Kafka 事件订阅，您需要修改 Fullnode 节点的配置文件 (`config.conf`)，添加 `event.subscribe` 配置项。

### 插件配置项

以下是 `event.subscribe` 配置项的示例：

```
event.subscribe = {
  version = 1 
  startSyncBlockNum = 0 

  native = {
    useNativeQueue = false 
  }

  path = "" 
  server = "" 
  dbconfig = "" 。
  contractParse = true,
  # ... 其他配置项 ...
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

### 配置事件订阅类型

TRON 事件订阅支持 `block`、`transaction`、`contractevent`、`contractlog`、`solidity`、`soliditytevent`、`soliditylog` 7 种类型的事件订阅。开发者需要根据业务需求进行配置，**建议只订阅 1-2 种事件类型，如果开启过多触发器，会导致性能下降。**

以下是一个订阅 `block` 事件的示例配置：

```
topics = [
  {
    triggerName = "block" 
    enable = true
    topic = "block" 
  }
]
```

  * `triggerName`: 内置字段，不可更改。
  * `enable`: 如果设置为 `true`，则开启对 `block` 事件的订阅。
  * `topic`: Kafka 接收事件对应的主题名称。您需要在 Kafka 中提前创建此主题。
 
更多关于事件订阅类型的说明请参考 [事件类型](../event/#_4) 章节。

### 配置事件过滤

`filter` 字段用于对所订阅事件进行过滤，可以指定区块范围 (`fromblock` - `toblock`)、特定合约地址 (`contractAddress`) 或特定合约主题 (`contractTopic`)，为开发者提供更高效、更精准的事件订阅服务。

```conf
filter = {
  fromblock = "" // 查询范围的起始区块号，可以是空字符串、"earliest" 或指定的区块号。
  toblock = "" // 查询范围的结束区块号，可以是空字符串、"latest" 或指定的区块号。
  contractAddress = [
    "" // 您希望订阅的合约地址。如果设置为空字符串，将接收所有合约地址的日志/事件。
  ]

  contractTopic = [
    "" // 您希望订阅的合约主题。如果设置为空字符串，将接收所有合约主题的日志/事件。
  ]
}
```

<a id="5"></a> 
## 创建 Kafka 订阅 Topic

Kafka 订阅 Topic 的名称必须与 `event.subscribe` 配置中 `topics` 字段的 `topic` 配置项一致。例如，如果开发者需要订阅 `block` 事件，并在 `block` 触发器中填写 `topic` 字段为 `"block"`，则需要在 Kafka 中创建名为 `"block"` 的 Topic，用于接收区块事件。

在 Linux 环境下，创建 Kafka Topic 的命令如下：

```
bin/kafka-topics.sh --create --topic block --bootstrap-server localhost:9092
```

<a id="6"></a> 
## 启动事件订阅节点

完成上述配置后，启动 Fullnode 节点时需要添加 `--es` 参数，以启用事件订阅功能。

```
java -jar FullNode.jar -c config.conf --es
```

### 验证插件加载

您可以通过查看 Fullnode 日志来验证 Kafka 事件插件是否成功加载：

```
grep -i eventplugin logs/tron.log
```

如果日志中出现类似以下字样，则表明事件订阅插件已成功加载：

```
[o.t.c.l.EventPluginLoader] 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

### 验证事件订阅

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


