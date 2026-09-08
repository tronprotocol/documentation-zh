# 为 wallet-cli 编写脚本

本页介绍如何从 shell 脚本和 CI 中调用 wallet-cli；完整的接口规范见
[machine-interface.md](../machine-interface.md)。

## 先确认可用能力

在脚本中写死命令或参数之前，请先查询 CLI 提供的能力。一次调用即可返回全部命令、以 JSON Schema 描述的参数、各命令支持的链家族，以及持续维护的错误码索引：

```bash
wallet-cli --json-schema | jq '.commands[] | select(.id == "tx.send") | {families, examples}'
wallet-cli --json-schema | jq '.errorCodes'
```

建议使用该接口，而不是抓取 `--help` 的文本输出；这份目录与参数解析器和帮助文本来自同一数据源。

## 三项基本规则

**1. 始终添加 `-o json`。** text 输出面向人工阅读，格式可能变化；JSON 输出才是稳定的程序接口。
每次运行只会在 stdout 输出一个 JSON 对象：

```bash
wallet-cli account balance --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.balance","data":{"address":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","balance":"1976489000","decimals":6,"symbol":"TRX"},"meta":{"durationMs":1114,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

**2. 先检查退出码，再检查 `error.code`。** `0` 表示成功，`1` 表示运行时失败，`2` 表示命令用法错误。脚本需要在不同网络之间切换时，应单独处理退出码 `2` 下的两个错误码：`family_mismatch`（命令或账户不适用于所选网络的链家族）和 `invalid_option`（使用了属于另一个家族的参数）：

```bash
if out=$(wallet-cli account balance --network tron:3448148188 -o json); then
  bal=$(jq -r '.data.balance' <<<"$out")     # 原始 SUN，是*字符串*
else
  code=$(jq -r '.error.code' <<<"$out")      # e.g. timeout, rpc_error
fi
```

**3. 通过 stdin 传入敏感信息，不要放在 argv 中。** 参数中的密码、助记词或私钥可能出现在 shell 历史
和 `ps` 输出中。wallet-cli 也不会读取任何专用的敏感信息环境变量：

```bash
printf '%s' "$PW" | wallet-cli tx send --to T... --amount 1 \
  --network tron:3448148188 --password-stdin -o json
```

（`$PW` 应来自密钥存储，并仅作为本次管道使用的临时 shell 变量；不要从仓库中的文件读取，也不要长期 `export`。每次运行只能使用一个 `*-stdin` 标志。）

## 等待确认

`tx send` 在提交时就返回。对脚本来说，最简单且安全的写法是 `--wait`：

```bash
wallet-cli tx send --to T... --amount 1 --network tron:3448148188 \
  --password-stdin --wait --wait-timeout 90000 -o json
```

也可以解耦：先取出 `data.txId`，再轮询 [`tx status`](../commands/tx/status.md) 直到 `data.state` 为 `confirmed`（遇到 `failed` 则中止）。完整的四状态轮询模式，以及批量操作的相关规则，见 [machine-interface.md → 脚本安全](../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)。

## 分离签名与广播 {#sign-here-broadcast-there}

`--sign-only` 把签名和广播拆开了，但它在签名之前仍然要通过所选的 RPC 端点完成构建和估算。如果签名机没有链访问权限，请在联网机器上构建未签名的 hex，在离线机器上对这份产物签名，再回到联网机器广播：

```bash
# 在联网的构建机上
wallet-cli tx send --to T... --amount 1 --network tron:3448148188 \
  --build-only --expiration 3600000 -o json | jq -r '.data.hex' > unsigned.hex

# 在离线的签名机上
printf '%s' "$PW" | wallet-cli tx sign --file unsigned.hex --network tron:3448148188 \
  --offline --password-stdin --out signed.hex

# 回到联网机器
wallet-cli tx broadcast --file signed.hex --network tron:3448148188 -o json
```

上述 **hex** 格式适用于两个链家族：TRON 使用 protobuf，EVM 使用 RLP。`--expiration` 仅适用于 TRON；示例将交易有效期设为一小时，以便在不同机器之间传递文件并完成签名，允许的上限为 24 小时。节点默认有效期约为 60 秒，`tx sign --offline` 会拒绝已过期的交易，因此应设置满足流程所需的最短有效期；过期后需要重新构建。EVM 交易没有过期时间字段，请省略该参数。如果签名机器可以访问 RPC，只是不希望由它广播，可使用 `tx send --sign-only` 直接输出已签名的 hex。

TRON 也接受已签名交易的 JSON，但 JSON 只能走 `--transaction` 或 `--tx-stdin`；`--file` 和 `--hex` 只收 hex：

```bash
wallet-cli tx send ... --sign-only -o json | jq -c '.data.signed' > signed.json
wallet-cli tx broadcast --tx-stdin --network tron:3448148188 -o json < signed.json
```

`--transaction` 和 `--tx-stdin` 都标注为 `(TRON only)`；在 EVM 网络上它们会以 `invalid_option` 失败。可能面向两个家族的脚本，请优先使用 `--file` / `--hex`。

## 超时与重试

每次 RPC 或设备调用都受 `--timeout`（毫秒）限制。出现 `error.code = "timeout"` 时，读取类命令可以
适当增大超时时间后重试。对于 `tx send`，应先使用已有的 txid 查询 `tx status`；未确认状态就直接
重发可能造成重复付款。

## 另请参见

- [machine-interface](../machine-interface.md)——响应 schema、错误码、稳定性承诺
- [命令参考](../commands/index.md)——每条命令的 `data` 返回数据，以及[哪些命令能在哪些网络上运行](../commands/index.md#which-commands-run-on-which-networks)
