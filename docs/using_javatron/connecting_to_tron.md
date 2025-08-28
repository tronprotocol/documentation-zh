# 连接到TRON网络

TRON网络主要分为主网，Shasta测试网，Nile测试网以及私网，因此对于java-tron客户端，可以通过对配置文件中配置项的修改使其连接到任意一个TRON网络中。目前测试网中，Shasta测试网不支持节点加入，Nile测试网支持。

您需要设置如下配置项，将java-tron连接到其中一个TRON网络：

* 网络ID(`p2p.version`): 表示希望加入的网络。相关配置项：
```
node {
  ...
  p2p {
    version = 11111
  }
  ...
}
```
特别的：
    * 主网：`version=11111`
    * Nile测试网：`version = 201910292`
    * 私链网络：自定义，设置成其它值

* 创世块：需保证创世块的设置与网络中其它节点的相同，否则无法和其他节点建立连接。相关配置项：
```
genesis.block = {
  # Reserve balance
  assets = [
    {
      accountName = "Zion"
      accountType = "AssetIssue"
      address = "TLLM21wteSPs4hKjbxgmH1L6poyMjeTbHm"
      balance = "99000000000000000"
    },
    {
      accountName = "Sun"
      accountType = "AssetIssue"
      address = "TXmVpin5vq5gdZsciyyjdZgKRUju4st1wM"
      balance = "0"
    },
    {
      accountName = "Blackhole"
      accountType = "AssetIssue"
      address = "TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy"
      balance = "-9223372036854775808"
    }
  ]

  witnesses = [
    {
      address: THKJYuUmMKKARNf7s2VT51g5uPY6KEqnat,
      url = "http://GR1.com",
      voteCount = 100000026
    },
    {
      address: TVDmPWGYxgi5DNeW8hXrzrhY8Y6zgxPNg4,
      url = "http://GR2.com",
      voteCount = 100000025
    },
    {
      address: TWKZN1JJPFydd5rMgMCV5aZTSiwmoksSZv,
      url = "http://GR3.com",
      voteCount = 100000024
    },
    {
      address: TDarXEG2rAD57oa7JTK785Yb2Et32UzY32,
      url = "http://GR4.com",
      voteCount = 100000023
    },
    {
      address: TAmFfS4Tmm8yKeoqZN8x51ASwdQBdnVizt,
      url = "http://GR5.com",
      voteCount = 100000022
    },
    {
      address: TK6V5Pw2UWQWpySnZyCDZaAvu1y48oRgXN,
      url = "http://GR6.com",
      voteCount = 100000021
    },
    {
      address: TGqFJPFiEqdZx52ZR4QcKHz4Zr3QXA24VL,
      url = "http://GR7.com",
      voteCount = 100000020
    },
    {
      address: TC1ZCj9Ne3j5v3TLx5ZCDLD55MU9g3XqQW,
      url = "http://GR8.com",
      voteCount = 100000019
    },
    {
      address: TWm3id3mrQ42guf7c4oVpYExyTYnEGy3JL,
      url = "http://GR9.com",
      voteCount = 100000018
    },
    {
      address: TCvwc3FV3ssq2rD82rMmjhT4PVXYTsFcKV,
      url = "http://GR10.com",
      voteCount = 100000017
    },
    {
      address: TFuC2Qge4GxA2U9abKxk1pw3YZvGM5XRir,
      url = "http://GR11.com",
      voteCount = 100000016
    },
    {
      address: TNGoca1VHC6Y5Jd2B1VFpFEhizVk92Rz85,
      url = "http://GR12.com",
      voteCount = 100000015
    },
    {
      address: TLCjmH6SqGK8twZ9XrBDWpBbfyvEXihhNS,
      url = "http://GR13.com",
      voteCount = 100000014
    },
    {
      address: TEEzguTtCihbRPfjf1CvW8Euxz1kKuvtR9,
      url = "http://GR14.com",
      voteCount = 100000013
    },
    {
      address: TZHvwiw9cehbMxrtTbmAexm9oPo4eFFvLS,
      url = "http://GR15.com",
      voteCount = 100000012
    },
    {
      address: TGK6iAKgBmHeQyp5hn3imB71EDnFPkXiPR,
      url = "http://GR16.com",
      voteCount = 100000011
    },
    {
      address: TLaqfGrxZ3dykAFps7M2B4gETTX1yixPgN,
      url = "http://GR17.com",
      voteCount = 100000010
    },
    {
      address: TX3ZceVew6yLC5hWTXnjrUFtiFfUDGKGty,
      url = "http://GR18.com",
      voteCount = 100000009
    },
    {
      address: TYednHaV9zXpnPchSywVpnseQxY9Pxw4do,
      url = "http://GR19.com",
      voteCount = 100000008
    },
    {
      address: TCf5cqLffPccEY7hcsabiFnMfdipfyryvr,
      url = "http://GR20.com",
      voteCount = 100000007
    },
    {
      address: TAa14iLEKPAetX49mzaxZmH6saRxcX7dT5,
      url = "http://GR21.com",
      voteCount = 100000006
    },
    {
      address: TBYsHxDmFaRmfCF3jZNmgeJE8sDnTNKHbz,
      url = "http://GR22.com",
      voteCount = 100000005
    },
    {
      address: TEVAq8dmSQyTYK7uP1ZnZpa6MBVR83GsV6,
      url = "http://GR23.com",
      voteCount = 100000004
    },
    {
      address: TRKJzrZxN34YyB8aBqqPDt7g4fv6sieemz,
      url = "http://GR24.com",
      voteCount = 100000003
    },
    {
      address: TRMP6SKeFUt5NtMLzJv8kdpYuHRnEGjGfe,
      url = "http://GR25.com",
      voteCount = 100000002
    },
    {
      address: TDbNE1VajxjpgM5p7FyGNDASt3UVoFbiD3,
      url = "http://GR26.com",
      voteCount = 100000001
    },
    {
      address: TLTDZBcPoJ8tZ6TTEeEqEvwYFk2wgotSfD,
      url = "http://GR27.com",
      voteCount = 100000000
    }
  ]

  timestamp = "0" #2017-8-26 12:00:00

  parentHash = "0xe58f33f9baf9305dc6f82b9f1934ea8f0ade2defb951258d50167028c780351f"
}
```

