# 开发示例

本文将以在 `java-tron` 中新增一个 `setPeer` HTTP 接口为例，详细讲解参与 `java-tron` 开发的流程。在开始开发之前，请确保您已完成开发环境的配置，例如已根据 [IntelliJ IDEA 开发环境配置指南](run-in-idea.md) 配置好本地环境。

**背景**：有时由于网络原因，`java-tron` 节点可能无法连接到对等节点。为了增强节点的网络连接稳定性，我们希望实现一个功能，允许在节点运行时动态添加信任节点，即使在节点发现服务失效的情况下也能连接到网络。

## 1. 准备开发环境

### 1.1 Fork `java-tron` 代码仓库

首先，从 TRON 官方 GitHub 仓库 [tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) Fork 一个新的代码仓库到您个人的 GitHub 账户。然后，将您的 Fork 仓库克隆到本地，并添加 `upstream` 远程仓库以跟踪官方更新：

```
git clone https://github.com/yourname/java-tron.git
git remote add upstream https://github.com/tronprotocol/java-tron.git
```

### 1.2 同步仓库

在开发新功能之前，务必将您个人 Fork 的仓库与 `upstream`（上游）仓库进行同步，以获取最新的代码更新：

```
git fetch upstream
git checkout develop
git merge upstream/develop --no-ff
```

### 1.3 创建新分支

