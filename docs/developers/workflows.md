# java-tron CI 工作流

本文概述贡献者在准备 java-tron Pull Request 时需要了解的 GitHub Actions 检查。如果实现发生变化，应以 java-tron 仓库中的工作流文件为最终依据。

## 工作流何时运行

| 工作流 | PR 目标分支 | 仅修改文档的 PR | 其他触发方式 |
| --- | --- | --- | --- |
| PR Check（`pr-check.yml`） | `develop`、`release_**` | 运行 | 推送到 `master` 或 `release_**` |
| PR Build（`pr-build.yml`） | `master`、`develop`、`release_**` | 跳过 | 手动触发 |
| 单节点集成测试（`integration-test-single-node.yml`） | `develop`、`release_**` | 跳过 | 推送到 `master` 或 `release_**`；手动触发 |
| 多节点集成测试（`integration-test-multinode.yml`） | `develop`、`release_**` | 跳过 | 推送到 `master` 或 `release_**`；手动触发 |
| CodeQL（`codeql.yml`） | `develop` | 跳过 | 推送到 `develop`、`master` 或 `release_**`；每周定时运行 |
| Math 使用检查（`math-check.yml`） | `develop`、`release_**` | 运行 | 推送到 `master` 或 `release_**`；手动触发 |
| 审查者分配（`pr-reviewer.yml`） | `develop`、`release_**` | 运行 | 无 |
| 关闭 PR 时取消工作流（`pr-cancel.yml`） | 任意分支 | 未合并的 PR 关闭时运行 | 无 |

如果 Pull Request 仅修改文档或部分仓库元数据文件，PR Build、两个集成测试工作流和 CodeQL 会被跳过。如果同一 Pull Request 还包含其他文件，符合目标分支条件的工作流会正常运行。PR Check、Math 使用检查、审查者分配和关闭时取消工作流没有此路径排除规则。

## PR 校验和代码检查

对于目标为 `develop` 或 `release_**` 的 PR，PR Check 会强制执行以下标题和描述规则：

- 使用 `type: description` 或 `type(scope): description` 格式。
- 标题长度保持在 10～72 个字符之间。
- `type` 必须是 `feat`、`fix`、`refactor`、`docs`、`style`、`test`、`chore`、`ci`、`perf`、`build` 或 `revert`。
- 标题中的描述部分不得以 ASCII 大写字母开头，标题结尾不得使用句号。
- PR 描述去除首尾空白后至少包含 20 个字符。
- 未知 `scope` 只会产生警告，不会导致检查失败。

该工作流还会运行 Checkstyle，并检查 `common/src/main/resources/reference.conf` 的键名格式、嵌套深度、服务端口冲突和配置注释。这些检查也会针对目标为 `develop` 或 `release_**` 且仅修改文档的 PR 运行。

## 多平台构建和覆盖率

由 PR 触发时，PR Build 会在四种环境中执行完整的 Gradle 构建：

| 环境 | 架构 | JDK | 平台相关检查 |
| --- | --- | --- | --- |
| macOS 26 | ARM64 | 17 | 常规 `framework` 测试使用 RocksDB |
| Ubuntu 24.04 | ARM64 | 17 | 常规 `framework` 测试使用 RocksDB |
| Rocky Linux 8 容器 | x86-64 | 8 | 有针对性的 RocksDB 引擎测试 |
| Debian 11 容器 | x86-64 | 8 | 有针对性的 RocksDB 测试和覆盖率报告 |

覆盖率门禁要求：

- 变更的 Java 源代码行覆盖率必须高于 60%；没有变更 Java 源代码行时跳过此项门禁。
- 与基准提交相比，整体覆盖率的下降不得超过 0.1 个百分点。

## 集成、安全和 Math 检查

本套文档对应的源码版本包含两个完整集成测试工作流：

- 单节点工作流针对一个节点运行完整测试集。
- 多节点工作流针对由三个见证节点组成的环境运行完整测试集。

它们会针对目标为 `develop` 或 `release_**` 且符合路径条件的 PR 运行，也会在推送到 `master` 或 `release_**` 时运行，并且支持手动触发。

CodeQL 仅针对目标为 `develop` 的 PR 运行。此外，它还会在推送到 `develop`、`master` 或 `release_**` 时运行，并且每周定时运行。

Math 使用检查会拒绝直接使用 `java.lang.Math`，并要求贡献者改用 `org.tron.common.math.StrictMathWrapper`。该检查也会针对目标为 `develop` 或 `release_**` 且仅修改文档的 PR 运行。

## `scope` 校验和审查者分配

PR 校验和审查者分配使用不同的 `scope` 列表。PR 校验的已知列表包含 32 个 `scope`，审查者映射表包含 26 个 `scope`：

| 分类 | 数量 | `scope` |
| --- | ---: | --- |
| PR 校验和审查者映射均包含 | 24 | `framework`、`chainbase`、`actuator`、`consensus`、`common`、`crypto`、`plugins`、`protocol`、`net`、`db`、`vm`、`tvm`、`api`、`jsonrpc`、`rpc`、`http`、`event`、`config`、`trie`、`metrics`、`test`、`docker`、`lite`、`toolkit` |
| 仅 PR 校验包含 | 8 | `block`、`proposal`、`log`、`version`、`freezeV2`、`DynamicEnergy`、`stable-coin`、`reward` |
| 仅审查者映射包含 | 2 | `backup`、`ci` |

未知 PR `scope` 只会产生校验警告。审查者分配使用独立的 `scope` 映射表。

## PR 关闭时取消工作流

当 PR 在未合并的情况下被关闭时，java-tron 会尝试取消以下工作流中处于排队或运行状态的任务：

- PR Build
- CodeQL
- 单节点集成测试
- 多节点集成测试

## Sonar 配置

java-tron 仓库保留了 `sonar-project.properties` 以及用于静态分析的 SonarQube Gradle 插件配置，但 java-tron 的 GitHub Actions 工作流不会调用 Sonar。如果配置了外部 Sonar 或 SonarCloud 集成，则不属于本文所述工作流文件的范围。

## 在本地运行检查

[开发示例](demo.md#4-checkstyle)提供了推荐的 Checkstyle、完整构建和 RocksDB 命令，并说明了 ARM64 与 x86-64 环境之间的 JDK 和存储引擎差异。
