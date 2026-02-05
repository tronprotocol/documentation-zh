# 在 IntelliJ IDEA 中配置 java-tron 开发环境

为简化 Java 开发流程并提升效率，选择并配置一款集成开发环境（IDE）是至关重要的第一步。本指南将以 IntelliJ IDEA 为例，详细阐述如何搭建和配置 java-tron 的集成开发环境。

java-tron 节点支持部署在 `Linux` 或 `MacOS` 操作系统上。其支持的 JDK 版本要求如下：

- x86_64架构上：仅支持Oracle JDK 8 
- arm64架构上：仅支持JDK 17

下面的配置以x86_64架构、Oracle JDK 8为示例：

## 前置条件

在开始配置之前，请确保您的开发环境满足以下条件：

  - 操作系统为 `Linux` 或 `MacOS`
  - 已安装 Oracle JDK 8
  - 已安装 `git`
  - 已安装 [IntelliJ IDEA](https://www.jetbrains.com/idea/download/)


## 配置 IntelliJ IDEA 环境

### 步骤 1：安装 Lombok 插件

Lombok 通过注解的方式简化 Java 代码，是 java-tron 开发的必备插件。

1.  打开 IntelliJ IDEA，导航至 `Preferences` -\> `Plugins`。
2.  在市场（Marketplace）中搜索 `Lombok`。
3.  点击 “Install” 进行安装，并根据提示重启 IDE。

### 步骤 2：启用注解处理

为了让 Lombok 的注解生效，必须启用注解处理器。

1.  导航至 `Preferences` -\> `Build, Execution, Deployment` -\> `Compiler` -\> `Annotation Processors`。
2.  勾选 `Enable annotation processing` 复选框。
3.  点击 “Apply” 保存设置。

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_annotation.png)

### 步骤 3：验证并统一 JDK 版本
为确保项目能够正确编译和运行，必须在 IntelliJ IDEA 的两个关键位置都将 JDK 版本设置为 Oracle JDK 8。

#### 1. 配置项目 SDK (Project SDK)
这是用于编译项目源代码和进行语法分析的核心 JDK。

1.  导航至 `File` -\> `Project Structure` -\>，在左侧面板中选择 Project。
2.  在 `Project SDK` 下拉菜单中，确认已选择 `1.8` 版本。

#### 2. 配置 Gradle JVM
这是用于执行 Gradle 构建任务（如 build, clean）的 JDK。

1. 导航至 `Preferences` -\> `Build, Execution, Deployment` -> `Build Tools` -> `Gradle`。
2. 在右侧的 Gradle JVM 下拉菜单中，确保选择的也是与 Project SDK 一致的 `1.8` 版本。

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_JDK.png)

> **重要提示**: **Project SDK** 和 **Gradle JVM** 这两个设置必须完全一致，且都指向 Oracle JDK 8（也就是图中的1.8，1.8和8只是命名方式的不同，在java-tron的文档中，非特殊情形下，统一命名成8），否则可能会在构建过程中遇到意外错误。



## 获取并编译项目源码

### 步骤 1：克隆源码

将 `java-tron` 的源代码克隆到本地，并切换到 `develop` 分支。

```
git clone https://github.com/tronprotocol/java-tron.git
cd java-tron
git checkout -t origin/develop
```

### 步骤 2：编译 `java-tron`

您可以通过两种方式编译项目：

  * **使用终端编译:**

    在 `java-tron` 项目根目录下，执行以下 Gradle 命令:

    ```
    # 执行完整编译，包含所有测试用例
    ./gradlew clean build
    ```

    若要跳过单元测试，以加快编译速度，可使用 `-x test` 参数：

    ```
    # 跳过测试进行编译
    ./gradlew clean build -x test
    ```

  * **使用 IntelliJ IDEA 界面编译:**

    在 IntelliJ IDEA 中打开 `java-tron` 项目，点击顶部菜单栏的 `Build` -\> `Build Project` 来编译整个项目。


## 配置代码风格检查

java-tron 遵循 `Google checkstyle` 代码规范。在 IDEA 中，通过配置 `Checkstyle` 插件，可以实时检查代码风格，确保代码提交质量。

### 步骤 1：安装 Checkstyle 插件

1.  在 IDEA 中，导航至 `Preferences` -\> `Plugins`。
2.  在市场（Marketplace）中搜索 `Checkstyle` 插件并安装。

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_checkstyle.png)

### 步骤 2：配置 Checkstyle 规则

1.  首先，获取代码风格配置文件。您可以直接使用项目本地的 `config/checkstyle/checkStyleAll.xml` 文件，或者从 [官方 GitHub 代码库](https://github.com/tronprotocol/java-tron/blob/develop/config/checkstyle/checkStyleAll.xml) 下载。
2.  在 IDEA 中，导航至 `Preferences` -\> `Tools` -\> `Checkstyle`，进入配置面板。
3.  在 `Configuration File` 面板中，点击 `+` 号添加一个新的配置。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_checkStyleAll.png)
4.  在弹出的窗口中，设置 `Description` 为 `tron-checkstyle`，并选择刚刚下载的 `checkStyleAll.xml` 文件。
5.  勾选新添加的 `tron-checkstyle` 规则，并点击 “Apply” 和 “OK”。

配置完成后，您即可使用 `Checkstyle` 插件对代码进行风格检查。它支持多种检查范围，可以对整个项目、单个模块，或是当前正在编辑的文件进行分析。最常用的操作是检查当前文件：

1. 在代码编辑器中右键单击。
2. 选择 “Check Current File”。

如果检测出代码风格问题，`Checkstyle` 会在下方窗口列出提示。请根据这些提示逐一修改，确保在提交代码前修复所有问题，以维护代码库的统一规范。

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_stylecheck.png)
   

## 运行与调试

<a id="rndstep1"></a>
### 步骤 1：创建工作目录

在运行 java-tron 之前，您需要创建一个工作目录，用于存放节点运行时产生的数据库文件及日志文件。

```shell
mkdir /Users/javatrondeploy
```

> **重要提示**：java-tron 会在此目录下寻找 `config.conf` 配置文件。在启动节点前，请确保您已经将正确的配置文件放置在该目录中。

### 步骤 2：配置运行/调试选项

接下来，在 IntelliJ IDEA 中创建一个运行配置，用于指定 java-tron 应用程序的启动方式。

1.  在 IDEA 右上角，点击 `Add Configuration...`。
2.  点击 `+` -\> `Application`，创建一个新的运行配置。
3.  请从上到下依次找到并设置以下选项：
      * **Name:** 为配置命名，例如 `Fullnode`。
      * **JDK**：确保选择 `java 8 1.8`。
      * **Main Class:** 设置为 `org.tron.program.FullNode`。
      * **Program Arguments:** 传入节点启动参数。例如，使用 `-c config.conf` 来指定配置文件。
      * **Working Directory:** 设置为您在 [步骤 1](#rndstep1) 中创建的目录，例如 `/Users/javatrondeploy`。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_RunDebug.png)
4.  点击 “Apply” 保存配置。

### 步骤 3: 启动节点

现在，您可以通过 IDEA 启动 java-tron 节点：

  * **运行节点:** 点击顶部菜单栏的 `Run` -\> `Run 'FullNode'`。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_runjavatron.png)
  * **调试节点:** 在代码中设置断点，然后点击 `Run` -\> `Debug 'FullNode'`。程序将在断点处暂停，方便您进行逐行跟踪调试。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_debug.png)

节点启动后，相关日志文件将输出到您配置的 `Working directory` 中。
