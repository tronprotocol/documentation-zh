# wallet-cli

`wallet-cli` 是 TRON 网络的命令行钱包，官方仓库为
[tronprotocol/wallet-cli](https://github.com/tronprotocol/wallet-cli)。它在本地管理密钥和账户，
并连接 TRON 服务，用于查询链上数据以及构建、签名和广播交易。

仓库提供两种实现：

- **[Java CLI](java-cli.md)** —— 原始的全功能实现。它既提供面向用户的交互式 REPL，也提供供脚本
  调用 Java JAR 的非交互式标准 CLI。
- **[TypeScript / npm CLI](typescript-cli.md)** —— 面向智能体优先设计的 Node.js 实现，以
  `@tron-walletcli/wallet-cli` 发布，采用分组命令、确定的退出码和结构化 JSON 输出。

## 入口对比

两个界面都可以查询账户数据。Java CLI 接受任意地址，而 TypeScript CLI 操作的是本地钱包中已经
保存的账户：

=== "Java 标准 CLI"

    ```bash
    java -jar java/build/libs/wallet-cli.jar --network nile get-account --address TXyz...
    ```

=== "Java 交互模式"

    ```
    GetAccount TXyz...
    ```

=== "TypeScript / npm CLI"

    ```bash
    wallet-cli account info --network tron:nile
    ```

    该命令使用活动账户。可以通过 `--account` 传入本地钱包中已有的账户 ID、标签或地址，选择其他
    已保存的账户。

## 选择实现

| 实现 | 命令风格 | 适用场景 |
|------|----------|----------|
| [Java CLI](java-cli.md) | `GetAccount` 等交互式命令，或 `get-account` 等标准 CLI 命令 | 完整的 TRON 钱包功能、手动操作以及 Java JAR 集成 |
| [TypeScript / npm CLI](typescript-cli.md) | `account info`、`tx send` 等分组命令 | 自动化、CI/CD、结构化 JSON 集成以及 AI 智能体 |

两种实现有各自独立的安装与运行要求。请继续阅读 [Java CLI 概览](java-cli.md) 或
[TypeScript / npm CLI 概览](typescript-cli.md)。
