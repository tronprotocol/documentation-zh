# 数据备份和恢复

Java-Tron会将持久化存储的数据写入到数据目录，默认的数据目录为：`/output-directory/`，如需指定其它目录，可以在java-tron节点启动命令中加入 `-d` 或者 `--output-directory` 参数来指定数据存储位置。
```
$ java -jar fullnode.jar -d ./outputdir
```

# 数据备份
对节点数据进行备份之前，请先关闭节点进程。具体请参考如下步骤：

首先，使用命令`$ ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'` 获取java-tron的进程id，然后使用命令`kill -15 进程id` 关闭进程。或者使用如下的停止脚本：

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

然后，当关闭了Java-tron进程后，可通过如下命令进行数据的备份。

```
$ tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
```

# 数据恢复

当恢复数据时，只需将相应的数据拷贝到节点目录下即可。假如数据库备份文件名为`output-directory.20220628152402.etgz`，则恢复数据库文件的命令为：

```
$ tar xzvf output-directory.20220628152402.etgz
```

# 公共备份数据 

对于主网和nile测试网，由于新节点启动后，需要同步的数据量较大，因此同步数据需要较长的时间。为了方便开发者进行快速的节点部署，社区定期提供数据快照。数据快照是TRON网络节点某一时刻的数据库备份的压缩文件，开发者可以通过下载并使用数据快照加快节点同步过程。

### FullNode数据快照

下表为Fullnode数据快照的下载地址，请根据所在地和节点数据库类型，以及是否需要查询历史内部交易等需求选择适合的数据快照。


| Fullnode节点数据源 | 下载地址 | 说明 |
| -------- | -------- | -------- |
| 官方数据源(美洲:美国弗吉尼亚)   | http://34.86.86.229/     | LevelDB数据，不包含内部交易 (截止2024-8-6 约1821G)    |
| 官方数据源(亚洲:新加坡)     | http://34.143.247.77/    | LevelDB数据，不包含内部交易 (截止2024-8-5 约1819G)    |
| 官方数据源(亚洲:新加坡)     | http://35.197.17.205/     | RocksDB数据，不包含内部交易 (截止2024-8-6 约1799G)    |
| 官方数据源(亚洲:新加坡)     | http://35.247.128.170/    | LevelDB数据，包含内部交易（截止2024-8-6 约2000G）    |
| 官方数据源(美洲:美国弗吉尼亚)     | http://34.48.6.163/    | LevelDB数据，不包含内部交易，包含账户历史余额（截止2024-8-6 约2288G）    |

注意：LevelDB和RocksDB的数据不允许混用。FullNode的数据库类型通过配置文件的配置项`db.engine` 进行指定，可选值为`LEVELDB`或者`ROCKSDB`。

Nile测试网数据下载地址：https://database.nileex.io


### Lite FullNode数据快照

TRON网络从GreatVoyage-V4.1.0版本开始，支持Lite FullNode类型的节点。相比于普通的FullNode，Lite FullNode不但数据库小，而且启动速度快，它只需要状态数据和必要的历史数据就可以启动。下表为Lite Fullnode数据快照的下载地址。

| Lite Fullnode节点数据源 | 下载地址 | 说明 |
| -------- | -------- | -------- |
| 官方数据源(美洲:美国弗吉尼亚)   | http://34.143.247.77/    | LevelDB数据，截止2024-8-5 约42G    |

小提示：如果用户已经有Fullnode的全量数据，可以使用[Lite FullNode数据剪裁工具](../../using_javatron/toolkit/#_6)自行将fullnode数据切分成Lite fullnode数据。

### 数据快照的使用

无论是Fullnode数据快照还是lite Fullnode数据快照，使用步骤相同，具体如下：

  1. 根据自己需求下载相应压缩备份数据库。
  2. 解压备份数据库压缩文件至output-directory目录，或者根据自己需求指定解压的目标目录。
  3. 启动节点。节点默认读取output-directory目录，如需指定其他目录，请在节点启动时，添加参数 -d 数据库目录名


