## 前提

分别为fullnode和soliditynode创建一个目录  

```text
/deploy/fullnode
/deploy/soliditynode
```

克隆最新的master分支上的代码[https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) 到  

```text      
/deploy/java-tron 
```

请确保已经安装恰当的依赖环境。  

* JDK 1.8 (JDK 1.9+ is not supported yet)
* On Linux Ubuntu system (e.g. Ubuntu 16.04.4 LTS), ensure that the machine has [__Oracle JDK 8__](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04), instead of having __Open JDK 8__ in the system. If you are building the source code by using __Open JDK 8__, you will get [__Build Failed__](https://github.com/tronprotocol/java-tron/issues/337) result.
* Open **UDP** ports for connection to the network
* **MINIMUM** 2 CPU Cores


## 部署指南

1.&nbsp;编译java-tron项目   
```text
cd /deploy/java-tron 
./gradlew build
```

2.&nbsp;复制FullNode.jar和SolidityNode.jar以及相应的配置文件到各自的目录    
```text
download your needed configuration file from https://github.com/tronprotocol/TronDeployment.  

main_net_config.conf is the configuration for MainNet, and test_net_config.conf is the configuration for TestNet.  

please rename the configuration file to `config.conf` and use this config.conf to start FullNode and SoliditNode.  

cp build/libs/FullNode.jar ../fullnode  

cp build/libs/SolidityNode.jar ../soliditynode
```

3.&nbsp;用以下命令运行FullNode     
```text
java -jar FullNode.jar -c config.conf // make sure that your config.conf is downloaded from https://github.com/tronprotocol/TronDeployment
```

4.&nbsp;配置SolidityNode配置文件       

需要编辑`config.conf`文件来连接本地的FullNode。修改`node`里的`trustNode`为`127.0.0.1:50051`，这是默认rpc端口。设置`listen.port`为1024-65535间任意数字。不要使用0-1024间的数字，因为可能会导致与系统服务冲突。同样，为了避免冲突，可以把`rpc port`改为`50052`。  

**请为FullNode转发UDP端口18888**

```text
rpc {
      port = 50052
    }
```

5.&nbsp;用以下命令运行SolidityNode   
```text        
java -jar SolidityNode.jar -c config.conf //make sure that your config.conf is downloaded from https://github.com/tronprotocol/TronDeployment
```

6.&nbsp;在公链环境中运行超级节点   
```text
java -jar FullNode.jar -p your private key --witness -c your config.conf(Example：/data/java-tron/config.conf)
Example:
java -jar FullNode.jar -p 650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812 --witness -c /data/java-tron/config.conf
```

这与运行一个个人测试网相似，除了`config.conf`中的IP不一样。  

7.&nbsp;在个人测试网环境中运行超级节点   

你需要修改一下config.conf配置文件内容：    

- Replace existing entry in genesis.block.witnesses with your address
- Replace existing entry in seed.node ip.list with your ip list
- The first Super Node start, needSyncCheck should be set false
- Set p2p version to 61 

```text
cd build/libs
java -jar FullNode.jar -p your private key --witness -c your config.conf (Example：/data/java-tron/config.conf)
Example:
java -jar FullNode.jar -p 650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812 --witness -c /data/java-tron/config.conf
```


## 日志与网络连接验证  

日志位于`/deploy/\*/logs/tron.log`。 使用`tail -f /logs/tron.log/`命令来查看块同步日志。  

你可以看到类似如下块同步的日志信息：  

**FullNode**
```text
12:00:57.658 INFO  [pool-7-thread-1] [o.t.c.n.n.NodeImpl](NodeImpl.java:830) Success handle block Num:236610,ID:0000000000039c427569efa27cc2493c1fff243cc1515aa6665c617c45d2e1bf
```
**SolidityNode**
```text
12:00:40.691 INFO  [pool-17-thread-1] [o.t.p.SolidityNode](SolidityNode.java:88) sync solidity block, lastSolidityBlockNum:209671, remoteLastSolidityBlockNum:211823
```
## 优雅的停止节点

Create file stop.sh，use kill -15 to close java-tron.jar（or FullNode.jar、SolidityNode.jar）.
You need to modify pid=`ps -ef |grep java-tron.jar |grep -v grep |awk '{print $2}'` to find the correct pid.
```text
#!/bin/bash
while true; do
  pid=`ps -ef |grep java-tron.jar |grep -v grep |awk '{print $2}'`
  if [ -n "$pid" ]; then
    kill -15 $pid
    echo "The java-tron process is exiting, it may take some time, forcing the exit may cause damage to the database, please wait patiently..."
    sleep 1
  else
    echo "java-tron killed successfully!"
    break
  fi
done
```

## 快速部署节点

Download fast deployment script, run the script according to different types of node.   

<h3>使用范围</h3>

This script could be used on Linux/MacOS, but not on Windows.
Just Support FullNode and SolidityNode.

<h3>下载运行脚本</h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
```

<h3>参数含义</h3>

```shell
bash deploy_tron.sh --app [FullNode|SolidityNode] --net [mainnet|testnet|privatenet] --db [keep|remove|backup] --heap-size <heapsize>

--app Optional, Running application. The default node is Fullnode and it could be FullNode or SolidityNode.
--net Optional, Connecting network. The default network is mainnet and it could be mainnet, testnet.
--db  Optional, The way of data processing could be keep, remove and backup. Default is keep. If you launch two different networks, like from mainnet to testnet or from testnet to mainnet, you need to delete database.
--trust-node  Optional, It only works when deploying SolidityNode. Default is 127.0.0.1:50051. The specified gRPC service of Fullnode, like 127.0.0.1:50051 or 13.125.249.129:50051.
--rpc-port  Optional, Port of grpc. Default is 50051. If you deploy SolidityNode and FullNode on the same host，you need to configure different ports.
--commit  Optional, commitid of project.
--branch  Optional, branch of project.  Mainnet default is latest release and Testnet default is master.
--heap-size  Optional, jvm option: Xmx. The default heap-size is 0.8 * memory size.
--work_space  Optional, default is current directory.
```

<h3> Deployment of FullNode on the one host </h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
bash deploy_tron.sh
```

<h3> Deployment of SolidityNode on the one host </h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
# User can self-configure the IP and Port of GRPC service in the turst-node field of SolidityNode. trust-node is the fullnode you just deploy.
bash deploy_tron.sh --app SolidityNode --trust-node <grpc-ip:grpc-port>
```

<h3> Deployment of FullNode and SolidityNode on the same host </h3>

```shell
# You need to configure different gRPC ports on the same host because gRPC port is available on SolidityNode and FullNodeConfigure and it cannot be set as default value 50051. In this case the default value of rpc port is set as 50041.
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
bash deploy_tron.sh --app FullNode
bash deploy_tron.sh --app SolidityNode --rpc-port 50041
```

## Grpc Gateway部署

<h3> 摘要 </h3>

This script helps you download the code from https://github.com/tronprotocol/grpc-gateway and deploy the code on your environment.

<h3> 前提 </h3>

Please follow the guide on https://github.com/tronprotocol/grpc-gateway 
Install Golang, Protoc, and set $GOPATH environment variable according to your requirement.

<h3> 下载运行脚本 </h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_grpc_gateway.sh -O deploy_grpc_gateway.sh
```

<h3> 参数含义 </h3>

```shell
bash deploy_grpc_gateway.sh --rpchost [rpc host ip] --rpcport [rpc port number] --httpport [http port number] 

--rpchost The fullnode or soliditynode IP where the grpc service is provided. Default value is "localhost".
--rpcport The fullnode or soliditynode port number grpc service is consuming. Default value is 50051.
--httpport The port intends to provide http service provided by grpc gateway. Default value is 18890.
```

<h3> 示例 </h3>

使用默认配置：
```shell
bash deploy_grpc_gateway.sh
```
使用自定义配置：
```shell
bash deploy_grpc_gateway.sh --rpchost 127.0.0.1 --rpcport 50052 --httpport 18891
```

## 高级配置  

Read the [Advanced Configuration](../advanced-configuration.md)
