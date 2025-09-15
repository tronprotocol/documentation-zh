# 部署文档

## 前提

分别为fullnode和soliditynode创建一个目录

> NOTE: 原则上不鼓励继续使用 SolidityNode, 目前 FullNode 可以替代 SolidityNode 的功能.

```text
/deploy/fullnode
/deploy/soliditynode
```

克隆最新的master分支上的代码[https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) 到

```text
/deploy/java-tron
```

请确保已经安装恰当的依赖环境。

* JDK 1.8 (JDK 1.9+ is not supported yet)
* On Linux Ubuntu system (e.g. Ubuntu 16.04.4 LTS), ensure that the machine has [__Oracle JDK 8__](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04), instead of having __Open JDK 8__ in the system. If you are building the source code by using __Open JDK 8__, you will get [__Build Failed__](https://github.com/tronprotocol/java-tron/issues/337) result.
* Open **UDP** ports for connection to the network
* **MINIMUM** 2 CPU Cores


## 部署指南

1. 编译java-tron项目

```shell
cd /deploy/java-tron
./gradlew build
```

2. 复制FullNode.jar和SolidityNode.jar以及相应的配置文件到各自的目录

```shell
download your needed configuration file from https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/resources/config.conf.

config.conf is the configuration for MainNet. To set up a testnet node, please modify the parameters in the configuration file.

cp build/libs/FullNode.jar ../fullnode

cp build/libs/SolidityNode.jar ../soliditynode
```

3. 用以下命令运行FullNode

```shell
java -jar FullNode.jar -c config.conf // make sure that your config.conf is downloaded from https://github.com/tronprotocol/TronDeployment
```

4. 配置SolidityNode配置文件

需要编辑`config.conf`文件来连接本地的FullNode。修改`node`里的`trustNode`为`127.0.0.1:50051`，这是默认rpc端口。设置`listen.port`为1024-65535间任意数字。不要使用0-1024间的数字，因为可能会导致与系统服务冲突。同样，为了避免冲突，可以把`rpc port`改为`50052`。

**请为FullNode转发UDP端口18888**

```conf
rpc {
      port = 50052
    }
```

5. 用以下命令运行SolidityNode

```shell
java -jar SolidityNode.jar -c config.conf //make sure that your config.conf is downloaded from https://github.com/tronprotocol/TronDeployment
```

6. 在公链环境中运行超级节点

```shell
java -jar FullNode.jar -p your private key --witness -c your config.conf(Example：/data/java-tron/config.conf)
Example:
java -jar FullNode.jar -p 650950B1...295BD812 --witness -c /data/java-tron/config.conf
```

这与运行一个个人测试网相似，除了`config.conf`中的IP不一样。

7. 在个人测试网环境中运行超级节点

你需要修改一下config.conf配置文件内容：

* Replace existing entry in genesis.block.witnesses with your address
* Replace existing entry in seed.node ip.list with your ip list
* The first Super Node start, needSyncCheck should be set false
* Set p2p version to 61

```shell
cd build/libs
java -jar FullNode.jar -p your private key --witness -c your config.conf (Example：/data/java-tron/config.conf)
Example:
java -jar FullNode.jar -p 650950B1...295BD812 --witness -c /data/java-tron/config.conf
```

## 日志与网络连接验证

日志位于`/deploy/\*/logs/tron.log`。 使用`tail -f /logs/tron.log/`命令来查看块同步日志。

你可以看到类似如下块同步的日志信息：

### FullNode

```log
12:00:57.658 INFO  [pool-7-thread-1] [o.t.c.n.n.NodeImpl](NodeImpl.java:830) Success handle block Num:236610,ID:0000000000039c427569efa27cc2493c1fff243cc1515aa6665c617c45d2e1bf
```

### SolidityNode

```log
12:00:40.691 INFO  [pool-17-thread-1] [o.t.p.SolidityNode](SolidityNode.java:88) sync solidity block, lastSolidityBlockNum:209671, remoteLastSolidityBlockNum:211823
```

## 优雅的停止节点

创建stop.sh文件，使用命令`kill -15`关闭FullNode.jar（或者SolidityNode.jar）。
修改pid=`ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`来找到正确的pid。

```shell
#!/bin/bash
while true; do
  pid=`ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
  if [ -n "$pid" ]; then
    kill -15 $pid
    echo "The java-tron process is exiting, it may take some time, forcing the exit may cause damage to the database, please wait patiently..."
    sleep 1
  else
    echo "java-tron killed successfully!"
    break
  fi
done
```

## 快速部署节点

下载快速部署脚本，根据部署节点类型，执行脚本。

### 使用范围

脚本可以再Linux/MacOS上使用，不支持Windows系统。
只支持FullNode与SolidityNode的部署。

### 下载运行脚本

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
```

### 参数含义

```shell
bash deploy_tron.sh --app [FullNode|SolidityNode] --net [mainnet|testnet|privatenet] --db [keep|remove|backup] --heap-size <heapsize>

--app Optional, Running application. The default node is Fullnode and it could be FullNode or SolidityNode.
--net Optional, Connecting network. The default network is mainnet and it could be mainnet, testnet.
--db  Optional, The way of data processing could be keep, remove and backup. Default is keep. If you launch two different networks, like from mainnet to testnet or from testnet to mainnet, you need to delete database.
--trust-node  Optional, It only works when deploying SolidityNode. Default is 127.0.0.1:50051. The specified gRPC service of Fullnode, like 127.0.0.1:50051 or 13.125.249.129:50051.
--rpc-port  Optional, Port of grpc. Default is 50051. If you deploy SolidityNode and FullNode on the same host，you need to configure different ports.
--commit  Optional, commitid of project.
--branch  Optional, branch of project.  Mainnet default is latest release and Testnet default is master.
--heap-size  Optional, jvm option: Xmx. The default heap-size is 0.8 * memory size.
--work_space  Optional, default is current directory.
```

### 部署FullNode

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
bash deploy_tron.sh
```

### 部署SolidityNode

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
# User can self-configure the IP and Port of GRPC service in the turst-node field of SolidityNode. trust-node is the fullnode you just deploy.
bash deploy_tron.sh --app SolidityNode --trust-node <grpc-ip:grpc-port>
```

### FullNode和SolidityNode部署在同一主机上

```shell
# You need to configure different gRPC ports on the same host because gRPC port is available on SolidityNode and FullNodeConfigure and it cannot be set as default value 50051. In this case the default value of rpc port is set as 50041.
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
bash deploy_tron.sh --app FullNode
bash deploy_tron.sh --app SolidityNode --rpc-port 50041
```

## Grpc Gateway部署

### 前提

请参照：[https://github.com/tronprotocol/grpc-gateway](https://github.com/tronprotocol/grpc-gateway)
安装Golang, Protoc, 并且设置$GOPATH环境变量。

### 下载运行脚本

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_grpc_gateway.sh -O deploy_grpc_gateway.sh
```

### 参数含义

```shell
bash deploy_grpc_gateway.sh --rpchost [rpc host ip] --rpcport [rpc port number] --httpport [http port number]

--rpchost The fullnode or soliditynode IP where the grpc service is provided. Default value is "localhost".
--rpcport The fullnode or soliditynode port number grpc service is consuming. Default value is 50051.
--httpport The port intends to provide http service provided by grpc gateway. Default value is 18890.
```

### 示例

使用默认配置：

```shell
bash deploy_grpc_gateway.sh
```

使用自定义配置：

```shell
bash deploy_grpc_gateway.sh --rpchost 127.0.0.1 --rpcport 50052 --httpport 18891
```

## 事件订阅部署

* **api** 模块定义了介于java-tron与插件间的事件订阅接口。
* **app** 模块是加载插件示例，开发者可以用来调试。
* **kafkaplugin** 模块是kafka的实现。它实现了IPluginEventListener，它从java-tron接受事件并转给kafka服务。
* **mongodbplugin** 模块是mongodb的实现。

### 搭建运行环境

1. Clone the repo `git clone https://github.com/tronprotocol/event-plugin.git`
2. Go to eventplugin `cd event-plugin`
3. run `./gradlew build`

* 这一步会生成`plugin-kafka-1.0.0.zip`，位于`event-plugin/build/plugins/`目录下。

### 编辑java-tron的 **config.conf** 文件，增加以下字段

```conf
event.subscribe = {
    path = "" // absolute path of plugin
    server = "" // target server address to receive event triggers
    dbconfig="" // dbname|username|password
    topics = [
        {
          triggerName = "block" // block trigger, the value can't be modified
          enable = false
          topic = "block" // plugin topic, the value could be modified
        },
        {
          triggerName = "transaction"
          enable = false
          topic = "transaction"
        },
        {
          triggerName = "contractevent"
          enable = true
          topic = "contractevent"
        },
        {
          triggerName = "contractlog"
          enable = true
          topic = "contractlog"
        }
    ]

    filter = {
       fromblock = "" // the value could be "", "earliest" or a specified block number as the beginning of the queried range
       toblock = "" // the value could be "", "latest" or a specified block number as end of the queried range
       contractAddress = [
           "" // contract address you want to subscribe, if it's set to "", you will receive contract logs/events with any contract address.
       ]

       contractTopic = [
           "" // contract topic you want to subscribe, if it's set to "", you will receive contract logs/events with any contract topic.
       ]
    }
}


```

 ***path**: "plugin-kafka-1.0.0.zip"文件的绝对路径
 ***server**: Kafka服务地址
 ***topics**: 每一种事件匹配一个Kafka主题，我们支持四种事件订阅：区块事件，交易事件，合约事件以及合约日志事件
 ***dbconfig**: mongodb的配置，dbname|username|password。如果使用kafka，可以忽略这个参数。
 ***triggerName**: 触发类型，只读。
 ***enable**: 是否开启事件订阅。
 ***topic**: kafka接收事件的主题。请确保Kafka在运行中。
 ***filter**: 事件订阅过滤选项。
 **注意**: 如果服务器地址不是127.0.0.1, 请在config/server.properties文件中设置listeners=PLAINTEXT://:9092，advertised.listeners to PLAINTEXT://host_ip:9092

### 安装Kafka

**Mac环境**:

```shell
brew install kafka
```

**Linux环境**:

```shell
cd /usr/local
wget http://archive.apache.org/dist/kafka/0.10.2.2/kafka_2.10-0.10.2.2.tgz
tar -xzvf kafka_2.10-0.10.2.2.tgz
mv kafka_2.10-0.10.2.2 kafka

add "export PATH=$PATH:/usr/local/kafka/bin" to end of /etc/profile
source /etc/profile


kafka-server-start.sh /usr/local/kafka/config/server.properties &

```

**注意**: 请确保Kafka的版本与build.gradle中eventplugin项目的版本一致。

### 运行Kafka

**Mac环境**:

```shell
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties
```

**Linux环境**:

```shell
zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties &
Sleep about 3 seconds
kafka-server-start.sh /usr/local/kafka/config/server.properties &
```

### 创建主题接受事件，主题的定义位于config.conf文件中

**Mac环境**:

```shell
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic block
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic transaction
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractlog
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractevent
```

**Linux环境**:

```shell
kafka-topics.sh  --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic block
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic transaction
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractlog
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractevent
```

### Kafka用户

**Mac环境**:

```shell
kafka-console-consumer --bootstrap-server localhost:9092  --topic block
kafka-console-consumer --bootstrap-server localhost:9092  --topic transaction
kafka-console-consumer --bootstrap-server localhost:9092  --topic contractlog
kafka-console-consumer --bootstrap-server localhost:9092  --topic contractevent
```

**Linux环境**:

```shell
kafka-console-consumer.sh --zookeeper localhost:2181 --topic block
kafka-console-consumer.sh --zookeeper localhost:2181 --topic transaction
kafka-console-consumer.sh --zookeeper localhost:2181 --topic contractlog
kafka-console-consumer.sh --zookeeper localhost:2181 --topic contractevent
```

### 在java-tron中加载插件

* add --es to command line, for example:

```shell
 java -jar FullNode.jar -p privatekey -c config.conf --es
```

### 事件订阅过滤

事件订阅过滤参数在config.conf文件中设置：

```conf
filter = {
       fromblock = "" // the value could be "", "earliest" or a specified block number as the beginning of the queried range
       toblock = "" // the value could be "", "latest" or a specified block number as end of the queried range
       contractAddress = [
           "TVkNuE1BYxECWq85d8UR9zsv6WppBns9iH" // contract address you want to subscribe, if it's set to "", you will receive contract logs/events with any contract address.
       ]

       contractTopic = [
           "f0f1e23ddce8a520eaa7502e02fa767cb24152e9a86a4bf02529637c4e57504b" // contract topic you want to subscribe, if it's set to "", you will receive contract logs/events with any contract topic.
       ]
    }
```

### 下载并安装MongoDB

#### 建议配置

* CPU/ RAM: 16Core / 32G
* DISK: 500G
* System: CentOS 64

MongoDB的版本是**4.0.4**，以下是安装命令:

* cd /home/java-tron
* curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.4.tgz
* tar zxvf mongodb-linux-x86_64-4.0.4.tgz
* mv mongodb-linux-x86_64-4.0.4 mongodb

#### 设计环境变量

* export MONGOPATH=/home/java-tron/mongodb/
* export PATH=$PATH:$MONGOPATH/bin

#### 创建配置文件

The path is : /etc/mongodb/mgdb.conf

* cd /etc/mongodb
* touch mgdb.conf

创建数据和日志文件夹，并把它们的绝对路径加入mgdb.conf

#### 示例

* dbpath=/home/java-tron/mongodb/data
* logpath=/home/java-tron/mongodb/log/mongodb.log
* port=27017
* logappend=true
* fork=true
* bind_ip=0.0.0.0
* auth=true
* wiredTigerCacheSizeGB=2

#### 注意

* bind_ip must be configured to 0.0.0.0，otherwise remote connection will be refused.
* wiredTigerCacheSizeGB, must be configured to prevent OOM

#### 运行MongoDB

```shell
mongod  --config /etc/mongodb/mgdb.conf
```

#### 创建管理员账户

```shell
- mongo
- use admin
- db.createUser({user:"root",pwd:"admin",roles:[{role:"root",db:"admin"}]})
```

#### 创建事件日志以及所有者账户

* db.auth("root", "admin")
* use eventlog
* db.createUser({user:"tron",pwd:"123456",roles:[{role:"dbOwner",db:"eventlog"}]})

> database: eventlog, username:tron, password: 123456

#### 防火墙策略

```shell
iptables -A INPUT -p tcp -m state --state NEW -m tcp --dport 27017 -j ACCEPT
```

#### 远程连接mongo

* mongo 47.90.245.68:27017
* use eventlog
* db.auth("tron", "123456")
* show collections
* db.block.find()

#### 查询区块事件触发数据

* db.block.find({blockNumber: {$lt: 1000}});  // 返回区块高度小于1000的数据

#### 设置数据库索引

```shell
cd /{projectPath}
sh insertIndex.sh
```

## 事件订阅数据查询服务部署

### 下载代码

git clone https://github.com/tronprotocol/tron-eventquery.git
cd troneventquery

### 编译

```shell
mvn package
```

代码编译成功后，在/troneventquery目录下会生成troneventquery.jar文件。

需要创建一个config.conf配置文件用来设置mongodb的配置属性，我们在/troneventquery/config.conf中提供了个示例，如果有需要可以进行修改。

**注意：**

config.conf文件应该位于/troneventquery文件夹下。

 * mongo.host=IP
 * mongo.port=27017
 * mongo.dbname=eventlog
 * mongo.username=tron
 * mongo.password=123456
 * mongo.connectionsPerHost=8
 * mongo.threadsAllowedToBlockForConnectionMultiplier=4

**mongo.dbname**的值是指定的事件订阅数据库的名称，不可以修改。

### 运行

* troneventquery/deploy.sh 是用来部署事件订阅数据查询服务的。
* troneventquery/insertIndex.sh 是用来设置mongodb索引来加速查询的。

## 高级配置

Read the [Advanced Configuration](./advanced-configuration.md)
