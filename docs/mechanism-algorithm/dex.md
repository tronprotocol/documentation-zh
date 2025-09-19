# 去中心化交易所（DEX）

TRON 网络原生支持 **去中心化交易所（Decentralized Exchange, DEX）**，其核心由多个交易对构成。本文将介绍交易对的基本概念、创建方法、交易流程、注资与撤资机制，并附上常用查询方式与价格计算方法。



## 什么是交易对

一个交易对（`Exchange`）表示任意两种 TRC-10 代币之间的交易市场，可以是：

- 任意两个 TRC-10 代币之间；
- 一个 TRC-10 代币与 TRX 之间。

任何账户都可以创建任意组合的交易对，即使网络中已有相同组合。TRON 网络中所有交易对都遵循 **Bancor 协议** 进行资产兑换，且默认两种代币权重相等。因此，交易对中两种代币的余额比即为当前价格。

**示例：**  
假设一个交易对中包含的两个代币 ABC 和 DEF：

- ABC 的余额为 `10,000,000`；
- DEF 的余额为 `1,000,000`；

则当前汇率为：10 ABC = 1 DEF


## 创建交易对

任何账户都可以发起交易对创建。**创建交易对的手续费为 1024 TRX，且会被销毁**。

交易对创建时需要提供初始的两种代币余额，成功创建后系统会自动从发起者账户中扣除相应代币。

### 合约：`ExchangeCreateContract`

参数如下：

- `first_token_id`：第一个代币的 ID；
- `first_token_balance`：第一个代币的初始余额；
- `second_token_id`：第二个代币的 ID；
- `second_token_balance`：第二个代币的初始余额。

> **注意：** 若包含 TRX，请使用 `_` 表示；TRX 的单位为 `sun`（1 TRX = 1,000,000 sun）。

### 示例：

```
ExchangeCreate abc 10000000 _ 1000000000000
```
上述命令表示创建 `abc` 与 `TRX` 的交易对，初始分别注入 10,000,000 个 abc 代币 （创建代币精度 0-6）和 1,000,000,000,000 sun（即 1,000,000 TRX）。若账户余额不足，将导致创建交易失败。


## 交易
所有账户均可在任意交易对中进行即时交易。交易无需挂单，价格和数量完全基于 Bancor 协议计算。

### 合约：`ExchangeTransactionContract`
参数如下：

- `exchange_id`：交易对 ID（系统会按创建时间分配唯一 ID）；
- `token_id`：卖出的代币 ID；
- `quant`：卖出的数量；
- `expected`：希望获得的最小另一种代币数量（若实际获得小于该值，则交易失败）。

#### 示例：
假设 `abc` 与 `TRX` 的交易对 ID 为 1，当前：

- abc 余额为 10,000,000；
- TRX 余额为 1,000,000；

若用户希望花费 100 TRX（100,000,000 sun）买入至少 990 个 abc，则执行：
```
ExchangeTransaction 1 _ 100000000 990
```
交易成功后，用户账户中 `TRX` 减少，`abc` 增加；交易对中 `TRX` 增加，`abc` 减少。
用户账户实际获得的 `abc` 数量可通过 `gettransactioninfobyid` 接口，查询 `exchange_received_amount` 字段。

## 注资
当交易对中某一代币余额偏低时，会导致交易造成剧烈价格波动。此时，**交易对的创建者可以选择向其注入更多资产**，以提升稳定性。

>**注资规则：**
>- **仅交易对创建者可执行；**
>- **无需手续费；**
>- **系统会根据当前价格比例计算另一代币所需数量，以保持价格不变。**

### 合约：`ExchangeInjectContract`
参数如下：

- `exchange_id`：交易对 ID；
- `token_id`：要注资的代币 ID；
- `quant`：注资数量。

### 示例：
假设 `abc` 与 `TRX` 的交易对 ID 为 1，当前：
- `abc` 余额为 10,000,000，
- `TRX` 余额为 1,000,000，

若创建者希望将 abc 增加 10%（即增加 1,000,000 abc），则执行：

```
ExchangeInject 1 abc 1000000
```
若成功，交易对将新增 1,000,000 abc 以及对应比例的 100,000 TRX，创建者账户中这些资产将被扣除。

## 撤资（Withdraw）
交易对资产完全归创建者所有。创建者可以随时撤出交易对中的部分资产。

>**撤资规则：**
>- **仅交易对创建者可执行；**
>- **无需手续费；**
>- **系统按当前代币比例撤出另一种代币，确保价格不变，但会提升价格波动性。**

### 合约：`ExchangeWithdrawContract`
参数如下：

- `exchange_id`：交易对 ID；
- `token_id`：要撤资的代币 ID；
- `quant`：撤资数量。

### 示例：
假设 `abc` 与 `TRX` 的交易对 ID 为 1，当前：
- `abc` 余额为 10,000,000，
- `TRX` 余额为 1,000,000，

若创建者希望将 abc 撤出 10%（即减少 1,000,000 abc），则执行：

```
ExchangeWithdraw 1 abc 1000000
```
交易成功后，交易对中将减少 1,000,000 abc 以及对应比例的 100,000 TRX，创建者账户中增加这些资产。

## 查询与计算
### 查询交易对信息
TRON 提供多种交易对查询接口：

**1. 查询所有交易对信息：** `ListExchanges`

**2. 分页查询交易对列表：** `GetPaginatedExchangeList`



**3. 查询指定交易对详情：** `GetExchangeById`

详细 API 文档参考：
[RPC-API 接口文档](https://tronprotocol.github.io/documentation-zh/api/rpc/)

### 价格计算
假设交易对中：

- `first_token_price = 100 sun`；
- `first_token_balance = 1,000,000`；
- `second_token_balance = 2,000,000`；

则 `second_token_price` 为：

```
second_token_price = first_token_price * (first_token_balance / second_token_balance)
                   = 100 * (1,000,000 / 2,000,000)
                   = 50 sun
```
### 兑换数量计算
假设使用 `first_token` 兑换 `second_token`：

- `sellTokenQuant`：出售的 `first_token` 数量；
- `buyTokenQuant`：兑换获得的 `second_token` 数量；
- `balance`：当前交易对中 `second_token` 的余额；
- `supply`：Bancor 协议公式中使用的固定常数 `10^18`。

计算流程如下：

```
supplyQuant = -supply * (1.0 - Math.pow(1.0 + (double) sellTokenQuant / (firstTokenBalance + sellTokenQuant), 0.0005));
buyTokenQuant = (long)(balance * (Math.pow(1.0 + (double) supplyQuant / supply, 2000.0) - 1.0));
```
>**注意**: 市场价格会因网络中其他交易行为实时波动。

更多接口详情，请参考：[HTTP API 文档](https://tronprotocol.github.io/documentation-zh/api/http/)。

