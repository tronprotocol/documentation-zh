# levelDB 启动优化插件

## 介绍

随着levelDB的运行，manifest文件会持续增长，过大的manifest文件不但影响节点启动速度，而且还有可能会导致内存持续增长系统退出的问题。
为此在`GreatVoyage-v4.3.0(Bacon)`引入了leveldb 启动优化插件，插件优化了manifest的文件大小以及LevelDB的启动过程，减少了内存占用，提升了节点启动速度。

使用本工具进行任何操作之前，需要首先停止当前运行的FullNode节点。 此工具提供了根据当前`数据库`(database)情况,对 manifest 进行重新归整的功能。

更多的设计思想，请参考: [TIP298](https://github.com/tronprotocol/tips/issues/298) 。

## 使用

### 选项

此工具提供了归整manifest 功能

- `-b | --batch-size`: [ int ]  此选项用于指定批处理manifest 大小,默认值：80000。
- `-d | --database-directory`: [ string ]  此选项用于指定FullNode数据库父级目录,默认值：output-directory/database。
- `-m | --manifest-size`: [ int ] 此选项用于指定最小需要批处理manifest 文件大小低于此值，不进行处理，单位M，默认值：0。
- `-h | --help`: [ bool ]  此选项用于查看帮助，默认值：false。

### 获取方式
- 通过编译
  在java-tron 下，执行 ``./gradlew build`` ，在 `build/libs/`下可找到ArchiveManifest.jar。
- 直接下载
  [下载链接](https://github.com/tronprotocol/java-tron/releases)

### 使用步骤

- 1. 确保 FullNode 服务停止。
- 2. 执行 ArchiveManifest 插件。
- 3. 启动 FullNode 服务。

> Note: ``步骤 ii`` 不是每次必需，但是为了优化体验，建议每次执行。

### 使用说明

FullNode 运行之后，默认数据库目录：`output-directory`  ，优化插件会处理 `output-directory/database`目录。

####  1. 单独使用
指定批处理manifest 大小 5120，目录为/tmp/output-directory/database,最小处理大小为 4M。

首先, 停止FullNode并执行命令:

```shell
# 简单起见，将快照数据集存放在`/tmp`目录下
java -jar ArchiveManifest.jar -b 5120 -d /tmp/output-directory/database -m 4
```

命令执行完毕之后，将在`./logs`目录下生成`archive.log`日志, 可查看此次归整情况

#### 2. 集成启动脚本

也可以将此归整插件集成到启动脚本。

```shell
#!/bin/bash

APP=$1

MANIFEST_OPT=$2

ALL_OPT=$*



rebuildManifest() {

 APP=''

 ARCHIVE_JAR='ArchiveManifest.jar'

 if [[ $1 == '-r' ]] ; then

   buildManifest

 elif [[ $2 == '-r' ]]  ; then

   buildManifest

 fi

}


buildManifest() {

 ARCHIVE_JAR='ArchiveManifest.jar'

 echo $ALL_OPT

 java -jar $ARCHIVE_JAR $ALL_OPT

 if [ $? == 0 ] ; then

     echo 'rebuild manifest success'

 else

     echo 'rebuild manifest fail, log in logs/archive.log'

 fi

}



APP=${APP:-"FullNode"}

START_OPT=`echo ${@:2}`

JAR_NAME="$APP.jar"

MAX_STOP_TIME=60

MEM_OPT=''





checkpid() {

 pid=`ps -ef | grep $JAR_NAME |grep -v grep | awk '{print $2}'`

 return $pid

}





stopService() {

  count=1

  while [ $count -le $MAX_STOP_TIME ]; do

    checkpid

    if [ $pid ]; then

       kill -15 $pid

       sleep 1

    else

       echo "java-tron stop"

       return

    fi

    count=$[$count+1]

    if [ $count -eq $MAX_STOP_TIME ]; then

      kill -9 $pid

      sleep 1

    fi

  done

}

startService() {
 echo `date` >> start.log

 total=`cat /proc/meminfo  |grep MemTotal |awk -F ' ' '{print $2}'`

 xmx=`echo "$total/1024/1024*0.6" | bc |awk -F. '{print $1"g"}'`

 directmem=`echo "$total/1024/1024*0.1" | bc |awk -F. '{print $1"g"}'`

 logtime=`date +%Y-%m-%d_%H-%M-%S`

 export LD_PRELOAD="/usr/lib64/libtcmalloc.so"

  nohup java -Xms$xmx -Xmx$xmx -XX:+UseConcMarkSweepGC -XX:+PrintGCDetails -Xloggc:./gc.log\

 -XX:+PrintGCDateStamps -XX:+CMSParallelRemarkEnabled -XX:ReservedCodeCacheSize=256m -XX:+UseCodeCacheFlushing\

 $MEM_OPT -XX:MaxDirectMemorySize=$directmem -XX:+HeapDumpOnOutOfMemoryError -jar $JAR_NAME $START_OPT -c config.conf  >> start.log 2>&1 &

 pid=`ps -ef |grep $JAR_NAME |grep -v grep |awk '{print $2}'`

 echo "start java-tron with pid $pid on $HOSTNAME"

}



stopService

rebuildManifest

sleep 5

startService
```
启动示例
> Note: 在以上脚本中 `-r` 参数 固定在第一个参数或者第二个参数(后续版本优化)
```shell
# 简单起见，将历史数据集存放在`/tmp`目录下
./start.sh -r -b 5120 -d /tmp/output-directory/database -m 4
````

