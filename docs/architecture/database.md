# 数据库配置
java-tron数据存储支持使用 LevelDB 或者 RocksDB，默认使用LevelDB。您也可以选择RocksDB，它提供了丰富的配置参数，允许节点根据自身机器配置情况进行调优，节点数据库占用的磁盘空间相比于LevelDB更少，同时RocksDB支持在运行时进行数据备份，备份时间仅需要几秒钟。

下面介绍如何将java-tron节点的存储引擎设置成RocksDB，以及如何进行leveldb和rocksdb的数据转换。
# rocksdb

### 1. config配置说明

 使用rocksdb作为数据存储引擎，需要将db.engine配置项设置为"ROCKSDB"
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/db_engine.png)
 注意: rocksdb只支持db.version=2, 不支持db.version=1。
 rocksdb支持的优化参数如下：
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/rocksdb_tuning_parameters.png)

### 2. 使用rocksdb数据备份功能

 选择rocksdb作为数据存储引擎，可以使用其提供的运行时数据备份功能。
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/db_backup.png)
 注意: FullNode可以使用数据备份功能；为了不影响SuperNode的产块性能，数据备份功能不支持SuperNode，但是SuperNode的备份服务节点可以使用此功能。

### 3. leveldb数据转换为rocksdb数据

  leveldb和rocksdb的数据存储架构并不兼容，请确保节点始终使用同一种数据引擎。我们提供了数据转换脚本，用于将leveldb数据转换到rocksdb数据。
  使用方法：

```text
cd 源代码根目录
./gradlew build   #编译源代码
java -jar build/libs/DBConvert.jar  #执行数据转换指令
```

  注意：如果节点的数据存储目录是自定义的，运行DBConvert.jar时添加下面2个可选参数。

  **src_db_path**:指定LevelDB数据库路径源，默认是 output-directory/database

  **dst_db_path**:指定RocksDB数据库路径，默认是 output-directory-dst/database

  例如，如果节点是像这样的脚本运行的:

```shell
nohup java -jar FullNode.jar -d your_database_dir &
```

  那么，你应该这样运行数据转换工具DBConvert.jar:

```shell
java -jar build/libs/DBConvert.jar  your_database_dir/database  output-directory-dst/database
```

  注意：必须停止节点的运行，然后再运行数据转换脚本。
  如果不希望节点停止时间太长，可以在节点停止后先将leveldb数据目录output-directory拷贝一份到新的目录下，然后恢复节点的运行。

  在新目录的上级目录中执行DBConvert.jar并指定参数`src_db_path`和`dst_db_path` 。
  例如:

```shell
cp -rf output-directory /tmp/output-directory
cd /tmp
java -jar DBConvert.jar output-directory/database  output-directory-dst/database
```

  整个的数据转换过程可能需要10个小时左右。

### 4. rocksdb与leveldb的对比

你可以查看以下文档获取详细的信息：
[rocksdb与leveldb对比](https://github.com/tronprotocol/documentation/blob/master/TRX_CN/Rocksdb_vs_Leveldb.md)
