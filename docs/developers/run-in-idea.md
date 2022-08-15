# 配置InteliJ IDE开发环境

对于Java开发，为了降低开发难度，提高开发效率，开发者应首先选择并配置一款Java集成开发环境，如IntelliJ IDEA、NetBeans或者Eclipse等，本文将以InteliJ IDEA举例来介绍如何配置Java-tron集成开发环境。

本文介绍在InteliJ IDEA中配置Java-tron集成开发环境。Java-tron节点支持部署在 `Linux` 或 `MacOS` 操作系统上，并且依赖`Oracle JDK 1.8` ，不支持其它版本的JDK。在配置InteliJ IDE开发环境前，请确保如下前置条件：

* 在`Linux` 或 `MacOS` 操作系统上配置开发环境
* 系统安装了`Oracle JDK 1.8`、`git`、[InteliJ IDEA](https://www.jetbrains.com/idea/download/#section=mac)
        
## 配置InteliJ IDEA
InteliJ IDEA 配置步骤如下：

* 安装Lombok插件

    在[IDEA]->[Preferences]->[Plugins] 中搜索`lombok` 安装插件，`Lombok`通过加注解的方式让Java-tron代码更加简洁。

* 打开`Enable annotation processing`配置项
      ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_annotation.png)
* 检查JDK版本，确保InteliJ IDEA中使用的是`Oracle JDK 1.8`
      ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_JDK.png)
  
* 下载Java-tron源码

    将Java-tron源代码克隆到本地，并且切换到`develop`分支。
    ```
    $ git clone https://github.com/tronprotocol/java-tron.git
    $ git checkout -t origin/develop
    ```
    

## 配置代码风格检查插件
Java-tron代码风格需要符合`Google check style` 规范。在IDEA中，可以使用`Checkstyle` 插件检查代码是否符合`Google check style `规范。插件的安装及配置流程如下：

* 在[IDEA]->[Preferences]->[Plugins] 中搜索`checkstyle`安装插件
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_checkstyle.png)
    
* 代码风格配置

    首先下载[Java-tron代码风格检查配置文件](https://github.com/tronprotocol/java-tron/blob/develop/config/checkstyle/checkStyleAll.xml)，然后在Checkstyle配置页面中，点击"+“，选择使用刚刚下载的"checkStyleAll.xml”，添加完成后，可以在"Configuration Files"列表中看到此文件，最后点击"Apply"完成配置。
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_checkStyleAll.png)

    配置完成`Checkstyle`插件后，就可以使用`Checkstyle`检查代码了。`Checkstyle`可以对某个模块或者整个工程做检查，也可以对单个文件做检查，在文件编辑器的右键菜单中选择"Check Current File"，checkstyle就会对该文件进行检查了。如果检测出代码问题，则需根据提示依次修改。当没有代码问题时，才可以提交代码。

    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_stylecheck.png)
   

## 编译Java-tron

您可以使用终端，在Java-tron工程目录下，通过如下命令编译Java-tron：

```
$ ./gradlew clean build
```
上面的编译命令会执行所有测试用例，可以使用`-x test`跳过测试用例的执行过程：
```
$ ./gradlew clean build -x test
```

您也可以在IDEA中使用图形化方式编译Java-tron：在IDEA中打开Java-tron工程，点击"Build" -> "Build Project" 编译工程。

## 运行和调试
在运行Java-tron之前，需要创建一个工作目录，用于存放节点运行时产生的数据库文件及日志文件。
```
$ mkdir /Users/javatrondeploy
```


在"Run/Debug Configurations"配置面板中，指定运行Java-tron的JDK版本为`java 8`，然后再配置运行Java-tron的命令行参数，比如通过`-c`参数指定节点配置文件为`config.conf`。

"Working directory"配置成之前创建的Java-tron的工作目录，Java-tron启动时会在该目录下寻找`config.conf`配置文件，请确保`config.conf`已经放到该目录下。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_RunDebug.png)


设置完成后，点击"Apply"按钮完成配置。然后您就可以在IDEA中点击"Run"->"Run FullNode" 启动Java-tron节点，或者点击"Run"->"Debug FullNode"以debug模式启动节点。节点启动后，Java-tron日志存储在Working Directory配置的工作目录下。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_runjavatron.png)



如果想要调试Java-tron代码，可以在Java-tron代码中打断点，然后以debug模式启动，这样就可以逐行跟踪调试代码了。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_debug.png)

