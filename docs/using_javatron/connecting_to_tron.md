# 连接 TRON 网络指南

TRON 网络分为以下几类：

- **主网（Mainnet）**
- **Nile 测试网**
- **Shasta 测试网**（目前不支持节点加入）
- **私有链（Private Network）**

本指南将介绍如何配置 java-tron 客户端连接到这些网络，涵盖基础配置网络、节点发现、节点连接，日志与节点状态验证以及如何排查连接问题。



## 基础配置网络

通过修改 [配置文件](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/resources/config.conf) 中的以下关键项，可将 java-tron 节点接入指定网络：

### 网络标识（P2P 网络 ID）

网络ID(`p2p.version`): 表示希望加入的网络。相关配置项：
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

- 主网：`version=11111`
- Nile 测试网：`version = 201910292`
- Shasta 测试网：`version = 1`
- 私链网络：自定义，设置成其它值

### 创世块（Genesis Block）
需保证创世块 `genesis.block` 的设置与网络中其它节点的相同，否则无法和其他节点建立连接。主网的 `genesis.block` 配置如下：
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
### 启用节点发现
节点发现通过配置文件开启和关闭。默认开启，相关配置项如下：
```
node.discovery = {
  ...
  enable = true
  ...
}
```


### 引导节点
java-tron 使用 [Kademlia](https://zh.wikipedia.org/wiki/Kademlia) 协议发现其他节点。节点发现需要引导节点 (boot 节点)，借助引导节点发现 TRON 网络中的其他节点。引导节点由两部分组成，一部分是种子节点，一部分是配置的主动连接节点，详情见[主动连接](#active-peers)。

种子节点也由两部分组成：

#### 配置的 `seed.node` 
使用 `seed.node` 初始化网络连接。应设置为在线稳定的全节点。


```
seed.node = {
  ip.list = [
    "3.225.171.164:18888",
    "52.8.46.215:18888",
    ...
    "18.163.230.203:18888"
    #"[2a05:d014:1f2f:2600:1b15:921:d60b:4c60]:18888", // use this if support ipv6
    #"[2600:1f18:7260:f400:8947:ebf3:78a0:282b]:18888", // use this if support ipv6
  ]
}
```
对于TRON主网，可以使用 [社区公共节点](https://developers.tron.network/docs/networks#public-node) 作为种子节点。如果想要获取最新的`seed.node`，可以在官方的 [配置文件](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf) 查看。
如果网卡支持 ipv6，可以使用上述列表中的 ipv6 地址格式的种子节点，将注释符 `#` 去掉即可。

#### 从数据库中读取的持久化节点
持久化节点需要开启节点持久化服务。如果开启该功能，[路由表](https://zh.wikipedia.org/wiki/Kademlia#%E8%B7%AF%E7%94%B1%E8%A1%A8) 中的节点会被定时任务写入数据库，如果节点启动的时候基于此数据库，会从数据库中读取这些节点作为种子节点使用。相关配置项：
```
node.discovery = {
  ...
  persist = true
  ... 
}
```

节点发现基于 UDP 协议 (User Datagram Protocol)，绑定的默认端口是 `18888`，也可以绑定其他端口。相关配置项：
```
node {
  ...
  listen.port = 18888
  ...
}
```

### 关闭节点发现

在某些情况下，不需要开启节点发现，比如，运行一个本地测试节点或部署一个具有固定的一些节点的测试网络。这时可以通过将配置项设置成 `node.discovery.enable = false` 来关闭节点发现，也可以通过防火墙关闭 UDP `18888` 端口来实现。

## 节点连接

### 节点连接数量
`node.maxConnections`  表示节点与其它节点的最大连接数量，默认值是 30。设置更大的值可以使节点能够建立更多的连接，加入网络的效率更高，同时广播的效率也更高，但是，相对的维护连接需要的带宽也更高，性能消耗也更大，因此，请根据实际情况设置。 
```
node {
  ...
  maxConnections = 30           # 最大连接数
  ...
}
```



### 主动连接（Active Peers）
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
- DNS 节点(低优先级)，DNS 树获取的备用节点，需要配置 treeUrls，在前两个来源不足时使用，一般不会使用到。相关配置项(一般不配置)：
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
  相比较传统的静态种子节点列表，DNS 树机制在 P2P 网络引导方面具有节点动态更新、不易受攻击等优势。
  
可以看到，目前主动连接的目标节点来源只有两类，一类是配置的主动节点，一类是节点发现获取到的可连接节点。

### 被动连接
- `node.passive` 配置的节点。当这些节点主动向当前节点发起连接时，当前节点都会无条件的接受。

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

和节点发现基于 UDP 协议不一样，节点连接基于 TCP 协议 (Transmission Control Protocol)，但是被动连接绑定的端口号和节点发现绑定的端口号是一样的。如果一个节点为了安全起见，不想有被动连接，可以通过防火墙关闭 TCP 18888 端口实现。如果某个节点关闭了被动连接，整个网络拓扑会变成如下图所示：

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_topology.png)

## 日志与节点状态验证
### 查看同步日志
TRON 节点日志位于 `logs/tron.log`，可通过如下命令实时查看：

```
$ tail -f logs/tron.log
```
### 同步中日志示例：
```
pushBlock block number:76, cost/txs:13/0 false
Success process block Num:76,ID:000000000000004c9e3899ee9952a7f0d9e4f692c7070a48390e6fea8099432f.
```
### 生产区块日志示例（超级代表节点）：
```
Generate block 79336 begin
Generate block 79336 success, trxs:0, pendingCount: 0, rePushCount: 0, postponedCount: 0
```
### 查询节点状态
使用 HTTP 接口获取当前节点运行状态：

```
$ curl http://127.0.0.1:16887/wallet/getnodeinfo
```
返回示例：
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
### 验证节点同步状态
可在 [TRONSCAN 区块浏览器](https://tronscan.org/) 查询当前区块高度，并与本地接口返回结果对比：
```
curl http://127.0.0.1:16887/wallet/getnowblock
```
若区块高度一致，则说明本地节点同步正常。

## 常见连接问题排查
遇到节点无法连接网络时，可参考以下问题排查：

- **本地时钟偏差**

    使用以下命令同步系统时间：
    ```
    sudo ntpdate -s time.nist.gov
    ```

- **UDP 被防火墙阻挡**

    节点发现协议依赖 UDP，如被防火墙阻断，可改用 `node.active` 指定固定节点。
  
- **未被动接受连接**

    使用 `node.passive` 接收来自可信节点的主动连接。
  
- **Shasta 测试网不支持新节点加入**，请选择 Nile 测试网。

## 连接私链网络
开发者可通过搭建私有 TRON 网络，获得更大的测试灵活性和控制能力。

### 配置要点：
- 使用私有的 `node.p2p.version` 值，确保不会与主网或测试网冲突

### 搭建参考：
- 请参考文档 [私链网络](https://tronprotocol.github.io/documentation-zh/using_javatron/private_network/) 获取完整的私链部署说明。
