# levelDB 启动优化插件

## 介绍

随着levelDB的运行，manifest文件会持续增长，过大的manifest文件不但影响节点启动速度，而且还有可能会导致内存持续增长系统退出的问题。
为此在`GreatVoyage-v4.3.0(Bacon)`引入了leveldb 启动优化插件，插件优化了manifest的文件大小以及LevelDB的启动过程，减少了内存占用，提升了节点启动速度。

使用本工具进行任何操作之前，需要首先停止当前运行的FullNode节点。 此工具提供了根据当前`数据库`(database)情况,对 manifest 进行重新归整的功能。

更多的设计思想，请参考: [TIP298](https://github.com/tronprotocol/tips/issues/298) 。

## 使用

### 插件选项

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

首先, 停止FullNode并执行命令:

```shell
java -jar ArchiveManifest.jar [-b batchSize] [-d databaseDirectory] [-m manifestSize]
```

命令执行完毕之后，将在`./logs`目录下生成`archive.log`日志, 可查看此次归整情况

> Note: 执行完成后，如果成功 日志会显示如下类似内容，运行一般在120s内，视FullNode服务持续运行时长决定，失败会有相应的错误信息
>
> `[main] [archive](ArchiveManifest.java:144) DatabaseDirectory:output-directory/database, maxManifestSize:0, maxBatchSize:80000,database reopen use 80 seconds total.`

最后,启动停止FullNode服务

#### 2. 集成启动脚本

也可以将此归整插件集成到启动脚本。

```shell
#!/bin/bash

APP=$1

MANIFEST_OPT=$2

ALL_OPT=$*

NEED_REBUILD=0

if [[ $1 == '--rewrite--manifest' ]]  ; then
   APP=''
   NEED_REBUILD=1

 elif [[ $2 == '--rewrite--manifest' ]]  ; then
   NEED_REBUILD=1
 fi


rebuildManifest() {

 if [[ $NEED_REBUILD == 1 ]] ; then
   buildManifest
 fi

}


buildManifest() {

 ARCHIVE_JAR='ArchiveManifest.jar'

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

checkPath(){
  path='output-directory/database'
  flag=1
  for p in ${ALL_OPT}
  do
   	 if [[ $flag == 0 ]] ; then
   	 	path=`echo $p`
   	 	break
   	 fi
   	 if [[ $p == '-d' || $p == '--database-directory' ]] ; then
   	 	path=''
   	 	flag=0
   	 fi
  done

  if [[ -z "${path}" ]]; then
     echo '-d /path or --database-directory /path'
     return 1
  fi

  if [[ -d ${path} ]]; then
    return 0
  else
    echo $path 'not exist'
    return 1
  fi
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

 total=16*1024*1024

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

checkPath

if [[ 0 ==  $? ]] ; then
 rebuildManifest
else
 exit -1
fi

sleep 5

startService
```
启动示例
> Note: 将上述脚本保存为start.sh，在以上脚本中 `--rewrite--manifest` 参数 固定在第一个参数或者第二个参数
>
> OPTIONS
>
>            --rewrite--manifest       开启数据库优化插件，开启此项后 以上插件选项的`-d -m -b -h` 才会生效
```shell
./start.sh [FullNode|SolidityNode] [--rewrite--manifest] [-b batchSize] [-d databaseDirectory] [-m manifestSize]
````

