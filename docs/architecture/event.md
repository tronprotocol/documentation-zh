# 事件订阅

TRON 提供了强大的事件订阅机制，使开发者能够实时捕获链上关键事件，例如交易状态、合约调用和区块生成，从而构建功能丰富的去中心化应用（DApps）。


## 事件订阅方式概览

TRON 提供了两种主要的事件订阅方式，以满足不同场景下的需求。

### 1\. 本地事件插件订阅（推荐）

该方式基于可扩展的插件架构，可将链上事件实时或批量持久化到外部系统，如 **MongoDB** 数据库或 **Kafka** 消息队列。此方案专为对事件可靠性、持久化和数据分析有较高要求的生产环境而设计。

这种方式有如下优势：

  - **多样化的插件支持：** 目前支持 Kafka 和 MongoDB。
  - **丰富的数据类型：** 可订阅区块、交易、智能合约事件及日志。
  - **支持复杂过滤：** 可根据特定条件过滤事件。
  - **历史事件回溯：** V2.0 框架支持从指定区块高度开始同步历史事件。
  - **生产级可靠性：** 推荐用于需要数据完整性和可靠性的场景。

> **注意：** 在网络分叉等极端情况下，未固化（non-solidified）的事件可能会被回滚。因此，在对数据可靠性要求较高的场景中，强烈建议订阅**固化事件（solidified events）**。

### 2\. 内置消息队列订阅（ZeroMQ）

Java-tron 节点内置 **ZeroMQ** 消息队列，提供轻量级的事件推送能力。这种方式无需部署额外插件，适用于对实时性要求较高，但不需要存储或回溯事件的简单场景，例如快速开发和测试。

这种方式有如下优势：

  - **无需部署插件：** 直接连接 TRON 节点即可订阅。
  - **高实时性：** 专为实时事件推送而设计。
  - **轻量级：** 适合快速原型开发和测试环境。


## 事件服务框架（基于本地插件）

Java-tron 当前支持两个事件服务框架版本：`V1.0` 和 `V2.0`。

  - **V1.0：** 仅支持新区块产生时的实时事件推送。
  - **V2.0：** **推荐使用**，新增了历史事件回溯功能，允许从任意区块高度开始同步。

详细对比与选择建议请参考：[事件服务框架 V2.0 介绍](https://medium.com/tronnetwork/event-service-framework-v2-0-0622f2f07249)。

**工作流程：**

1.  **事件采集：** TRON 节点从链上区块中获取事件信息。
2.  **事件入队：** 将事件封装并写入事件缓存队列。
3.  **插件消费：** 事件插件异步消费队列数据。
4.  **事件推送：** 插件将数据推送到目标系统（例如 Kafka 或 MongoDB）。
5.  **业务处理：** 外部业务应用持续消费这些事件数据。



## 事件类型

开发者可通过修改节点配置文件 `config.conf`，灵活指定需要订阅的事件类型。

### 1\. 交易事件

用于订阅交易相关的事件信息。

**配置示例：**

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

**参数说明：**

  - `triggerName`: 事件类型标识，交易事件固定为 `"transaction"`。
  - `enable`: 是否订阅此类型的事件。
  - `topic`: 在 MongoDB 或 Kafka 中接收此类型事件的主题名，该参数值需与 MongoDB 或 Kafka 的配置保持一致。
  - `solidified`: 如果设为 `true`，则仅订阅已固化的交易事件。
  - `ethCompatible`: 如果设为 `true`，将包含 ETH 兼容字段（如 `transactionIndex`, `logList`）。

**交易事件中包含的主要字段：**

  - `transactionId`: 交易哈希。
  - `blockNumber`: 区块高度。
  - `energyUsage`: 此次调用中消耗的能量(Energy) 总量。
  - `energyFee`: 此次调用中消耗的 TRX 数量（以 `sun` 为单位）。

更多字段请参考 [TransactionLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/TransactionLogTrigger.java)。

### 2\. 区块事件

用于订阅区块生成信息。

**配置示例：**

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

**区块事件中包含的主要字段：**

  - `blockHash`: 区块哈希。
  - `blockNumber`: 区块高度。
  - `transactionSize`: 区块中包含的交易数量。
  - `latestSolidifiedBlockNumber`: 最新的固化块的高度
  - `transactionList`: 交易哈希列表

更多字段请参考 [BlockLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/BlockLogTrigger.java)。

### 3\. 合约事件与日志

用于订阅智能合约事件和日志。

**配置示例：**

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

**合约事件中包含的主要字段：**

  - `transactionId`: 交易哈希。
  - `contractAddress`: 合约地址。
  - `blockNumber`: 合约事件所在的区块高度。

更多字段请参考 [ContractEventTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractEventTrigger.java) 和  [ContractLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractLogTrigger.java)。

> 注意：**合约事件**与**合约日志事件**订阅支持以下过滤参数：
> ```
> fromBlock: 起始区块索引
> toBlock: 结束区块索引
> contractAddress: 合约地址
> contractTopics: contract topics列表
> ```



### 4\. 固化块通知事件

用于实时获取最新固化块高度，适用于需要同步最新固化状态的场景。

**配置示例：**

```
event.subscribe.topics = [
  {
    triggerName = "solidity"
    enable = true
    topic = "solidity"
  }
]
```

**固化快通知事件中包含的主要字段：**

  - `latestSolidifiedBlockNumber`: 最新固化块高度。
  - `timestamp`: 区块时间戳。

更多字段请参考 [SolidityTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/SolidityTrigger.java)。


## 迁移至新版事件服务（V2.0）

新版 `V2.0` 事件服务框架引入了历史事件回溯功能，并对事件推送机制进行了全面优化。以下是迁移至 `V2.0` 的操作步骤。

### 迁移前评估

在迁移之前，请考虑以下因素：

  - **内部交易日志支持：** `V2.0` 暂不支持内部交易日志（`internalTransactionList` 字段为空）。如果您的业务依赖此字段，请继续使用 `V1.0`。
  - **插件版本：** 建议将事件插件同步升级至最新版，以避免处理大量历史数据时可能出现的性能问题。

### 迁移操作步骤

#### 步骤 1：获取新版事件插件

你可以从 GitHub 获取源码并自行构建，或直接下载官方发布的版本。

**通过源码构建：**

```
git clone git@github.com:tronprotocol/event-plugin.git
cd event-plugin
git checkout master
./gradlew build
```
构建完成后，生成的 `.zip` 文件即为插件包。

**直接下载官方发布版本：**

访问 [event-plugin Releases 页面](https://github.com/tronprotocol/event-plugin/releases) 下载最新插件包。

#### 步骤 2：修改 FullNode 配置

在 `config.conf` 文件中，将事件服务版本修改为使用`V2.0`，值为 1 。

```
event.subscribe.version = 1 # 1 表示 V2.0，0 表示 V1.0
```

#### 步骤 3：配置事件插件

新版插件的配置方式与旧版基本一致。你可以参考官方文档进行部署：

  - [事件插件部署(MongoDB)](/documentation-zh/architecture/use-mongodb/)
  - [事件插件部署(Kafka)](/documentation-zh/architecture/use-kafka/)

#### 步骤 4（可选）：配置历史事件同步起点

如果你需要从指定区块高度开始同步历史事件，请在配置文件中加入以下配置。

```
event.subscribe.startSyncBlockNum = <block_height>
```

#### 步骤 5：启动 FullNode 和插件

完成上述配置后，使用以下命令启动 `FullNode` 并加载事件插件。

```
java -jar FullNode.jar -c config.conf --es
```