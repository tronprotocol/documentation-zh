# Java CLI

`wallet-cli` 的 Java 实现提供两种入口：

- **交互模式（REPL）** —— 带 Tab 补全和交互式提示的人性化 shell。
- **标准 CLI 模式** —— 非交互式接口，具有确定的退出码和可选的 JSON 输出。

两种入口使用同一个 Java JAR，并共同覆盖 Java 实现的功能面，但有些命令只在其中一种模式下可用。
有关基于 npm 的实现，请参见 [TypeScript / npm CLI](typescript-cli.md)。

## 构建

Java 实现位于仓库的 `java/` 目录中，使用 Gradle 构建，需要 **Java 8**。下面的命令均以仓库根目录
为工作目录，以便与本节其他位置使用的路径保持一致。

```bash
git clone https://github.com/tronprotocol/wallet-cli.git
cd wallet-cli

# 构建项目和 fat JAR
./java/gradlew -p java build shadowJar
```

执行 `shadowJar` 后，可以使用生成的 JAR 运行钱包：

```bash
java -jar java/build/libs/wallet-cli.jar
```

## 运行

### 交互模式（REPL）

不带任何命令启动即进入交互式 shell。下面两种方式均可：

```bash
./java/gradlew -p java run
# 或者，使用已构建的 JAR：
java -jar java/build/libs/wallet-cli.jar
```

随后在提示符下输入命令（例如 `Login`、`GetBalance`、`SendCoin ...`）。命令名不区分大小写，
并支持 Tab 补全。输入 `Help` 列出所有命令，或输入 `Help <Command>` 查看某条命令的详细说明。

### 标准 CLI 模式

在命令行上传入一条命令及其选项。进程执行该命令、打印结果后退出：

```bash
java -jar java/build/libs/wallet-cli.jar --network nile get-balance --address TXyz...
java -jar java/build/libs/wallet-cli.jar --output json --network nile get-account --address TXyz...
```

标准 CLI 的命令名采用 kebab-case（`get-account`、`send-coin`）；大多数命令同时接受去掉连字符的
别名（`getaccount`、`sendcoin`）。并非每条命令都注册了这种别名——例如 `alias-*` 系列命令只能用
带连字符的形式。

此外还有一条 `help` 命令，用于查看单条命令的用法：

```bash
java -jar java/build/libs/wallet-cli.jar help --command send-coin
```

## 全局选项（标准 CLI）

执行修饰类全局选项由 `GlobalOptions` 解析，可以写在命令名**之前或之后**。顶层模式选择器有更严格的
位置规则，具体说明如下。

| 选项 | 取值 | 说明 |
|------|------|------|
| `--network` | `main`、`nile`、`shasta`、`custom` | 选择要连接的网络。 |
| `--grpc-endpoint` | `host:port` | 覆盖 gRPC 端点（配合 `--network custom` 使用）。 |
| `--output` | `text`（默认）、`json` | 输出格式。 |
| `--wallet` | 名称或路径 | 按名称或路径选择特定的钱包 keystore。 |
| `--quiet` | 标志 | 抑制非必要的提示性输出。 |
| `--verbose` | 标志 | 开启调试日志。（与 `--quiet` 冲突。） |
| `--password-stdin` | 标志 | 从 stdin 读取钱包密码（覆盖 `MASTER_PASSWORD`）。 |
| `--interactive` | 标志 | 启动交互式 REPL，而非执行某条命令。 |
| `--help`、`-h` | 标志 | 显示全局帮助，或某条命令的帮助。（`help --command <name>` 命令作用相同。） |
| `--version` | 标志 | 打印版本信息。 |

说明：

- 执行修饰类选项 `--network`、`--grpc-endpoint`、`--output`、`--wallet`、`--quiet`、
  `--verbose` 和 `--password-stdin` 可在命令名之前或之后识别。
- 顶层模式选择器 `--version` 和 `--interactive` 必须写在命令名之前；出现在命令之后时，会被视为
  命令自身的参数。
