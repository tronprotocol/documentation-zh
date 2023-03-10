# 使用Java-tron内置的消息队列进行事件订阅
TRON提供了事件订阅服务，开发者不但可以通过事件插件来获取链上事件，还可以通过[Java-tron 内置的ZeroMQ消息队列](https://github.com/tronprotocol/tips/blob/master/tip-28.md)来订阅事件。所不同的是，事件插件需要额外部署，用来实现事件转储：开发者可以根据需求选择合适的存储工具，如MongoDB，Kafka等，插件帮助完成对订阅的事件的存储工作。而Java-tron内置的ZeroMQ，不需要额外的部署操作，事件订阅者直接连接发布者ip及端口、设置订阅主题，接收订阅的事件即可，但该方式不提供事件存储功能。因此，当开发者希望短期并直接从节点订阅事件，那么使用内置的消息队列将是一个更合适的选择。

本文将详细介绍如何通过Java-tron内置的消息队列来订阅事件。


## 配置节点
要使用节点内置的ZeroMQ进行事件订阅，需要在节点配置文件中将`useNativeQueue`配置项设置为`true`。
```
event.subscribe = {
  native = {
    useNativeQueue = true // if true, use native message queue, else use event plugin.
    bindport = 5555 // bind port
    sendqueuelength = 1000 //max length of send queue
  }

  ......
 
  topics = [
    {
      triggerName = "block" // block trigger, the value can't be modified
      enable = true
      topic = "block" // plugin topic, the value could be modified
    },
    ......
  ]
}
```

* `native.useNativeQueue`: true为使用内置消息队列，false为使用事件插件
* `native.bindport`: ZeroMQ发布者绑定端口。本例中为`5555`，所以订阅者应连接的发布者地址为`"tcp://127.0.0.1:5555"`
* `native.sendqueuelength`: 发送队列的长度，即当订阅者接收消息较慢的情况下，TCP缓冲区最多容纳的发布者发布的消息数量，超过则丢弃
* `topics`: 订阅的[事件类型](../../architecture/event/#_2)，包括区块类型、交易类型等

## 启动节点
事件订阅服务默认为关闭状态，需要通过配置命令行参数 `--es` 的方式来启用。开启事件订阅服务的节点的启动命令如下：
```
$ java -jar FullNode.jar --es
```

## 准备事件订阅脚本
本文以Nodejs为例来说明如何订阅事件。

首先，下载zeromq库：
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
本示例将订阅者连接到了节点事件发布者，并订阅了`block`事件。

## 启动订阅者
Nodejs启动命令如下：
```
$ node subscriber.js

> Subscriber connected to port 5555
```
当节点有新的区块时，该订阅者将收到区块事件，输出信息如下：
```
received a message related to: blockTrigger, containing message: {"timeStamp":1678343709000,"triggerName":"blockTrigger","blockNumber":1361,"blockHash":"00000000000005519b3995cd638753a862c812d1bda11de14bbfaa5ad3383280","transactionSize":0,"latestSolidifiedBlockNumber":1361,"transactionList":[]}
received a message related to: blockTrigger, containing message: {"timeStamp":1678343712000,"triggerName":"blockTrigger","blockNumber":1362,"blockHash":"0000000000000552d53d1bdd9929e4533a983f14df8931ee9b3bf6d6c74a47b0","transactionSize":0,"latestSolidifiedBlockNumber":1362,"transactionList":[]}
```