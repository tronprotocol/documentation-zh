# java-tron 文档

java-tron 是 TRON 网络的官方 Java 客户端实现，由 TRON 协议团队主导开发并完全开源。它实现了 TRON 主网的全部协议规范，包括 DPoS 共识、TVM 虚拟机、账户与资源模型、智能合约、去中心化交易所、多签权限管理等核心能力，是运行全节点、参与超级代表选举、部署合约和构建 DApp 的基础设施。

本文档面向 java-tron 节点运维者、协议研究者、DApp 开发者和核心贡献者，覆盖从节点部署、网络接入、API 调用到协议机制和源码贡献的完整链路。源码与版本发布：[github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)。

## 选择你的入口

<div class="grid cards" markdown>

-   __新手入门__

    ---

    第一次接触 java-tron 或 TRON 协议？先从循序渐进的实践路径开始，再将共识概览和术语表作为参考。

    - [开始使用](getting_started/index.md)
    - [动手入门指南](getting_started/getting_started_with_javatron.md)
    - [波场共识 (DPoS)](mechanism-algorithm/dpos.md)
    - [术语表](glossary.md)

-   __运行节点__

    ---

    涵盖 java-tron 部署、配置、网络连接、日志、监控、存储、备份和维护的指南。

    - [节点运维概览](using_javatron/index.md)
    - [部署 java-tron](using_javatron/installing_javatron.md)
    - [节点配置](using_javatron/configuration.md)
    - [节点日志](using_javatron/logging.md)
    - [节点监控](using_javatron/metrics.md)
    - [升级到新版本](releases/upgrade-instruction.md)
    - [私链网络](using_javatron/private_network.md)

-   __DApp 开发__

    ---

    在 TRON 上构建 DApp 所需的智能合约开发、java-tron API 和命令行工具。

    - [使用 java-tron 构建 DApp](contracts/index.md)
    - [选择 API](api/index.md)
    - [HTTP 接口](api/http/index.md)
    - [JSON-RPC 接口](api/json-rpc/index.md)
    - [gRPC 接口](api/rpc/index.md)
    - [智能合约](contracts/contract.md)
    - [wallet-cli](clients/wallet-cli/index.md)

-   __贡献核心__

    ---

    涵盖参与 java-tron 贡献、配置开发环境、理解 CI 与代码库，以及遵循 Issue、TIP 和网络治理流程的指南。

    - [贡献者概览](developers/index.md)
    - [开发者指南](developers/java-tron.md)
    - [TIPs 工作流程](developers/tip-workflow.md)
    - [配置 IDE](developers/run-in-idea.md)
    - [核心模块](developers/code-structure.md)

</div>

## 按主题浏览

- __[开始使用](getting_started/index.md)__ — 通过动手实践创建 TRON 账户、启动并验证 java-tron 节点，以及使用 wallet-cli 或 cURL 发送交易或查询链上数据
- __[运维节点](using_javatron/index.md)__ — 涵盖 java-tron 部署、配置、网络连接、日志、监控、存储、备份和维护的指南
- __[API 参考](api/index.md)__ — 介绍如何在 HTTP、JSON-RPC 和 gRPC 接口之间选择，并提供参考索引和机器可读定义
- __[wallet-cli](clients/wallet-cli/index.md)__ — 面向 TRON 和部分 EVM 网络的命令行钱包——Java 版侧重交互操作，TypeScript 版面向自动化代理
- __[理解协议](mechanism-algorithm/index.md)__ — 涵盖 TRON 共识、超级代表、账户与签名、网络资源、系统合约和账户权限的文档
- __[参与 java-tron 贡献](developers/index.md)__ — 涵盖参与 java-tron 贡献、配置开发环境、理解 CI 与代码库，以及遵循 Issue、TIP 和网络治理流程的指南
- __[构建 DApp](contracts/index.md)__ — 在 TRON 上构建 DApp 所需的智能合约开发与开发工具
- __[版本发布](releases/index.md)__ — 节点升级流程、发布包签名验证和版本历史
- __[附录](glossary.md)__ — 常见 TRON 与 java-tron 术语释义

## 其它资源

- [TRON 白皮书](https://tron.network/static/doc/white_paper_v_2_1.pdf) — TRON 协议设计与愿景的官方文献
- [TRON 改进提案 (TIPs)](https://github.com/tronprotocol/tips) — 协议演进提案的提交、讨论与归档仓库
- [TRON 开发者中心](https://developers.tron.network/) — DApp 开发者文档、SDK、教程的英文总入口
- [TRON 官网](https://tron.network/index?lng=zh) — 项目动态、生态合作伙伴、社区入口

## 文档权威来源

英文文档仓库 ([`documentation-en`](https://github.com/tronprotocol/documentation-en)) 是 java-tron 文档的权威来源，本中文文档仓库 ([`documentation-zh`](https://github.com/tronprotocol/documentation-zh)) 为其翻译跟进版本。当中英文内容不一致时，以英文版为准；内容变更应先在英文源上进行，再同步到中文译文。
