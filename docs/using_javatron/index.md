# 运维 java-tron 节点

涵盖 java-tron 部署、配置、网络连接、日志、监控、存储、备份和维护的指南。

## 首次部署

对于新节点，请先阅读以下页面：

1. [部署 java-tron 节点](installing_javatron.md) — 硬件和 JDK 要求、客户端获取方式，以及 FullNode、SolidityNode 和出块节点的启动选项。
2. [配置节点](configuration.md) — 配置优先级、网络与对等节点、存储、API 服务、TVM 执行设置、限流、出块凭据、事件与监控设置、动态重载行为和配置验证。
3. [检查节点日志](logging.md) — 定位并跟踪节点日志和垃圾回收日志，根据需要自定义 Logback 或标准输出，并在故障排查时调整日志级别。

## 可选部署场景

| 主题 | 指南 | 涵盖内容 |
|---|---|---|
| Lite FullNode | [Lite FullNode](litefullnode.md) | Lite FullNode 概念、使用状态快照启动、减少存储、API 限制、部署和数据裁剪 |
| 私链网络 | [私链网络](private_network.md) | 由一个出块超级代表节点和一个普通 FullNode 组成的基础私链所需的前置条件和部署步骤 |

## 其他配置

- [连接 TRON 网络](connecting_to_tron.md) — 网络和创世区块设置、节点发现、主动与被动节点、连接限制、状态验证、故障排查和私链连接。
- [数据库配置](../architecture/database.md) — 不同 CPU 架构支持的存储引擎、RocksDB 配置与优化，以及 x86_64 上从 LevelDB 迁移到 RocksDB。
- [事件订阅](../architecture/event.md) — 通过 Kafka 或 MongoDB 插件进行本地事件订阅、支持的事件类型和过滤器、事件查询服务以及内置 ZeroMQ 订阅。
- [设置节点指标监控](metrics.md) — 启用 java-tron 指标并部署 Prometheus 和 Grafana。

## 维护与恢复

- [备份与恢复](backup_restore.md) — 停止并归档节点数据目录、恢复备份，以及使用公开的主网或 Nile 数据快照。
- [节点维护工具](toolkit.md) — Keystore 管理、数据库分区、Lite FullNode 数据裁剪、快速复制、LevelDB 到 RocksDB 转换、LevelDB 启动优化和 Merkle 根计算。
