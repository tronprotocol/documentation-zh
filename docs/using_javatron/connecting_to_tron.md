# 连接到TRON网络

TRON网络主要分为主网，Shasta测试网，Nile测试网以及私网，因此对于java-tron客户端软件，可以通过对配置文件中配置项的修改使其连接到任意一个TRON网络中。目前Shasta测试网不支持节点加入，Nile测试网支持。

您需要设置如下配置项，将java-tron连接到其中一个TRON网络：

* `node.p2p.version` ： 用来设置P2P网络id，只有网络id相同的节点才能握手成功。
    * TRON主网：`node.p2p.version=11111`
    * Nile测试网：`node.p2p.version = 201910292`
    * 私链网络：设置成其它值
* `seed.node`：设置种子节点
* `genesis.block`：创世块设置。如果想要加入一个网络中，必须保证创世块的设置与网络中其它节点的相同，否则无法加入到该网络。


## 节点发现 
节点发现通过配置文件开启和关闭，通常开启，相关配置项如下：

```
node.discovery = {
  enable = true 
}
```

java-tron使用Kademlia 协议发现其他节点。节点发现需要引导节点(bootstrap节点)，通过引导节点发现TRON网络中的其他节点。引导节点由两部分组成，一部分是种子节点，一部分是配置的主动连接节点，详情见[主动连接](#_4)。

种子节点也由两部分组成：

- 配置的seed.node：
```
seed.node = {
  # List of the seed nodes
  # Seed nodes are stable full nodes

  ip.list = [
    "3.225.171.164:18888",
    "52.8.46.215:18888",
    "3.79.71.167:18888",
    "108.128.110.16:18888",
    "18.133.82.227:18888",
    "35.180.81.133:18888",
    "13.210.151.5:18888",
    "18.231.27.82:18888",
    "3.12.212.122:18888",
    "52.24.128.7:18888",
    "15.207.144.3:18888",
    "3.39.38.55:18888",    
    "54.151.226.240:18888",
    "35.174.93.198:18888",
    "18.210.241.149:18888",
    "54.177.115.127:18888",
    "54.254.131.82:18888",
    "18.167.171.167:18888",
    "54.167.11.177:18888",
    "35.74.7.196:18888",
    "52.196.244.176:18888",
    "54.248.129.19:18888",
    "43.198.142.160:18888",
    "3.0.214.7:18888",
    "54.153.59.116:18888",
    "54.153.94.160:18888",
    "54.82.161.39:18888",
    "54.179.207.68:18888",
    "18.142.82.44:18888",
    "18.163.230.203:18888"
  ]
}

```
如果想要获取最新的seed.node，可以在官方的[配置文件](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf)查看。

- 从数据库中读取的持久化节点。持久化节点是在节点运行期间连接良好的节点，持久化节点需要开启节点持久化服务。持久化节点一般在节点重启时用到。相关配置项：
```
node.discovery = {
  persist = true
}
```

种子节点作为引导节点，也属于被发现的节点。如果节点发现没有开启，节点不会主动连接这些种子节点。

节点发现基于udp协议，绑定的默认端口是18888，也可以绑定其他端口，比如19999，但是不建议这么做。相关配置项：
```
node {
  listen.port = 18888
}
```
如果绑定的是其他节点，比如19999，也可以正常工作，但是整个网络拓扑就会变成如下图所示：

![image](https://raw.githubusercontent.com/King31T/documentation-zh/network_connecting/images/network_topology1.png)

在某些情况下，不需要开启节点发现，比如，运行一个本地测试节点或部署一个具有固定的一些节点的测试网络。这时可以通过将配置项设置成`node.discovery.enable = false`来关闭节点发现进程，也可以通过关闭udp 18888端口来实现。

## 节点连接

### 节点连接数量
`node.maxConnections`表示节点与其它节点的最大连接数量，默认值是30。设置更大的值可以使节点能够建立更多的连接，加入网络的效率更高，同时广播的效率也更高，但是，相对的维护连接需要的带宽也更高，性能消耗也更大，因此，请根据实际情况设置。  
```
node {
    maxConnections = 30
}
```

### 主动连接
主动连接的目标节点来源于四部分：

- 配置的主动节点(最高优先级)，不依赖于节点发现，即使节点发现没有开启，当前节点也会主动向这些节点发起连接。相关配置项：
```
node {
  active = [
    # Active establish connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
 }
``` 
- 检测过的节点(高优先级)，需要开启节点检测服务，节点检测是对上述节点发现获取到的可连接节点进行进一步检测，检测内容包括对方节点的响应速度、剩余的连接数等。一般不启用节点检测，默认false，相关配置项：
```
#Whether to enable the node detection function, default false
#nodeDetectEnable = false
```
- 节点发现获取到的可连接节点(中优先级)
- DNS节点(最低优先级/备用)，DNS树获取的备用节点，需要配置treeUrls，在前三种来源不足时使用，一般不会使用到。相关配置项(一般不配置)：
```
dns {
  # dns urls to get nodes, url format tree://{pubkey}@{domain}, default empty
  treeUrls = [
    #"tree://AKMQMNAJJBL73LXWPXDI4I5ZWWIZ4AWO34DWQ636QOBBXNFXH3LQS@main.trondisco.net",
  ]
}
```
可以看到，目前主动连接的目标节点来源只有两类，一类是配置的主动节点，一类是节点发现获取到的可连接节点。

### 被动连接
当`node.passive`配置中的节点主动与当前节点建立连接时，当前节点都会无条件的接受。

```
node {
  passive = [
    # Passive accept connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
 }
```

另外，节点在发现其他节点的同时也会被其他节点发现，所以，被动连接的来源除了上述配置的节点，还来源于其他节点。

和节点发现基于udp协议不一样，节点连接基于tcp协议，但是被动连接绑定的端口号和节点发现绑定的端口号是一样的。如果一个节点不想有被动连接，可以通过关闭tcp 18888端口实现。如果某个节点关闭了被动连接，整个网络拓扑会变成如下图所示：

![image](https://raw.githubusercontent.com/King31T/documentation-zh/network_connecting/images/network_topology2.png)

## 日志与网络连接验证
java-tron 节点日志为节点目录下的`/logs/tron.log`。在节点安装目录下，可以使用如下命令查看节点最新日志，以了解节点区块同步情况：

```
$ tail -f /logs/tron.log/
```

如果一切正常，您将看到类似如下区块同步的日志信息：
```
15:41:48.033 INFO  [nioEventLoopGroup-6-2] [DB](Manager.java:1208) pushBlock block number:76, cost/txs:13/0 false
15:41:48.033 INFO  [nioEventLoopGroup-6-2] [net](TronNetDelegate.java:255) Success process block Num:76,ID:000000000000004c9e3899ee9952a7f0d9e4f692c7070a48390e6fea8099432f.
```

对于超级代表的产块的全节点，您将看到如下生产区块的日志信息：

```
02:31:33.008 INFO  [DPosMiner] [DB](Manager.java:1383) Generate block 79336 begin
02:31:33.059 INFO  [DPosMiner] [DB](SnapshotManager.java:315) flush cost:51, create checkpoint cost:49, refresh cost:2
02:31:33.060 INFO  [DPosMiner] [DB](Manager.java:1492) Generate block 79336 success, trxs:0, pendingCount: 0, rePushCount: 0, postponedCount: 0
```

如果节点日志中没有报告任何错误消息，则表示一切正常。您也可以通过发送http请求，来判断节点是否已经启动，以及查看节点的状态：包括节点配置信息，节点所在机器信息，节点peers连接情况等：
```
$ curl http://127.0.0.1:16887/wallet/getnodeinfo
```

返回结果：

```
{
    "activeConnectCount": 3,
    "beginSyncNum": 42518346,
    "block": "Num:42518365,ID:000000000288c75d1967232f1efe606ff90b9dd76660d7de8cc091849be6bf10",
    "cheatWitnessInfoMap": {
        ...
    },
    "configNodeInfo": {
        ...
        "codeVersion": "4.5.1",
        "dbVersion": 2,
        "discoverEnable": true,
        "listenPort": 18888,
        ...
    },
    "currentConnectCount": 18,
    "machineInfo": {
        ...
    },
    "passiveConnectCount": 15,
    "peerList": [
        ...
    ],
    "solidityBlock": "Num:42518347,ID:000000000288c74b723398aef104c585bad1c7cbade7793c5551466bd916feee",
    "totalFlow": 8735314
}
```

为了让用户与TRON网络交互，java-tron节点必须处于运行状态，并且处于同步正常的状态。节点是否与网络中其它节点保持同步，可以通过在Tronscan查询当前的区块高度和节点ID，并与本地节点`/wallet/getnowblock`的结果进行比较，如果相等，则说明本地节点的同步状态是正常的。

## 连接问题
有时java-tron无法连接到对等节点，常见的原因有:

* 本地时钟错误。参与到TRON网络需要一个精确的时钟。可以使用`sudo ntpdate -s time.nist.gov` 命令重新同步本地时钟。
* 某些防火墙配置可能会禁止UDP流量，而节点发现服务建立在UDP协议基础之上，因此可以通过配置[`node.active`](#_5)，在节点发现无效的情况下连接到网络。
* 通过配置[`node.passive`](#_5)，以接受可信的节点的主动连接。
* Shasta测试网暂时不支持节点加入到网络中 ，如果需要运行节点加入到公共测试网络，可以选择Nile测试网。

## 连接到私链网络
对于开发人员来说，他的节点有可能并不需要连接到TRON主网或者TRON公共测试网络，而是需要连接到私有测试网络，因为私链不但对机器配置没有要求，而且在私链网络的沙盒环境下，更容易测试各种功能，可以自由破坏而不需要承担任何后果。

私链网络需要将[私链配置文件](https://github.com/tronprotocol/tron-deployment/blob/master/private_net_config.conf)中的配置项`node.p2p.version`配置成一个没有被任何其他现有的公共网络（TRON主网，测试网）使用的值。有关私链搭建的详细说明请参考 [私链网络](private_network.md)。

