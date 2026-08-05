# 节点配置

java-tron 使用 [HOCON](https://github.com/lightbend/config/blob/main/HOCON.md) 配置文件。命令行选项 `-c` 用于指定配置名称或路径；java-tron 可以将其解析为文件系统中的文件，也可以解析为应用程序中打包的资源。

本指南介绍当前的配置模型、节点运维者最常用的设置，以及哪些变更需要重启节点。

## 配置文件与优先级 { #configuration-files-and-precedence }

java-tron 内置了两个用途不同的配置文件：

| 文件 | 用途 |
|---|---|
| `common/src/main/resources/reference.conf` | 定义完整的默认值集合，并始终作为回退配置。 |
| `framework/src/main/resources/config.conf` | 提供内置的主网部署配置和运行参数覆盖。当解析出的名称为 `config.conf`，且文件系统中不存在对应文件时，加载该文件。 |

配置按照以下顺序解析和应用：

1. 配置名称取自 `-c` 传入的值；如果省略 `-c`，FullNode 默认使用 `config.conf`。
2. java-tron 检查该名称是否指向文件系统中已存在的文件。相对路径以进程的当前工作目录为基准解析。
3. 如果文件不存在，java-tron 会查找同名的 classpath 资源。例如，文件系统中没有 `config.conf` 时，`-c config.conf` 仍可加载 JAR 中内置的 `config.conf`。
4. 如果两种来源都不存在，节点会因配置路径错误而启动失败。
5. 加载选中的配置，并以 `reference.conf` 作为回退配置。
6. 对应的命令行参数覆盖已加载的配置值。
7. 最后应用特定平台的约束。

无论是通过 `-c` 指定，还是自动发现的 `./config.conf`，外部配置文件都**不会**继承内置 `config.conf` 中的值。因此，即使所有省略的配置项仍会从 `reference.conf` 获取默认值，精简的外部配置文件也可能与内置配置产生不同的运行行为。

特定平台的约束可能覆盖已经解析的配置。尤其是 ARM64 仅支持 RocksDB，因此无论配置文件或 CLI 如何设置，java-tron 都会强制将 `storage.db.engine` 设置为 `ROCKSDB`。

生产部署应从目标网络的当前配置模板开始，并保留该网络必需的特定配置。当前 java-tron 源文件如下：

- [完整默认值（`reference.conf`）](https://github.com/tronprotocol/java-tron/blob/master/common/src/main/resources/reference.conf)
- [主网配置模板（`config.conf`）](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf)

对于 Nile 或其他网络，应使用为该网络提供的配置模板。节点发现、P2P 版本、种子节点和创世块配置必须全部指向同一个网络。支持的网络配置模板请参阅[部署 java-tron](installing_javatron.md#network-types)。

## 使用外部配置启动节点

通过 `-c` 指定外部配置文件，并通过 `-d` 选择节点的输出目录：

```bash
java -jar FullNode.jar \
  -c /etc/java-tron/mainnet.conf \
  -d /var/lib/java-tron
```

要运行出块节点，请添加 `--witness`：

```bash
java -jar FullNode.jar \
  --witness \
  -c /etc/java-tron/mainnet.conf \
  -d /var/lib/java-tron
```

如果命令行选项和配置文件控制同一行为，命令行选项会覆盖配置文件中的值，但仍受上述特定平台约束的限制。

HOCON 同时支持嵌套对象和点分隔键。例如，以下内容只是配置片段，并非完整的主网配置：

```hocon
storage.db.directory = "database"

node {
  listen.port = 18888

  discovery {
    enable = true
    persist = true
  }

  http {
    fullNodeEnable = true
    fullNodePort = 8090
  }

  jsonrpc {
    httpFullNodeEnable = false
    httpFullNodePort = 8545
  }
}
```

配置键名称和值类型必须与 `reference.conf` 完全一致。尤其要注意：布尔值使用不加引号的 `true` / `false`，数值使用数字，文本使用带引号的字符串，列表使用方括号。

## 网络与对等节点配置

主要的 P2P 配置如下：

| 配置路径 | 用途 |
|---|---|
| `node.p2p.version` | 标识 P2P 协议使用的 TRON 网络。 |
| `node.listen.port` | 节点接受 P2P 连接的 TCP 端口。 |
| `node.discovery.enable` | 启用节点发现。 |
| `node.discovery.persist` | 持久化已发现的节点。 |
| `node.discovery.external.ip` | 向对等节点广播指定的公网 IP 地址。 |
| `seed.node.ip.list` | 提供引导节点。 |
| `node.active` | 列出节点应主动维持连接的对等节点。 |
| `node.passive` | 列出受信任的入站对等节点地址。 |
| `node.maxConnections` | 限制对等节点连接总数。 |
| `node.maxConnectionsWithSameIp` | 限制来自同一 IP 地址的对等节点连接数。 |

当节点需要接受入站连接时，应在主机防火墙中开放 P2P 监听端口。如果节点位于 NAT 后方，请确保对外广播的地址、端口转发和节点配置保持一致。

有关节点发现、种子节点、主动/被动节点、IPv6 和连接数限制的示例，请参阅[连接 TRON 网络指南](connecting_to_tron.md)。

## 存储与输出目录

`-d` / `--output-directory` 选项用于选择节点输出根目录，`storage.db.directory` 用于选择该根目录下的数据库目录。例如：

```bash
java -jar FullNode.jar -c /etc/java-tron/mainnet.conf -d /data/fullnode
```

```hocon
storage {
  db.engine = "LEVELDB"
  db.sync = false
  db.directory = "database"
}
```

在此示例中，默认数据库位置位于 `/data/fullnode/database` 下。同一台机器上的每个 java-tron 进程都应使用不同的 `-d` 目录，不能让两个正在运行的进程指向同一个数据库。

`storage.properties` 列表可以为各个数据库分别设置路径和 LevelDB 调优参数。每个条目都必须包含 `name`；`path` 同时适用于 LevelDB 和 RocksDB，而 `blockSize`、`writeBufferSize`、`cacheSize` 和 `maxOpenFiles` 仅适用于 LevelDB。

更改数据库引擎或性能设置前，请参阅[数据库配置指南](../architecture/database.md)。有关运行数据的处理，请参阅[备份与恢复](backup_restore.md)和[节点维护工具](toolkit.md)。

## API 服务与端口 { #api-services-and-ports }

以下默认值来自 `reference.conf`。外部配置可以覆盖每项服务的启用开关和端口。

| 服务 | 启用开关 | 端口配置 | 默认值 |
|---|---|---|---|
| FullNode HTTP | `node.http.fullNodeEnable` | `node.http.fullNodePort` | 启用，`8090` |
| Solidity HTTP | `node.http.solidityEnable` | `node.http.solidityPort` | 启用，`8091` |
| PBFT HTTP | `node.http.PBFTEnable` | `node.http.PBFTPort` | 启用，`8092` |
| FullNode gRPC | `node.rpc.enable` | `node.rpc.port` | 启用，`50051` |
| Solidity gRPC | `node.rpc.solidityEnable` | `node.rpc.solidityPort` | 启用，`50061` |
| PBFT gRPC | `node.rpc.PBFTEnable` | `node.rpc.PBFTPort` | 启用，`50071` |
| FullNode JSON-RPC | `node.jsonrpc.httpFullNodeEnable` | `node.jsonrpc.httpFullNodePort` | 禁用，`8545` |
| Solidity JSON-RPC | `node.jsonrpc.httpSolidityEnable` | `node.jsonrpc.httpSolidityPort` | 禁用，`8555` |
| PBFT JSON-RPC | `node.jsonrpc.httpPBFTEnable` | `node.jsonrpc.httpPBFTPort` | 禁用，`8565` |

请求和消息大小限制分别配置：

- `node.http.maxMessageSize` 控制 HTTP 请求体大小。
- `node.rpc.maxMessageSize` 控制 gRPC 消息大小。
- `node.jsonrpc.maxMessageSize` 控制 JSON-RPC 请求体大小。
- `node.jsonrpc.maxBatchSize`、`maxResponseSize` 和 filter 限制用于约束 JSON-RPC 工作负载。

使用 `node.disabledApi` 可以禁用指定的 HTTP、gRPC 或 PBFT 方法，但它不会禁用 JSON-RPC 方法；要禁用 JSON-RPC 服务，请使用对应的 `node.jsonrpc.*Enable` 开关。

不要将管理类接口或交易构造接口直接暴露给不受信任的网络。应通过主机或网络控制限制访问，并在需要时将公共服务置于配置适当的网关之后。有关各协议的具体行为，请参阅 [HTTP API](../api/http/index.md) 和 [JSON-RPC API](../api/json-rpc/index.md) 指南。

## TVM 与 constant call 配置 { #tvm-and-constant-call-configuration }

TVM 模拟和 Energy 估算行为通过 `vm` 配置：

| 配置路径 | 默认值 | 用途 |
|---|---:|---|
| `vm.supportConstant` | `false` | 启用只读的 constant call。 |
| `vm.maxEnergyLimitForConstant` | `100000000` | 单次 constant call 可用的最大 Energy。配置绑定期间，小于 3,000,000 的值会提高到该下限。 |
| `vm.estimateEnergy` | `false` | 启用专用的 `estimateenergy` 实现。 |
| `vm.estimateEnergyMaxRetry` | `3` | Energy 估算期间的最大重试次数；取值会被限制在 0–10 范围内。 |
| `vm.constantCallTimeoutMs` | `0` | 通过 constant call 路径执行的调用可使用的执行时限，单位为毫秒。 |
| `vm.vmTrace` | `false` | 启用 TVM trace 输出。 |

`vm.constantCallTimeoutMs = 0` 保留原有行为，即 constant call 使用网络的
`MAX_CPU_TIME_OF_ONE_TX` 限制。正值设置仅适用于 constant call 的执行时限，
单位为毫秒。负值或因数值过大而无法安全转换为 VM 微秒级执行时限的值会导致
配置加载失败。debug 模式和独立 SolidityNode 不会执行该时限检查；发送到
FullNode `/walletsolidity` 接口的 constant call 仍受该时限限制。

该配置适用于通过 HTTP、gRPC 和 JSON-RPC 执行的 constant call，包括
[`/wallet/triggerconstantcontract`](../api/http/smart-contract/triggerconstantcontract.md)、
ABI `view`/`pure` 函数被分派到 constant call 路径时的
[`/wallet/triggersmartcontract`](../api/http/smart-contract/triggersmartcontract.md)、
[`/wallet/estimateenergy`](../api/http/smart-contract/estimateenergy.md)、
[`eth_call`](../api/json-rpc/smart-contract/eth_call.md) 和
[`eth_estimateGas`](../api/json-rpc/smart-contract/eth_estimateGas.md)。

对于生产节点，当复杂的只读调用需要更长执行时间时，可使用
`vm.constantCallTimeoutMs`。修改这些 `vm` 配置需要重启进程；动态配置重载不会
应用这些变更。

## 限流

API 限制在 `rate.limiter` 下配置：

- `rate.limiter.http` 定义各 servlet 的 HTTP 规则。
- `rate.limiter.rpc` 定义各方法的 gRPC 规则。
- `rate.limiter.global.qps` 限制 HTTP 和 gRPC 请求总量。
- `rate.limiter.global.ip.qps` 限制来自单一源 IP 的请求。
- `rate.limiter.global.api.qps` 提供各接口的默认限制。
- `rate.limiter.apiNonBlocking` 选择以非阻塞或阻塞方式获取 permit。

当 `rate.limiter.apiNonBlocking` 为 `true` 时，超限请求会立即被拒绝；为 `false` 时，QPS 和单 IP QPS 策略会阻塞等待令牌。`GlobalPreemptibleAdapter` 的行为不同：它最多等待两秒以获取并发 permit，超过两秒仍未获得时拒绝请求。

P2P 消息限制独立配置在 `rate.limiter.p2p` 下。

## 出块凭证

使用 `--witness` 启动的节点需要访问出块账户的签名私钥。生产部署应优先使用 `localwitnesskeystore`。`localwitness` 会将私钥直接存储在配置文件中，因此必须格外注意文件保护。

应将配置文件和 keystore 文件的访问权限限制为节点的操作系统用户，不要将密钥提交到源码仓库，也不要在测试环境中重复使用生产私钥。有关说明，请参阅[启动出块节点](installing_javatron.md#starting-a-block-production-node)和[使用 keystore 指定私钥](installing_javatron.md#keystore-password)。

## 事件订阅与监控

事件投递由 `event.subscribe` 控制。其配置用于选择原生队列或事件插件、插件路径或目标服务器，以及启用的触发器主题。完整配置请参阅[事件订阅](../architecture/event.md)。

Prometheus 监控配置位于 `node.metrics.prometheus` 下，包括启用开关和监听端口。采集和仪表板说明请参阅[节点监控](metrics.md)。

## 动态配置重载

动态重载默认关闭：

```hocon
node.dynamicConfig {
  enable = true
  checkInterval = 600
}
```

`checkInterval` 的单位是秒。由于重载服务会监视所选文件的修改，应当配合磁盘上的配置文件使用该功能，配置文件可以通过 `-c` 指定，也可以是自动发现的 `./config.conf`。

目前动态重载只会应用 `node.active` 和 `node.passive` 的变更。其他配置（包括端口、存储、API 开关、限流以及 `node.fastForward`）都需要重启进程。重载成功消息使用 `DEBUG` 级别，默认会被 `app` logger 的 `INFO` 级别隐藏。编辑文件后，可以为 `app` logger 启用 `DEBUG` 以查看重载消息，也可以通过节点运行状态验证更新后的对等连接。

## 验证配置变更

在生产环境中应用配置前：

1. 保留一份可恢复的最近正常配置文件。
2. 检查 HOCON 的大括号、逗号、列表语法、键名拼写和值类型。
3. 确认配置文件属于目标网络，并包含该网络必需的覆盖值。
4. 确认所有配置的监听端口都可用且已获防火墙放行。
5. 启动或重启节点，并检查 `logs/tron.log` 中与配置、端口绑定、数据库和对等连接相关的错误。
6. 验证区块同步以及所有计划开放的 API。

如果配置修改似乎没有生效，请先确认实际选择的配置来源：显式指定的 `-c` 路径、隐式的 `./config.conf`，或内置的 `config.conf`。随后重启节点，除非修改的是动态重载支持的两个对等节点列表之一。
