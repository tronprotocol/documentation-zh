# 开发示例

本文通过一个小型的 `java-tron` 贡献示例介绍开发流程：新增一个只读 HTTP 接口，返回当前运行节点的软件版本。该接口有意保持简单，以便示例重点展示当前的 Servlet 实现、注册、测试和贡献方式，而不引入数据库或钱包依赖。

下面使用的 `/wallet/getnodeversion` 只是一个示例接口，目前 `java-tron` 并未提供该接口。在提议新增公共接口之前，请先创建 Issue 或与维护者讨论使用场景，并确认 `/wallet/getnodeinfo` 等现有接口是否已经能够提供所需数据。

开始之前，请按照 [IntelliJ IDEA 开发环境配置指南](run-in-idea.md)完成开发环境配置。

## 1. 准备开发环境

### 1.1 Fork 并克隆 `java-tron`

将 [tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) Fork 到您的 GitHub 账户。克隆您的 Fork，然后添加官方仓库作为 `upstream` 远程仓库：

```shell
git clone https://github.com/yourname/java-tron.git
cd java-tron
git remote add upstream https://github.com/tronprotocol/java-tron.git
```

### 1.2 同步仓库

开始新工作之前，请先同步本地 `develop` 分支：

```shell
git fetch upstream
git checkout develop
git merge upstream/develop --no-ff
```

### 1.3 创建分支

