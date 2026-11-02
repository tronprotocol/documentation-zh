# java-tron 节点升级指南

本指南详细介绍了如何安全地将您的 java-tron 节点部署至最新版本。

对于**强制升级**的版本，请严格遵循本指南完成部署。对于**非强制升级**的版本，您可以根据实际需求选择是否升级。

* 对于**标准节点**，请参考 [标准节点升级流程](#standard-node-upgrade-process)。
* 对于配置了**主备高可用**的节点，请遵循 [主备节点升级指南](#primary-backup-upgrade) 以确保服务的平稳过渡。

## 标准节点升级流程 { #standard-node-upgrade-process }


所有全节点（FullNode），包括超级代表（Super Representative）的出块节点，都应遵循以下步骤完成升级。

### 第 1 步：准备新版本程序包 { #prepare-the-new-version-package }

您可以选择直接下载编译好的 java-tron 可执行文件，也可下载新版本的源代码并自行编译，以获取新版本可执行文件。请在 java-tron 当前运行目录之外的其它路径下执行以下操作。

#### 方式一：下载可执行文件 (推荐)

1.  访问 [java-tron GitHub Releases](https://github.com/tronprotocol/java-tron/releases) 页面，根据系统架构下载最新的可执行文件：x86-64 使用 `FullNode-x64.jar`，ARM64 使用 `FullNode-aarch64.jar`。完成签名校验后，将下载的文件重命名为 `FullNode.jar`，供后续步骤使用。
2.  **安全校验**：为确保文件的完整性和安全性，请务必根据 [java-tron 一致性校验](signature_verification.md) 文档对下载的 JAR 文件进行签名校验。

#### 方式二：从源码编译

1.  克隆 `java-tron` 仓库并切换到目标版本的分支。

    ```bash
    # 克隆仓库
    git clone https://github.com/tronprotocol/java-tron.git

    # 切换到指定版本分支
    cd java-tron
    git checkout -b release_vx.x.x
    ```

2.  执行编译命令。编译成功后，新的可执行文件 `FullNode.jar` 将生成在 `build/libs/` 目录下。

    ```bash
    ./gradlew clean build -x test
    ```

### 第 2 步：停止运行中的节点

> **注意**：如果这是您首次部署节点，请直接跳至 [第 5 步：启动节点](#start-the-node)。

1.  使用以下命令查找 java-tron 进程的 `PID`。

    ```bash
    ps -ef | grep java
    ```

2.  停止节点进程。

    ```bash
    kill -15 <进程ID>
    ```

### 第 3 步：备份关键数据 { #back-up-critical-data }

建议您在升级前进行一次完整备份。请按指定顺序执行以下备份步骤：请务必依次备份可执行文件、数据库和配置文件。

1. **备份当前的可执行文件**

    ```bash
    mv $JAVA_TRON.jar $JAVA_TRON.jar.`date "+%Y%m%d%H%M%S"`
    ```

2. **备份当前数据库 `output-directory`**

    ```bash
    tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
    ```

3. **备份当前配置文件**

    ```bash
    mv $config.conf $config.conf.`date "+%Y%m%d%H%M%S"`
    ```

这样可以确保在升级失败或遇到任何问题时，您能利用备份迅速回滚至上一版本。

### 第 4 步：替换旧文件 { #step-4-replace-old-files }

准备好新版本可执行文件，并备份好原节点数据后，请根据以下步骤替换旧文件：

1.  将 [第 1 步](#prepare-the-new-version-package) 中获取的新版本 `FullNode.jar` 拷贝到 java-tron 的工作目录。
2. 检查并更新配置文件。除非版本发布要求修改，否则更新配置文件是可选的。您可以采用以下任一方式：

    - **从模板开始，合并自定义配置（推荐）。** 使用相同网络的 `config.conf` 模板替换配置文件，然后将备份配置中受支持的自定义设置合并到该文件中。
    - **更新现有配置文件。** 将备份配置文件复制回原路径，再根据配置差异和版本发布说明添加或调整配置项。

        例如，如果备份文件名为 `config.conf.20261021153000`，可以使用以下命令恢复一份副本：

        ```bash
        cp config.conf.20261021153000 config.conf
        ```

        请将示例中的备份文件名替换为实际文件名。编辑恢复后的 `config.conf`，并保留备份文件不变。

    无论采用哪种方式，都应阅读版本发布说明，并将自己的配置与当前的 `config.conf`（`framework/src/main/resources/config.conf`）和 `reference.conf`（`common/src/main/resources/reference.conf`）进行比较。`reference.conf` 提供回退默认值，并记录受支持的参数，包括仅以注释示例形式出现的可选配置项。`config.conf` 是部署模板，包含常用配置项和用于部署的配置覆盖值。

> **关于数据库**：您通常可以直接使用 java-tron 工作目录下原有的数据库文件，也可考虑使用预先构建的 [数据库快照](../using_javatron/backup_restore.md)。

### 第 5 步：启动节点 { #start-the-node }

#### 超级代表节点 (出块节点)

对于出块节点，请参考[启动出块节点](../using_javatron/installing_javatron.md#starting-a-block-production-node)

#### 普通全节点

对于普通全节点，请参考[启动全节点连接主网](../using_javatron/installing_javatron.md#starting-a-fullnode-on-the-tron-main-network)



### 第 6 步：验证与监控

1.  **等待节点同步**：节点启动后，将开始同步区块数据。请耐心等待其追赶至网络最新区块高度。
2.  **检查日志**：观察日志输出，确保节点正常运行且没有错误信息。
3.  **确认同步状态**：您需要通过对比本地节点和 TRON 主网的最新区块高度来验证同步是否完成。当两者高度基本一致时，即代表节点升级成功。
    - 查询本地节点区块高度：可调用 `/wallet/getnowblock` API:

        ```bash
        curl http://127.0.0.1:8090/wallet/getnowblock
        ```

    - 查询主网区块高度：可实时访问 [区块链浏览器 TRONSCAN](https://tronscan.org) 查看。

**应急预案**：如果在升级过程中遇到任何导致节点无法启动或运行异常的问题，请立即使用 [第 3 步](#back-up-critical-data) 中备份的数据恢复至旧版本，并及时提交 Github Issue 或反馈至 TRON 社区以寻求帮助。

-----

## 主备节点升级指南 { #primary-backup-upgrade }

为确保服务的高可用性，主备节点的升级应采用滚动升级（Rolling Upgrade）策略。

1.  **升级备用节点 (Backup Node)** 
      * 首先，在**备用节点**上完整执行上述 [标准节点升级流程](#standard-node-upgrade-process) 中的所有步骤。
2.  **执行切换**
      * 确认备用节点已成功升级并完成区块同步后，停止**主节点 (Master Node)** 的进程。
      * 此时，备用节点将自动接管，成为新的主节点（Active Node），对外提供服务。
3.  **升级原主节点**
      * 在确认新的主节点（原备用节点）稳定运行后，对原主节点执行 [标准节点升级流程](#standard-node-upgrade-process) 进行升级。
      * **异常处理**：如果在此期间，新的主节点出现故障，应立即停止对其的升级操作，并重新启动原主节点以恢复服务。同时，请保存故障节点的完整日志，以供问题排查。以便进行问题排查。如需进一步支持，请携带相关日志在 Github 提交 Issue 或通过社区反馈。
4.  **恢复主备架构**
      * 等待原主节点升级、启动并同步完成后，停止当前提供服务的节点（原备用节点）。
      * 原主节点将自动重新接管，恢复其 Active Node 的角色。
5.  **重启备用节点**
      * 最后，重新启动已完成升级的备用节点，使其恢复 Backup 状态，至此整个主备升级流程完成。
