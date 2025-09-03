# Toolkit：Java-tron节点维护工具集

TRON Toolkit 是一个集成了多种 `java-tron` 周边工具的实用程序，旨在简化节点维护和管理任务。未来，我们将持续为其添加更多功能，以提升开发者的使用体验。目前，Toolkit 提供了以下核心功能：

* [数据存储分区](#_2) - 解决链上数据增长带来的存储压力
* [轻节点数据裁剪](#_5) - 轻节点数据定期剪裁
* [数据拷贝](#_11) - 实现数据库快速拷贝
* [数据转换](#_13) - 支持 LevelDB 到 RocksDB 的数据库格式转换
* [LevelDB启动优化](#leveldb) - 加快数据库类型为LevelDB的节点启动速度

本文将详细介绍如何获取和使用 TRON Toolkit。

## Toolkit的获取
您可以通过编译 `java-tron` 源代码或直接从已发布的版本中获取 `Toolkit.jar` 文件。推荐从 [GitHub Releases](https://github.com/tronprotocol/java-tron/releases) 下载最新版本。

### 从源代码编译

1. **克隆 `java-tron` 源代码仓库**：
   ```
   $ git clone https://github.com/tronprotocol/java-tron.git
   $ git checkout -t origin/master
   ```
2. **编译项目**：
   ```
   $ cd java-tron
   $ ./gradlew clean build -x test
   ```

编译成功后，`Toolkit.jar` 文件将生成在 `java-tron/build/libs/` 目录下。

## 数据存储分区工具
随着 TRON 链上数据的持续增长（目前主网全节点数据已达 2TB，每日增长约 1.2GB），节点的数据存储压力日益增大。为了解决单个磁盘容量不足的问题，TRON Toolkit 引入了**数据库存储分区工具**。该工具允许您根据配置将部分数据库迁移到其他存储盘，从而在磁盘空间不足时，无需更换原有磁盘，只需增加新的存储设备即可。

### 命令与参数
使用 `db mv` 命令来执行数据迁移操作：

```
# full command
java -jar Toolkit.jar db mv [-h] [-c=<config>] [-d=<database>]
# examples
java -jar Toolkit.jar db mv -c config.conf -d /data/tron/output-directory
```

**可选参数**：

*   `-c | --config <string>`：指定 FullNode 配置文件路径。默认值为 `config.conf`。
*   `-d | --database-directory <string>`：指定 FullNode 数据库目录。默认值为 `output-directory`。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

### 使用步骤

请按照以下步骤使用数据库存储分区工具：

1. [停止 FullNode 服务](#1-fullnode)
2. [配置数据库存储迁移](#2)
3. [执行数据库迁移](#3)
4. [重新启动 FullNode 服务](#4-fullnode)


#### 1. 停止 FullNode 服务
在执行数据库迁移之前，**必须**停止当前运行的 FullNode 服务。您可以使用以下命令查找 FullNode 进程 ID（PID）并终止进程：
```
kill -15 $(ps -ef | grep FullNode.jar | grep -v grep | awk '{print $2}')
```


#### 2. 配置数据库存储迁移
数据库迁移的配置通过 `java-tron` 节点配置文件中的 `storage.properties` 字段进行。您可以在 [java-tron 仓库](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf#L38) 中找到示例配置。

以下示例展示了如何将 `block` 和 `trans` 数据库迁移到 `/data1/tron` 目录：

```
storage {
 ......
  properties = [
    {
     name = "block",
     path = "/data1/tron",

    },
    {
     name = "trans",
     path = "/data1/tron",
   }
  ]
 ......
}

```

*   `name`：指定要迁移的数据库名称。
*   `path`：指定数据库迁移的目标目录。

工具会将 `name` 指定的数据库迁移到 `path` 指定的目录，并在原目录下创建一个软链接指向新目录。FullNode 启动后将通过此软链接找到数据。

#### 3. 执行数据库迁移

配置完成后，执行以下命令进行数据库迁移。命令执行时会显示当前迁移进度：

```
java -jar Toolkit.jar db mv -c config.conf -d /data/tron/output-directory
```

#### 4. 重新启动 FullNode 服务
数据库迁移完成后，重新启动 `java-tron` 节点。

**FullNode 启动命令示例**：

```
nohup java -Xms9G -Xmx9G -XX:ReservedCodeCacheSize=256m \
                -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
                -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
                -XX:+PrintGCDateStamps  -Xloggc:gc.log \
                -XX:+UseConcMarkSweepGC -XX:NewRatio=2 \
                -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
                -XX:+HeapDumpOnOutOfMemoryError \
                -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
                -jar FullNode.jar -c config.conf >> start.log 2>&1 &
```
**超级代表（SR）FullNode 启动命令示例**：
```
nohup java -Xms9G -Xmx9G -XX:ReservedCodeCacheSize=256m \
               -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
               -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
               -XX:+PrintGCDateStamps  -Xloggc:gc.log \
               -XX:+UseConcMarkSweepGC -XX:NewRatio=2 \
               -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
               -XX:+HeapDumpOnOutOfMemoryError \
               -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
               -jar FullNode.jar --witness -c config.conf >> start.log 2>&1 &
```
## 轻节点数据剪裁工具
TRON Toolkit 提供了**数据裁剪工具**，主要用于生成和管理轻节点数据。

全节点的完整数据可被分成两部分：快照数据集（Snapshot dataset）或历史数据集（History dataset）。

*   **快照数据集**：用于启动轻节点，不包含裁剪时的最新区块高度之前的历史数据。
*   **历史数据集**：用于历史数据查询。

快照数据集只包含所有的账户状态数据和最近的 65536 个区块的历史数据。其占用空间小，约为全节点数据的 3%，而轻节点只基于快照数据集来启动，所以，Lite Fullnode 具有占用磁盘空间小，启动速度快的优点。

而数据剪裁工具能够根据当前最新区块高度将FullNode的完整数据切分为**快照数据集**（Snapshot dataset）或**历史数据集**（History dataset）；同时数据裁剪工具还支持将历史数据集与快照数据集进行合并，以满足不同的使用场景：


* **将全节点数据切分成轻节点数据**：通过将全节点数据切分为快照数据集，即可得到用于启动轻节点的数据。
* **定期剪裁轻节点数据**：轻节点启动后数据量会随时间增长，因此可能需要定期裁剪。使用数据裁剪工具将轻节点数据切分为新的快照数据集，即可实现裁剪。
* **将轻节点数据转回全节点数据**：如果需要轻节点支持历史数据查询，可以将其转换为全节点。除了直接下载全节点数据库快照外，您也可以先将全节点数据切分为历史数据集，然后将其与轻节点的快照数据集合并，从而得到一个完整的全节点数据。

> **重要提示**：在使用本工具进行任何操作之前，**必须**停止当前运行的节点。



### 命令与参数
使用 `db lite` 命令来执行数据裁剪操作：
```
# full command
  java -jar Toolkit.jar db lite [-h] -ds=<datasetPath> -fn=<fnDataPath> [-o=<operate>] [-t=<type>]
# examples
  #split and get a snapshot dataset
  java -jar Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
  #split and get a history dataset
  java -jar Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
  #merge history dataset and snapshot dataset
  java -jar Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
```
**可选参数**：

*   `-o | --operation <split | merge>`：指定操作类型，`split`（拆分）或 `merge`（合并）。默认值为 `split`。
*   `-t | --type <snapshot | history>`：仅与 `-o split` 配合使用。`snapshot` 表示切分为快照数据集，`history` 表示切分为历史数据集。
*   `-fn | --fn-data-path <string>`：
    *   当操作类型为 `split` 时，指定待裁剪数据的目录。
    *   当操作类型为 `merge` 时，指定轻节点的数据库目录或快照数据集的目录。
*   `-ds | --dataset-path <string>`：
    *   当操作类型为 `split` 时，指定切分完成的快照数据集或历史数据集的输出目录。
    *   当操作类型为 `merge` 时，指定历史数据集目录。


### 使用示例
节点数据库通常默认保存在 `output-directory/database` 目录下。以下示例将以该默认目录进行说明。

#### 切分快照数据集

此功能可将全节点数据转换为轻节点数据，也可用于定期裁剪轻节点数据。步骤如下：

首先，停止节点，然后执行以下命令：


```
# 简单起见，将快照数据集存放在`/tmp`目录下
java -jar Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
```

* `--fn-data-path`： 待剪裁数据目录，即节点数据目录
* `--dataset-path`： 存放输出的快照数据集的目录

命令执行完毕后，将在 `/tmp` 目录下生成一个名为 `snapshot` 的目录。此目录中的数据即为轻节点数据。将该目录中的数据拷贝到节点数据库目录中（例如，将 `snapshot` 目录重命名为 `database` 并拷贝到 Lite FullNode 的运行目录 `output-directory` 下），然后启动轻节点即可。

#### 切分历史数据集

切分历史数据集的命令如下：

```
# 简单起见，将历史数据集存放在 `/tmp` 目录下
java -jar Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
```

*   `--fn-data-path`：全节点数据目录
*   `--dataset-path`：存放输出的历史数据集的目录

命令执行完毕后，将在 `/tmp` 目录下生成一个名为 `history` 的目录，其中包含切分好的历史数据集。

#### 合并历史数据集和快照数据集

历史数据集和快照数据集中都包含一个 `info.properties` 文件，用于记录数据拆分时的区块高度。
> **请注意**：在合并两个数据集时，历史数据集的区块高度必须大于或等于快照数据集的区块高度。通过 `merge` 操作合并后，轻节点将成为一个真正的全节点。

合并历史数据集和快照数据集的命令如下：

```shell
# 简单起见，假设快照数据集存放在 `/tmp/snapshot`，历史数据集存放在 `/tmp/history`
java -jar Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
```

*   `--fn-data-path`：快照数据集目录。
*   `--dataset-path`：历史数据集目录。

命令执行完毕后，合并后的数据将覆盖 `--fn-data-path` 指定的快照数据集所在目录。将合并完成的数据拷贝到节点数据库目录下，轻节点即可转换为全节点。
    

## 数据拷贝工具

节点数据库通常较大，传统的数据拷贝操作耗时较长。TRON Toolkit 提供了**数据库快速拷贝功能**，通过创建硬链接的方式，在同一磁盘中实现 LevelDB 或 RocksDB 数据库的高效拷贝。

### 命令与参数
使用 `db cp` 命令来执行数据拷贝操作：

```shell
# full command
  java -jar Toolkit.jar db cp [-h] <src> <dest>
# examples
  java -jar Toolkit.jar db cp  output-directory/database /tmp/databse
```

**可选参数**：

*   `<src>`：指定源数据库目录。默认值为 `output-directory/database`。
*   `<dest>`：指定拷贝的目标目录。默认值为 `output-directory-cp/database`。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

> **重要提示**：在使用本工具进行任何操作之前，**必须**停止当前运行的节点。

## 数据转换工具

TRON Toolkit 支持数据库数据转换功能，可以将 LevelDB 格式的数据转换为 RocksDB 格式。

### 命令与参数

使用 `db convert` 命令来执行数据转换操作：


```
# full command
  java -jar Toolkit.jar db convert [-h] [--safe] <src> <dest>
# examples
  java -jar Toolkit.jar db convert  output-directory/database /tmp/database
```

**可选参数**：

*   `<src>`：指定 LevelDB 数据目录。默认值为 `output-directory/database`。
*   `<dest>`：指定输出的 RocksDB 数据目录。默认值为 `output-directory-dst/database`。
*   `--safe <boolean>`：是否以安全模式转换数据。默认值为 `false`，但为了更好的数据兼容性，建议设置成`true`。
    *   如果启用安全模式，工具将从 LevelDB 读取数据并写入 RocksDB，此过程耗时较长。
    *   如果禁用安全模式（默认），由于当前版本中 RocksDB 与 LevelDB 兼容，工具仅会将 `engine.properties` 配置项从 `leveldb` 更改为 `rocksdb`，操作速度更快。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

> **重要提示**：在使用本工具进行任何操作之前，**必须**停止当前运行的节点。

## LevelDB 启动优化工具

随着 LevelDB 数据库的持续运行，其 `manifest` 文件会不断增长。过大的 `manifest` 文件不仅会影响节点启动速度，还可能导致内存持续增长并引发服务异常中止。为了解决这些问题，TRON Toolkit 提供了 **LevelDB 启动优化工具**。该工具可以优化 `manifest` 文件大小和 LevelDB 的启动过程，从而减少内存占用并提升节点启动速度。

### 命令与参数

使用 `db archive` 命令来执行 LevelDB 启动优化操作：


```
# full command
   java -jar Toolkit.jar db archive [-h] [-b=<maxBatchSize>] [-d=<databaseDirectory>] [-m=<maxManifestSize>]
# examples
   #1. use default settings
   java -jar Toolkit.jar db archive 
   #2. specify the database directory as /tmp/db/database
   java -jar Toolkit.jar db archive -d /tmp/db/database 
   #3. specify the batch size to 64000 when optimizing manifest
   java -jar Toolkit.jar db archive -b 64000
   #4. specify optimization only when Manifest exceeds 128M
   java -jar Toolkit.jar db archive -m 128 
```

**可选参数**：

*   `-b | --batch-size <integer>`：指定 `manifest` 批处理大小。默认值为 `80000`。
*   `-d | --database-directory <string>`：指定 LevelDB 数据库目录。默认值为 `output-directory/database`。
*   `-m | --manifest-size <integer>`：`manifest` 文件的最小大小（单位：MB）。当 `manifest` 文件大小低于此值时，不进行处理；高于此值时才进行批处理。默认值为 `0`。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

> **重要提示**：在使用本工具进行任何操作之前，**必须**停止当前运行的节点。

