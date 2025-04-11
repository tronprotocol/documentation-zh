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
java-tron节点在有足够的对等节点之前会不断地尝试与网络上的其他节点建立连接，同时它也会接受来自其他节点的连接。java-tron使用节点发现协议查找对等点。在发现协议中，节点间交换连接细节，然后建立会话，交换TRON网络数据。

首先，如果需要java-tron节点进行节点发现，那么要在节点配置文件中开启节点发现服务：

```
node.discovery = {
  enable = true
  ...
}
```

然后，对于加入到TRON网络的新节点，可以通过配置`种子节点`使当前节点更容易的连接到对等节点，然后再通过对等节点获取到其它节点的地址信息。一般将种子节点设置成稳定在线的全节点，对于TRON主网，可以使用社区公共节点作为种子节点，例如:

```
seed.node = {
  # List of the seed nodes
  # Seed nodes are stable full nodes

  ip.list = [
    "3.225.171.164:18888",
    "52.53.189.99:18888",
    "18.196.99.16:18888",
    "34.253.187.192:18888",
    "18.133.82.227:18888",
    "35.180.51.163:18888",
    "54.252.224.209:18888",
    "18.231.27.82:18888",
    "52.15.93.92:18888",
    "34.220.77.106:18888",
    "15.207.144.3:18888",
    "13.124.62.58:18888",    
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

在某些情况下，不需要开启节点发现进程，比如，运行一个本地测试节点或部署一个具有固定的一些节点的测试网络。这时可以通过将配置项设置成`node.discovery.enable = false`来关闭节点发现进程。

## 节点连接数量限制
`node.maxActiveNodes`表示节点与其它节点的最大连接数量，默认值是30。设置更大的值可以使节点能够建立更多的连接，加入网络的效率更高，同时广播的效率也更高，但是，相对的维护连接需要的带宽也更高，性能消耗也更大，因此，请根据实际情况设置。
```
node {
    maxActiveNodes = 30
}
```

## 主动连接与被动连接
java-tron支持设置其主动连接的节点`node.active`以及被动连接的节点`node.passive`。配置`node.active`和`node.passive`对改善节点的网络连接稳定性有很大的帮助。

当java-tron启动后，会主动与`node.active`中的对等节点建立连接。

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

当`node.passive`中的节点主动与当前节点建立连接时，当前节点都会无条件的接受。

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

