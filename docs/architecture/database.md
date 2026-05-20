# 数据库配置指南

在 TRON Java 实现（java-tron）中，节点数据存储引擎提供LevelDB和RocksDB两种选择。数据库在不同架构上的区别：

- x86_64架构上，数据库支持LevelDB和RocksDB，当前RocksDB的版本是v5.15.10
- arm64架构上，数据库仅支持RocksDB，当前RocksDB的版本是v9.7.4 

开发者可根据平台环境、硬件条件及性能需求，灵活选择合适的存储引擎。相比之下，RocksDB 提供更丰富的配置参数，且通常具有更高的存储效率。本文将介绍如何启用 RocksDB，以及如何将 x86_64 平台的 LevelDB 转换为 RocksDB。


## 使用 RocksDB

### 1. 配置 RocksDB 作为存储引擎

要启用 RocksDB，请在配置文件中设置 `storage.db.engine` 为 `"ROCKSDB"`：

```
storage {
  # 持久化数据的存储引擎
  db.engine = "ROCKSDB"
  db.sync = false
  db.directory = "database"
  transHistory.switch = "on"
}
```

### 2. RocksDB 优化参数
RocksDB 支持多种调优参数，可根据节点服务器性能进行配置。以下是一个推荐的参数示例：
```
dbSettings = {
  levelNumber = 7
  # compactThreads = 32
  blocksize = 64                 # 单位：KB
  maxBytesForLevelBase = 256     # 单位：MB
  maxBytesForLevelMultiplier = 10
  level0FileNumCompactionTrigger = 4
  targetFileSizeBase = 256       # 单位：MB
  targetFileSizeMultiplier = 1
  maxOpenFiles= 5000
}
```



## x86_64 平台从 LevelDB 迁移至 RocksDB
若需从 LevelDB 迁移到 RocksDB，需使用官方提供的转换工具 `Toolkit.jar`。

> **注意**：`db convert` 子命令仅支持 x86_64。在 arm64 上执行时会打印 "unsupported architecture" 提示后直接退出，不会进行任何转换。

### 1. 数据转换步骤
```
cd java-tron                                   # 源码根目录
./gradlew build -xtest -xcheck                 # 编译项目                        
java -jar build/libs/Toolkit.jar db convert    # 执行数据转换
```
### 2. 位置参数
若您的节点使用了自定义的数据目录，可在 `db convert` 后按顺序追加两个位置参数，分别指定 LevelDB 源路径与 RocksDB 目标路径：

```
java -jar build/libs/Toolkit.jar db convert <src> <dst>
```

- `<src>`：LevelDB 数据库路径（默认为 `output-directory/database`）
- `<dst>`：RocksDB 数据库存储路径（默认为 `output-directory-dst/database`）

例如，若节点是通过如下方式运行：
```
nohup java -jar build/libs/FullNode.jar -d your_database_dir &
```
则应使用如下命令进行转换：
```
java -jar build/libs/Toolkit.jar db convert  your_database_dir/database output-directory-dst/database
```
### 3. 停止节点后进行转换
> **必须节点停止运行后再执行数据转换操作**。

若希望减少停机时间，可按照以下流程操作：

1. 停止节点运行；
2. 复制原始 LevelDB 数据目录至新目录；
3. 重新启动节点（继续使用原目录）；
4. 在新目录中执行数据转换操作。

示例命令如下：

```
java -jar build/libs/Toolkit.jar db cp output-directory/database /tmp/output-directory/database
cd /tmp
java -jar build/libs/Toolkit.jar db convert output-directory/database output-directory-dst/database
```

>备注：
整个数据转换过程预计耗时约 **10 小时**，具体时间依赖于数据量和磁盘性能。

## 关于 LevelDB
LevelDB 是 x86_64 平台 java-tron 节点默认的数据存储引擎，适用于资源有限或轻量级的部署场景。它结构简单、易于维护，但在数据压缩、备份能力和大规模节点性能上不如 RocksDB。
