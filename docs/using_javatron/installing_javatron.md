# 部署 java-tron 节点

本文档将指导开发者如何在 `Linux` 或 `macOS` 操作系统上部署 TRON java-tron 节点。

**重要提示：**java-tron 节点目前仅支持 `Oracle JDK 1.8`，不支持其他版本的 JDK。

## 硬件配置要求

运行 java-tron 节点所需的最小硬件配置如下：

* **CPU**: 8 核
* **内存**: 16 GB
* **SSD**: 3 TB
* **网络带宽**：100 Mbps

推荐的配置是：

* **CPU**: 16 核
* **内存**: 32 GB
* **SSD**: 3.5 TB+
* **网络带宽**：100 Mbps

对于作为**产块节点**的超级代表 (SR)，建议配置：

* **CPU**: 32 核
* **内存**: 64 GB
* **SSD**: 3.5 TB+
* **网络带宽**：100 Mbps


## 获取 java-tron 客户端

您可以在 [这里](https://github.com/tronprotocol/java-tron/releases) 直接下载官方提供的客户端，也可以自行通过编译源码来打包客户端。

### 编译 java-tron 前的先决条件
在编译 java-tron 之前，请确保您具备：

- 操作系统：`Linux` 或 `macOS`（不支持 `Windows`）。
- 已安装 Git 和根据您 CPU 架构安装的正确 JDK 版本。

步骤 1：验证 Git 是否安装

如果未安装 Git，请从 [https://git-scm.com/downloads](https://git-scm.com/downloads) 下载。

```bash
git --version
```

步骤 2：检查您的 CPU 架构并安装正确的 JDK

```bash
uname -m
```

- 如果您的架构是 `x86_64`（Intel/AMD 64 位）：
    - 安装 Java SE 8（Oracle JDK 8）：[https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)
    - 验证：
    ```bash
    java -version
    ```
    输出应显示以 `1.8` 开头的版本。

- 如果您的架构是 `arm64` 或 `aarch64`（Apple Silicon / ARM 服务器）：
    - 安装 Java SE 17（JDK 17）：[https://www.oracle.com/java/technologies/downloads/#java17](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)
    - 验证：
    ```bash
    java -version
    ```
    输出应显示以 `17` 开头的版本。

### 编译 java-tron 源代码

1.  克隆仓库并切换到 `master` 分支：
    ```
    git clone https://github.com/tronprotocol/java-tron.git
    git checkout -t origin/master
    cd java-tron
    ```
2.  然后，运行以下命令来构建 java-tron：
    ```
    ./gradlew clean build -x test
    ```
    * 参数 `-x test` 表示跳过测试用例的执行。您可以移除此参数以在编译期间执行测试代码，但这将延长编译时间。
    * 如果在构建过程中遇到 `DependencyVerificationException`，请刷新依赖项并重新生成验证元数据：
      ```
      ./gradlew clean build -x test --refresh-dependencies
      ```
    * 编译完成后，`FullNode.jar` 文件将在 `java-tron/build/libs/` 目录中生成。

## 启动 java-tron 节点

全节点作为 TRON 网络的入口，通过 HTTP 和 RPC API 提供完整接口。客户端可借助这些端点执行资产转账、部署智能合约并调用链上逻辑。全节点必须接入 TRON 网络，才能参与共识与交易处理。

### TRON 网络类型
TRON 网络主要分为以下几类：

- **主网（Mainnet）**  
  承载真实价值（TRX、TRC-20 代币等）的公共区块链，由庞大的去中心化网络保障安全。

- **[Nile 测试网（Testnet）](https://nileex.io/)**  
  面向未来的测试网，新功能和治理提案会率先在此上线，供开发者体验，因此其代码版本通常领先于主网。

- **[Shasta 测试网](https://shasta.tronex.io/)**  
  与主网的特性和治理提案保持高度一致，网络参数及软件版本与主网同步，为开发者提供接近真实的最终测试环境。

- **私有网络**  
  由私人实体搭建的定制化 TRON 网络，用于测试、开发或特定业务场景。

启动全节点时，通过指定对应的配置文件即可选择网络：主网配置：[config.conf](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf)；Nile 测试网配置：[config-nile.conf](https://github.com/tron-nile-testnet/nile-testnet/blob/master/framework/src/main/resources/config-nile.conf)

### 启动全节点连接主网

以下是启动 **主网全节点** 的命令，使用默认内置的主网配置文件：

`
nohup java -jar ./build/libs/FullNode.jar -c config.conf &
`

*   `nohup ... &`：在后台运行命令并忽略挂断信号。

> 对于生产环境部署或长期运行的主网节点，请参考下方 [主网 FullNode 部署的 JVM 参数优化](#主网-fullnode-部署的-jvm-参数优化) 章节，以获取完整的Java启动命令。

使用一下命令查看全节点运行日志，可以看到区块同步进度，节点连接状态等信息：
```bash
tail -f ./logs/tron.log
```

使用 TRON 官方区块链浏览器 [TronScan](https://tronscan.org/#/) 查看主网交易、区块、账户、超级代表投票和治理指标等信息。

请参见后续章节，了解在 Nile 测试网和私有网络中部署全节点的详细说明。

#### 主网 FullNode 部署的 JVM 参数优化
为了在连接主网时获得更高的效率和稳定性，请参考以下针对不同架构的完整Java程序启动命令：

##### x86_64（JDK 8）
```bash
$ nohup java -Xms9G -Xmx12G -XX:ReservedCodeCacheSize=256m \
             -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
             -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
             -XX:+PrintGCDateStamps  -Xloggc:gc.log \
             -XX:+UseConcMarkSweepGC -XX:NewRatio=3 \
             -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
             -XX:+HeapDumpOnOutOfMemoryError \
             -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
             -jar ./build/libs/FullNode.jar -c main_net_config.conf &
```
##### ARM64（JDK 17）
```bash
$ nohup java -Xmx9G -XX:+UseZGC \
             -Xlog:gc,gc+heap:file=gc.log:time,tags,level:filecount=10,filesize=100M \
             -XX:ReservedCodeCacheSize=256m \
             -XX:+UseCodeCacheFlushing \
             -XX:MetaspaceSize=256m \
             -XX:MaxMetaspaceSize=512m \
             -XX:MaxDirectMemorySize=1g \
             -XX:+HeapDumpOnOutOfMemoryError \
             -jar ./build/libs/FullNode.jar -c main_net_config.conf &
```

#### Java 启动参数解释
**通用内存参数：**

*   `-Xms` / `-Xmx`：设置 JVM 堆的初始值和最大值。
    * 对于最低硬件要求（16 GB RAM 的服务器）：建议 JDK 8 使用 `-Xms9G -Xmx12G`；JDK 17 使用 `-Xmx9G`。
    * 对于 RAM ≥32 GB 的服务器，建议将最大堆值（`-Xmx`）设置为总 RAM 的 40%，最小堆值设置为 `-Xms9G`。
*   `-XX:MetaspaceSize` / `-XX:MaxMetaspaceSize`：设置元空间（类元数据）的初始值和最大值。
*   `-XX:MaxDirectMemorySize`：限制 NIO Direct Byte Buffers 使用的内存。
*   `-XX:ReservedCodeCacheSize`：设置 JIT 代码缓存的最大值。
*   `-XX:+UseCodeCacheFlushing`：允许 JVM 在代码缓存满时刷新它。
*   `-XX:+HeapDumpOnOutOfMemoryError`：如果发生 OutOfMemoryError，则将堆内存转储到文件。

**JDK 8（CMS GC）特有参数：**

*   `-XX:+UseConcMarkSweepGC`：启用并发标记清除（CMS）垃圾收集器。
*   `-XX:NewRatio=3`：设置老年代与新生代的比例为 3:1。
*   `-XX:+CMSScavengeBeforeRemark`：在 CMS 重新标记阶段之前触发一次 Minor GC，以减少暂停时间。
*   `-XX:+ParallelRefProcEnabled`：启用并行引用处理，以减少暂停时间。
*   `-XX:+UseCMSInitiatingOccupancyOnly` 和 `-XX:CMSInitiatingOccupancyFraction=70`：强制 CMS 在老年代使用率达到 70% 时开始回收。
*   `-XX:+PrintGCDetails`、`-XX:+PrintGCDateStamps`、`-Xloggc:gc.log`：传统的 GC 日志记录设置。

**JDK 17（ZGC）特有参数：**

*   `-XX:+UseZGC`：启用 ZGC，一种可扩展的低延迟垃圾收集器。
*   `-Xlog:gc...`：统一的 JVM 日志记录配置。示例配置了带有文件轮换（10 个文件，每个 100MB）的 GC 日志。

### 启动全节点连接 Nile 测试网

使用 `-c` 参数将节点指向对应网络的配置文件。由于 Nile 测试网可能包含主网尚未发布的新功能，**强烈建议**按照 [Nile 测试网源码编译指南](https://github.com/tron-nile-testnet/nile-testnet/blob/master/README.md#building-the-source-code) 编译源码。

```bash
nohup java -jar ./build/libs/FullNode.jar -c config-nile.conf &
```

Nile 相关资源：区块浏览器、水龙头、钱包、开发者文档及网络统计信息，请访问 [nileex.io](https://nileex.io/)。

### 接入 Shasta 测试网

Shasta 不接受公共节点连接同步区块，仅可通过 TronGrid 端点以API方式访问；详情见 [TronGrid 服务](https://developers.tron.network/docs/trongrid)。
Shasta 相关资源（浏览器、水龙头、钱包、开发者文档及网络统计）请访问 [shastaex.io](https://shasta.tronex.io/)。

### 启动全节点连接私有网络

如需为测试或开发搭建私有网络，请遵循[私有网络指南](https://tronprotocol.github.io/documentation-zh/using_javatron/private_network/)。

### 启动出块节点

在上述全节点启动命令中添加 `--witness` 参数，`FullNode` 将作为**出块节点** (SR Node) 运行。出块节点除了支持全节点的所有功能外，还支持区块生产和交易打包。

**重要提示**:

* 请确保您拥有一个超级代表 (SR) 账户并获得了足够的投票。如果您获得了前 27 名的投票，您需要启动一个 SR 节点来参与区块生产。
  * 请注意，即使您的节点未进入前 27 名，使用`--witness`参数启动的节点仍会作为一个普通节点运行；一旦排名进入前 27 名，它就能立即开始出块。
* 将 SR 代表账户的**私钥**填写到 `config.conf` 的 `localwitness` 列表中。

以下是 `localwitness` 配置示例：

```json
localwitness = [
    650950B1...295BD812
]
```

然后执行以下命令来启动出块节点：

```shell
java -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c config.conf
```

> **注意：** 对于主网 SR 节点，请参考 [主网 FullNode 部署的 JVM 参数优化](#主网-fullnode-部署的-jvm-参数优化) 章节，获取适用于不同架构的完整 Java 启动命令。对于配备 64 GB 内存的服务器，建议将 JVM 堆大小设置为 `-Xms9G -Xmx24G`。

### 主从模式的出块全节点

为了提高出块全节点的可靠性，可以部署多个相同账户的出块全节点，形成主从模式。当一个具有出块权限的账户部署大于等于两个节点时（推荐数量：2个，主节点及从节点各1个），需要完善各节点配置文件中的`node.backup`。`node.backup`的配置项说明如下：

```ini
node.backup {
  # udp listen port, each member should have the same configuration
  port = 10001

  # my priority, each member should use different priority
  priority = 8

  # time interval to send keepAlive message, each member should have the same configuration unit: ms
  keepAliveInterval = 3000

  # peers‘ ip list, must not include myself
  members = [
    # "ip",
    # "ip"
  ]
}
```

比如，某个具有出块权限的账户部署了2个节点，两个节点的ip分别为192.168.0.100，192.168.0.101，那么他们的`node.backup`配置需如下所示：

* ip为192.168.0.100的配置
  
```ini
node.backup {
  port = 10001
  priority = 8
  keepAliveInterval = 3000
  members = [
    "192.168.0.101"
  ]
}
```

* ip为192.168.0.101的配置

```ini
node.backup {
  port = 10001
  priority = 7
  keepAliveInterval = 3000
  members = [
    "192.168.0.100"
  ]
}
```

**注意**：

* 节点只有同步到最新状态时才会启动备份服务，最新状态的定义为：（节点的系统时间 - 最新同步成功的区块时间） < 区块生产间隔（每个slot的时间，当前为3s）
* 当一个priority高的节点出现故障失去主节点的身份，别的从节点竞争获得主节点的位置，在该priority高的节点恢复正常、重新具备出块的条件时，其不会自动获得主节点的身份，需要等到当前的主节点发生故障之后才能重新竞争获得。
* 主从切换需要的时间：当主节点发生故障，从节点切换为主节点的时间最少需要2*keepAliveTimeout，其中keepAliveTimeout=keepAliveInterval * 6。需要2个keepAliveTimeout是因为从节点切换为主节点中间需要经过预备状态(INIT)的过渡，即从节点(SLAVER) -> 预备节点(INIT) -> 主节点(MASTER)。

## 优化与注意事项

### 加快节点数据同步

对于主网和 Nile 测试网，新节点启动后需要同步的数据量较大，将花费较长时间。您可以使用 [数据快照](https://tronprotocol.github.io/documentation-zh/using_javatron/backup_restore/#_5) 来加快节点同步速度。

操作步骤如下：

1. 下载最新的数据快照。
2. 将其解压至 `tron` 项目的 `output-directory` 目录下。
3. 启动节点，节点将在数据快照的基础上继续同步。

### 使用 Keystore + 密码指定超级代表账户私钥

为了避免以明文方式在配置文件中指定私钥，您可以选择使用 `keystore` 文件和密码的方式。

1. **配置步骤**:
    * 注释掉节点配置文件中的 `localwitness` 配置项。
    * 取消 `localwitnesskeystore` 配置项的注释，并填入 `keystore` 文件的路径。
    * 注意，`keystore` 文件需要放置在启动命令执行的当前目录或其子目录下。
        * 例如，如果当前目录是 `A`，`keystore` 文件的路径是 `A/B/localwitnesskeystore.json`，则配置应为：

        ```json
        localwitnesskeystore = ["B/localwitnesskeystore.json"]
        ```

    * 您可以使用 `wallet-cli` 项目的 `registerwallet` 命令生成 `keystore` 文件和密码。

1. **启动出块节点**:

    * **不使用 `nohup` 命令，人机交互的方式启动节点（推荐）**
        * **注意事项**: 此方式在启动节点时需要人机交互输入密码。建议使用会话保持工具，例如 `screen` 或 `tmux`。

        ```shell
        java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c config.conf
        ```

        * 在节点启动过程中，系统会提示您输入密码。正确输入密码后，节点将完成启动。

    * **使用 `nohup` 命令，直接在命令行中通过 `--password` 传入密码**

        ```shell
        nohup java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c config.conf --password "密码" > start.log 2>&1 &
        ```

### 使用 `tcmalloc` 优化内存占用

为达到内存使用的最优化，您可以使用 Google `tcmalloc` 替代系统 `glibc malloc`。

1. **安装 `tcmalloc`**:
    * **Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable**:

    ```shell
    sudo apt install libgoogle-perftools4
    ```

    * **Ubuntu 16.04 LTS**:

    ```shell
    sudo apt install libgoogle-perftools4
    ```

    * **CentOS 7**:

    ```shell
    sudo yum install gperftools-libs
    ```

2. **修改启动脚本**:

    * 在您的节点启动脚本中添加以下两行。请注意，不同 Linux 发行版上 `libtcmalloc.so.4` 的路径可能略有差异。

    ```bash
    #!/bin/bash

    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4" # 根据 您的系统调整路径
    export TCMALLOC_RELEASE_RATE=10

    # original start command
    java -jar .....
    ```

    * **Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable**:

    ```bash
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

    * **Ubuntu 16.04 LTS**:

    ```bash
    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

    * **CentOS 7**:

    ```bash
    export LD_PRELOAD="/usr/lib64/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```
  
