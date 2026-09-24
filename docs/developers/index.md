# 参与 java-tron 贡献

涵盖参与 java-tron 贡献、配置开发环境、理解 CI 与代码库，以及遵循 Issue、TIP 和网络治理流程的指南。

## 开始贡献

1. [开发者指南](java-tron.md) — 贡献和提交规则、分支管理、代码审查、CI 要求、命名规范、PR 与提交信息规范以及行为准则。
2. [IntelliJ IDEA 配置](run-in-idea.md) — JDK 要求、源码编译、代码风格检查以及运行或调试 java-tron。
3. [开发示例](demo.md) — 添加 `setPeer` HTTP API、编写测试、运行 CheckStyle 并提交 PR。
4. [CI 工作流](workflows.md) — 工作流触发条件、PR 检查、构建、覆盖率、集成测试、安全检查、审查人分配和本地检查。
5. [Issue 工作流](issue-workflow.md) — Issue 提交与处理流程以及标签分类。
6. [网络治理](governance.md) — 网络参数提案讨论、链上提交、超级代表投票和实现流程。
7. [TIP 规范与指南](tip-workflow.md) — TIP 类型、提交和审查流程、状态、组成、链接规则和辅助文件。

## TIPs

- [TRON 改进提案](tips.md) — 按类别和状态编制的 TIP 索引。

## 理解代码库

- [核心模块](code-structure.md) — Protocol、Common、ChainBase、Consensus、Actuator、Crypto 和 Framework 模块的代码组织与职责。
- [ChainBase 深入解析](chainbase.md) — ChainBase 中的交易处理、状态回滚、持久化、区块固化和原子性。
- [P2P 网络深入解析](network.md) — 对等节点连接管理、区块同步以及区块与交易广播，包括限制、验证和背压机制。