## 节点发现 

### 开启与关闭
节点发现通过配置文件开启和关闭，通常开启，相关配置项如下：

```
node.discovery = {
  ...
  enable = true
  ...  
}
```

### 引导节点
java-tron使用[Kademlia](https://zh.wikipedia.org/wiki/Kademlia)协议发现其他节点。节点发现需要引导节点(boot节点)，借助引导节点发现TRON网络中的其他节点。引导节点由两部分组成，一部分是种子节点，一部分是配置的主动连接节点，详情见[主动连接](#_7)。

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
    #"[2a05:d014:1f2f:2600:1b15:921:d60b:4c60]:18888", // use this if support ipv6
    #"[2600:1f18:7260:f400:8947:ebf3:78a0:282b]:18888", // use this if support ipv6
  ]
}

```
如果网卡支持ipv6，可以使用上述列表中的ipv6地址格式的种子节点，将注释符`#`去掉即可。
如果想要获取最新的seed.node，可以在官方的[配置文件](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf)查看。

- 从数据库中读取的持久化节点。持久化节点需要开启节点持久化服务。如果开启该功能，[路由表](https://zh.wikipedia.org/wiki/Kademlia#%E8%B7%AF%E7%94%B1%E8%A1%A8)中的节点会被定时任务写入数据库，如果节点启动的时候基于此数据库，会从数据库中读取这些节点作为种子节点使用。相关配置项：
```
node.discovery = {
  ...
  persist = true
  ... 
}
```


节点发现基于udp协议，绑定的默认端口是18888，也可以绑定其他端口。相关配置项：
```
node {
  ...
  listen.port = 18888
  ...
}
```

在某些情况下，不需要开启节点发现，比如，运行一个本地测试节点或部署一个具有固定的一些节点的测试网络。这时可以通过将配置项设置成`node.discovery.enable = false`来关闭节点发现，也可以通过防火墙关闭udp 18888端口来实现。


## 节点连接

### 节点连接数量
`node.maxConnections`表示节点与其它节点的最大连接数量，默认值是30。设置更大的值可以使节点能够建立更多的连接，加入网络的效率更高，同时广播的效率也更高，但是，相对的维护连接需要的带宽也更高，性能消耗也更大，因此，请根据实际情况设置。  
```
node {
  ...
  maxConnections = 30
  ...
}
```

### 主动连接
主动连接的目标节点来源于三部分：

- 配置的主动节点(高优先级)，不依赖于节点发现，即使节点发现没有开启，当前节点也会主动向这些节点发起连接。相关配置项：
```
node {
  ...
  active = [
    # Active establish connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
  ...
 }
``` 
- 节点发现获取到的可连接节点(中优先级)
- DNS节点(低优先级)，DNS树获取的备用节点，需要配置treeUrls，在前两个来源不足时使用，一般不会使用到。相关配置项(一般不配置)：
```
dns {
  ...
  # dns urls to get nodes, url format tree://{pubkey}@{domain}, default empty
  treeUrls = [
    #"tree://AKMQMNAJJBL73LXWPXDI4I5ZWWIZ4AWO34DWQ636QOBBXNFXH3LQS@main.trondisco.net",
  ]
  ...
}
```
相比较传统的静态种子节点列表，DNS 树机制在P2P网络引导方面具有节点动态更新、不易受攻击等优势。

可以看到，目前主动连接的目标节点来源只有两类，一类是配置的主动节点，一类是节点发现获取到的可连接节点。

### 被动连接
- `node.passive`配置的节点。当这些节点主动向当前节点发起连接时，当前节点都会无条件的接受。

```
node {
  ...
  passive = [
    # Passive accept connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
  ...
 }
```

- 其他节点。节点在发现其他节点的同时也会被其他节点发现，这些节点也有可能向当前节点主动发起连接。

和节点发现基于udp协议不一样，节点连接基于tcp协议，但是被动连接绑定的端口号和节点发现绑定的端口号是一样的。如果一个节点为了安全起见，不想有被动连接，可以通过防火墙关闭tcp 18888端口实现。如果某个节点关闭了被动连接，整个网络拓扑会变成如下图所示：

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_topology.png)

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

