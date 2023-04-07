# 数据库存储分区插件

## 介绍

伴随java-tron运行，链上数据持续增长，数据存储压力会随之而来，目前tron链上全节点数据已接近1T，每日数据增长1.2G，按照目前数据增长情况，
一年增长450G，之后增长速度会更快。用户为了读写性能，可能采用比较昂贵的磁盘，如SSD等，存储成本会越来越高。
为此在`GreatVoyage-v4.5.2(xxx)`引入数据库存储分区插件，插件能够根据用户对数据库配置，将数据迁移到其他存储盘，如SATA。

使用本工具进行任何操作之前，需要首先停止当前运行FullNode节点。 此工具提供根据当前`数据库配置`情况,对数据进行迁移存储功能。


## 使用

### 插件选项

此工具提供数据进行迁移存储功能

- `-c | --config`: [ string ]  此选项用于指定 FullNode 配置文件,默认值：config.conf。
- `-d | --database-directory`: [ string ]  此选项用于指定FullNode数据库目录,默认值：output-directory。
- `-h | --help`: [ bool ]  此选项用于查看帮助，默认值：false。

### 获取方式
  在java-tron 下，执行 `./gradlew build -xtest` ，在 `build/libs/`下可找到Toolkit.jar。

### 使用步骤

1. 停止 FullNode 服务。
2. 进行数据库存储迁移配置。
3. 执行 Toolkit 数据库迁移命令。
4. 启动 FullNode 服务。


### 使用说明

FullNode 运行之后，如果没有指定`-d ` 参数，默认数据库目录：`output-directory`。

#### 步骤一： 停止 FullNode 服务

使用命令`kill -15`关闭FullNode.jar

查找 pid: `ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`。


#### 步骤二： 进行数据库存储迁移配置

数据库相关配置存在conf文件中 [storage.properties](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf#L37) 模块

以迁移`block` 和 `trans` 库为例

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


##### 步骤三：执行 Toolkit 数据库迁移命令
执行后会显示当前迁移进度
 ```bash
 #help
   $ java -jar Toolkit.jar db mv -h

 #use default
  $ java -jar Toolkit.jar db mv

 #use customization
  $ java -jar Toolkit.jar db mv -c main_net_config.conf -d /data/tron/output-directory
```

##### 步骤四：启动 FullNode 服务

 ```bash
 #full node
   $ nohup java -Xms9G -Xmx9G -XX:ReservedCodeCacheSize=256m \
                -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
                -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
                -XX:+PrintGCDateStamps  -Xloggc:gc.log \
                -XX:+UseConcMarkSweepGC -XX:NewRatio=2 \
                -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
                -XX:+HeapDumpOnOutOfMemoryError \
                -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
                -jar FullNode.jar -c main_net_config.conf >> start.log 2>&1 &

 #sr node
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
