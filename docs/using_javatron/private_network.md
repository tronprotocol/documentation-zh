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
    | `genesis.block.assets`     | 给特定账户预置 TRX。将预先准备的账户地址写入，并以 SUN 为单位指定余额（`1 TRX = 1,000,000 SUN`；例如，`100000000` 表示分配 100 TRX）    | 与 SR 配置值相同     | 创世块相关的配置     |
    | `node.p2p.version`     | 除 `11111`、`201910292` 和 `1` 之外的任意正整数     | 与 SR 配置值相同      | 只有 `node.p2p.version` 相同的节点才能完成 P2P 握手     |
    | `seed.node.ip.list`     | 列表留空     | 按 `SR_IP:SR_P2P_PORT` 格式添加 SR 节点，其中端口使用 SR 的 `node.listen.port` 配置值    | 使 FullNode 与 SR 节点建立连接并同步数据     |
    | `node.fastForward` | 列表留空 | 列表留空 | 删除模板中预设的 fast-forward 地址。如需中继节点，请仅使用私有网络中的中继节点。 |
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
   
     网络参数可以通过 [getchainparameters](../api/http/witness-and-governance/getchainparameters.md) 接口获取。主网的当前网络参数及相关提案可在 TRONSCAN [参数&提案页面](https://tronscan.org/#/sr/committee) 查看。

     如需使用自己的 SR 账户，基于已有主网状态部署私有网络，请先获取数据库快照，或将节点同步到所需高度。然后使用 [DBFork 工具](https://github.com/tronprotocol/tron-docker/blob/main/tools/toolkit/DBFork.md) 修改本地数据库。默认情况下（即未使用 `--retain-witnesses` 时），工具会根据 `fork.conf` 中的 `witnesses` 配置，替换 `witness` 库中的见证人记录和 `witness_schedule` 库中的活跃见证人列表。工具还会根据 `accounts` 配置处理 `account` 库中的账户：地址不存在时新增账户，已存在时修改指定字段。仅配置 `witnesses` 不会自动创建对应账户，因此，数据库中尚不存在的 SR 地址还需加入 `accounts` 配置。启动 SR 节点后，这些账户即可参与出块。
  
     私有链启动后，您可能需要调整某些网络参数（例如手续费，能量单价等），这可以通过两种方式实现：

     * **方式一：通过配置文件设置 (适用于初始部署)**  

        一些网络参数可以通过配置文件直接设置。可用的配置项及其默认值请参阅 [`reference.conf`](https://github.com/tronprotocol/java-tron/blob/master/common/src/main/resources/reference.conf)。
      
         **示例**：将以下配置项添加到 `.conf` 文件已有的 `committee` 块中，以开启多签和合约创建：
      
         ```properties
         committee = {
           allowCreationOfContracts = 1
           allowMultiSign = 1
         }
         ```

       * **方式二：通过链上提案修改 (适用于运行中的网络)**
        
        这是链上治理的标准方式。任何超级代表（SR）、超级代表合伙人（SR Partner）或超级代表候选人（SR Candidate）都可以创建提案或对提案表示赞成，但只有当前活跃 SR 的赞成才计入提案通过阈值。

         - 创建提案：使用 [proposalcreate](../api/http/witness-and-governance/proposalcreate.md) API，通过参数序号指定要修改的参数及其新值。参数序号请参阅下文链接的 `ProposalType` 映射。
         - 赞成提案：使用 [proposalapprove](../api/http/witness-and-governance/proposalapprove.md) API 赞成提案或取消赞成。判断提案是否达到通过阈值时，只统计当前活跃 SR 的有效赞成；未赞成或已取消赞成不会增加赞成数量。
         - 相关接口：
              - 获取所有提案：[listproposals](../api/http/witness-and-governance/listproposals.md)
              - 根据 ID 获取提案：[getproposalbyid](../api/http/witness-and-governance/getproposalbyid.md)
 
 
         **示例代码 (使用 TronWeb)：**

         以下代码片段演示了如何创建一个提案来修改两个网络参数，并对其进行投票。在 [proposalcreate](../api/http/witness-and-governance/proposalcreate.md) 中，网络参数用序号表示，序号和名称之间的映射定义在 java-tron 源码的 [`enum ProposalType`](https://github.com/tronprotocol/java-tron/blob/master/actuator/src/main/java/org/tron/core/utils/ProposalUtil.java) 中（枚举项括号内即为参数序号）。

         本示例使用 [TronWeb v6](https://tronweb.network/docu/docs/intro/#instantiation)。将环境变量 `SR_PRIVATE_KEY` 设置为创世 SR 账户的私钥，该账户已注册为见证人，并确保它有足够的余额或带宽来执行交易。本示例假设账户使用默认权限，且该账户不会同时提交其他提案。代码会等待交易在 FullNode 上成功入块，然后根据提案发起者和参数查找新提案，而不是预先假定提案 ID。

         ```javascript
         const { TronWeb } = require('tronweb');
         const tronWeb = new TronWeb({
             fullHost: 'http://localhost:8090',
             privateKey: process.env.SR_PRIVATE_KEY
         });
         const owner = tronWeb.defaultAddress.hex;
         const parameters = [{ key: 9, value: 1 }, { key: 10, value: 1 }];
         // 按 key 的字符串顺序排序，以与 Protobuf map 的序列化顺序一致。
         parameters.sort((a, b) => {
             const keyA = String(a.key);
             const keyB = String(b.key);
             return keyA < keyB ? -1 : keyA > keyB ? 1 : 0;
         });
         const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

         async function broadcastAndWait(unsignedTransaction) {
             const signed = await tronWeb.trx.sign(unsignedTransaction);
             const result = await tronWeb.trx.sendRawTransaction(signed);
             if (!result.result) {
                 throw new Error(`Broadcast failed: ${JSON.stringify(result)}`);
             }
             const deadline = Date.now() + 120000;
             while (Date.now() < deadline) {
                 const info = await tronWeb.fullNode.request(
                     'wallet/gettransactioninfobyid', { value: signed.txID }, 'post'
                 );
                 if (info.id === signed.txID && info.blockNumber !== undefined) {
                     // SUCESS 是 Protobuf 中的枚举名称；返回结果可能省略这一默认值。
                     const status = info.result ?? 'SUCESS';
                     if (status !== 'SUCESS') {
                         throw new Error(`Transaction ${signed.txID} failed: ${status}`);
                     }
                     return signed.txID;
                 }
                 await sleep(1000);
             }
             throw new Error(`Timed out waiting for ${signed.txID}; check it before retrying.`);
         }

         async function modifyChainParameters() {
             const previousIds = new Set(
                 (await tronWeb.trx.listProposals()).map((p) => p.proposal_id)
             );
             const createTxId = await broadcastAndWait(
                 await tronWeb.transactionBuilder.createProposal(parameters, owner)
             );
             const matches = (await tronWeb.trx.listProposals()).filter((p) =>
                 !previousIds.has(p.proposal_id) &&
                 p.proposer_address.toLowerCase() === owner.toLowerCase() &&
                 p.parameters.length === parameters.length &&
                 parameters.every((expected) => p.parameters.some((actual) =>
                     Number(actual.key) === expected.key && Number(actual.value) === expected.value
                 ))
             );
             if (matches.length !== 1) {
                 throw new Error(`Cannot uniquely identify the proposal from ${createTxId}; inspect listproposals.`);
             }
             const proposalID = matches[0].proposal_id;
             const voteTxId = await broadcastAndWait(
                 await tronWeb.transactionBuilder.voteProposal(proposalID, true, owner)
             );
             console.log({ proposalID, createTxId, voteTxId });
         }

         modifyChainParameters().catch((error) => {
             console.error(error);
             process.exitCode = 1;
         });
         ```
      
         赞成提案不会立即使参数生效。到达维护期时，java-tron 会根据当时活跃 SR 的赞成情况处理已到期的提案，仅在提案通过时，参数才会生效。您可以通过 [listproposals](../api/http/witness-and-governance/listproposals.md) 查看提案状态，并通过 [getchainparameters](../api/http/witness-and-governance/getchainparameters.md) 验证当前网络参数的值。

         **仅有一个 SR 的私有网络：** 当前 [`ProposalCapsule.hasMostApprovals`](https://github.com/tronprotocol/java-tron/blob/master/chainbase/src/main/java/org/tron/core/capsule/ProposalCapsule.java) 的实现使用整数运算：`approvalCount >= activeWitnessCount * 7 / 10`。只有一个活跃 SR 时，阈值为零，因此待处理的提案在到期时即使没有任何赞成票，也能通过。
  
      需要注意的是，具有相互依赖关系的网络参数不能包含在同一个提案中，正确的方法是将它们分成不同的提案，并注意它们的顺序。例如，应先激活 `ALLOW_TVM_SHANGHAI`，再发起启用 95 号参数（`ALLOW_TVM_PRAGUE`）的提案。
     
     
