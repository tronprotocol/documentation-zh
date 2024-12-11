# 部署Java-Tron节点
Java-tron节点支持部署在 `Linux` 或 `MacOS` 操作系统上，并且依赖`Oracle JDK 1.8` ，不支持其它版本的JDK。

运行Java-tron节点需要的最小的硬件配置是 `8核CPU`、`16G内存`、`2T SDD`，推荐的配置是： `16核CPU`、`32G内存`、`2.5T+ SDD`，超级代表产块节点建议 `32核CPU`、`64G内存`。

# 编译源码
首先，通过如下git命令将Java-tron源代码克隆到本地，并且切换到master分支。在执行命令前，请确保已经安装了`git`工具。

```
$ git clone https://github.com/tronprotocol/java-tron.git
$ git checkout -t origin/master
```

然后，通过执行如下命令编译Java-tron源代码。参数`-x test`表示跳过执行测试用例，您也可以去掉这个参数，以在编译的过程中执行测试代码，这将使编译时间更长。编译完成之后，FullNode.jar会生成在 `java-tron/build/libs/`目录下。

```
$ cd java-tron
$ ./gradlew clean build -x test
```



# 运行Java-tron节点

你可以选择不同的配置文件将Java-tron节点连接到不同的网络中，其中主网全节点配置文件为：[main_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf)，其它网络节点配置文件在[这里](https://github.com/tronprotocol/tron-deployment)下载。

### 启动全节点

Fullnode作为TRON网络的入口点，拥有完整的历史数据，并提供对外访问的HTTP API和GRPC API。您可以通过全节点与TRON网络进行交互，如：资产转移、合约部署、合约交互等。主网全节点启动命令如下，并通过`-c`参数指定全节点的配置文件。下面启动命令中使用的是主网的配置文件，因此启动的是一个主网的全节点，启动Nile测试网的全节点或者私链的全节点，请使用对应的配置文件：

````
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c main_net_config.conf
````

* -XX:+UseConcMarkSweepGC  ：指定并行垃圾回收。要放在 -jar 参数前面，不能放在最后面。
* -Xmx  ：JVM堆所占内存的最大值，可以设置成物理内存的80%。

main_net_config.conf里面的部分配置参考[网络配置](./connecting_to_tron.md)章节。

Java-tron启动后，日志会输出在文件java-tron/logs/tron.log中，查看文件可以看到以下内容显示网络层建立P2P连接，之后节点开始区块同步：
```
16:41:11.229 INFO  [main] [app](Args.java:1143) ************************ Net config ************************
16:41:11.229 INFO  [main] [app](Args.java:1144) P2P version: 201910292
16:41:11.229 INFO  [main] [app](Args.java:1145) Bind IP: 192.168.20.101
16:41:11.229 INFO  [main] [app](Args.java:1146) External IP: 203.12.203.3
16:41:11.229 INFO  [main] [app](Args.java:1147) Listen port: 18888
16:41:11.229 INFO  [main] [app](Args.java:1148) Discover enable: true
... ...
16:41:32.838 INFO  [peerClient-13] [DB](Manager.java:1936) HeadNumber: 52347923, syncBeginNumber: 52347923, solidBlockNumber: 52347905.
16:41:32.839 INFO  [peerClient-13] [net](SyncService.java:197) Get block chain summary, low: 52347923, highNoFork: 52347923, high: 52347923, realHigh: 52347923
16:41:32.839 INFO  [peerClient-13] [net](PeerConnection.java:184) Send peer /182.125.127.201:18888 message type: SYNC_BLOCK_CHAIN
size: 1, start block: Num:52347923,ID:00000000031ec413b7d75adeb141cfb6acf01127436dcd02eafbaf58df07f9e5
```
如果节点启动异常，该日志也会输出错误信息。

### 启动出块的全节点

将`--witness`参数添加到启动命令中，fullnode将作为出块的全节点运行。出块全节点除了支持fullnode的所有功能，它还支持区块生产和交易打包。请确保您拥有一个超级代表账户，并获得他人的投票，如果票数排在前27名，您需要启动一个出块的全节点参与区块生产。

将超级代表地址的私钥填写到main_net_config.conf的localwitness列表中，示例如下。但如果不希望使用这种以明文的方式进行私钥指定，可以使用keystore + 密码的方式，请参考下面[其它说明](#_3)。

```
localwitness = [
    650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812
]
```

然后执行如下命令来启动节点:

```
$ java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c main_net_config.conf
```

**注意**：对于主网和nile测试网，由于新节点启动后，需要同步的数据量较大，因此同步数据需要较长的时间。可以使用 [数据快照](../backup_restore/#_5) 来加快节点同步速度，Nile测试网[下载](https://database.nileex.io)。首先下载最新的数据快照，并将其解压至tron项目的output-directory目录下，然后再启动节点，这样节点将在数据快照的基础上进行同步。

# 其它说明
### 如何使用keystore+密码的方式指定witness账户私钥

1. 这种方式指定私钥，需要在启动节点时进行人机交互，因此请不要使用nohup命令，建议使用会话保持工具，如screen, tmux等。
2. 注释掉节点配置文件中的localwitness配置项，取消localwitnesskeystore配置项的注释，填入keystore文件的路径，注意keystore文件需要放到启动命令执行的当前目录下或者其子目录下。如当前目录是A，keystore文件的目录是A/B/localwitnesskeystore.json，则需要配置成：
    ```
    localwitnesskeystore = [
          "B/localwitnesskeystore.json"
    ]
    ```
    注：可以使用[wallet-cli](https://github.com/tronprotocol/wallet-cli.git)项目的registerwallet命令生成 keystore + 密码。
3. 启动出块的全节点
    ```
      $ java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c main_net_config.conf
    ```
4. 正确的输入密码，完成节点启动。



### 使用tcmalloc优化内存占用

为达到内存使用最优化，可以使用 google tcmalloc 替代系统 glibc malloc. 方法如下：
安装tcmalloc，然后在启动脚本中添加以下两行，不同的linux发行版tcmalloc的路径略有差异。
```
#!/bin/bash

export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
export TCMALLOC_RELEASE_RATE=10

# original start command
java -jar .....
```

在各个linux发行版上安装命令如下：

* Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable
    安装

    ```
    sudo apt install libgoogle-perftools4
    ```

    在启动脚本中添加：

    ```
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

* Ubuntu 16.04 LTS
    安装同上，在启动脚本中添加：

    ```
    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

* CentOS 7
  安装
    ```
    sudo yum install gperftools-libs
    ```
    在启动脚本中添加：
    ```
    export LD_PRELOAD="/usr/lib64/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```
