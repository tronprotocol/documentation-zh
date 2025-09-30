# TRON 网络节点数据备份与恢复

java-tron 节点将其持久化数据存储在指定的数据目录下。默认的数据目录是 `/output-directory/`。您可以通过在 java-tron 节点启动命令中添加 `-d` 或 `--output-directory` 参数来指定不同的数据存储位置，例如：

```
java -jar fullnode.jar -d ./outputdir
```


## 备份节点数据

在备份节点数据之前，请务必 **关闭节点进程**。您可以按照以下步骤进行操作：

首先，使用以下命令获取 java-tron 进程的 PID：

```
ps -ef | grep FullNode.jar | grep -v grep | awk '{print $2}'
```

然后，使用获取到的 PID 来终止进程。建议使用以下停止脚本来安全关闭 java-tron 进程，以避免数据库损坏：

```
#!/bin/bash
while true; do
  pid=`ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
  if [ -n "$pid" ]; then
    kill -15 $pid
    echo "The java-tron process is exiting, it may take some time, forcing the exit may cause damage to the database, please wait patiently..."
    sleep 1
  else
    echo "java-tron killed successfully!"
    break
  fi
done
```

当 java-tron 进程成功关闭后，您可以使用以下命令进行数据备份：

```
tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
```


## 恢复节点数据

恢复数据非常简单，只需将备份的数据复制到节点的数据目录下即可。

如果您的数据库备份文件名为 `output-directory.20220628152402.etgz`，您可以使用以下命令来恢复数据库文件：

```
tar xzvf output-directory.20220628152402.etgz
```

## 使用公共备份数据（数据快照）

对于主网和 Nile 测试网，由于新节点启动时需要同步的数据量巨大，这会导致同步过程耗时较长。为了方便开发者快速部署节点，TRON 社区会定期提供 **数据快照**。

数据快照是 TRON 网络节点在某个特定时刻的数据库备份压缩文件。开发者可以通过下载并使用数据快照来显著加快节点的同步过程。

### 主网数据快照

#### FullNode 数据快照

下表列出了 FullNode 数据快照的下载地址。请根据您所在的地理位置、节点数据库类型以及是否需要查询历史内部交易等需求，选择最适合的数据快照。

| FullNode 节点数据源 | 下载地址 | 说明 |
| :------------------ | :------- | :--- |
| 官方数据源 (美洲: 美国弗吉尼亚) | [http://34.86.86.229/](http://34.86.86.229/) | LevelDB 数据，不包含内部交易 |
| 官方数据源 (亚洲: 新加坡) | [http://34.143.247.77/](http://34.143.247.77/) | LevelDB 数据，不包含内部交易 |
| 官方数据源 (美洲: 美国) | [http://35.197.17.205/](http://35.197.17.205/) | RocksDB 数据，不包含内部交易 |
| 官方数据源 (亚洲: 新加坡) | [http://35.247.128.170/](http://35.247.128.170/) | LevelDB 数据，包含内部交易 |
| 官方数据源 (美洲: 美国弗吉尼亚) | [http://34.48.6.163/](http://34.48.6.163/) | LevelDB 数据，不包含内部交易，包含账户历史余额 |

**注意：** **LevelDB** 和 **RocksDB** 数据不允许混用。FullNode 的数据库类型通过配置文件中的 `db.engine` 配置项指定，可选值为 `LEVELDB` 或 `ROCKSDB`。

#### Lite FullNode 数据快照

TRON 网络从 GreatVoyage-V4.1.0 版本开始支持 **Lite FullNode** 类型的节点。相比于普通的 FullNode，Lite FullNode 拥有更小的数据库和更快的启动速度，因为它只需要状态数据和必要的历史数据即可启动。下表列出了 Lite FullNode 数据快照的下载地址。

| Lite FullNode 节点数据源 | 下载地址 | 说明 |
| :----------------------- | :------- | :--- |
| 官方数据源 (亚洲: 新加坡) | [http://34.143.247.77/](http://34.143.247.77/) | LevelDB 数据 |

**小提示：** 如果您已经拥有 FullNode 的全量数据，可以使用 [Lite FullNode 数据裁剪工具](https://tronprotocol.github.io/documentation-zh/using_javatron/toolkit/#_6)自行将 FullNode 数据裁剪为 Lite FullNode 数据。

#### 数据快照的解压方式
TRON 网络快照数据大小通常超过 2TB。我们强烈推荐使用流式处理方式（即边下载边解压），以有效节省您的磁盘空间。具体操作命令如下：

```
wget -q -O - SNAPSHOT_URL/FullNode_output-directory.tgz | tar -zxvf -
```

##### 方法 1：流式下载并解压（推荐，节省空间）

此方法无需先存储完整的压缩包，而是直接将数据解压到目标目录，显著减少了磁盘占用。

##### 方法 2：先下载后解压（需充足存储空间）

```
# 1. 下载完整快照文件
wget SNAPSHOT_URL/FullNode_output-directory.tgz

# 2. 解压文件
tar -zxvf FullNode_output-directory.tgz
```

此方法会先下载完整的快照文件，然后再进行解压。请注意，解压时您需要同时保留压缩包和解压后的文件，因此建议至少准备两个 3TB 或更大的磁盘（一个用于存储压缩包，另一个用于存储解压后的数据。解压完成后，您可以释放用于存储压缩包的磁盘，从而节省成本）。

#### 数据快照的使用步骤

无论是 FullNode 数据快照还是 Lite FullNode 数据快照，使用步骤都相同：

1.  根据您的需求下载相应的压缩备份数据库文件。
2.  将备份的数据库压缩文件解压到 `output-directory` 目录。如果您希望指定其他目录，也可以将其解压到指定的目标目录。
3.  启动节点。节点默认读取 `output-directory` 目录。如果您的数据解压到了其他目录，请在节点启动时添加 `-d` 参数并指定数据库目录名。

### Nile 测试网数据快照

关于 Nile 测试网数据快照的详细信息，请参照 [官网](https://nileex.io/)。使用方法与主网数据快照相同。
