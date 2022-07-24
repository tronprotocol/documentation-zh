# 部署Java-Tron节点

支持的操作系统：`Linux` ，`MacOS`

依赖和工具：`Oracle JDK 1.8` ,`git`

**注意**：请安装`Oracle JDK 1.8` ，而不是 `Open JDK 1.8`

# 推荐配置
如果您需要部署一个主网或者Nile测试网上的java-tron节点，推荐的机器配置如下：

* CPU：16核 
* 内存：32G 
* SSD：1.5T以上
* 带宽：100M 

如果是超级代表搭建产块的全节点，建议配置是 CPU：32核， 内存：64G。

如果您只需要对Java-tron的某些功能或者您的DAPP应用进行开发或者测试，而仅需要搭建一个私链网络，那么推荐的配置为：至少两核CPU。

# Java-Tron部署指南
无论哪种类型的节点，部署流程都是一样的，请参考如下步骤：
## 1. 获取Fullnode.jar
可以通过编译源代码或者从已发布版本直接获取[Fullnode.jar](https://github.com/tronprotocol/java-tron/releases)

### 编译Java-tron源码
通过编译源代码的方式获取到可执行文件，需要首先将源码克隆到本地，然后执行编译命令：

1. 获取Java-tron源码
  通过如下命令获取Java-tron源代码。在执行命令前，请确保已经安装了`git`工具。

    ```
    $ git clone https://github.com/tronprotocol/java-tron.git
    $ git checkout -t origin/master
    ```
2. 编译
  直接通过执行如下命令即可完成Java-tron项目的编译。参数`-x test`表示跳过执行测试用例，您也可以去掉这个参数，只是需要更多的编译时间。
  
    ```
    $ cd java-tron
    $ ./gradlew clean build -x test
    ```
    编译完成之后，FullNode.jar会生成在 `java-tron/build/libs/FullNode.jar`，然后您可以拷贝`FullNode.jar`到您的部署目录中。
 
## 2. 获取Java-tron配置文件
主网全节点配置文件：[main_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf)，其它网络节点配置文件在[这里](https://github.com/tronprotocol/tron-deployment)下载。

## 3. 启动Java-Tron节点
启动一个全节点/产块的全节点的命令如下：

* 启动全节点：

    Fullnode作为TRON网络的入口点，拥有完整的历史数据，并提供对外访问的HTTP API和GRPC API。您可以通过全节点与TRON网络进行交互，如：资产转移、合约部署、合约交互等。主网全节点启动命令如下，并通过`-c`参数指定全节点的配置文件。下面启动命令中使用的是主网的配置文件，因此启动的是一个主网的全节点，启动Nile测试网的全节点或者私链的全节点，请使用对应的配置文件：

    ````
    $  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c main_net_config.conf
    ````
    
    * -XX:+UseConcMarkSweepGC  ：指定并行垃圾回收。要放在 -jar 参数前面，不能放在最后面。
    * -Xmx  ：JVM堆的最大值，可以设置成物理内存的80%。

* 启动出块的全节点

    将`--witness`参数添加到启动命令中，fullnode将作为出块的全节点运行。出块全节点除了支持fullnode的所有功能，它还支持区块生产和交易打包。请确保您拥有一个超级代表账户，并获得他人的投票，如果票数排在前27名，您需要启动一个出块的全节点参与区块生产。
  
    将超级代表地址的私钥填写到main_net_config.conf的localwitness列表中，示例如下。但如果不希望使用这种以明文的方式进行私钥指定，可以使用keystore + 密码的方式，请参考[其它说明](#_2)

    ```
    localwitness = [
       650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812
    ]
    ```
  
    然后执行如下命令来启动节点:
  
    ```
      $ java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c main_net_config.conf
    ```

**注意**：对于主网和nile测试网，由于新节点启动后，需要同步的数据量较大，因此同步数据需要较长的时间。可以使用 [数据快照](../backup_restore/#_5) 来加快节点同步速度。首先下载最新的数据快照，并将其解压至tron项目的output-directory目录下，然后再启动节点，这样节点将在数据快照的基础上进行同步。

# 其它说明
**如何使用keystore+密码的方式指定witness账户私钥**

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



**使用tcmalloc优化内存占用**

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