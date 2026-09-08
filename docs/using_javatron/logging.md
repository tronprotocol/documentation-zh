# 节点日志

java-tron 使用 Logback 记录节点应用日志。从 GreatVoyage-v4.8.2 开始，通过 Java Util Logging（JUL）输出的日志（包括 grpc-java 诊断日志）会被桥接到 Logback，使节点运维人员能够通过同一套日志配置对其进行管理。JVM 生成的输出（如垃圾回收日志）则通过 JVM 启动参数单独配置。

## 默认日志文件

内置的 Logback 配置将不同类别的运行日志写入不同的文件：

| 文件 | 内容 |
| --- | --- |
| `./logs/tron.log` | 节点生命周期、同步、P2P、API、共识及运行诊断等主节点日志 |
| `./logs/db/db.log` | 通过专用 `LEVELDB` 和 `ROCKSDB` logger 路由的日志 |
| `./logs/grpc/grpc.log` | 通过 `io.grpc` 路由的 grpc-java 传输和协议诊断日志 |

每个默认的滚动文件 appender 都会按天轮转，并在当前日志文件达到约 500 MB 时轮转。每个 appender 的归档文件均使用 gzip 压缩，最多保留最近 7 个日周期产生的归档文件，同时受 50 GB 归档总大小上限的约束。

配置中定义了控制台 appender，但默认没有将其添加到 root logger。

`LEVELDB` 和 `ROCKSDB` logger 通过 `DB` appender 直接写入 `db.log`，不经过异步队列。gRPC 的 `GRPC` appender 使用可容纳 1,024 个事件的非阻塞队列；队列已满时，新的 gRPC 日志事件可能会被丢弃，以避免阻塞 gRPC 线程。相比之下，主日志的 `ASYNC` appender 使用可容纳 100 个事件的队列，并会在队列已满时阻塞日志生产线程。将 gRPC appender 的 `discardingThreshold` 设置为 `0` 可以避免基于优先级提前丢弃日志，但无法避免非阻塞队列已满时丢弃日志。

## JVM 垃圾回收日志

垃圾回收日志由 JVM 生成，与 java-tron 的 Logback 配置无关。只有通过 JVM 启动参数启用 GC 日志记录时，才会创建 GC 日志文件。

对于使用 JDK 17 的 ARM64 环境，java-tron 提供的参数包括：

```text
-Xlog:gc,gc+heap:file=gc.log:time,tags,level:filecount=10,filesize=100M
```

此配置将 GC 和堆事件写入 `gc.log`，在文件达到 100 MB 时轮转，并在当前 `gc.log` 之外最多保留 10 个已轮转的文件。

对于使用 JDK 8 的 x86_64 环境，java-tron 提供的参数包括：

```text
-XX:+PrintGCDetails
-XX:+PrintGCDateStamps
-Xloggc:gc.log
```

此配置将带时间戳的详细 GC 事件写入 `gc.log`。与 JDK 17 配置不同，这些参数没有配置按大小轮转或保留策略。若不通过外部方式进行轮转或归档，该文件会持续增长。

对于 JDK 8 和 JDK 17，相对路径 `gc.log` 均基于进程的工作目录解析，而不是基于 `FullNode.jar` 所在目录解析。

使用以下命令持续查看 GC 日志：

```bash
tail -f ./gc.log
```

如果未提供适当的 JVM 日志参数，直接使用 `java -jar FullNode.jar` 启动节点不会创建 GC 日志。

## 查看节点日志

使用主日志查看区块同步和节点的一般运行状态：

```bash
tail -f ./logs/tron.log
```

排查 gRPC 连接、传输或 TLS 问题时，查看专用的 gRPC 日志：

```bash
tail -f ./logs/grpc/grpc.log
```

查看路由到专用数据库 logger 的存储引擎诊断日志时，请使用：

```bash
tail -f ./logs/db/db.log
```

## 使用自定义 Logback 配置

