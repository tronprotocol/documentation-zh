# TRON MongoDB 事件订阅插件：部署与使用指南

本指南旨在帮助开发者快速部署和使用 TRON MongoDB 事件订阅插件，实现链上事件的实时数据采集、持久化存储与查询。文档涵盖系统环境配置、插件部署、数据库安装、查询服务构建及接口调用等全流程。


本指南将带您从环境准备到接口调用，一步步完成 TRON MongoDB 事件订阅服务的完整部署与使用。主要流程包括：

- [检查系统配置](#1)
- [了解系统架构](#2)
- [部署事件订阅插件](#3)
- [安装并配置 MongoDB](#4)
- [部署事件查询服务](#5)
- [启动服务并验证数据](#6)
- [调用 API 查询事件](#7)


<a id="1"></a> 
## 推荐系统配置

为了确保 TRON 节点与事件服务的高效稳定运行，推荐以下配置：

*   **CPU**：16 核及以上
*   **RAM**：32 GB 或更高
*   **SSD**：2.5 TB 以上
*   **操作系统**：Linux 或 macOS

<a id="2"></a> 
## 系统架构与工作机制
TRON MongoDB 事件订阅系统包含三大核心模块：

1. 事件订阅插件：连接 TRON 节点，捕获事件数据，然后写入 MongoDB。
2. MongoDB 数据库：事件数据持久化存储层。
3. 事件查询服务：提供 HTTP API，供外部查询事件数据。

<a id="3"></a> 
## 部署事件订阅插件

### 构建插件

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```
构建完成后，生成的插件文件：
```
event-plugin/build/plugins/plugin-mongodb-*.zip
```

### 3.2 FullNode 节点配置

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
*   `topics`：目前支持七种事件类型：`block`、`transaction`、`contractevent`、 `contractlog`、`solidity`、`solidityevent` 和 `soliditylog`。详细信息请参考 [事件类型](../event/#_4) 章节。
    *   `triggerName`：触发器名称，不可修改。
    *   `enable`：是否启用该事件订阅。`true` 为开启，`false` 为禁用。
    *   `topic`：MongoDB 中接收事件的集合名称，可修改。
*   `filter`：事件过滤条件。
    *   `fromblock`：查询范围的起始区块号，可以是""、`"earliest"` （从创世区块开始查询） 或指定的区块号。
    *   `toblock`：查询范围的结束区块号，可以是""、`"latest"` （最新区块） 或指定的区块号。
    *   `contractAddress`：您希望订阅的合约地址列表。如果设置为空字符串，将接收所有合约地址的日志/事件。
    *   `contractTopic`：您希望订阅的合约主题列表。如果设置为空字符串，将接收所有合约主题的日志/事件。

<a id="4"></a> 
## 安装与配置 MongoDB

MongoDB 将用于存储 TRON 事件数据。请按照以下步骤安装和配置 MongoDB：

### 安装 MongoDB

首先，创建 MongoDB 的安装目录，并下载、解压 MongoDB 安装包：

```
mkdir /home/java-tron
cd /home/java-tron
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.4.tgz
tar zxvf mongodb-linux-x86_64-4.0.4.tgz
mv mongodb-linux-x86_64-4.0.4 mongodb
```

### 设置环境变量

为了便于后续操作，请设置 MongoDB 的环境变量：

```
export MONGOPATH=/home/java-tron/mongodb/
export PATH=$PATH:$MONGOPATH/bin
```

### 配置 MongoDB

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

**重要配置说明**：

*   `bind_ip=0.0.0.0`：必须配置为 `0.0.0.0`，否则将拒绝远程连接。
*   `wiredTigerCacheSizeGB`：必须配置此参数以防止内存溢出 (OOM) 问题。

### 4.4 启动 MongoDB

使用配置文件启动 MongoDB 服务：

```
mongod --config /home/java-tron/mongodb/mgdb.conf &
```

### 4.5 创建管理员用户和数据库用户

连接到 MongoDB 并创建管理员用户，然后创建用于事件订阅的数据库和用户：

```
mongo
use admin
db.createUser({user:"root",pwd:"admin",roles:[{role:"root",db:"admin"}]})

db.auth("root", "admin")
use eventlog
db.createUser({user:"tron",pwd:"123456",roles:[{role:"dbOwner",db:"eventlog"}]})
```

<a id="5"></a> 
## 部署事件查询服务（Event Query Service）

事件查询服务提供 HTTP 接口，用于查询 MongoDB 中存储的事件数据。该服务依赖 Java 环境。

**注意**：请确保 JDK 使用的是 **Oracle JDK 8**，而不是 Open JDK 8。

### 步骤 1：下载源码

克隆 `tron-eventquery` 项目源码：

```
git clone https://github.com/tronprotocol/tron-eventquery.git
cd tron-eventquery
```

### 步骤 2：构建服务

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

### 步骤 3：启动 TRON Event Query Service

启动 `tron-eventquery` 服务并插入索引：

```
sh deploy.sh
sh insertIndex.sh
```

**注意**：默认端口为 `8080`。如需修改，请编辑 `deploy.sh` 脚本，例如：

```
nohup java -jar -Dserver.port=8081 target/troneventquery-1.0.0-SNAPSHOT.jar 2>&1 &
```

<a id="6"></a> 
## 启动服务与验证数据

完成上述部署步骤后，您可以启动 TRON FullNode 节点并验证事件订阅服务是否正常工作。

### 启动 FullNode 节点

**重要提示**：在启动 FullNode 节点之前，请确保 MongoDB 服务已成功启动。

启动 FullNode 节点的命令如下：

```
java -jar FullNode.jar -c config.conf --es
```

有关 FullNode 节点的安装，请参考 [部署 FullNode](https://tronprotocol.github.io/documentation-zh/using_javatron/installing_javatron/) 文档。

### 验证插件加载

您可以通过查看 FullNode 日志来验证事件插件是否成功加载：

```
tail -f logs/tron.log | grep -i eventplugin
```

如果看到类似以下字样，则表示插件已成功加载：

```text
o.t.c.l.EventPluginLoader 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

### 验证数据是否存入 MongoDB

连接到 MongoDB 并查询数据，以验证事件数据是否已从节点获取并通过事件订阅存储到 MongoDB 中：

```
mongo 47.90.245.68:27017
use eventlog
db.auth("tron", "123456")
show collections
db.block.find()
```

如果有返回信息，则说明数据已成功存储。否则，请查看 FullNode 日志逐步排查问题。


<a id="7"></a> 
## 调用 API 查询事件

TRON Event Query Service 提供了一系列 HTTP API 接口，用于查询 MongoDB 中存储的事件数据。具体 API 及其用法请参考[Event Query Service HTTP API](https://github.com/tronprotocol/tron-eventquery?tab=readme-ov-file#main-http-service)。
