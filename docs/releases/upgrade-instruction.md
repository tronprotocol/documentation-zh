# java-tron 节点升级指南

本指南详细介绍了如何安全地将您的 java-tron 节点部署至最新版本。

对于**强制升级**的版本，请严格遵循本指南完成部署。对于**非强制升级**的版本，您可以根据实际需求选择是否升级。

  * 对于**标准节点**，请参考 [标准节点升级流程](#standard_process)。
  * 对于配置了**主备高可用**的节点，请遵循 [主备节点升级指南](#primary/backup_upgrade) 以确保服务的平稳过渡。

<a id="standard_process"></a> 
## 标准节点升级流程

所有全节点（FullNode），包括超级代表（Super Representative）的出块节点，都应遵循以下步骤完成升级。

<a id="step1"></a> 
### 第 1 步：准备新版本程序包

您可以选择直接下载编译好的 java-tron 可执行文件，也可下载新版本的源代码并自行编译，以获取新版本可执行文件。请在 java-tron 当前运行目录之外的其它路径下执行以下操作。

#### 方式一：下载可执行文件 (推荐)

1.  访问 [java-tron GitHub Releases](https://github.com/tronprotocol/java-tron/releases) 页面，下载最新版本的 `FullNode.jar` 可执行文件。
2.  **安全校验**：为确保文件的完整性和安全性，请务必根据 [java-tron 一致性校验](https://tronprotocol.github.io/documentation-zh/releases/signature_verification/) 文档对下载的 JAR 文件进行签名校验。

#### 方式二：从源码编译

1.  克隆 `java-tron` 仓库并切换到目标版本的分支。
    ```
    # 克隆仓库
    $ git clone https://github.com/tronprotocol/java-tron.git

    # 切换到指定版本分支
    $ cd java-tron
    $ git checkout -b release_vx.x.x
    ```
2.  执行编译命令。编译成功后，新的可执行文件 `FullNode.jar` 将生成在 `build/libs/` 目录下。
    ```
    $ ./gradlew clean build -x test
    ```

### 第 2 步：停止运行中的节点

> **注意**：如果这是您首次部署节点，请直接跳至 [第 5 步：启动节点](#step5)。

1.  使用以下命令查找 java-tron 进程的 `PID`。
    ```
    $ ps -ef | grep java
    ```
2.  停止节点进程。
    ```
    $ kill -15 <进程ID>
    ```
<a id="step3"></a> 
### 第 3 步：备份关键数据

建议您在升级前进行一次完整备份。请按指定顺序执行以下备份步骤：请务必依次备份可执行文件、数据库和配置文件。

1. **备份当前的可执行文件**
    ```
    $ mv $JAVA_TRON.jar $JAVA_TRON.jar.`date "+%Y%m%d%H%M%S"`
    ```
2. **备份当前数据库 `output-directory`**
    ```
    $ tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
    ```
3. **备份当前配置文件**
    ```
    $ mv $config.conf $config.conf.`date "+%Y%m%d%H%M%S"`
    ```
这样可以确保在升级失败或遇到任何问题时，您能利用备份迅速回滚至上一版本。

### 第 4 步：替换旧文件

准备好新版本可执行文件，并备份好原节点数据后，请根据以下步骤替换旧文件：

1.  将 [第 1 步](#step1) 中获取的新版本 `FullNode.jar` 拷贝到 java-tron 的工作目录。
2. 更新配置文件 (可选)
    - 建议使用新版本的配置文件替换现有文件。替换后，请将您之前的自定义设置（例如，私钥、`keystore` 路径）合并到新文件中。
    - **配置更新策略**
        - 此步骤并非强制性的。 您可以根据自己节点的实际情况和需求，来决定是否更新配置文件。不过，我们仍强烈建议您使用最新的配置文件，以确保节点完全兼容并支持所有新功能。
        - 如果某一版本要求必须更新配置文件，我们会在其版本发布说明 (Release Notes) 中进行明确说明。请务必在升级前仔细阅读相关的发布说明。

> **关于数据库**：您通常可以直接使用 java-tron 工作目录下原有的数据库文件，也可考虑使用预先构建的 [数据库快照](https://tronprotocol.github.io/documentation-zh/using_javatron/backup_restore)。

<a id="step5"></a> 
### 第 5 步：启动节点

请根据节点类型及 CPU 架构选择下方对应的启动命令作为参考。命令中各参数的说明请参见 [节点部署](https://tronprotocol.github.io/documentation-zh/using_javatron/installing_javatron/#_2) 章节，具体参数值请根据实际运行环境进行调整。

#### 超级代表节点 (出块节点)
 * **x86_64 架构（仅支持 JDK 8）**
```bash
nohup java -Xms9G -Xmx24G -XX:ReservedCodeCacheSize=256m \
    -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
    -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
    -XX:+PrintGCDateStamps  -Xloggc:gc.log \
    -XX:+UseConcMarkSweepGC -XX:NewRatio=3 \
    -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
    -jar ./build/libs/FullNode.jar --witness -c config.conf &
```

* **ARM64 架构（仅支持 JDK 17）**
```bash
nohup java -Xms9G -Xmx24G -XX:+UseZGC \
    -Xlog:gc,gc+heap:file=gc.log:time,tags,level:filecount=10,filesize=100M \
    -XX:ReservedCodeCacheSize=256m \
    -XX:+UseCodeCacheFlushing \
    -XX:MetaspaceSize=256m \
    -XX:MaxMetaspaceSize=512m \
    -XX:MaxDirectMemorySize=1g \
    -XX:+HeapDumpOnOutOfMemoryError \
    -jar ./build/libs/FullNode.jar --witness -c config.conf &
```
> *注意*：推荐使用 `keystore` 文件或在配置文件中管理私钥，而不是直接在命令行中作为参数传入。

#### 普通全节点
 * **x86_64 架构（仅支持 JDK 8）**
```bash
nohup java -Xms9G -Xmx12G -XX:ReservedCodeCacheSize=256m \
             -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
             -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
             -XX:+PrintGCDateStamps  -Xloggc:gc.log \
             -XX:+UseConcMarkSweepGC -XX:NewRatio=3 \
             -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
             -XX:+HeapDumpOnOutOfMemoryError \
             -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
             -jar ./build/libs/FullNode.jar -c main_net_config.conf &
```
* **ARM64 架构（仅支持 JDK 17）**
```bash
nohup java -Xmx9G -XX:+UseZGC \
             -Xlog:gc,gc+heap:file=gc.log:time,tags,level:filecount=10,filesize=100M \
             -XX:ReservedCodeCacheSize=256m \
             -XX:+UseCodeCacheFlushing \
             -XX:MetaspaceSize=256m \
             -XX:MaxMetaspaceSize=512m \
             -XX:MaxDirectMemorySize=1g \
             -XX:+HeapDumpOnOutOfMemoryError \
             -jar ./build/libs/FullNode.jar -c main_net_config.conf &
```



### 第 6 步：验证与监控

1.  **等待节点同步**：节点启动后，将开始同步区块数据。请耐心等待其追赶至网络最新区块高度。
2.  **检查日志**：观察日志输出，确保节点正常运行且没有错误信息。
3.  **确认同步状态**：您需要通过对比本地节点和 TRON 主网的最新区块高度来验证同步是否完成。当两者高度基本一致时，即代表节点升级成功。
    - 查询本地节点区块高度：可调用 `/wallet/getnowblock` API:
        ```
        curl http://127.0.0.1:8090/wallet/getnowblock
        ```
    - 查询主网区块高度：可实时访问 [区块链浏览器 TRONSCAN](https://tronscan.org) 查看。

**应急预案**：如果在升级过程中遇到任何导致节点无法启动或运行异常的问题，请立即使用 [第 3 步](#step3) 中备份的数据恢复至旧版本，并及时提交 Github Issue 或反馈至 TRON 社区以寻求帮助。

-----
<a id="primary/backup_upgrade"></a> 
## 主备节点升级指南

为确保服务的高可用性，主备节点的升级应采用滚动升级（Rolling Upgrade）策略。

1.  **升级备用节点 (Backup Node)** 
      * 首先，在**备用节点**上完整执行上述 [标准节点升级流程](#standard_process) 中的所有步骤。
2.  **执行切换**
      * 确认备用节点已成功升级并完成区块同步后，停止**主节点 (Master Node)** 的进程。
      * 此时，备用节点将自动接管，成为新的主节点（Active Node），对外提供服务。
3.  **升级原主节点**
      * 在确认新的主节点（原备用节点）稳定运行后，对原主节点执行 [标准节点升级流程](#standard_process) 进行升级。
      * **异常处理**：如果在此期间，新的主节点出现故障，应立即停止对其的升级操作，并重新启动原主节点以恢复服务。同时，请保存故障节点的完整日志，以供问题排查。以便进行问题排查。如需进一步支持，请携带相关日志在 Github 提交 Issue 或通过社区反馈。
4.  **恢复主备架构**
      * 等待原主节点升级、启动并同步完成后，停止当前提供服务的节点（原备用节点）。
      * 原主节点将自动重新接管，恢复其 Active Node 的角色。
5.  **重启备用节点**
      * 最后，重新启动已完成升级的备用节点，使其恢复 Backup 状态，至此整个主备升级流程完成。