以节点所运行的同一 java-tron 版本内置的 `logback.xml` 为起点。当前版本的参考文件为 [`framework/src/main/resources/logback.xml`](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/logback.xml)。

使用自定义文件启动节点：

```bash
java -jar FullNode.jar --log-config /absolute/path/to/logback.xml
```

如果省略 `--log-config`，java-tron 将使用内置的 Logback 配置。如果指定该参数，其值必须指向一个可读取的普通文件，否则节点将启动失败。

自定义 Logback 配置会取代内置配置。请包含部署所需的 appender 和关闭钩子，例如专用 gRPC appender、Prometheus `METRICS` appender 和 `TronLogShutdownHook`。

## 将日志输出到 stdout

默认文件已经定义了 `CONSOLE` appender。将其添加到 root logger，即可同时写入 stdout 和主日志：

```xml
<root level="INFO">
  <appender-ref ref="CONSOLE"/>
  <appender-ref ref="ASYNC"/>
  <appender-ref ref="METRICS"/>
</root>
```

如果只需将主节点日志输出到 stdout，请省略 `ASYNC` 引用。如果节点暴露 Prometheus 指标，并使用 `tron:error_info_total` 进行告警，请保留 `METRICS`。

默认的 `CONSOLE` appender 配有 `INFO` 阈值。若要在 stdout 中显示 `DEBUG` 或 `TRACE` 事件，除了修改相应 logger 的级别，还需要降低该 appender 过滤器的阈值，或移除该过滤器。

## 关闭与日志刷新

默认的 `TronLogShutdownHook` 会等待应用程序完成关闭后再停止 Logback，最长等待窗口为 180 秒。主日志和 gRPC 的异步 appender 随后最多允许 5 秒排空各自的队列。

`kill -9` 等强制终止、JVM 崩溃或操作系统故障会绕过正常的关闭钩子，因此仍可能丢失缓冲区中的日志。

## 由日志生成的 Prometheus 指标

启用 Prometheus 监控后，默认添加到 root logger 的 `METRICS` appender 会为到达 root logger 的 `ERROR` 事件递增 `tron:error_info_total`。该指标的标签为 logger 名称和异常类型。

配置了 `additivity="false"` 的专用 logger 不会向 root logger 传播日志。在默认配置中，`LEVELDB`、`ROCKSDB` 和 `io.grpc` 均采用此设置。因此，仅写入 `db.log` 或 `grpc.log` 的 `ERROR` 日志不会递增 `tron:error_info_total`。`DB` logger 允许向 root logger 传播日志，因此仍会被该指标统计。应将该指标视为传播到 root logger 的应用错误信号，而不是所有日志文件中每一条 `ERROR` 日志的总数。Prometheus 配置方法参见[节点监控](metrics.md)。

## 排查问题时调整日志级别

仅在排查特定组件问题时修改日志级别，并在收集完所需诊断信息后恢复默认级别。

root logger 和许多 java-tron 模块 logger 的默认级别均为 `INFO`。显式配置了级别的模块 logger 不会继承 root logger 的级别，因此调整日志输出时应修改相应的模块 logger。

例如，仅保留 `WARN` 及以上级别的 P2P 网络日志：

```xml
<logger name="net" level="WARN"/>
```

启用 Prometheus 监控后，java-tron 会在启动时收集数据库统计信息，之后每六小时收集一次。使用以下配置在主日志中启用其调试输出：

```xml
<logger name="metrics" level="DEBUG"/>
```

`io.grpc` logger 配置了 `additivity="false"`，默认只通过 `GRPC` appender 写入日志。修改其自身级别以控制 `grpc.log`：

```xml
<logger name="io.grpc" level="WARN" additivity="false">
  <appender-ref ref="GRPC"/>
</logger>
```

避免在生产节点上长时间全局启用 `DEBUG` 或 `TRACE`，这些级别可能会产生大量日志。
