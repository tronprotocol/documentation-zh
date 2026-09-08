# 快速上手

本页介绍首次运行流程：构建 wallet-cli、创建并解锁账户、查看账户信息，以及发送第一笔 TRX。所有操作
都在交互式提示符中完成。

## 构建并发送第一笔交易

```console
# 1. 构建
$ git clone https://github.com/tronprotocol/wallet-cli.git
$ cd wallet-cli/java && ./gradlew build && cd build/libs

# 2. 启动交互式钱包
$ java -jar wallet-cli.jar

# 3. 在钱包提示符下：创建账户（或使用 ImportWallet）、解锁并查看
> RegisterWallet             # 先两次提示输入密码，再询问助记词长度
> Login                      # 解锁账户
> GetAddress                 # 显示你的地址
> GetBalance                 # TRX 余额

# 4. 发送 1 TRX（金额以 SUN 计；1 TRX = 1,000,000 SUN）
> SendCoin <toAddress> 1000000
```

> 在主网上执行这些命令会使用**真实资产**。学习阶段请用 `SwitchNetwork` 切换到测试网（Nile 或
> Shasta），并从该网络的水龙头领取测试币。

## 如何创建账户

你可以通过向不存在的账户转账来创建账户，也可以用 **CreateAccount** 命令发起一笔交易来创建账户。
两种方式都会燃烧一笔账户激活费并消耗带宽；这两项都由链参数决定、可经治理提案修改，并不是固定数额
——具体规则见 [commands/account](../commands/account.md#how-to-create-account)。

完整的 `CreateAccount` 示例见 [commands/account](../commands/account.md)。

## 下一步

- [command-flow](command-flow.md)——一次完整的端到端会话
- [commands/wallet](../commands/wallet.md)——创建 / 导入 / 备份钱包
- [commands/network](../commands/network.md)——切换到测试网
- [concepts/resources](../concepts/resources.md)——带宽与能量