从 `develop` 分支创建新分支。分支命名请遵循[分支命名规范](java-tron.md/#_8)；本示例使用 `feature/add_node_version_api`：

```shell
git checkout -b feature/add_node_version_api develop
```

## 2. 添加 HTTP 接口

FullNode HTTP API 在 `framework` 模块中实现。HTTP 处理器是由 Spring 管理并继承 `RateLimiterServlet` 的组件，`FullNodeHttpApiService` 负责将它们注册到 Jetty。

### 2.1 创建 `GetNodeVersionServlet.java`

创建 `framework/src/main/java/org/tron/core/services/http/GetNodeVersionServlet.java`：

```java
package org.tron.core.services.http;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.tron.json.JSONObject;
import org.tron.program.Version;

@Component
public class GetNodeVersionServlet extends RateLimiterServlet {

  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    try {
      JSONObject result = new JSONObject();
      result.put("version", Version.getVersion());
      response.getWriter().println(result.toJSONString());
    } catch (Exception e) {
      Util.processError(e, response);
    }
  }

  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) {
    doGet(request, response);
  }
}
```

继承 `RateLimiterServlet` 后，该接口会接入 java-tron 的 HTTP 限流、指标统计、JSON 内容类型设置以及按请求生效的 JSON 输出格式设置。`@Component` 使 Spring 能够注入该 Servlet。处理器通过 `Util.processError` 序列化错误，与当前 HTTP API 的实现方式保持一致。

为与类似的只读钱包接口保持一致，本示例同时接受 GET 和 POST 请求。新增接口时应只开放实际需要的请求方法。

### 2.2 注册 Servlet

打开 `framework/src/main/java/org/tron/core/services/http/FullNodeHttpApiService.java`，声明 `GetNodeVersionServlet` 成员变量，并使用 `@Autowired` 注入其实例：

```java
@Autowired
private GetNodeVersionServlet getNodeVersionServlet;
```

然后在现有的 `addServlet(ServletContextHandler context)` 方法中注册该接口：

```java
@Override
protected void addServlet(ServletContextHandler context) {
  // 现有的 Servlet 注册...
  context.addServlet(
      new ServletHolder(getNodeVersionServlet), "/wallet/getnodeversion");
}
```

不要为单个接口创建第二个 `ServletContextHandler`，也不要重写 `start()`。`FullNodeHttpApiService` 从 `HttpService` 继承服务器生命周期管理，`addServlet(...)` 才是注册路由的扩展点。

如果该接口还需要由 SolidityNode 或 PBFT 服务提供，请在相应服务中明确注册合适的处理器。注册到 FullNode 并不会自动在其他服务端口上公开该路由。

### 2.3 调用接口

在本地启动 FullNode，然后通过默认的 FullNode HTTP 端口调用接口：

```bash
curl --request GET 'http://127.0.0.1:8090/wallet/getnodeversion'
```

响应中包含当前运行节点编译时写入的版本：

```json
{"version":"<current-java-tron-version>"}
```

如果已经在配置文件中修改 `node.http.fullNodePort`，请使用配置后的端口，而不是 `8090`。

## 3. 添加单元测试

`java-tron` 当前使用 JUnit 4 编写此类 Servlet 测试。请将测试放在 `framework/src/test/java` 下与被测类相同的包中。

创建 `framework/src/test/java/org/tron/core/services/http/GetNodeVersionServletTest.java`：

```java
package org.tron.core.services.http;

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.tron.json.JSONObject;
import org.tron.program.Version;

public class GetNodeVersionServletTest {

  private GetNodeVersionServlet servlet;

  @Before
  public void setUp() {
    servlet = new GetNodeVersionServlet();
  }

  @Test
  public void testDoGet() throws Exception {
    MockHttpServletRequest request = new MockHttpServletRequest();
    MockHttpServletResponse response = new MockHttpServletResponse();

    servlet.doGet(request, response);

    JSONObject result = JSONObject.parseObject(response.getContentAsString());
    assertEquals(200, response.getStatus());
    assertEquals(Version.getVersion(), result.getString("version"));
  }

  @Test
  public void testDoPost() throws Exception {
    MockHttpServletRequest request = new MockHttpServletRequest();
    MockHttpServletResponse response = new MockHttpServletResponse();

    servlet.doPost(request, response);

    JSONObject result = JSONObject.parseObject(response.getContentAsString());
    assertEquals(200, response.getStatus());
    assertEquals(Version.getVersion(), result.getString("version"));
  }
}
```

与其他针对单个 Servlet 的测试一样，该测试直接调用 `doGet` 和 `doPost`。测试继承的限流器或完整的 Jetty 路由需要依赖由 Spring 管理的组件，因此应使用相应的集成测试基础设施，而不是直接实例化 Servlet。

在仓库根目录运行该测试：

```bash
./gradlew :framework:test \
  --tests org.tron.core.services.http.GetNodeVersionServletTest \
  --no-daemon
```

## 4. 运行代码质量检查 { #run-code-quality-checks }

对修改的生产代码和测试代码运行 Checkstyle：

```bash
./gradlew \
  :framework:checkstyleMain \
  :framework:checkstyleTest
```

常规构建会执行范围更广的验证任务：

```bash
./gradlew clean build --no-daemon
```

在 x86_64 环境中，项目要求使用 JDK 8，常规测试任务默认使用 LevelDB。请另行运行有针对性的 RocksDB 引擎测试：

```bash
./gradlew :framework:testWithRocksDb --no-daemon
```

在 ARM64 环境中，项目要求使用 JDK 17，`framework` 模块的常规测试任务已经使用 RocksDB，因此通常无需再运行 `testWithRocksDb`。

GitHub Actions 还会执行一些难以在单台开发机器上完整复现的检查。有关触发矩阵、覆盖率阈值和分支差异，请参阅 [java-tron CI 工作流](workflows.md)。

## 5. 提交代码并创建 Pull Request

将源代码和测试一起提交。提交信息请遵循 [Commit 描述规范](java-tron.md/#commit)：

```bash
git add \
  framework/src/main/java/org/tron/core/services/http/GetNodeVersionServlet.java \
  framework/src/main/java/org/tron/core/services/http/FullNodeHttpApiService.java \
  framework/src/test/java/org/tron/core/services/http/GetNodeVersionServletTest.java
git commit -m 'feat: add node version HTTP API'
```

将分支推送到您的 Fork：

```bash
git push origin feature/add_node_version_api
```

从您的分支向 `tronprotocol/java-tron:develop` 创建 Pull Request。在 Pull Request 描述中说明使用场景、API 行为、兼容性影响、测试和文档更新。请求最终审查前，请确保所有必要检查均已通过。

![提交 Pull Request 示例](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/javatron_pr.png)
