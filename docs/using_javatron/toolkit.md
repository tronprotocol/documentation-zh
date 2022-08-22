# 数据库存储分区工具


随着链上数据持续增长，数据存储压力会越来越大，目前TRON公链的全节点数据已接近1T，每日数据增长约1.2G，按照目前数据增长速度，一年增长450G左右。用户单个磁盘可能会遇到容量不足的情况，需要更换更大的磁盘，为此在`GreatVoyage-v4.5.2 (Aurelius)`引入数据库存储分区工具，工具能够根据用户的配置，将部分数据迁移到其他存储盘，当用户遇到磁盘空间不足时，只需要根据容量需求增加磁盘即可，无需更换原来的磁盘。
 

## 编译
在java-tron工程下，执行`./gradlew build -x test`，工具会生成在`build/libs/Toolkit.jar`。
  
## 选项

此工具提供数据迁移存储功能，可选命令参数如下：

- `-c | --config`: [ string ]  此选项用于指定 FullNode 配置文件,不指定会使用默认值：config.conf。
- `-d | --database-directory`: [ string ]  此选项用于指定FullNode数据库目录,不指定会使用默认值：output-directory。
- `-h | --help`: [ bool ]  此选项用于查看帮助，默认值：false。



## 使用说明
请按如下步骤使用数据库存储分区工具：

1. [停止 FullNode 服务](#fullnode)
2. [数据库存储迁移配置](#_5)
3. [执行数据库迁移](#_6)
4. [重新启动 FullNode 服务](#fullnode_1)


### 停止 FullNode 服务

使用命令`kill -15 pid`关闭FullNode.jar，FullNode进程pid查找命令: 
```
$ ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
```


### 数据库存储迁移配置

数据库迁移的配置在Java-tron节点配置文件中 [storage.properties](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf#L37) 字段。下面以只迁移`block` 和 `trans` 数据库为例，说明如何将部分数据库迁移到其它存储盘：

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
`name`是数据库名称,`path`是数据库迁移的目的目录，工具会将`name`指定的数据库迁移到`path`指定的目录，然后会在原来的路径下创建一个软链接指向`path`目录，`FullNode`启动后会根据软链接寻找到`path`目录。


### 执行数据库迁移

执行后会显示当前迁移进度。

```bash
$ java -jar Toolkit.jar db mv -c main_net_config.conf -d /data/tron/output-directory
```

### 重新启动 FullNode 服务
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