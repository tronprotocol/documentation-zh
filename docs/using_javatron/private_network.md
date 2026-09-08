# 私链网络

本文档将指导如何搭建一个基础的 TRON 私有网络。该网络将包含一个负责生成区块的超级代表节点和一个仅用于同步区块数据和广播交易的普通全节点。

## 前置要求

在开始之前，请确保您的开发环境满足以下条件：

- **Java Development Kit (JDK)**：x86_64 架构上，须安装 JDK 8（推荐最新的小版本）；arm64 架构上，须安装 JDK 17。 
- **TRON 账户**：您需要预先创建至少两个 TRON 网络地址，并安全地保存好地址和其对应的私钥。其中一个地址将作为初始见证节点（超级代表），另一个用于普通账户。
- **地址创建工具**：您可以使用以下任一工具来生成和管理您的 TRON 账户：
    - [wallet-cli](../clients/wallet-cli/index.md)：官方命令行钱包，适合在服务器环境中使用。提供交互式的 Java 版和面向脚本的 TypeScript 版。
    - [TronLink](https://www.tronlink.org/cn/)：一款支持 TRON 网络的多链钱包，提供友好的图形用户界面，方便创建和管理地址。
    - [TronWeb](https://tronweb.network/docu/docs/intro/)：一个便于开发者与 TRON 网络进行交互和构建 dApp 的 JavaScript 库。
    - [Trident](https://github.com/tronprotocol/trident)：一个轻量级的 Java SDK，旨在帮助开发者简单高效地将 TRON 区块链功能集成到 Java 应用中

## 部署指南

从操作流程上看，部署一个私有链节点与部署一个主网节点基本相同。不同点在于节点配置文件内容不同，搭建私链最主要的是要修改配置文件中的配置项，使节点间组成私链网络，可以进行网络发现，区块同步和广播交易。

1. 准备节点目录

    为保持配置和数据的隔离，建议为每个节点创建独立的部署目录。

      ```bash
      # 创建超级代表 (SR) 节点目录
      mkdir SR
      
      # 创建普通全节点目录
      mkdir FullNode
      ```

2. 获取 java-tron 客户端
    
     - 从 [java-tron GitHub Releases](https://github.com/tronprotocol/java-tron/releases) 页面下载适用于系统架构的最新 FullNode JAR：x86-64 使用 `FullNode-x64.jar`，ARM64 使用 `FullNode-aarch64.jar`，并将下载的文件重命名为 `FullNode.jar`。
    - 将下载的 `JAR` 文件分别复制到两个节点目录中。

     ```bash
     cp FullNode.jar ./SR
     cp FullNode.jar ./FullNode
     ```

3. 准备配置文件

    - 下载当前的 [`framework/src/main/resources/config.conf`](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf)。
    - 将 `node.p2p.version` 修改为未被公共网络使用的正整数。当前公共网络 ID 为：主网 `11111`、Nile `201910292`、Shasta `1`。
    - 将其分别复制到两个节点目录中，并重命名以作区分。

      ```bash
      # 用于 SR 节点的配置文件
      cp private_net_config.conf ./SR/supernode.conf
      
      # 用于普通全节点的配置文件
      cp private_net_config.conf ./FullNode/fullnode.conf
      ```

4. 修改节点配置
  
    这是搭建私有链最关键的一步。请根据下表说明，分别编辑 `supernode.conf` 和 `fullnode.conf` 文件。

    | 配置项名称 | SR 节点 (`supernode.conf`) | 全节点 (`fullnode.conf`) | 说明 |
    | :-------- | :-------- | :-------- | :-------- |
    | `localwitness`     | 账户私钥     | 不需填值     |  用于签名区块的私钥，仅产块节点需要。     |
    | `genesis.block.witnesses`	     | SR 地址     | 与 SR 配置值相同 | 创世块相关的配置   |
    | `genesis.block.assets`     | 给特定账户预置 TRX。将预先准备的账户地址写入并按需指定其 TRX 余额    | 与 SR 配置值相同     | 创世块相关的配置     |
    | `node.p2p.version`     | 除 `11111`、`201910292` 和 `1` 之外的任意正整数     | 与 SR 配置值相同      | 只有 `node.p2p.version` 相同的节点才能完成 P2P 握手     |
    | `seed.node.ip.list`     | 列表留空     | 按 `SR_IP:SR_P2P_PORT` 格式添加 SR 节点，其中端口使用 SR 的 `node.listen.port` 配置值    | 使 FullNode 与 SR 节点建立连接并同步数据     |
    | `block.needSyncCheck`     | `false`     | `true`     | 第 1 个 SR 将 `block.needSyncCheck` 设置为 `false`，其他 SR 设置为 `true`      |
    | `node.discovery.enable`     | `true`     | `true`     | 如果配置成 `false`，则当前节点不会被其他节点发现     |
    |`block.proposalExpireTime`|`600000` |与 SR 配置值相同  |默认提案过期时间是 3 天：259200000(ms)；由于逻辑上强制提案最少需要经历一个完整的维护期时间间隔，所以如果希望提案快速通过，需要将该项和维护期时间间隔项同时设置成小值|
    |`block.maintenanceTimeInterval`|`300000`| 与 SR 配置值相同  | 维护期时间间隔，默认是 6 小时：21600000(ms)|
    |`committee.allowSameTokenName` |`1`|`1`|如果配置为 `1` (true)，则允许相同的 token name|
    |`committee.allowTvmTransferTrc10` | `1`|`1`|如果配置为 `1` (true)，允许 TVM 通过智能合约转账 TRC-10 token |  

5. 调整网络端口 (如需)    
    修改配置文件中的端口号，将 SR 和 FullNode 的配置成不相同的端口号。此步骤仅在同一台机器上运行多个节点时是必需的，以避免端口冲突。否则，可跳过此步。
    
    * `node.listen.port`：P2P 监听端口
    * `node.http.fullNodePort`、`node.http.solidityPort` 和 `node.http.PBFTPort`：HTTP 监听端口
    * `node.rpc.port`、`node.rpc.solidityPort` 和 `node.rpc.PBFTPort`：gRPC 监听端口
    * `node.jsonrpc.httpFullNodePort`、`node.jsonrpc.httpSolidityPort` 和 `node.jsonrpc.httpPBFTPort`：启用相应服务时使用的 JSON-RPC 监听端口

    对应的启用开关和默认值请参阅[节点配置中的端口表](configuration.md#api-services-and-ports)。

6. 启动节点
    超级代表（产块节点）和普通全节点的启动命令略有不同。

    * 启动超级代表 (SR) 节点：

      ```bash
      cd SR
      java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c supernode.conf
      ```

    * 启动普通全节点：

      ```bash
      cd FullNode
      java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  -c fullnode.conf
      #启动后，请观察控制台日志，确保全节点能够成功连接到SR节点并开始同步区块。
      ```


7. 高级操作：修改网络参数
   
     网络参数可以通过 [getchainparameters](../api/http/witness-and-governance/getchainparameters.md) 接口获取。主网的当前网络参数及相关提案可在 TRONSCAN [参数&提案页面](https://tronscan.org/#/sr/committee) 查看。若希望私链的网络参数与主网保持一致，可使用 [DBFork](https://github.com/tronprotocol/tron-docker/blob/main/tools/toolkit/DBFork.md) 工具，它可以捕获主网的最新状态。
  
     私有链启动后，您可能需要调整某些网络参数（例如手续费，能量单价等），这可以通过两种方式实现：

     * **方式一：通过配置文件设置 (适用于初始部署)**  

        一些网络参数可以通过配置文件直接设置，当前定义可在 [`Constant.java`](https://github.com/tronprotocol/java-tron/blob/master/common/src/main/java/org/tron/core/Constant.java) 中查看。
      
         **示例**：在 `.conf` 文件中添加以下 `committee` 块来开启多签和合约创建:
      
         ```properties
         committee = {
           allowCreationOfContracts = 1
           allowAdaptiveEnergy = 0
           allowMultiSign = 1
           allowDelegateResource = 1
           allowSameTokenName = 0
           allowTvmTransferTrc10 = 1
         }
         ```

       * **方式二：通过链上提案修改 (适用于运行中的网络)**
        
        这是链上治理的标准方式。任何超级代表（SR）、超级代表合伙人（SR Partner）或超级代表候选人（SR Candidate）都可以创建提案或对提案表示赞成，但只有当前活跃 SR 的赞成才计入提案通过阈值。

         - 创建提案：SR 使用 [proposalcreate](../api/http/witness-and-governance/proposalcreate.md) API，通过参数序号指定要修改的参数及其新值（参数序号列表)。
         - 赞成提案：SR 使用 [proposalapprove](../api/http/witness-and-governance/proposalapprove.md) API 赞成提案或取消赞成。判断提案是否达到通过阈值时，只统计当前活跃 SR 的有效赞成；未赞成或已取消赞成不会增加赞成数量。
         - 相关接口：
              - 获取所有提案：[listproposals](../api/http/witness-and-governance/listproposals.md)
              - 根据 ID 获取提案：[getproposalbyid](../api/http/witness-and-governance/getproposalbyid.md)
 
 
         **示例代码 (使用 TronWeb)：**

         以下代码片段演示了如何创建一个提案来修改两个网络参数，并对其进行投票。在 [proposalcreate](../api/http/witness-and-governance/proposalcreate.md) 中，网络参数用序号表示，序号和名称之间的映射定义在 java-tron 源码的 [`enum ProposalType`](https://github.com/tronprotocol/java-tron/blob/master/actuator/src/main/java/org/tron/core/utils/ProposalUtil.java) 中（枚举项括号内即为参数序号）。

         ```javascript
         var TronWeb = require('tronweb');
         var tronWeb = new TronWeb({
             fullHost: 'http://localhost:8090',
             privateKey: 'privateKey'
         })

         var parametersForProposal1 = [{"key":9,"value":1},{"key":10,"value":1}];

         async function modifyChainParameters(parameters,proposalID){
      
             parameters.sort((a, b) => {
                     return a.key.toString() > b.key.toString() ? 1 : a.key.toString() === b.   key.toString() ? 0 : -1;
                 })
             var unsignedProposal1Txn = await tronWeb.transactionBuilder.createProposal (parameters,"41D0B69631440F0A494BB51F7EEE68FF5C593C00F0")
             var signedProposal1Txn = await tronWeb.trx.sign(unsignedProposal1Txn);
             var receipt1 = await tronWeb.trx.sendRawTransaction(signedProposal1Txn);

             setTimeout(async function() {
                 console.log(receipt1)
                 console.log("Vote proposal 1 !")
                 var unsignedVoteP1Txn = await tronWeb.transactionBuilder.voteProposal (proposalID, true, tronWeb.defaultAddress.hex)
                 var signedVoteP1Txn = await tronWeb.trx.sign(unsignedVoteP1Txn);
                 var rtn1 = await tronWeb.trx.sendRawTransaction(signedVoteP1Txn);
             }, 4000)

         }

         modifyChainParameters(parametersForProposal1, 1) 
         ```
      
      提案投票通过并在维护期结束后，新的网络参数将会生效。您可以通过 [listproposals](../api/http/witness-and-governance/listproposals.md) 或 [getchainparameters](../api/http/witness-and-governance/getchainparameters.md) 来验证变更。
  
      需要注意的是，具有相互依赖关系的网络参数不能包含在同一个提案中，正确的方法是将它们分成不同的提案，并注意它们的顺序。例如，应先激活 `ALLOW_TVM_SHANGHAI`，再发起启用 95 号参数（`ALLOW_TVM_PRAGUE`）的提案。
     
     
