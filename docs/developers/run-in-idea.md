# 使用IDEA运行FullNode节点

该文档旨在方便有一定经验的开发者在集成开发环境IDEA中运行FullNode节点
**以下内容针对java-tron的master分支**

## 一、配置集成开发环境IDEA

### IDEA配置

- Oracle JDK 1.8 **当前不支持OpenJDK**

- 安装Lombok插件

![image](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/images/lombok.png)

- 将Compiler下Annotation Processors中的Enable annotation processing前打勾

![image](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/images/annnotation.png)

## 二、部署指南

### 1.创建目录

_/deploy_

```shell
mkdir deploy
```

### 2.克隆最新的代码

```shell
git clone https://github.com/tronprotocol/java-tron
```

### 3.切换master分支

```shell
cd java-tron
git checkout -t origin/master
```

### 4.编译代码

```shell
./gradlew build
```

编译过程可能需要一定时间，请耐心等待。
若编译成功，你可以看到类似如下信息：

![image](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/images/build_success_test.png)

如果不想执行单元测试任务，可运行如下命令：

```shell
./gradlew build -x test
```

### 5.启动FullNode节点

编译成功后，可通过java-tron/src/main/java/org/tron/program/FullNode.java路径找到主函数文件，启动一个全节点。

![image](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/images/start.png)

启动后可查看日志验证是否启动成功，日志路径为：/deploy/java-tron/logs/tron.log。
若启动成功，可看到如下日志：

![image](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/images/start_success.png)

使用tail -f /logs/tron.log命令可查看实时日志，如下：

![image](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/images/start_successed.png)
