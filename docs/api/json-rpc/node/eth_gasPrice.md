# eth_gasPrice

当前 energy 单价（即 Tron 中 gas 的对应物）。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#gasPrice`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}'
```

## 响应

`wallet.getEnergyFee()` 的 hex 编码，单位 sun（1 TRX = 1e6 sun）。该值由链参数 `getEnergyFee` 决定，可被链上提案修改。

下例为上面 curl 调用 Nile testnet 抓回的真实响应（Nile 当前 energy 单价 = 100 sun/energy）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x64"
}
```

> 主网与各 testnet 的 energy 单价可能不同，且会随提案变更；`buildTransaction` 的 `gas` 参数乘以该值得到 `feeLimit`。

### 异常响应

无。
