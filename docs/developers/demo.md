# 开发示例
本文将以新增一个`setPeer` HTTP接口为例说明如何参与Java-tron开发。在开发前，请先配置[InteliJ IDE开发环境](../run-in-idea)。

有时由于网络原因，Java-tron节点可能无法连接到对等节点，如果能在节点运行时添加信任节点，这将使节点可以在节点发现无法工作的的情况下也能连接到网络。

## Fork Java-tron代码仓库

从 [https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) 项目中Fork一个新的repository到自己个人的代码仓库中，然后使用如下命令将代码克隆到本地:
    
```
$ git clone https://github.com/yourname/java-tron.git
$ git remote add upstream https://github.com/tronprotocol/java-tron.git
```
    
## 同步仓库 
    
开发新功能之前，应先将个人Fork的仓库和上游仓库进行同步：
    
```
$ git fetch upstream 
$ git checkout develop 
$ git merge upstream/develop --no-ff
```

## 创建新分支
从自己仓库的develop分支拉出一个新的分支用于本地开发，请参考[分支命名规范](../java-tron/#_8)，在本例中，新分支的名称为：`feature/add-new-http-demo`。

```
$ git checkout -b feature/add-new-http-demo develop
```

## 代码实现

在IDEA中打开Java-tron工程。在`java-tron/framework/src/main/java/org/tron/core/services/http`目录下新建一个servlet用于处理HTTP请求：SetPeerServlet.java，该文件中应包含两个函数`doGet`和`doPost`。`doGet`用于处理http get请求，`doPost`用于处理http post请求。如果不支持其中某种类型的请求，方法内容为空即可。
```java
@Component
@Slf4j(topic = "API")
public class SetPeerServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
    {}
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
    {}
}
```

在该示例中setPeer请求应该通过post方式发送，因此需要在`doPost`方法中添加处理逻辑，`doGet`方法内容为空。

`doPost`方法的逻辑为：

1. 获取传入的参数
2. 通过addPeer方法将peer信息添加到信任节点列表中
3. 将addPeer的处理结果返回给前端用户

```java
@Component
@Slf4j(topic = "API")
public class SetPeerServlet extends HttpServlet {
  @Autowired
  private ChannelManager channelManager;
    
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
  ......
}
```


将添加信任节点的处理逻辑单独放在`addPeer`方法中，这样不但可以使代码逻辑更加清晰，而且更易于测试。

`addPeer`函数的逻辑为：

1. 检查用户输入的参数，确保节点ip和端口不为空
2. 通过`Node.instanceOf(peerIP)`构建节点信息
3. 确保添加的信任节点不是自己
4. 将节点加入到自己的信任节点列表中


```java
  boolean addPeer(String peerIP) {
    try {
      if (peerIP != "") {
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
完成SetPeerServlet的实现，还需要将其注册到节点HTTP API服务列表中，[FullNodeHttpApiService](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/http/FullNodeHttpApiService.java) 是节点HTTP API服务的注册入口。

在`FullNodeHttpApiService`类的`start`函数中调用`context.addServlet`方法将SetPeerServlet注册到服务列表中，HTTP 接口的名字定义为`/wallet/setpeer`。

```java

public class FullNodeHttpApiService implements Service {
    ......
    @Autowired
    private SetPeerServlet setPeerServlet;
    .......
    
    @Override
    public void start() {
        ......
        context.addServlet(new ServletHolder(setPeerServlet), "/wallet/setpeer");
        .......
    }
    
}
```
然后可以对以上代码进行调试，在IDEA中启动Java-tron节点，在终端中通过Curl命令访问节点：

```curl
$ curl --location --request POST 'http://127.0.0.1:16667/wallet/setpeer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "peer":"192.163.3.2:16667"
}'
```
返回结果：

```
Success to set trusted peer:192.163.3.2:16667
```

至此，该功能的代码编写完成，然后需要针对改动编写单元测试。对于简单的改动，可以在开发代码完成之后，再编写单元测试，但对于较大的改动，建议在开发的同时编写单元测试。

## 编写单元测试

Java-tron项目的单元测试基于JUnit框架，关于JUnit的用法请参考[JUnit官网](https://junit.org)。下面简单介绍Java-tron单元测试用例规范和常用注解说明。

### Java-tron单元测试用例规范
编写Java-tron单元测试时，请遵守如下规范：

* 所有测试类应放在test目录下，并且测试类的包应该和被测试代码包结构保持一致。一般使用 `Test` 作为类名的后缀
* 测试方法必须使用 @Test 修饰，并且是public void类型，一般用 `test` 作为方法名的前缀
* 测试类中的每个测试方法必须可以独立测试，方法间不能有任何依赖

### 常用注解说明
下面为一些常用的注解的说明，其它注解请参考[JUnit官网文档](https://junit.org)。

* `@Test` - 将一个普通方法修饰成一个测试方法
* `@Ignore` - 所修饰的测试方法会被测试运行器忽略
* `@BeforeClass` - 会在所有的方法执行前被执行，static方法 （全局只会执行一次，而且是第一个运行）
* `@AfterClass` - 会在所有的方法执行之后进行执行，static方法 （全局只会执行一次，而且是最后一个运行）
* `@Before` - 会在每一个测试方法被运行前执行一次
* `@After` - 会在每一个测试方法运行后被执行一次


### 单元测试类的组成
一个单元测试类应包含一下三部分内容：

* @Before或者@BeforeClass修饰的函数，用于进行测试用例执行前的初始化工作
* @After或者@BeforeClass修饰的函数，用于处理测试用例执行完成后的数据清理工作
* @Test修饰的测试方法

```java
public class demoTest {

  @Before
  public void init() {
    // Initialization work before test case execution
  }
  @After
  public void destroy() {
      // Destroy work after test case execution

  }
  @Test
  public void testDemoMethod() { 
  }
}

```

对于本文示例，应在`framework/src/test/java/org/tron/core/services/http/`目录下新建一个文件：SetPeerServletTest.java 来编写测试用例。


```java
public class SetPeerServletTest {
  private static TronApplicationContext context;
  private static Application appT;
  public static ChannelManager channelManager;
  @Before
  public void init() {
    
    Args.setParam(new String[]{}, Constant.TEST_CONF);
    context = new TronApplicationContext(DefaultConfig.class);
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
    Assert.assertFalse(setPeerServlet.addPeer("127.0.0.1"));
  }
}
```

## CheckStyle代码风格检查
逐个检查修改的文件，在右键菜单中选择`Check Current File`，如果检查出代码风格问题，请根据提示逐个修改。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/demo_codestyle_error.png)
对图中代码风格警告，进行修复，然后，再一次检查该文件，，直至没有warning。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/demo_codestyle.png)

## 提交代码

代码完成之后提交commit，请参考[commit规范](../java-tron/#commit)。
```
git add .
git commit -m 'add a new http api setpeer'
```
     
提交新的分支到个人远端仓库：
     
```
git push origin feature/add-new-http-demo
```

## 提交Pull Request

在Github从你自己的仓库向`tronprotocol/java-tron`提交一个推送代码请求 Pull Request。

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/javatron_pr.png)

