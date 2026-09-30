# wallet-cli 8004

读取并管理 ERC-8004 Agent 身份。

ERC-8004 身份注册表（Identity Registry）本身是一个 NFT 合约：每个 Agent 是一个 token，其 id 就是它的 Agent ID，其 URI 指向一份由你自行托管的注册文档。wallet-cli 负责读取注册表并为注册表交易签名；它不负责构建或托管该文档。

## 用法

```
wallet-cli 8004 COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `8004 show` | [show.md](show.md) | 加载单个 Agent：所有者、URI、已批准的操作者，以及它的注册文档 |
| `8004 operator-check` | [operator-check.md](operator-check.md) | 某个操作者是否可以管理某所有者的全部 Agent |
| `8004 register` | [register.md](register.md) | 注册一个新 Agent |
| `8004 update` | [update.md](update.md) | 修改某个 Agent 的 URI |
| `8004 transfer` | [transfer.md](transfer.md) | 把某个 Agent 转移给新的所有者 |
| `8004 approve` | [approve.md](approve.md) | 为单个 Agent 批准一个操作者，或清除该批准 |
| `8004 add-operator` | [add-operator.md](add-operator.md) | 允许某个操作者管理本账户拥有的全部 Agent |
| `8004 remove-operator` | [remove-operator.md](remove-operator.md) | 收回该权限 |

## 工作方式

- **网络。** 注册表部署在 `tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base` 和 `base-sepolia` 上。在 `ethereum` 和 `sepolia` 上，所有命令都会以 `unsupported_network_capability` 失败。
- **Agent ID** 是十进制字符串。id 可以带上它的规范网络 id，例如 `tron:3448148188:172` 或 `eip155:97:42`（不接受 `nile:172` 这样的别名形式）；该网络必须就是当前所选网络，否则命令以 `chain_id_mismatch` 失败。
- **URI** 必须是 `https://`、`ipfs://`，或 base64 JSON 的 `data:` URI，最长 2048 个字符。[`show`](show.md) 只会加载 `https://` 和 `http://` 的注册文档，因此优先使用 `https://`。
- **读取类命令**（`show`、`operator-check`）不需要钱包。**写入类命令**用当前账户签名，并接受常规的交易选项：`--wait`、`--sign-only`、`--build-only`，以及 TRON 上的 `--fee-limit`、`--permission-id`、`--expiration`。
- **谁可以写。** `update` 和 `transfer` 需要该 Agent 的所有者、它已批准的操作者（来自 `approve`），或该所有者的操作者（来自 `add-operator`）。`approve` 需要所有者或该所有者的操作者——Agent 自身已批准的操作者不能把批准再转授出去。其他任何人都会在手续费估算阶段、签名之前被以 `not_authorized` 拒绝；不存在的 Agent ID 则以 `agent_not_found` 失败。
- **回执**把 Agent 相关字段归在 `data.identity` 下。那些需要在变更之后从链上读回的值——新 Agent 的 `agentId`、`newURI`、`newOwner`，以及操作者的 `approved`——只有加了 `--wait` 才会出现。

## 另请参见

[`contract send`](../contract/send.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
