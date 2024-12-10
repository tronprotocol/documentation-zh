# Java-tron节点维护工具 - Toolkit

Toolkit工具箱集成了一系列java-tron周边工具，未来还将向其增加更多的功能，以方便开发者使用。目前Toolkit包括的功能如下：

* [数据存储分区](#_1)
* [轻节点数据裁剪](#_6)
* [数据拷贝](#_9)
* [数据转换](#_11)
* [LevelDB启动优化](#leveldb)

下面详细介绍Toolkit工具箱的获取及使用。

## Toolkit的获取
可以通过编译java-tron源代码或者从已发布版本直接获取 [`Toolkit.jar`](https://github.com/tronprotocol/java-tron/releases)

编译源码：

1. 获取java-tron源码
   ```
   $ git clone https://github.com/tronprotocol/java-tron.git
   $ git checkout -t origin/master
   ```
2. 编译

   ```
   $ cd java-tron
   $ ./gradlew clean build -x test
   ```

   编译完成之后，`Toolkit.jar`会生成在 `java-tron/build/libs/` 目录下。

## 数据库存储分区工具
随着链上数据持续增长，数据存储压力会越来越大，目前TRON公链的全节点数据已达到1T，每日数据增长约1.2G，按照目前数据增长速度，一年增长450G左右。用户单个磁盘可能会遇到容量不足的情况，需要更换更大的磁盘，为此Toolkit工具箱引入了数据库存储分区工具，工具能够根据用户的配置，将部分数据迁移到其他存储盘，当用户遇到磁盘空间不足时，只需要根据容量需求增加磁盘即可，无需更换原来的磁盘。

### 命令及参数
通过`db mv`来使用Toolkit提供的数据迁移存储功能：

```
# full command
java -jar Toolkit.jar db mv [-h] [-c=<config>] [-d=<database>]
# examples
java -jar Toolkit.jar db mv -c main_net_config.conf -d /data/tron/output-directory
```

可选命令参数如下：

- `-c | --config`: [ string ]  此选项用于指定 FullNode 配置文件,不指定会使用默认值：config.conf。
- `-d | --database-directory`: [ string ]  此选项用于指定FullNode数据库目录,不指定会使用默认值：output-directory。
- `-h | --help`: [ bool ]  此选项用于查看帮助，默认值：false。


### 使用说明
请按如下步骤使用数据库存储分区工具：

1. [停止 FullNode 服务](#fullnode)
2. [数据库存储迁移配置](#_4)
3. [执行数据库迁移](#_5)
4. [重新启动 FullNode 服务](#fullnode_1)


#### 停止 FullNode 服务

使用命令`kill -15 pid`关闭FullNode.jar，FullNode进程pid查找命令: 
```
$ ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
```


#### 数据库存储迁移配置

数据库迁移的配置在Java-tron节点配置文件中的 [storage.properties](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf#L37) 字段。下面以只迁移`block` 和 `trans` 数据库为例，说明如何将部分数据库迁移到其它存储盘：

```conf
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
`name`是数据库名称,`path`是数据库迁移的目的目录，工具会将`name`指定的数据库迁移到`path`指定的目录，然后会在原来的目录下创建一个软链接指向`path`目录，`FullNode`启动后会根据软链接寻找到`path`目录。


#### 执行数据库迁移

执行命令如下，执行后会显示当前迁移进度。

```bash
$ java -jar Toolkit.jar db mv -c main_net_config.conf -d /data/tron/output-directory
```

#### 重新启动 FullNode 服务
迁移完成后，重新启动Java-tron节点。
```
# FullNode
$ nohup java -Xms9G -Xmx9G -XX:ReservedCodeCacheSize=256m \
                -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
                -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
                -XX:+PrintGCDateStamps  -Xloggc:gc.log \
                -XX:+UseConcMarkSweepGC -XX:NewRatio=2 \
                -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
                -XX:+HeapDumpOnOutOfMemoryError \
                -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
                -jar FullNode.jar -c main_net_config.conf >> start.log 2>&1 &

# Super representitive's FullNode
$ nohup java -Xms9G -Xmx9G -XX:ReservedCodeCacheSize=256m \
               -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
               -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
               -XX:+PrintGCDateStamps  -Xloggc:gc.log \
               -XX:+UseConcMarkSweepGC -XX:NewRatio=2 \
               -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
               -XX:+HeapDumpOnOutOfMemoryError \
               -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
               -jar FullNode.jar --witness -c main_net_config.conf >> start.log 2>&1 &
```
## 轻节点数据剪裁工具

Toolkit提供数据剪裁工具，主要用于轻节点数据的生成以及轻节点数据的剪裁。

数据剪裁工具根据当前`最新区块高度`(latest_block_number)可将完整数据切分成快照数据集（Snapshot dataset）或历史数据集（History dataset），快照数据集用于启动轻节点，历史数据集用于历史数据查询。通过快照数据集启动的轻节点不支持查询剪裁时的最新区块高度之前的历史数据。数据剪裁工具还提供了将历史数据集同快照数据集合并的功能，使用场景如下：

* 将全节点数据切分成轻节点数据

轻节点只基于快照数据集启动，使用数据剪裁工具将全节点数据切分成快照数据集，即得到轻节点数据。

* 定期剪裁轻节点数据

由于轻节点启动后，会保存与全节点同样的数据，所以轻节点虽然在启动时数据量非常小，但是后期的数据膨胀速度与全节点相同，因此可能需要定期剪裁数据。裁剪轻节点数据也是使用数据剪裁工具将轻节点数据切分成快照数据集，即得到裁剪后的轻节点数据。

* 将轻节点数据转回全节点数据

由于轻节点不支持历史数据查询，如果要支持，则需要将轻节点数据变为全节点数据，那么该节点也就从轻节点变成了全节点。可以直接下载全节点数据库快照实现，也可以使用数据剪裁工具：首先将全节点数据切分成历史数据集，再合并历史数据集与轻节点的快照数据集，得到全节点数据。



注意：使用本工具进行任何操作之前，需要首先停止当前运行的节点。 



### 命令及参数
通过`db lite`指令来使用Toolkit提供的数据剪裁工具：
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
可选命令参数如下：

- `--operation | -o`: [ split | merge ]  此选项用于指定使用拆分功能还是合并功能，默认为split。
- `--type | -t`: [ snapshot | history ]  此选项只能同`-o split`配合使用。 `snapshot` 指示切分为快照数据集，`history`指示切分为历史数据集。 
- `--fn-data-path | -fn`: 当操作类型是 `split`时, `fn-data-path` 用于指示待剪裁数据的目录；当操作类型是 `merge`时， `fn-data-path`指示轻节点的数据库目录或者快照数据集的目录。
- `--dataset-path | -ds`: 当操作类型是 `split`时, `dataset-path` 用于指示切分完成的快照数据集或历史数据集输出目录；当操作类型是 `merge`时， `dataset-path`指示历史数据集目录。


### 使用说明
节点数据库默认保存在`output-directory/database`目录下，本章节中的例子将以默认数据库目录进行说明。


下面通过以下三个例子来说明如何使用数据剪裁工具：

* **切分快照数据集**
    该功能可将全节点数据转换成轻节点数据，也可用于定期剪裁轻节点数据，步骤如下：
    
    首先, 停止节点然后执行命令:

    ```shell
    # 简单起见，将快照数据集存放在`/tmp`目录下
    java -jar Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
    ```

    * --fn-data-path： 待剪裁数据目录，即节点数据目录
    * --dataset-path： 存放输出的快照数据集的目录

    命令执行完毕之后，将在`/tmp`目录下生成`snapshot`目录，此目录中的数据即为轻节点数据，将该目录中的数据拷贝到节点数据库目录中即可。假设节点的数据库目录为`output-directory/database`, 则可以将`snapshot`目录名修改为`database`，并拷贝到Lite FullNode的运行目录output-directory之下，完成轻节点数据剪裁，最后启动轻节点。 

* **切分历史数据集**
    
    切分历史数据集的命令如下：

    ```shell
    # 简单起见，将历史数据集存放在`/tmp`目录下
    java -jar Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
    ```

    * --fn-data-path： 全节点数据目录
    * --dataset-path： 存放输出的历史数据集的目录


    命令执行完毕之后，将在`/tmp`目录下生成`history`目录，即切分好的历史数据集。
    
* **合并历史数据集和快照数据集**

    历史数据集和快照数据集中都保存了一个info.properties文件，用于记录数据拆分时的区块高度。需要注意的是，两个数据集进行合并时，历史数据集的区块高度必须大于等于快照数据集的区块高度。通过merge操作将历史数据集同快照数据集进行合并之后，轻节点将成为一个真正的全节点。

    合并历史数据集和快照数据集的命令如下：
    
    ```shell
    # 简单起见，假设历史数据集存放在了`/tmp`目录下
    java -jar Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
    ```

    * --fn-data-path： 快照数据集目录
    * --dataset-path： 历史数据集目录


    命令执行完毕后，合并后的数据将覆盖快照数据集所在目录，即`--fn-data-path`指定的目录，将合并完成的数据拷贝到节点数据库目录下，轻节点变成一个全节点。
    
    
## 数据拷贝
节点数据库较大，数据库拷贝操作较耗时，而Toolkit工具箱提供数据库快速拷贝功能，通过创建一个硬链接来实现在同一文件系统中快速的拷贝LevelDB或者RocksDB数据库。

### 命令及参数
通过`db copy`来使用Toolkit提供的数据拷贝功能：

```shell
# full command
  java -jar Toolkit.jar db cp [-h] <src> <dest>
# examples
  java -jar Toolkit.jar db cp  output-directory/database /tmp/databse
```

可选命令参数如下：

- `<src>`: 此选项用于指定数据库目录，默认值为： `output-directory/database`
- `<dest>`: 拷贝的目标目录，默认值为： `output-directory-cp/database`
- `-h | --help`：[ bool ]  此选项用于查看帮助，默认值：false。

注意：使用本工具进行任何操作之前，需要首先停止当前运行的节点。 

## 数据转换

Toolkit工具箱支持数据库数据转换功能，可以将LevelDB的数据转换RocksDB数据。

### 命令及参数
通过`db convert`来使用Toolkit提供的数据转换功能：

```
# full command
  java -jar Toolkit.jar db convert [-h] [--safe] <src> <dest>
# examples
  java -jar Toolkit.jar db convert  output-directory/database /tmp/database
```

可选命令参数如下：

- `<src>`: 此选项用于指定LevelDB数据目录，默认值为： `output-directory/database`
- `<dest>`: 输出的RocksDB数据目录，默认值为： `output-directory-dst/database`
- `--safe`：是否以安全模式转换数据，默认为false。如果采用安全模式，则从leveldb读取数据然后写入rocksdb中，整个过程耗时较长。如果不采用安全模式，由于在当前版本中rocksdb与leveldb兼容，所以仅仅是将`engine.properties`配置项从leveldb更改为rocksdb。
- `-h | --help`：[ bool ]  此选项用于查看帮助，默认值：false。

注意：使用本工具进行任何操作之前，需要首先停止当前运行的节点。 

## LevelDB启动优化

随着levelDB的运行，levelDB manifest文件会持续增长，过大的manifest文件不但影响节点启动速度，而且还有可能出现由于内存持续增长导致服务异常中止的问题。 为了解决这一问题，Toolkit工具箱提供LevelDB启动优化工具，该工具可以优化manifest的文件大小以及LevelDB的启动过程，减少内存占用，提升节点启动速度。

### 命令及参数
通过`db archive`来使用Toolkit提供的LevelDB启动优化功能：

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

可选命令参数如下：

- `-b | --batch-size`: 指定manifest batch size，默认值为： 80000
- `-d | --database-directory`: LevelDB数据库目录，默认值为： `output-directory/database`
- `-m | --manifest-size`: manifest文件大小的最小值，manifest文件大小低于此值时，不进行处理，高于该值时才进行批处理，单位:M，默认值:0。
- `-h | --help`：[ bool ]  此选项用于查看帮助，默认值：false。

注意：使用本工具进行任何操作之前，需要首先停止当前运行的节点。 使用指南请参考[archive manifest](../../developers/archive-manifest/)。
