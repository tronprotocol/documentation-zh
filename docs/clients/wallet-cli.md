
# 什么是Wallet-Cli？
Wallet-Cli是一个支持TRON网络的交互式命令行钱包，用于在安全的本地环境中签名和广播交易，也可以获取链上数据。Wallet-Cli支持密钥创建和管理，您可以将私钥导入钱包中，Wallet-Cli会使用对称加密算法加密您的私钥，并存储到一个keystore文件中。Wallet-Cli本地不存储链上数据，它采用gRPC的方式与某一个Java-tron节点进行通信，您需要在配置文件中配置需要链接的Java-tron节点，下图是使用Wallet-Cli签名和广播TRX转账交易的流程：
![](https://i.imgur.com/NRKmZmE.png)

用户首先运行`Login`命令解锁钱包，然后运行`SendCoin`命令发送TRX，Wallet-Cli会本地构建和签名交易，然后将调用Java-tron节点的BroadcastTransaction gRPC API将交易广播的网络中，广播成功后Java-tron节点会返回交易hash给Wallet-Cli，Wallet-Cli将交易hash展示给用户。

安装和运行: [Wallet-Cli](https://github.com/tronprotocol/wallet-cli)


