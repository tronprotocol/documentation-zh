## Tron网络结构 
Tron网络采用Peer-to-Peer(P2P)的网络架构，网络中的节点地位对等。网络中的节点有SuperNode、FullNode、SolidityNode三种类型，SuperNode主要用于生成区块，FullNode用于同步区块、广播交易，SolidityNode用于同步固化的区块。任何部署运行Tron代码的设备都可以加入Tron网络并作为一个节点，和Tron网络中的其他节点有相同的地位，他们可以创建交易，广播交易，同步区块等，也可以作为SuperNode的候选人参与选举。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/network.png)

<h3> SuperNode介绍 </h3>
[超级代表](https://github.com/tronprotocol/Documentation/blob/master/中文文档/波场区块链浏览器介绍/什么是超级代表.md)(简称SR) 是TRON网络上的记账人，一共27个，负责对网络上广播出来的交易数据进行验证，并将交易打包进区块中，他们是轮流的方式打包区块。超级代表的信息是在TRON网络上公开的，所有人都可以获取这些信息，最便捷的方式是在TRON的[区块链浏览器](https://tronscan.org/#/sr/representatives)查看超级代表列表及其信息。

最低配置要求：  
CPU：16核 内存：32G 带宽：100M 硬盘：1T  
推荐配置要求：  
CPU：64核及以上 内存：64G及以上 带宽：500M及以上 硬盘：20T及以上  

<h3> FullNode介绍  </h3>
FullNode是拥有完整区块链数据的节点，能够实时更新数据，负责交易的广播和验证，提供操作区块链的api和查询数据的api。

最低配置要求：  
CPU：16核 内存：32G 带宽：100M 硬盘：1T  
推荐配置要求：  
CPU：64核及以上 内存：64G及以上 带宽：500M及以上 硬盘：20T及以上

<h3> SolidityNode介绍 </h3>
SolidityNode是只从自己信任的FullNode同步固化块的节点，并提供区块、交易查询等服务。

最低配置要求：  
CPU：16核 内存：32G 带宽：100M 硬盘：1T   
推荐配置要求：  
CPU：64核及以上 内存：64G及以上 带宽：500M及以上 硬盘：20T及以上

## 主网、测试网、私有网络 
加入主网或测试网或私有网络的节点在部署时运行的是同一份代码，区别仅仅在于节点启动时加载的配置文件不同。

<h3> 1. 主网 </h3>
[主网配置文件](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf)

<h3> 2. 测试网 </h3>
[测试网配置文件](https://github.com/tronprotocol/tron-deployment/blob/master/test_net_config.conf)

<h3> 3. 搭建私有网络 </h3>

<h4> 3.1 前提 </h4>

1.&nbsp;具备至少两个钱包账户的私钥与地址；[如何生成钱包账户](https://tronscan.org/#/wallet/new)    
2.&nbsp;至少部署一个SuperNode用于出块；     
3.&nbsp;部署任意数量的FullNode节点用于同步区块、广播交易；        
4.&nbsp;SuperNode与FullNode组成了私有网络，可以进行网络发现、区块同步、广播交易；    


<h4> 3.2 部署 </h4>

<h5> 3.2.1 步骤一:部署超级节点 </h5>
1.&nbsp;下载private_net_config.conf  

```text
wget https://raw.githubusercontent.com/tronprotocol/tron-deployment/master/private_net_config.conf
```
2.&nbsp;在localwitness中添加自己的私钥   
3.&nbsp;设置genesis.block.witnesses为私钥对应的地址   
4.&nbsp;设置p2p.version为除了11111之外的任意正整数   
5.&nbsp;第1个SR设置needSyncCheck为false，其他可以设置为true   
6.&nbsp;设置node.discovery.enable为true   
7.&nbsp;运行部署脚本    

```text
nohup java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c private_net_config.conf

命令行参数说明:
--witness: 启动witness功能，i.e.: --witness
--log-config: 指定日志配置文件路径，i.e.: --log-config logback.xml
-c: 指定配置文件路径，i.e.: -c config.conf
```
日志文件使用：
可以修改模块的level等级来控制日志的输出，默认每个模块的level级别为INFO，比如，只打印网络模块warn以上级别的信息，可以如下修改：  

```text
<logger name="net" level="WARN"/>
```

配置文件中需要修改的参数：  

localwitness:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/localwitness.jpg)
witnesses:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/witness.png) 
version:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/p2p_version.png)  
enable:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/discovery_enable.png)  

<h5> 3.2.2 步骤二:部署FullNode节点    </h5>

1.&nbsp;下载private_net_config.conf   
```text
wget https://raw.githubusercontent.com/tronprotocol/tron-deployment/master/private_net_config.conf
```
2.&nbsp;设置seed.node ip.list 为SR的ip地址和端口   
3.&nbsp;设置p2p.version与超级节点的p2p.version一致   
4.&nbsp;设置genesis.block 与SR中的genesis.block配置一致(包括Assets和Witness)    
5.&nbsp;设置needSyncCheck为true     
6.&nbsp;设置node.discovery.enable 为true     
7.&nbsp;如果FullNode和SR部署在同一台机器上，则需要修改listen.port、http端口、rpc 端口     
8.&nbsp;运行部署脚本
 
```text
nohup java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar -c private_net_config.conf
命令行参数说明:
--log-config: 指定日志配置文件路径，i.e.: --log-config logback.xml。
-c: 指定配置文件路径，i.e.: -c config.conf。
```
日志文件使用：
可以修改模块的level等级来控制日志的输出，默认每个模块的level级别为INFO，比如，只打印网络模块warn以上级别的信息，可以如下修改：

```text
<logger name="net" level="WARN"/>
```

配置文件中需要修改的参数：     

ip.list:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/ip_list.png)
p2p.version:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/p2p_version.png)
genesis.block:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/genesis_block.png)
needSyncCheck:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/need_sync_check.png)
node.discovery.enable:  
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/discovery_enable.png)



