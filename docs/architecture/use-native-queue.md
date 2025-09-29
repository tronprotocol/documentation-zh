# 使用 Java-tron 内置消息队列进行事件订阅

TRON 提供了灵活的事件订阅功能，开发者既可以通过 **事件插件** 获取链上事件，也可以使用 Java-tron 内置的 **ZeroMQ 消息队列** 实现轻量级订阅。

二者的核心区别在于：

* **事件插件** 需要单独部署，适用于将事件推送至外部系统（如 MongoDB、Kafka）进行落库、分析或异步处理；
* **ZeroMQ 消息队列** 是 Java-tron 内置实现，无需额外部署。事件订阅方只需连接节点的发布端口并配置订阅主题，即可实时接收事件。但该方式不支持事件持久化存储，仅适用于短期监听和即时处理场景。

因此，当您希望以最小成本、快速接入事件流，并不依赖持久化能力时，使用 **内置 ZeroMQ 消息队列** 将是更轻便、直接的选择。本指南将详细介绍如何通过 Java-tron 内置的消息队列来订阅事件。


### 配置节点
要通过 Java-tron 内置的 ZeroMQ 实现事件订阅，需在节点的配置文件中启用内置消息队列功能。具体操作如下：

```
event.subscribe = {
  native = {
    useNativeQueue = true 
    bindport = 5555 
    sendqueuelength = 1000 
  }

  ......
 
  topics = [
    {
      triggerName = "block" 
      enable = true
      topic = "block" 
    },
    ......
  ]
}
```

* `native.useNativeQueue`: `true` 为使用内置消息队列，`false` 为使用事件插件
* `native.bindport`: ZeroMQ 发布者绑定端口。本例中为 `5555`，所以订阅者应连接的发布者地址为`"tcp://127.0.0.1:5555"`
* `native.sendqueuelength`: 发送队列的长度，即当订阅者接收消息较慢的情况下，TCP 缓冲区最多容纳的发布者发布的消息数量，超过则丢弃
* `topics`: 订阅的 [事件类型](../event/#_4)，包括区块类型、交易类型等

### 启动节点
事件订阅服务默认为关闭状态，需要通过配置命令行参数 `--es` 的方式来启用。开启事件订阅服务的节点的启动命令如下：
```
$ java -jar FullNode.jar --es
```

### 准备事件订阅脚本

本文以 Node.js 为例来说明如何订阅事件。

首先，下载 `ZeroMQ` 库：
```
$ npm install zeromq@5
```
然后，编写订阅者代码：
```
// subscriber.js
var zmq = require("zeromq"),
var sock = zmq.socket("sub");

sock.connect("tcp://127.0.0.1:5555");
sock.subscribe("block");
console.log("Subscriber connected to port 5555");

sock.on("message", function(topic, message) {
  console.log(
    "received a message related to:",
    Buffer.from(topic).toString(),
    ", containing message:",
    Buffer.from(message).toString()
  );
});
```
本示例将订阅者连接到了节点事件发布者，并订阅了 `block` 事件。

### 启动订阅者

Node.js 启动命令如下：
```
$ node subscriber.js

> Subscriber connected to port 5555
```
当节点有新的区块时，该订阅者将收到区块事件，输出信息如下：
```
received a message related to: blockTrigger, containing message: {"timeStamp":1678343709000,"triggerName":"blockTrigger","blockNumber":1361,"blockHash":"00000000000005519b3995cd638753a862c812d1bda11de14bbfaa5ad3383280","transactionSize":0,"latestSolidifiedBlockNumber":1361,"transactionList":[]}
received a message related to: blockTrigger, containing message: {"timeStamp":1678343712000,"triggerName":"blockTrigger","blockNumber":1362,"blockHash":"0000000000000552d53d1bdd9929e4533a983f14df8931ee9b3bf6d6c74a47b0","transactionSize":0,"latestSolidifiedBlockNumber":1362,"transactionList":[]}
```
