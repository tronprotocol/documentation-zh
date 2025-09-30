# 私链网络

本文档将指导如何搭建一个基础的 TRON 私有网络。该网络将包含一个负责生成区块的超级代表节点和一个仅用于同步区块数据和广播交易的普通全节点。

## 前置要求
在开始之前，请确保您的开发环境满足以下条件：

- Java Development Kit (JDK)：您的环境必须安装 Oracle JDK 1.8。 
- TRON 账户：您需要预先创建至少两个 TRON 网络地址，并安全地保存好地址和其对应的私钥。其中一个地址将作为初始见证节点（超级代表），另一个用于普通账户。
- 地址创建工具：您可以使用以下任一工具来生成和管理您的 TRON 账户：
    - [Wallet-cli](https://github.com/tronprotocol/wallet-cli)：一个官方提供的命令行钱包工具，适合在服务器环境中使用。
    - [TronLink](https://www.tronlink.org/cn/)：一款支持TRON网络的多链钱包，提供友好的图形用户界面，方便创建和管理地址。
    - [TronWeb](https://tronweb.network/docu/docs/intro/)：一个便于开发者与TRON网络进行交互和构建dApp的JavaScript库。
    - [Trident](https://github.com/tronprotocol/trident)：一个轻量级的 Java SDK，旨在帮助开发者简单高效地将 TRON 区块链功能集成到 Java 应用中

## 部署指南
从操作流程上看，部署一个私有链节点与部署一个主网节点基本相同。不同点在于节点配置文件内容不同，搭建私链最主要的是要修改配置文件中的配置项，使节点间组成私链网络，可以进行网络发现，区块同步和广播交易。

1. 准备节点目录

    为保持配置和数据的隔离，建议为每个节点创建独立的部署目录。
      ```
      # 创建超级代表 (SR) 节点目录
      $ mkdir SR
      
      # 创建普通全节点目录
      $ mkdir FullNode
      ```

2. 获取 `java-tron` 客户端

    `java-tron` 是 TRON 网络的官方 Java 实现。
    
     - 从 [Java-tron GitHub Releases](https://github.com/tronprotocol/java-tron/releases) 页面下载最新的 `FullNode.jar`。
    - 将下载的 `JAR` 文件分别复制到两个节点目录中。
     ```
     $ cp FullNode.jar ./SR
     $ cp FullNode.jar ./FullNode
     ```

3. 准备配置文件

    - 下载官方提供的配置文件模板 ([config.conf](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/resources/config.conf))，并修改`p2p.version`为**11111**和**20180622**以外的任何值。
    - 将其分别复制到两个节点目录中，并重命名以作区分。
      ```
      # 用于SR节点的配置文件
      $ cp private_net_config.conf ./SR/supernode.conf
      
      # 用于普通全节点的配置文件
      $ cp private_net_config.conf ./FullNode/fullnode.conf
      ```

4. 修改节点配置
  
    这是搭建私有链最关键的一步。请根据下表说明，分别编辑 `supernode.conf` 和 `fullnode.conf` 文件。

    | 配置项名称 | SR 节点 (`supernode.conf`) | 全节点 (`fullnode.conf`) | 说明 |
    | :-------- | :-------- | :-------- | :-------- |
    | `localwitness`     | 账户私钥     | 不需填值     |  用于签名区块的私钥，仅产块节点需要。     |
    | `genesis.block.witnesses`	     | SR 地址     | 与 SR 配置值相同 | 创世块相关的配置，`genesis.block` 需要与 SR 节点的一样    |
    | `genesis.block.Assets`     | 给特定账户预置 TRX。将预先准备的账户地址写入并随意指定其 TRX 的余额。可以直接修改原来已有账户的 `address` 字段，其它字段不需要修改；或者在末尾添加新账户信息    | 与 SR 配置值相同     | 创世块相关的配置     |
    | `p2p.version`     | 11111 之外的任意正整数     | 与 SR 配置值相同      | SR 和 Fullnode 需相同，只有相同 version 的节点才能握手成功     |
    | `seed.node`     | 不需填值     | 将 `ip.list` 设置为 SR 的 IP 地址和 SR 配置文件中的 `listen.port` 端口号    | 能够让 Fullnode 与 SR node 建立连接并同步数据     |
    | `needSyncCheck`     | `false`     | `true`     | 第 1 个 SR 设置 `needSyncCheck` 为 `false`，其他设置为 `true`      |
    | `node.discovery.enable`     | `true`     | `true`     | 如果配置成 `false`，则当前节点不会被其他节点发现     |
    |`block.proposalExpireTime`|`600000` |与 SR 配置值相同  |默认提议生效时间是 3 天：259200000(ms)，如需快速通过提议，可将该项设置为更小的值，如 10 分钟，即 600000ms|
    |`block.maintenanceTimeInterval`|`300000`| 与 SR 配置值相同  | 维护期时间间隔，默认是 6 小时：21600000(ms)；如需快速通过提议，可将该项设置为更小的值，如 5 分钟，即 300000ms。|
    |`committee.allowSameTokenName` |`1`|`1`|允许相同的 token name|
    |`committee.allowTvmTransferTrc10` | `1`|`1`|允许智能合约转账 TRC-10 代币|  

5. 调整网络端口 (如需)    
    修改配置文件中的端口号，将 SR 和 FullNode 的配置成不相同的端口号。此步骤仅在同一台机器上运行多个节点时是必需的，以避免端口冲突。否则，可跳过此步。
    
    * `listen.port` ：P2P 监听端口
    * `http` 端口： HTTP 监听端口
    * `rpc` 端口： RPC 监听端口

6. 启动节点
    超级代表（产块节点）和普通全节点的启动命令略有不同。

    * 启动超级代表 (SR) 节点：
      ```
      $ cd SR
      $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c supernode.conf
      ```
    * 启动普通全节点：
      ```
      $ cd FullNode
      $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  -c fullnode.conf
      #启动后，请观察控制台日志，确保全节点能够成功连接到SR节点并开始同步区块。
      ```


7. 高级操作：修改动态网络参数
   
     动态网络参数可以通过 [getchainparameters](https://developers.tron.network/reference/wallet-getchainparameters) 接口获取。主网的当前动态参数及相关提案可在 TRONSCAN [参数&提议页面](https://tronscan.org/#/sr/committee) 查看。若希望私链的动态参数与主网保持一致，可使用 [DBFork](https://github.com/tronprotocol/tron-docker/blob/main/tools/toolkit/DBFork.md) 工具，它可以捕获主网的最新状态。
   
  
     私有链启动后，您可能需要调整某些网络参数（例如手续费，能量单价等），这可以通过两种方式实现：

     * **方式一：通过配置文件设置 (适用于初始部署)**  

        一些动态参数可以通过配置文件直接设置，这些动态参数可以在 [此处](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/core/Constant.java) 查看。
      
         **示例**：在 `.conf` 文件中添加以下 `committee` 块来开启多签和合约创建。 
      
         ```
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
        这是链上治理的标准方式，任何 Witness (SR、SR partner、SR candidate) 都有权创建提案，但只有超级代表（SR）有权投票批准。

         - 创建提案：Witness 使用 [proposalcreate API](https://developers.tron.network/reference/proposalcreate)，通过参数序号指定要修改的参数及其新值（参数序号列表)。
         - 批准提案：Witness 使用 [proposalapprove API](https://developers.tron.network/reference/proposalapprove)对提案进行投票(仅支持投赞成票，SR不投票意味着不同意该提案)。
         - 相关接口：
              - 获取所有提议：[listproposals](https://developers.tron.network/reference/wallet-listproposals)
              - 根据 ID 获取提议：[getproposalbyid](https://developers.tron.network/reference/getproposalbyid)
 
 
         **示例代码 (使用 TronWeb)：**

         以下代码片段演示了如何创建一个提案来修改两个网络参数，并对其进行投票。在 [proposalcreate](https://developers.tron.network/reference/proposalcreate) 中，动态参数用序号表示，动态参数的序号和名称之间的映射可以在 [此处](https://developers.tron.network/reference/wallet-getchainparameters) 查看。

         ```
         var TronWeb = require('tronweb');
         var tronWeb = new TronWeb({
             fullHost: 'http://localhost:16887',
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
      
      提案投票通过并在维护期结束后，新的网络参数将会生效。您可以通过 [listproposals](https://developers.tron.network/reference/wallet-listproposals) 或 [getchainparameters](https://developers.tron.network/reference/wallet-getchainparameters) 来验证变更。
  
      需要注意的是，具有相互依赖关系的动态参数不能包含在同一个提案中，正确的方法是将它们分成不同的提案，并注意它们的顺序。
     
     

