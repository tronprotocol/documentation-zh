
# 什么是wallet-cli？
wallet-cli是一个支持TRON网络的交互式命令行钱包，用于在安全的本地环境中签名和广播交易，也可以获取链上数据。wallet-cli支持密钥管理，您可以将私钥导入钱包中，wallet-cli会使用对称加密算法加密您的私钥，并存储到一个keystore文件中。wallet-cli本地不存储链上数据，它采用gRPC的方式与某一个java-tron节点进行通信，您需要在配置文件中配置需要链接的java-tron节点，下图是使用wallet-cli签名和广播TRX转账交易的流程：
![](https://i.imgur.com/NRKmZmE.png)

用户首先运行`Login`命令解锁钱包，然后运行`SendCoin`命令发送TRX，wallet-cli会本地构建和签名交易，然后将调用java-tron节点的BroadcastTransaction gRPC API将交易广播的网络中，广播成功后java-tron节点会返回交易hash给wallet-cli，wallet-cli将交易hash展示给用户。

安装和运行: [wallet-cli](https://github.com/tronprotocol/wallet-cli)


