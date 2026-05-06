# java-tron 文档

java-tron 是 TRON 网络的官方 Java 客户端实现，由 TRON 协议团队主导开发并完全开源。它实现了 TRON 主网的全部协议规范，包括 DPoS 共识、TVM 虚拟机、账户与资源模型、智能合约、去中心化交易所、多签权限管理等核心能力，是运行全节点、参与超级代表选举、部署合约和构建 DApp 的基础设施。

本文档面向 java-tron 节点运维者、协议研究者、DApp 开发者和核心贡献者，覆盖从节点部署、网络接入、API 调用到协议机制和源码贡献的完整链路。源码与版本发布：[github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)。

## 选择你的入口

<div class="grid cards" markdown>

-   __新手入门__

    ---

    第一次接触 java-tron 或 TRON 协议？从这里开始。

    - [入门指南](getting_started/getting_started_with_javatron.md)
    - [波场共识 (DPoS)](mechanism-algorithm/dpos.md)
    - [术语表](glossary.md)

-   __运行节点__

    ---

    部署、监控、维护 java-tron 节点的运维指南。

    - [部署 java-tron](using_javatron/installing_javatron.md)
    - [节点监控](using_javatron/metrics.md)
    - [升级到新版本](releases/upgrade-instruction.md)
    - [私链网络](using_javatron/private_network.md)

-   __DApp 开发__

    ---

    调用 java-tron 提供的 HTTP/gRPC/JSON-RPC 接口构建应用。

    - [HTTP 接口](api/http/index.md)
    - [JSON-RPC 接口](api/json-rpc/index.md)
    - [智能合约](contracts/contract.md)
    - [wallet-cli](clients/wallet-cli.md)

-   __贡献核心__

    ---

    修改 java-tron 源码、提 TIP、参与协议演进。

    - [开发者指南](developers/java-tron.md)
    - [TIPs 工作流程](developers/tips.md)
    - [配置 IDE](developers/run-in-idea.md)
    - [核心模块](developers/code-structure.md)

</div>

## 按主题浏览

- __[使用 java-tron](using_javatron/installing_javatron.md)__ — 部署、备份恢复、轻节点、私链网络、事件订阅、数据库配置、节点监控、维护工具
- __[API 接口](api/http/index.md)__ — HTTP、gRPC、JSON-RPC
- __[核心协议](mechanism-algorithm/dpos.md)__ — DPoS 共识、超级代表、账户模型、资源模型、智能合约、系统合约、去中心化交易所、账户权限管理
- __[java-tron 开发](developers/java-tron.md)__ — 开发者指南、TIPs 工作流程、Issue 流程、治理流程、IDE 配置、开发示例、核心模块
- __[DApp 开发](contracts/tools.md)__ — 开发工具
- __[客户端](clients/wallet-cli.md)__ — wallet-cli
- __[版本发布](releases/upgrade-instruction.md)__ — 新版本部署手册、一致性检验、历史版本
- __[附录](glossary.md)__ — 术语表

## 其它资源

- [TRON 白皮书](https://tron.network/static/doc/white_paper_v_2_1.pdf) — TRON 协议设计与愿景的官方文献
- [TRON 改进提案 (TIPs)](https://github.com/tronprotocol/tips) — 协议演进提案的提交、讨论与归档仓库
- [TRON 开发者中心](https://developers.tron.network/) — DApp 开发者文档、SDK、教程的英文总入口
- [TRON 官网](https://tron.network/index?lng=zh) — 项目动态、生态合作伙伴、社区入口
