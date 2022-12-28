# Java-tron新版本部署手册
对于强制升级的版本，请严格按照本指南进行新版本的部署。对于非强制升级的版本，可根据需求自行选择是否部署。

请参考[新版本部署步骤](#_1)进行升级，如果您部署了主备节点，请按照[主备节点部署指南](#_2)的流程进行升级。


## 新版本部署步骤
您的 FullNode,  产块的 FullNode 均需按照该本说明升级到最新版本，步骤如下：

### 1.准备新版本可执行文件

您可以直接下载Java-tron可执行文件，也可以下载最新版本的代码，然后编译，以获取新版本可执行文件。请在Java-tron运行目录以外的其它文件目录下，下载最新版本的代码或者jar包：

* 方式一：下载已发布的可执行文件
    
    在release页面 [https://github.com/tronprotocol/java-tron/releases](https://github.com/tronprotocol/java-tron/releases) 直接下载最新版本的FullNode.jar可执行文件。
    
    在使用之前，请首先对文件签名进行校验，以确保该JAR文件的一致性和完整性，校验步骤请参考[Java-tron一致性校验](https://tronprotocol.github.io/documentation-zh/releases/)。
    
    
* 方式二：编译源码
    
    下载对应版本源码，并切换到新版本的分支。
    ```
    $ git clone https://github.com/tronprotocol/java-tron.git
    $ git checkout -b relase_vx.x.x
    ```
    
    编译程序：在新版本代码目录，执行如下命令进行编译，编译完成的可执行文件生成在`build/libs` 目录中。
    ```
    $ ./gradlew clean build -x test
    ```
    

### 2.关闭Java-tron进程

* 首先通过如下命令获取节点进程ID
    ```
    $ ps -ef | grep java
    ```
    
* 停止节点进程
    ```
    $ kill -15 获取的进程id
    ```


### 3.备份
请依次备份升级前的可执行文件、数据库、配置文件。备份数据用于当升级中遇到问题导致新版本部署不成功时，可以恢复到老版本。

* 备份当前的可执行文件
    ```
    $ mv $JAVA_TRON.jar $JAVA_TRON.jar.`date "+%Y%m%d%H%M%S"`
    ```
* 备份当前数据库output-directory
    ```
    $ tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
    ```
* 备份当前配置文件
    ```
    $ mv $config.conf $config.conf.`date "+%Y%m%d%H%M%S"`
    ```


### 4.替换旧文件
准备好新版本可执行文件，并备份好原节点数据后，请根据如下步骤替换旧文件：

1. 将上步骤获取的最新版本jar包拷贝到Java-tron工作目录，以替换旧的可执行文件。
2. 用最新的配置文件覆盖旧的配置文件，如需修改配置，比如添加keystore file、私钥等，请自行修改。

注意：对于数据库文件，可以使用Java-tron工作目录下的原有数据库文件，也可以选择使用[数据库备份快照](https://tronprotocol.github.io/documentation-zh/using_javatron/backup_restore/#_4)。


### 5.启动节点
超级代表的产块的全节点和其它普通的全节点，启动命令不同，请根据实际情况选择启动命令：

* 对于超级代表的产块的全节点，启动命令为：
    ```
    nohup java -Xmx24g -XX:+UseConcMarkSweepGC  -jar FullNode.jar  -p  private key --witness -c main_net_config.conf </dev/null &>/dev/null &
    ```
    注意：私钥的设置不一定要使用如上命令行参数的方式，如果使用keystore file方式或者在配置文件中配置私钥的方式，请按照原先的方式设置即可。

* 对于普通的全节点，启动命令为：
    ```
    nohup java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c   main_net_config.conf </dev/null &>/dev/null &
    ```
             
### 6. 等待节点同步完成
节点成功启动后，请耐心等待节点区块同步。
### 7. 新版本部署完成
节点同步到网络最新区块后，才表示该节点本次新版本部署完成。

当升级中遇到任何问题，导致新版本部署不成功，请使用第三步中备份的数据，恢复到老版本，并及时在Github或社区中反馈，以尽快帮助您完成新版本的部署。


## 主备节点升级指南
主备节点的升级，请按照如下步骤进行：

1. 升级备份节点

    请按照[新版本部署步骤](#_1)先对备份节点进行升级。

2. 停止主节点

    备份节点成功升级部署了新版本后，请等待备份节点同步完成后，再关停主节点，这时备份节点会自动接替主节点，成为active node。

3. 升级主节点

    如果备份节点正常工作，则按照[新版本部署步骤](#_1)升级主节点。否则，关停备份节点，并启动主节点。如果出现错误，请联系TRON的技术人员，发送备份节点的日志以分析原因。

4. 关停备份节点

    等待主节点升级并同步完成后，再关停备份节点。备份节点关闭后，主节点将重新接手成为active node。

5. 开启备份节点