从本地 `develop` 分支创建一个用于本地开发的新分支。分支命名请遵循 [分支命名规范](java-tron.md/#_8)。本示例使用 `feature/add-new-http-demo` 作为分支名称。

```shell
git checkout -b feature/add-new-http-demo develop
```
## 2. 代码实现：新增 `setPeer` HTTP 接口

使用 IntelliJ IDEA 打开 `java-tron` 工程。接下来我们将实现一个 `setPeer` HTTP 接口，以支持用户通过 POST 请求添加信任节点。

### 2.1 创建 `SetPeerServlet.java`

在 `java-tron/framework/src/main/java/org/tron/core/services/http` 目录下，新建一个 `Servlet` 类：`SetPeerServlet.java`。该类包含 `doGet` 和 `doPost` 两个方法，分别用于处理 HTTP GET 和 POST 请求。如果某种请求类型不予支持，可将对应方法留空。

```java
package org.tron.core.services.http;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.tron.core.net.peer.ChannelManager;
import org.tron.core.net.peer.Node;
import org.tron.core.config.CommonParameter;
import org.tron.core.Constant;
import org.tron.core.exception.BadItemException;
import org.tron.core.services.http.fullnode.PostParams;
import org.tron.core.services.http.fullnode.Util;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;

import com.alibaba.fastjson.JSONObject;

@Component
@Slf4j(topic = "API")
public class SetPeerServlet extends HttpServlet {

  @Autowired
  private ChannelManager channelManager;

  protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    // GET 请求在此示例中不处理
  }

  protected void doPost(HttpServletRequest request, HttpServletResponse response) {
    try {
      PostParams params = PostParams.getPostParams(request);

      JSONObject jsonObject = JSONObject.parseObject(params.getParams());
      String peerIpPort = String.valueOf(jsonObject.get("peer"));

      boolean res = addPeer(peerIpPort);
      if (res) {
        response.getWriter().println("Success to set trusted peer:" + peerIpPort);
      } else {
        response.getWriter().println("Fail to set the trusted peer:" + peerIpPort);
      }

    } catch (Exception e) {
      logger.error("Exception occurs when setting peer: {}", e.getMessage());
      try {
        response.getWriter().println(Util.printErrorMsg(e));
      } catch (IOException ioe) {
        logger.error("IOException occurs when setting peer: {}", ioe.getMessage());
      }
    }
  }

  private boolean addPeer(String peerIP) {
    try {
      if (peerIP != null && !peerIP.isEmpty()) {
        Node node = Node.instanceOf(peerIP);
        if (!(CommonParameter.PARAMETER.nodeDiscoveryBindIp.equals(node.getHost())
            || CommonParameter.PARAMETER.nodeExternalIp.equals(node.getHost())
            || Constant.LOCAL_HOST.equals(node.getHost()))
            || CommonParameter.PARAMETER.nodeListenPort != node.getPort()) {

          InetAddress address = new InetSocketAddress(node.getHost(), node.getPort()).getAddress();
          channelManager.getTrustNodes().put(address, node);
          return true;
        }
      }
    } catch (Exception e) {
      logger.error("addPeer error - {}", e.getMessage());
    }
    return false;
  }
}
```

在上述代码中：

*   `doPost` 方法负责处理接收到的 POST 请求。它从请求参数中获取 `peer`（对等节点 IP:Port）信息。
*   `addPeer` 方法负责将该对等节点添加到信任节点列表中。该函数的逻辑如下：
    1.  检查用户输入的参数，确保节点 IP 和端口不为空。
    2.  通过 `Node.instanceOf(peerIP)` 构建节点信息。
    3.  确保添加的信任节点不是当前节点自身。
    4.  将节点加入到 `ChannelManager` 的信任节点列表中。

### 2.2 注册 `SetPeerServlet` 到 HTTP API 服务

完成 `SetPeerServlet` 的实现后，需要将其注册到节点的 HTTP API 服务中。 `FullNodeHttpApiService` 类是所有 HTTP 接口的注册入口。在该类的 `start` 方法中，使用 `context.addServlet` 将 `SetPeerServlet` 注册为名为 `/wallet/setpeer` 的 HTTP 接口：


```java
package org.tron.core.services.http;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.tron.core.services.Service;

@Component
public class FullNodeHttpApiService implements Service {

  @Autowired
  private SetPeerServlet setPeerServlet;

  // ... 其他成员变量和方法 ...

  @Override
  public void start() {
    // ... 其他初始化代码 ...
    ServletContextHandler context = new ServletContextHandler(ServletContextHandler.SESSIONS);
    // ... 其他 Servlet 注册 ...
    context.addServlet(new ServletHolder(setPeerServlet), "/wallet/setpeer");
    // ... 其他启动代码 ...
  }

  // ... 其他方法 ...
}
```

### 2.3 调试与测试

完成代码修改后，您可以在 IntelliJ IDEA 中启动 `java-tron` 节点进行调试。然后，在终端中使用 `curl` 命令访问新添加的 HTTP 接口：

```bash
curl --location --request POST 'http://127.0.0.1:16667/wallet/setpeer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "peer":"192.163.3.2:16667"
}'
```

如果请求成功，您将收到以下返回结果：

```text
Success to set trusted peer:192.163.3.2:16667
```

至此，`setPeer` 功能的代码编写完成。接下来，您需要为这些改动编写单元测试。

## 3. 编写单元测试

`java-tron` 项目的单元测试基于 JUnit 框架。关于 JUnit 的详细用法，请参考 [JUnit 官方文档](https://junit.org)。下面将介绍 `java-tron` 单元测试用例的规范和常用注解。

### 3.1 `java-tron` 单元测试用例规范

在编写 `java-tron` 的单元测试时，请遵循以下规范：

* **目录与包结构**：所有测试类应位于 test 目录下，并保持与被测试类相同的包结构。测试类名称建议以 `Test` 为后缀。
* **测试方法定义**：测试方法必须使用 `@Test` 注解修饰，并声明为 `public void` 类型。方法名称建议以 `test` 为前缀，以增强可读性。
* **方法独立性**：测试类中的每个方法应可独立运行，方法之间不得存在依赖关系，以确保测试的稳定性和可维护性。


### 3.2 常用 JUnit 注解说明

以下列出的是 JUnit 中常用的测试注解，更详细内容请参考 [JUnit 官方文档](https://junit.org)。

*   `@Test`：标记一个方法为测试方法，测试运行器将执行该方法。
*   `@Ignore`：忽略当前测试方法，运行时不会执行（可用于暂时跳过不稳定或未完成的测试）。
*   `@BeforeClass`：在所有测试方法执行前运行一次，必须为 `static` 方法（通常用于初始化共享资源）。
*   `@AfterClass`：在所有测试方法执行后运行一次，必须为 `static` 方法（通常用于释放共享资源）。
*   `@Before`：在每个测试方法执行前运行一次（用于准备测试环境，如初始化数据）。
*   `@After`：在每个测试方法执行后运行一次（用于清理测试环境，如关闭连接）。

### 3.3 单元测试类的组成
一个典型的单元测试类通常由以下三部分组成：

* **初始化方法**：使用 `@Before` 或 `@BeforeClass` 注解的方法，在测试执行前进行初始化操作，如准备测试数据或配置环境。
* **清理方法**：使用 `@After` 或 `@AfterClass` 注解的方法，在测试执行后进行清理操作，如释放资源或还原数据。
* **测试方法**：使用 `@Test` 注解的方法，编写具体的测试逻辑，用于验证代码行为是否符合预期。


```java
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class DemoTest {

  @Before
  public void init() {
    // 测试用例执行前的初始化工作
  }

  @After
  public void destroy() {
    // 测试用例执行后的数据清理工作
  }

  @Test
  public void testDemoMethod() {
    // 测试逻辑
  }
}
```

在本示例中，我们应在目录 `framework/src/test/java/org/tron/core/services/http/` 下新建测试类文件 `SetPeerServletTest.java`，用于编写对应的测试用例。


```java
package org.tron.core.services.http;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.tron.core.config.args.Args;
import org.tron.core.net.peer.ChannelManager;
import org.tron.core.services.http.fullnode.SetPeerServlet;
import org.tron.core.db.Manager;
import org.tron.core.db.TronApplicationContext;
import org.tron.core.Constant;
import org.tron.core.services.Application;
import org.tron.core.services.ApplicationFactory;

public class SetPeerServletTest {

  private static TronApplicationContext context;
  private static Application appT;
  public static ChannelManager channelManager;

  @Before
  public void init() {
    Args.setParam(new String[]{}, Constant.TEST_CONF);
    context = new TronApplicationContext(Manager.class);
    channelManager = context.getBean(ChannelManager.class);
    appT = ApplicationFactory.create(context);
    appT.initServices(Args.getInstance());
    appT.startServices();
    appT.startup();
  }

  @After
  public void destroy() {
    Args.clearParam();
    appT.shutdownServices();
    appT.shutdown();
  }

  @Test
  public void testAddPeer() {
    SetPeerServlet setPeerServlet = new SetPeerServlet();
    // 假设 127.0.0.1 是本地 IP，addPeer 应该返回 false，因为它不会添加自身为信任节点
    Assert.assertFalse(setPeerServlet.addPeer("127.0.0.1"));
  }
}
```

## 4. CheckStyle 代码风格检查

在提交代码之前，请务必对您修改的文件进行 CheckStyle 代码风格检查。在 IntelliJ IDEA 中，您可以右键点击文件，选择 “Check Current File”。如果检查出代码风格问题，请根据提示逐个修改，直至没有警告。

![CheckStyle 代码风格错误示例](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/demo_codestyle_error.png)

修复代码风格问题后，再次检查，确保所有警告都已消除：

![CheckStyle 代码风格修复后示例](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/demo_codestyle.png)

## 5. 提交代码与 Pull Request

### 5.1 提交 Commit

完成代码编写和测试后，提交您的更改。请参考 [Commit 规范](java-tron.md/#commit)。

```bash
git add .
git commit -m 'feat: add new http api setpeer'
```

### 5.2 推送新分支

将您的新分支推送到个人远程仓库：

```bash
git push origin feature/add-new-http-demo
```

### 5.3 提交 Pull Request

在 GitHub 上，从您自己的仓库向 `tronprotocol/java-tron` 提交一个 Pull Request。这将把您的更改提议给官方仓库。

![提交 Pull Request 示例](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/javatron_pr.png)

请确保您的 Pull Request 描述清晰，包含您所做更改的详细信息和目的。


