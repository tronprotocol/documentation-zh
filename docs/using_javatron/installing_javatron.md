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

### 编译 java-tron 源码

在开始编译之前，请确保您的系统已安装 `git` 工具。

1. 首先，通过 `git` 命令将 java-tron 源代码克隆到本地，并切换到 `master` 分支：

```shell
git clone https://github.com/tronprotocol/java-tron.git
git checkout -t origin/master
```

2. 然后，执行以下命令编译 java-tron 源代码：

```shell
cd java-tron
./gradlew clean build -x test
```

* 参数 `-x test` 表示跳过执行测试用例。您也可以去除此参数以在编译过程中执行测试代码，但这会延长编译时间。
* 编译完成后，`FullNode.jar` 文件将生成在 `java-tron/build/libs/` 目录下。

## 启动 java-tron 节点

您可以选择不同的配置文件将 java-tron 节点连接到不同的 TRON 网络:

* 主网全节点配置文件：[config.conf](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf)
* 其他网络节点配置文件：

  * Nile 测试网：https://nileex.io/
  * 私链网络：请参考[私链网络](https://tronprotocol.github.io/documentation-zh/using_javatron/private_network/)

### 启动全节点 (FullNode)

**全节点** (FullNode) 作为 TRON 网络的入口点，拥有完整的历史数据，并提供对外访问的 HTTP API、 gRPC API 和 JSON-RPC API。您可以通过全节点与 TRON 网络进行交互，例如资产转移、智能合约部署、智能合约交互等。

以下是启动**主网全节点**的命令，通过 `-c` 参数指定配置文件：

```shell
java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c config.conf
```

* `-XX:+UseConcMarkSweepGC`: 指定并发标记-清除 (CMS) 垃圾回收器。此参数必须放在 `-jar` 参数之前。
* `-Xmx`: 设置 Java 虚拟机 (JVM) 堆的最大值，通常建议设置为物理内存的 80%。
* 要启动 **Nile 测试网全节点** 或**私链全节点**，请使用本节开头部分列出的相应配置文件链接。

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
java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c config.conf
```

### 主从模式的出块全节点

为了提高出块全节点的可靠性，可以部署多个相同账户的出块全节点，形成主从模式。当一个具有出块权限的账户部署大于等于两个节点时，需要完善各节点配置文件中的`node.backup`。`node.backup`的配置项说明如下：

```ini
node.backup {
  # udp listen port, each member should have the same configuration
  port = 10001

  # my priority, each member should use different priority
  priority = 8

  # time interval to send keepAlive message, each member should have the same configuration unit: ms
  keepAliveInterval = 3000

  # peer's ip list, can't contain myself
  members = [
    # "ip",
    # "ip"
  ]
}
```

比如，某个具有出块权限的账户部署了3个节点，三个节点的ip分别为192.168.0.100，192.168.0.101，192.168.0.102，那么他们的`node.backup`配置需如下所示：

* ip为192.168.0.100的配置
  
```ini
node.backup {
  port = 10001
  priority = 8
  keepAliveInterval = 3000
  members = [
    "192.168.0.101",
    "192.168.0.102"
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
    "192.168.0.100",
    "192.168.0.102"
  ]
}
```

* ip为192.168.0.102的配置

```ini
node.backup {
  port = 10001
  priority = 6
  keepAliveInterval = 3000
  members = [
    "192.168.0.100",
    "192.168.0.101"
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
  
