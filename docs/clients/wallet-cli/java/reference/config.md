# 配置参考

`config.conf` 的完整参考。启动时，wallet-cli 先从进程工作目录读取 `./config.conf`；该文件不存在时，
则加载打包在 classpath 中的资源（源码检出中对应 `src/main/resources/config.conf`）。你也可以在运行时用
[`SwitchNetwork`](../commands/network.md) 切换网络。

## 最小配置

一份最小的 `config.conf` 只需要一个 FullNode 端点。保留 `net.type` 在配置主网 API key 时有用，但它并不决定当前使用哪个网络：

```
net {
  type = mainnet
}

fullnode = {
  ip.list = [
    "fullnode ip : port"
  ]
}
```

## 完整的带注释配置

包含可选的 Solidity 节点、Ledger 调试、账户锁定、GasFree、TronGrid API key、TronLink 多重签名和
记录条数限制：

```
net {
 type = mainnet
}

fullnode = {
  ip.list = [
    "fullnode ip : port"
  ]
}

#soliditynode = {
#  //此列表中的 IP 只能全部设为 solidity 节点。
#  ip.list = [
#     "ip : solidity port" // 默认 solidity
#  ]
#  // 注意：solidity 节点是可选的
#}

# 开启 ledger 调试
# ledger_debug = true

# 要使用登录账户的锁定/解锁功能，需要在 config.conf 中配置 lockAccount = true。
# 当前登录账户被锁定后，将不允许签名和交易。锁定之后可以再解锁，默认在 300 秒后
# 自动重新锁定；解锁时可以指定以秒为单位的时长参数。

# lockAccount = true

# 要使用 gasfree 功能，请先申请 APIkey 和 apiSecret。
# 详情请参考
# https://docs.google.com/forms/d/e/1FAIpQLSc5EB1X8JN7LA4SAVAG99VziXEY6Kv6JxmlBry9rUBlwI-GaQ/viewform
gasfree = {
  mainnet = {
     apiKey = ""
     apiSecret = ""
  }
  testnet = {
     apiKey = ""
     apiSecret = ""
  }
}

# 如果主网上的 gRPC 请求受到限速，可以申请 Trongrid 的 apiKey 以改善使用体验
grpc = {
  mainnet = {
    apiKey = ""
  }
}

# 设置可保留的交易记录与备份记录的最大条数
maxRecords = 1000

# 要使用 tronlink 多签功能，请先申请 secretId 和 secretKey。
# 详情请参考
# https://docs.google.com/forms/d/e/1FAIpQLSc5EB1X8JN7LA4SAVAG99VziXEY6Kv6JxmlBry9rUBlwI-GaQ/viewform
# 如果不想申请，可以使用下面这组有速率限制的 secretId 和 secretKey：
# secretId = "TEST", secretKey = "TESTTESTTEST", channel = "test".
tronlink = {
  mainnet = {
    secretId = ""
    secretKey = ""
    channel = ""
  }
  testnet = {
    secretId = ""
    secretKey = ""
    channel = ""
  }
}
```

## 字段汇总

| 字段 | 用途 |
|---|---|
| `net.type` | 决定是否加载 `grpc.mainnet.apiKey`。它并不决定当前使用哪个网络。 |
| `fullnode.ip.list` | FullNode 端点 `ip : port`。 |
| `soliditynode.ip.list` | 可选的 SolidityNode 端点。 |
| `ledger_debug` | 启用 Ledger 调试输出。 |
| `lockAccount` | 启用 [`Lock`/`Unlock`](../commands/wallet.md#lock) 功能（默认解锁时长 300 秒）。 |
| `gasfree.{mainnet,testnet}.apiKey` / `apiSecret` | [GasFree](../commands/gasfree.md) 凭据。 |
| `grpc.mainnet.apiKey` | 用于提高 gRPC 速率限制的 TronGrid API key。 |
| `maxRecords` | 保留的交易 / 备份记录的最大条数。 |
| `tronlink.{mainnet,testnet}.secretId` / `secretKey` / `channel` | [TronLink 多签](../commands/multisig.md#tronlinkmultisign) 凭据。 |

## 连接 Java-tron

wallet-cli 通过 gRPC 连接 Java-tron。启动时，程序会将配置中实际提供的 `fullnode.ip.list`、
`soliditynode.ip.list` 或两者，与内置的主网、Nile 和 Shasta 端点进行比较，据此**推断**所用网络。
未配置的端点类型不参与比较。例如，只配置 Nile FullNode 时，程序仍会识别为 Nile；无法匹配任何内置
网络的端点组合则会识别为 `CUSTOM`。`net.type = mainnet` 并不覆盖该判断，因此配合 Nile 端点时仍会
连接 Nile。发送资产前，请直接核对实际端点。

若想在不重新打包 JAR 的前提下覆盖内置配置，把 `config.conf` 放到运行 `java -jar` 时的工作目录即可。
你也可以在运行时使用 `SwitchNetwork` 在主网、Nile、Shasta 以及自定义端点之间切换——参见
[commands/network](../commands/network.md)。

## 另请参见

- [Java CLI 概览](../index.md)——安装与构建步骤
- [commands/network](../commands/network.md) · [commands/gasfree](../commands/gasfree.md) · [commands/multisig](../commands/multisig.md)
