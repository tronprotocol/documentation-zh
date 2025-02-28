# 私链网络

搭建私链需要部署至少一个产块的全节点，和任意数量的非产块的全节点用于同步区块和广播交易，本示例中只搭建了一个产块的节点和一个非产块的节点。搭建私链之前，请先安装`Oracle JDK 1.8`， 然后需要准备至少两个TRON网络地址并保存地址和对应的私钥，可以使用[wallet-cli](https://github.com/tronprotocol/wallet-cli)或者[Tronlink](https://www.tronlink.org/cn/)来创建地址。


# 部署指南
搭建私链节点的流程和搭建主网节点的流程一样，不同点在于节点配置文件内容不同，搭建私链最主要的是要修改配置文件中的配置项，使节点间组成私链网络，可以进行网络发现，区块同步和广播交易。

1. 创建目录

    创建部署目录，建议将两个节点放在不同的目录下。
      ```
      $ mkdir SR
      $ mkdir FullNode
      ```

2. 获取[FullNode.jar](https://github.com/tronprotocol/java-tron/releases)

    获取 FullNode.jar，将其分别放到SR和FullNode目录中。
     ```
     $ cp FullNode.jar ./SR
     $ cp FullNode.jar ./FullNode
     ```

3. 获取节点配置文件[private_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/private_net_config.conf)，

    获取节点配置文件 private_net_config.conf，将其分别放到SR和FullNode目录中,并分别修改文件名为：supernode.conf、 fullnode.conf。
      ```
      $ cp private_net_config.conf ./SR/supernode.conf
      $ cp private_net_config.conf ./FullNode/fullnode.conf
      ```

4. 修改各节点的配置文件
  
    请根据如下表格中的说明，依次修改节点的各个配置项：

    | 配置项名称 | SR Fullnode配置内容 | FullNode配置内容 | 说明 |
    | :-------- | :-------- | :-------- | :-------- |
    | localwitness     | witness账户私钥     | 不需填值     | 生成区块需要使用私钥签名     |
    | genesis.block.witnesses	     | 上面私钥对应的地址     | 与SR配置值相同 | 创世块相关的配置，genesis.block需要与SR节点的一样    |
    | genesis.block.Assets     | 给特定账户预置TRX。将预先准备的账户地址写入并随意指定其TRX的余额。可以直接修改原来已有账户的address字段，其它字段不需要修改；或者在末尾添加新账户信息    | 与SR配置值相同     | 创世块相关的配置     |
    | p2p.version     | 11111之外的任意正整数     | 与SR配置值相同      | SR 和fullnode需相同，只有相同version的节点才能握手成功     |
    | seed.node     | 不需填值     | 将ip.list设置为SR的ip地址和SR配置文件中的`listen.port`端口号    | 能够让fullnode与SR node建立连接并同步数据     |
    | needSyncCheck     | false     | true     | 第1个SR设置needSyncCheck为false，其他设置为true      |
    | node.discovery.enable     | true     | true     | 如果配置成false，则当前节点不会被其他节点发现     |
    |block.proposalExpireTime|600000 |与SR配置值相同  |默认提议生效时间是3天：259200000(ms)，如需快速通过提议，可将该项设置为更小的值，如10分钟，即600000ms|
    |block.maintenanceTimeInterval|300000| 与SR配置值相同  | 维护期时间间隔，默认是6小时: 21600000(ms),如需快速通过提议，可将该项设置为更小的值，如五分钟，即300000ms。|
    |committee.allowSameTokenName |1|1|允许相同的token name|
    |committee.allowTvmTransferTrc10 | 1|1|允许智能合约转账TRC10代币|

    

5. 修改配置文件中的端口号，将SR和FullNode的配置成不相同的端口号。注意，如果SR和FullNode运行在一台机器上，此步骤是必须的，否则，可跳过此步。
    * `listen.port` ： p2p的监听端口
    * `http`端口： Http监听端口
    * `rpc` 端口： rpc 监听端口
6. 启动节点

    产块的全节点和非产块的全节点，启动命令不同：

    * 产块的全节点
      ```
      $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c supernode.conf
      ```
    * 非产块的全节点
      ```
      $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  -c fullnode.conf
      ```


7. 修改网络动态参数

    动态参数可以通过[getchainparameters](https://developers.tron.network/reference/wallet-getchainparameters)获取。主网络的当前动态参数和与之相关的提案可以在[这里](https://tronscan.org/#/sr/committee)查看，动态参数在这里被称为网络参数。

    如果您希望私链的动态参数与主网保持一致，也许[dbfork](https://github.com/tronprotocol/tron-docker/tree/main/tools/dbfork)是您更感兴趣的，它可以捕获主网最新状态。
    
    如果要修改部分动态参数，有两种方法可供选择：

    * 配置文件  
      一些动态参数可以通过配置文件直接设置，这些动态参数可以在[此处](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/core/Constant.java)查看。下面是一个通过配置文件修改动态参数的示例。
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
    * 提案  
      任何witness(SR、SR partner、SR candidate)都有权创建提案，但是只有SR有权对提案进行投票。witness使用[proposalcreate](https://developers.tron.network/reference/proposalcreate)创建提案，之后SR使用[proposalapprove](https://developers.tron.network/reference/proposalapprove)批准提案(仅支持投赞成票，SR不投票意味着不同意该提案)。下面是一个通过提案修改两个动态参数的代码示例。在[proposalcreate](https://developers.tron.network/reference/proposalcreate)中，动态参数用序号表示，动态参数的序号和名称之间的映射可以在[此处](https://developers.tron.network/reference/wallet-getchainparameters)查看。
      ```
      var TronWeb = require('tronweb');
      var tronWeb = new TronWeb({
          fullHost: 'http://localhost:16887',
          privateKey: 'c741f5c0224020d7ccaf4617a33cc099ac13240f150cf35f496db5bfc7d220dc'
      })

      var parametersForProposal1 = [{"key":9,"value":1},{"key":10,"value":1}];

      async function modifyChainParameters(parameters,proposalID){
      
          parameters.sort((a, b) => {
                  return a.key.toString() > b.key.toString() ? 1 : a.key.toString() === b.key.toString() ? 0 : -1;
              })
          var unsignedProposal1Txn = await tronWeb.transactionBuilder.createProposal(parameters,"41D0B69631440F0A494BB51F7EEE68FF5C593C00F0")
          var signedProposal1Txn = await tronWeb.trx.sign(unsignedProposal1Txn);
          var receipt1 = await tronWeb.trx.sendRawTransaction(signedProposal1Txn);

          setTimeout(async function() {
              console.log(receipt1)
              console.log("Vote proposal 1 !")
              var unsignedVoteP1Txn = await tronWeb.transactionBuilder.voteProposal(proposalID, true, tronWeb.defaultAddress.hex)
              var signedVoteP1Txn = await tronWeb.trx.sign(unsignedVoteP1Txn);
              var rtn1 = await tronWeb.trx.sendRawTransaction(signedVoteP1Txn);
          }, 1000)

      }

      modifyChainParameters(parametersForProposal1, 1)
      ```
      通过上述代码创建提案后，您可以通过[listproposals](https://developers.tron.network/reference/wallet-listproposals)检查提案是否已获批准。当创建的提案过期后，如果上述接口返回值中的“state”为“APPROVED”，表示提案已获批准。  
      需要注意的是，具有相互依赖关系的动态参数不能包含在同一个提案中，正确的方法是将它们分成不同的提案，并注意它们的顺序。
