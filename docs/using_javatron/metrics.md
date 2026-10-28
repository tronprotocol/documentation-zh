# java-tron 节点指标监控

从 GreatVoyage-4.5.1 (Tertullian) 版本开始，节点通过 `/metrics` 端点暴露符合 Prometheus 文本格式的指标，使节点部署者可以更方便地监控节点的健康状态。各项暴露指标的含义请参考 tron-docker metric_monitor README 的 [All Metrics 章节](https://github.com/tronprotocol/tron-docker/blob/main/metric_monitor/README.md#all-metrics)。如果您想要监控节点的各项指标，则首先需要部署一个 Prometheus 服务，用于与 java-tron 节点通信，从该端点抓取指标数据。然后还需要部署一个可视化工具，如 Grafana，用于将 Prometheus 获取到的节点数据，以图像化界面的形式展示出来。下面将详细介绍 java-tron 节点监控系统的搭建流程。

## 配置 java-tron

如需使用 Prometheus 工具监控 java-tron 节点的运行情况，首先需要在节点配置文件中开启 Prometheus 指标监控，并设置 HTTP 端口号。在 `config.conf` 中找到 `node.metrics` 配置块，将 `prometheus.enable` 设置为 `true`：

```properties
node.metrics = {
  prometheus {
    enable = true
    port = 9527
  }
}
```

Prometheus 监控默认关闭；启用后默认监听 `9527` 端口，可通过 `node.metrics.prometheus.port` 修改监听端口。

有关 Prometheus 和旧版监控配置的详细说明，请参阅[事件订阅与监控](configuration.md#event-subscription-and-monitoring)。

## 启动 java-tron 节点

完成配置后，请参考[启动 java-tron 节点](installing_javatron.md#starting-a-java-tron-node)一节启动节点。

## 部署 Prometheus 服务

[Prometheus](https://prometheus.io/download/) 官方提供了预编译的二进制文件以及 Docker 镜像，您可以直接在官网下载或者在 Docker Hub 上拉取 Docker 镜像，更多的安装与配置说明，请参考 [Prometheus 文档](https://prometheus.io/docs/introduction/overview/)。作为简单的部署说明，本文将采用 Docker 镜像部署方式：

1. 安装 Prometheus

    安装 Docker 后，输入如下命令拉取 Prometheus 镜像：

    ```bash
    docker pull prom/prometheus
    ```

2. 准备 Prometheus 配置文件

    下面是一个 Prometheus 配置文件模板 `prometheus.yaml`：

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
        - 192.0.2.10:9527
        labels:
          group: group-xxx
          instance: xxx-01
      - targets:
        - 192.0.2.20:9527
        labels:
          group: group-xxx
          instance: xxx-02
    ```

    此示例监控分别运行在两台远程主机上的 java-tron 节点。IP 地址 `192.0.2.10` 和 `192.0.2.20` 为占位地址，请将其替换为节点实际的 IP 地址或主机名，并使用各节点配置的 Prometheus 指标端口。将该文件保存到本机的某个目录，例如 `/Users/test/deploy/prometheus/prometheus.yaml`。

3. 启动一个 Prometheus 容器

    通过如下命令启动一个 Prometheus 容器，并挂载上一步准备的配置文件（`/Users/test/deploy/prometheus/prometheus.yaml`）：

    ```shell
    docker run --name prometheus \
        -d -p 9090:9090 \
        -v /Users/test/deploy/prometheus/prometheus.yaml:/etc/prometheus/prometheus.yml \
        prom/prometheus:latest
    ```

    容器启动后，您可以通过 `http://localhost:9090/` 查看 Prometheus 服务的运行情况。

    以下截图中的地址和采集目标数量仅为示例，可能与您的实际配置不同。

    点击 "Status" -> "Configuration"，查看容器使用的配置文件是否正确：

    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_config.png)

    点击 "Status" -> "Targets"，查看各个监控的 java-tron 节点状态：

    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_targets.png)
    
    比如这个示例中，第一个 endpoint，状态为 `UP`，表示 Prometheus 可以正常地抓取该节点的数据。而第二个 endpoint，状态为 `DOWN`，表示异常，具体参考 "Error" 中的描述。

    当监控的 java-tron 节点的状态都正常后，您就可以通过 Grafana 等可视化工具监控指标数据了，本文将通过 Grafana 来展示数据。

## 部署 Grafana

Grafana 可视化工具的部署流程如下：

> **Grafana 界面版本说明：** Grafana 界面可能随版本变化。下方截图和操作步骤可能与最新版本不同。最新操作说明请参阅 [Grafana Prometheus 数据源文档](https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/)。

1. 安装 Grafana

    请参考官方文档安装 [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)。本文将采用 Docker 部署方式，拉取的镜像为开源版（`grafana/grafana`）：

    ```bash
    docker pull grafana/grafana
    ```

2. 启动 Grafana

    您可以通过如下 Docker 命令来启动 Grafana：

    ```bash
    docker run -d --name=grafana -p 3000:3000 grafana/grafana
    ```

3. 登录 Grafana 界面

    启动后，可以通过 `http://localhost:3000/` 进入 Grafana 页面，初始的用户名和密码均是 `admin`，输入后根据提示修改密码，然后就可以进入到主界面了。点击左侧菜单中的 "Connections"，选择 "Data sources" 配置 Grafana 的数据源，并添加一个 Prometheus 数据源。

    在 "Prometheus server URL" 中输入 Prometheus 服务的 IP 和端口。图中的 URL 仅为示例，请使用您自己的 Prometheus 服务地址。

    ![Grafana Connections 菜单和 Prometheus 数据源配置](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_prometheus.png)
    
    点击页面最下方的 "Save & test" 按钮。Grafana 会测试连接，测试成功后会显示成功提示。

4. 导入 Dashboard

    为了方便 java-tron 节点部署者，TRON 社区提供了一组预配置的 Grafana 仪表盘，每个仪表盘以一份 JSON 文件提供。请参考 tron-docker metric_monitor README 的 [Import dashboard 章节](https://github.com/tronprotocol/tron-docker/blob/main/metric_monitor/README.md#import-dashboard)将其导入到 Grafana。

    > **注意：** `node-exporter-full.json` 仪表盘展示主机资源指标，例如 CPU、内存、磁盘和网络使用情况。使用该仪表盘需要在被监控的主机上单独部署 Node Exporter，并配置 Prometheus 采集其指标。仅依靠 java-tron 的指标端点无法提供此仪表盘所需的指标。部署步骤请参阅 [Node Exporter 官方指南](https://prometheus.io/docs/guides/node-exporter/)。如果只需要 java-tron 仪表盘，可以跳过此模板。

    点击左侧菜单中的 "Dashboards"，然后选择 "New" → "Import"。点击 "Upload JSON file" 上传上面提到的 JSON 文件之一，如有提示，选择您的 Prometheus 数据源，然后点击 "Import"。
    
    ![Grafana Dashboards 的 New 和 Import 菜单](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/metrics_import.png)
    
    随后 Grafana 将根据导入的 JSON 文件渲染出对应的仪表盘，您可以实时监控节点的运行情况。
