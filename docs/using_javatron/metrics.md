# Java-tron节点指标监控
从GreatVoyage-4.5.1(Tertullian)版本开始，节点提供了一系列兼容prometheus协议的接口，使节点部署者可以更方便的监控节点的健康状态。如果您想要监控节点的各项指标，则首先需要部署一个prometheus服务，用于与Java-tron节点通信，通过节点接口获取到节点各项指标数据。然后还需要部署一个可视化工具，如Grafana，用于将prometheus获取到的节点数据，以图像化界面的形式展示出来。下面将详细介绍Java-tron节点监控系统的搭建流程。

## 配置Java-tron
如需使用Prometheus工具监控Java-tron节点的运行情况，首先需要在节点配置文件中开启prometheus指标监控，并设置http端口号：
```
node {
  ... ...
  p2p {
    version = 11111 # 11111: mainnet; 20180622: testnet
  }
 ####### add for prometheus start.
 metrics{
  prometheus{
  enable=true 
  port="9527"
  }
 }
 ####### add for prometheus end.
}

```
## 启动Java-tron节点
您可以通过如下命令启动Java-tron节点, 参考[部署Java-tron](./installing_javatron.md)章节。
```
$ java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c main_net_config.conf
```

## 部署Prometheus服务
[prometheus](https://prometheus.io/download/)官方提供了预编译的二进制文件以及docker镜像，您可以直接在官网下载或者在dockerhub上拉取docker镜像，更多的安装与配置说明，请参考[prometheus文档](https://prometheus.io/docs/introduction/overview/)。作为简单的部署说明，本文将采用docker镜像部署方式：

1. 安装prometheus

    下载docker后，输入如下命令拉取prometheus镜像：
    ```
    $ docker pull prom/prometheus
    ```

2. 下载Prometheus配置文件

    下面是一个prometheus配置文件模板`prometheus.yaml`：

    ```yaml
    global:
      scrape_interval: 30s
      scrape_timeout: 10s
      evaluation_interval: 30s
    scrape_configs:
    - job_name: java-tron
      honor_timestamps: true
      scrape_interval: 3s
      scrape_timeout: 2s
      metrics_path: /metrics
      scheme: http
      follow_redirects: true
      static_configs:
      - targets:
        - 127.0.0.1:9527
        labels:
          group: group-xxx
          instance: xxx-01
      - targets:
        - 172.0.0.2:9527
        labels:
          group: group-xxx
          instance: xxx-02
    ```
    您可以使用此模板，然后修改配置项 `targets` ，它用于配置Java-tron节点所在机器的ip和prometheus端口，如您部署了多个节点，可以通过配置多个 `targets`，来实现对多个节点的监控。

3. 启动一个Prometheus容器

    通过如下命令启动一个Prometheus容器，并指定使用上步骤中用户自定义的配置文件`/Users/test/deploy/prometheus/prometheus.yaml`
    ```shell
    $ docker run --name prometheus \
        -d -p :9090:9090 \
        -v  /Users/test/deploy/prometheus/prometheus.yaml:/etc/prometheus/prometheus.yml \
        prom/prometheus:latest
    ```


    容器启动后,您可以通过` http://localhost:9090/`查看prometheus服务的运行情况。
    
    点击"Status"-> "Configuration"，查看容器使用的配置文件是否正确：
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_config.png)

    点击"Status"-> "Targets"，查看各个监控的Java-tron节点状态：
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_targets.png)
    
    比如这个示例中，第一个endpoint，状态为`UP`，表示Prometheus可以正常的抓取该节点的数据。而第二个endpoint，状态为`DOWN`，表示异常，具体参考"Error"中的描述。

    当监控的Java-tron节点的状态都正常后，您就可以通过Grafana或Promdash等可视化工具监控指标数据了，本文将通过grafana来展示数据。

## 部署Grafana
Grafana可视化工具的部署流程如下：

1. 安装Grafana

    请参考官方文档安装[Grafana](https://grafana.com/docs/grafana/next/setup-grafana/installation/)。本文将采用docker部署方式，拉取的image版本为open source版：
    ```
    $ docker pull grafana/grafana-oss
    ```

2. 启动Grafana
  您可以通过如下docker命令来启动Grafana：
    ```
    $ docker run -d --name=grafana -p 3000:3000 grafana/grafana-oss
    ```
3. 登录Grafana界面

    启动后，可以通过`http://localhost:3000/`进入Grafana页面，初始的用户名和密码均是`admin`，输入后根据提示修改密码，然后就可以进入到主界面了。点击主页面左侧的设置图标，然后选择"Data Sources"配置Grafana的数据源：
    
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_datasource.png)

    在URL中输入prometheus服务的ip和端口：

    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_prometheus.png)
    
    然后点击页面最下方的"Save & test"按钮，保存设置。点击保存后，Grafana会检测与数据源的连接情况，如果成功通信，则会出现 `Data source is working` 字样。

4. 导入Dashboard

    Grafana的仪表盘需要配置，为了方便Java-tron节点部署者，TRON社区提供了一个较全面的仪表盘配置文件，您可以直接在Grafana dashboard中下载Java-tron仪表盘配置文件 [java-tron-template_rev1.json](https://grafana.com/grafana/dashboards/16567)，然后导入到Grafana。

    点击左侧的Dashboards图标，然后选择"+Import"，然后点击"Upload JSON file"导入已下载的仪表盘配置文件：
    
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_import.png)
    
    然后您就可以在仪表盘界面看到如下种类的监控信息，并实时监控节点的运行情况了：
    
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_dashboard.png)