- `--help` 和 `-h` 出现在命令之前时请求全局帮助，出现在命令之后时请求该命令的帮助。
- 带取值的全局选项（`--output`、`--network`、`--wallet` 和 `--grpc-endpoint`）既可将取值作为
  下一个 token 给出（`--network nile`），也可内联给出（`--network=nile`）。
- 带取值的选项不可重复出现；未知的全局选项会被拒绝。

## 鉴权（标准 CLI）

标准 CLI 模式是非交互的，因此从不提示输入密码。构建并签名交易的命令（本文档中标注为**需要鉴权**）
会自动完成鉴权：

1. 钱包密码从环境变量 `MASTER_PASSWORD` 读取；当传入 `--password-stdin` 时则从 **stdin** 读取
   （stdin 优先）。
2. keystore 从 `Wallet/` 目录加载。可用 `--wallet <name|path>` 选择特定钱包，或用
   `set-active-wallet` 设置一个**活动钱包**（见 [钱包管理](wallet-management.md)）。

大多数只读查询命令不需要鉴权。例外是作用于当前钱包的查询：`get-address` 始终需要鉴权，
`get-balance` / `get-usdt-balance` / `gas-free-info` 在省略 `--address` 时需要鉴权
（见 [查询](query.md) 和 [GasFree](gasfree.md)）。

```bash
export MASTER_PASSWORD='your-wallet-password'
java -jar java/build/libs/wallet-cli.jar --network nile send-coin --to TXyz... --amount 1000000
```

REPL 的鉴权方式不同：通过 `Login` / `LoginAll` 交互式登录，会话保持解锁状态。见
[钱包管理](wallet-management.md)。

## JSON 输出与退出码（标准 CLI）

使用 `--output json` 时，每条命令都会在 stdout 上输出单个 JSON 信封。

成功：

```json
{
  "success": true,
  "data": { }
}
```

错误：

```json
{
  "success": false,
  "error": "execution_error",
  "message": "human-readable explanation"
}
```

其他规则：

- 广播交易的命令会在 `data` 中包含交易 ID `txid`（仅限单签广播）。
- `deploy-contract` 会在 `data` 中包含部署得到的 `contract_address`。
- 当某个选项的别名被解析时，信封会包含一个 `meta.resolved` 数组描述解析结果（见
  [钱包管理](wallet-management.md) 中的别名系统）。

退出码：

| 码 | 含义 |
|----|------|
| `0` | 成功。 |
| `1` | 执行错误（`"error": "execution_error"` 等）。 |
| `2` | 用法错误（`"error": "usage_error"`——标志错误、缺少必填选项等）。 |

这使得标准 CLI 可安全地用脚本驱动：检查退出码，并从 stdout 解析这唯一的 JSON 对象即可。

## 网络与配置

各网络的默认节点端点以及其他默认值，位于 `java/src/main/resources/config.conf`（HOCON 格式）。
`--network` 标志在 `main`、`nile`（测试网）、`shasta`（测试网）和 `custom` 之间选择。对于
`custom`，用 `--grpc-endpoint host:port` 提供端点。

在 REPL 中，用 `SwitchNetwork` 切换网络，用 `CurrentNetwork` 查看当前网络。

## 命令参考

命令按领域分组：

- [钱包管理](wallet-management.md) —— 创建/导入/导出钱包、登录、备份、锁定、活动钱包、别名。
- [账户](accounts.md) —— 链上账户的创建与更新、余额、权限。
- [质押与资源](staking.md) —— 冻结/解冻（v1 与 v2）、资源代理、奖励。
- [交易](transactions.md) —— 转账 TRX/资产/USDT、多签签名、广播。
- [智能合约](smart-contracts.md) —— 部署、触发、常量调用、能量预估。
- [TRC-10 资产](trc10.md) —— 发行、更新、参与、转账以及查询 TRC-10 代币。
- [治理](governance.md) —— 见证人、投票、提案、佣金、奖励提取。
- [GasFree](gasfree.md) —— 免 gas（代付）的 USDT 转账。
- [查询](query.md) —— 区块、交易、链参数、价格、节点及工具类命令。
