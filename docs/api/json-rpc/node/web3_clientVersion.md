# web3_clientVersion

返回节点客户端版本字符串。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#web3ClientVersion`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无（`params: []`）。

请求示例：

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'
```

## 响应

格式 `TRON/v<version>/<os.name>/Java<javaSpecVersion>`，由 `Version.getVersion()` + `System.getProperty("os.name")` + `System.getProperty("java.specification.version")` 拼接而成。

下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "TRON/v4.8.1/Linux/Java1.8"
}
```

> 版本号会随节点升级变化；`os.name` / `java.specification.version` 取决于节点宿主环境。

### 异常响应

无业务异常。
