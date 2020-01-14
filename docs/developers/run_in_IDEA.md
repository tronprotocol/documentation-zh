# 使用IDEA运行我们的节点（针对当前master分支）

## 配置集成开发环境IDEA
**请确保IDEA已经完成如下配置**
- Oracle JDK 1.8（当前不支持OpenJDK）
- 安装Lombok插件

![截屏2020-01-14下午3.37.21](file:///Users/tron/Desktop/%E6%88%AA%E5%B1%8F2020-01-14%E4%B8%8B%E5%8D%883.37.21.png)

- 将Compiler下Annotation Processors中的Enable annotation processing前打勾

![截屏2020-01-14下午3.39.54](file:///Users/tron/Desktop/%E6%88%AA%E5%B1%8F2020-01-14%E4%B8%8B%E5%8D%883.39.54.png)

## 部署指南
**创建目录**
_/deploy/java-tron_

**克隆最新的代码https:github.com/tronprotocol/java-tron 到上述目录**
```swift
git clone https://github.com/tronprotocol/java-tron java-tron/
```

**切换master分支**
```swift
git checkout -t origin/master
```

**编译代码**
- 若编译test类
```swift
./gradlew build
```

编译成功，你可以看到类似如下块信息：

![截屏2020-01-14下午5.24.45](file:///Users/tron/Desktop/%E6%88%AA%E5%B1%8F2020-01-14%E4%B8%8B%E5%8D%885.24.45.png)

- 若不编译test类
```swift
./gradlew build -x test
```

编译成功，你可以看到类似如下块信息：

![截屏2020-01-14下午5.26.59](file:///Users/tron/Desktop/%E6%88%AA%E5%B1%8F2020-01-14%E4%B8%8B%E5%8D%885.26.59.png)

**启动程序**

![截屏2020-01-14下午4.46.34](file:///Users/tron/Desktop/%E6%88%AA%E5%B1%8F2020-01-14%E4%B8%8B%E5%8D%884.46.34.png)

启动后可查看日志验证是否启动成功，日志路径为：/deploy/java-tron/tron/logs/tron.log。
使用tail -f /logs/tron.log/命令来查看块同步日志。
若启动成功，你可以看到类似如下块同步的日志信息：

![截屏2020-01-14下午5.36.41](file:///Users/tron/Desktop/%E6%88%AA%E5%B1%8F2020-01-14%E4%B8%8B%E5%8D%885.36.41.png)
