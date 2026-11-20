# 账户模型

## 账户模型介绍

TRON 采用账户模型进行记账。网络中的所有活动，如转账、投票、部署合约等，都围绕账户展开。

* **唯一标识**：每个账户的唯一标识是其地址 (Address)，通常以 `T` 开头。
* **权限控制**：账户发起的交易必须由所选账户权限授权的一个或多个私钥签名，且签名者的权重之和必须达到该权限的阈值。
* **账户资产与能力**：每个账户可以拥有和管理多种资源，包括：

    * **资产**：TRX、TRC-10、TRC-20、TRC-721/TRC-1155 NFT 等。 
    * **网络资源**：带宽和能量。
    * **权限与活动**：发起交易、部署和调用智能合约、参与超级代表选举（投票或成为候选人）等。

## 创建账号的方式

创建一个新的 TRON 普通账户主要有两种方式。智能合约账户则通过合约部署创建。

**方式一：链下生成与激活**

* 生成地址：使用钱包应用（如 [TronLink](https://www.tronlink.org/)）生成密钥对（私钥和公钥），并由公钥派生地址。
* 激活账户：此时账户仅存在于理论上，需要被“激活”才能在链上使用。激活方式是从一个已存在的账户向这个新地址转入金额为正数的 TRX 或 TRC-10 token。交易成功后，新账户即在 TRON 网络上被创建。

**方式二：通过系统合约创建**

* 开发者可以调用 `AccountCreateContract` 系统合约，完成创建账户。

**账户的创建成本:**

通过 `AccountCreateContract`、使用 `TransferContract` 的 TRX 转账或使用 `TransferAssetContract` 的 TRC-10 转账创建账户时，需额外支付账户创建费，由交易发起账户承担并销毁。该费用由网络参数 `getCreateNewAccountFeeInSystemContract` 决定（主网当前为 1 TRX）。

交易还会消耗带宽，但不能使用每日免费带宽。如果发起账户通过质押或他人代理获得的带宽不足，则销毁固定费用 `getCreateAccountFee`（主网当前为 0.1 TRX），替代通常按字节计算的带宽费。这两项费用参数均可通过委员会提案修改。

智能合约执行也可以创建普通账户，例如向未激活地址转入金额为正数的 TRX 或 TRC-10 token，或执行 `SELFDESTRUCT` 并指定一个尚不存在的受益地址。执行 `SELFDESTRUCT` 时，即使合约余额为零，也可以创建受益账户。这些账户创建路径会产生额外的 25,000 能量基础成本，不适用上述两项固定费用。

## 生成密钥对算法

TRON 的签名算法为 ECDSA，选用曲线为 SECP256K1。其私钥为一个随机数，公钥为椭圆曲线上一个点。生成过程为：首先生成一个随机数 `d` 作为私钥，再计算 `P = d × G` 作为公钥，其中 `G` 为椭圆曲线的基点，基点是公开的。

私钥是一个 32 字节的大数，公钥由 2 个 32 字节的大数组成，分别是上述 `P` 点的横坐标和纵坐标。

## TRON 地址生成 { #tron-address-generation }

以下流程用于从公钥派生普通账户地址。智能合约地址采用独立的派生规则。

1. 用公钥 `P` 作为输入，计算 SHA3 得到结果 `H`，SHA3 选用 Keccak256。
2. 取 `H` 的最后 20 字节，在前面填充一个字节 `0x41` 得到 `address`。
3. 对 `address` 进行 Base58check 计算得到最终地址。

### Base58Check 计算过程

1. 计算校验码

    a. 对 `address` 进行 SHA256 哈希运算，得到 `h1`  
    b. 对 `h1` 再次进行 SHA256 运算，得到 `h2`  
    c. 取 `h2` 的前 4 字节作为校验码 `check`

2. 拼接数据  
将 `check` 拼接到 `address` 之后，得到 `address||check`
3. Base58 编码  
对 `address||check` 进行 Base58 编码，Base58 的字符表为：`"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"`  ，排除了易混淆字符：`0`(阿拉伯数字 0) 、`O`(大写字母 O)、`I`(大写字母 I)、`l`(小写字母 l)。

### TRON 地址特性

Base58 编码原理是将以 256 为基数的大整数转换为以 58 为基数表示，再映射到字符表。由于 `address||check` 首字节固定为 `0x41`，其十进制值 `N` 满足：`65 × 256²⁴ ≤ N < 66 × 256²⁴`。

- 长度为 `34` 位：由于 `58³⁴ > 66 × 256²⁴` 表明 `34` 位足够，`58³³ < 65 × 256²⁴` 表明 `33` 位不够，所以长度只能是 `34` 位
- 首字母为 `T`：首先长度已经确定是 `34` 位，并且由于 `27 × 58³³ > 66 × 256²⁴` 表明第一位必须小于 27， `26 × 58³³ < 65 × 256²⁴` 表明第一位必须大于等于 26，所以最高位只能是 `26`，而 `26` 对应 base58 字符表的 `T`(`0` 对应 `'1'`)

## 签名说明

交易可以使用 Owner 权限（`Permission_id = 0`）或已有的 Active 权限（`Permission_id ≥ 2`）进行签名。Witness 权限（`Permission_id = 1`）不能用于交易签名。

### 算法

1. 取交易的 `raw_data`，转成 `byte[]` 格式，记为 `data`（以 Java 中类型为例：`byte[]`）。
2. 对 `data` 进行 sha256 运算得到交易的 hash 值，记为 `hash`。
3. 使用交易合约的 `Permission_id` 所选账户权限授权的私钥 `d`，对 `hash` 进行签名。如果需要多个签名才能达到权限阈值，各签名者使用各自获授权的私钥对同一个 `hash` 签名。签名算法为 ECDSA 算法（选用的曲线为 SECP256K1）。每个签名结果包含 `r`，`s`，`v` 三个值：

    * **计算 `r` 值**：生成本次签名使用的 nonce `k`。java-tron 使用 HMAC-SHA256（`HMacDSAKCalculator`），根据私钥 `d` 和交易的 `hash` 确定性地派生 `k`，而非每次签名时随机抽取。计算临时公钥 `K = k × G`（`G`：曲线基点），再计算 `r = K_x mod n`，即 `K` 的横坐标模 `n`，其中 `n` 是曲线阶数（`n` 和 `G` 满足 `n × G = O`，`O` 是有限域上椭圆曲线群的零点）。`r` 为 32 个字节。
    * **计算 `s` 值**：先计算临时私钥 `k` 对 n 的模逆 `k⁻¹`，即 `k⁻¹` 满足 `k⁻¹ × k = 1 mod n`，再通过交易的 `hash`、用户的私钥 `d`、`r` 值计算 `s` 值，`s = (k⁻¹ × (hash + d × r)) mod n`。`s` 为 32 个字节。
    * **计算 `v` 值**：先计算`recoveryId`(恢复标识符)，由于 `r` 值有取模运算以及椭圆曲线的对称性，如果只有 `r` 值，一个 `r` 最多可以恢复出四个 `K`。`recoveryId` 的取值范围是 `0、1、2、3` 四个整数。`v`值的计算依赖于`recoveryId`，历史上为了和以太坊保持一致，`v`值设置成`recoveryId` 加`27`，即`v` 值的取值范围是 `27、28、29、30`。有了确定的 `v`，就可以恢复出唯一的 `K`。`v` 为 1 个字节。  

4. 将`r`，`s`，`recoveryId`或者`r`，`s`，`v`拼接后得到完整的签名值添加到交易中，拼接顺序为 `r || s || recoveryId` / `r || s || v`。目前官方客户端`wallet-cli`以及`java-tron`中产块时对区块的签名都是采用拼接`recoveryId`的形式，即`signature = r || s || recoveryId`


### Java 代码示例

```java
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    ECDSASignature signature = myKey.sign(hash);
    ByteString bsSign = ByteString.copyFrom(signature.toByteArray());
    transactionBuilderSigned.addSignature(bsSign);
    return transactionBuilderSigned.build();
}
```

## 签名验证

FullNode 节点收到交易后，会使用交易哈希和每个签名，通过 ECDSA 的恢复机制（ecrecover）恢复签名者的公钥，再由公钥派生签名者地址。节点根据交易合约的 `Permission_id` 所选账户权限校验这些地址。签名者必须获得该权限的授权，且权重之和必须达到权限阈值。签名者地址不必与交易中的 `owner_address` 相同。

### 算法

1. 恢复公钥点 `K`：通过签名中的 `v` 和 `r` 可以唯一恢复出临时公钥点 `K`。
2. 推导公钥 `P`：

    - 已知签名方程：`s = k⁻¹(hash + d × r) mod n`
    - 两边同乘 `k`：` s × k = (hash + d × r) mod n`
    - 两边再同乘曲线的基点 `G`（利用 `K = k × G` 和 `P = d × G`）：` s × K = hash × G + r × P`
    - 因 `s、K、hash、G、r` 均已知，可求得 `P`

3. 生成 TRON 地址：[同 TRON 地址的生成](#tron-address-generation)。
4. 权限验证：根据 `Permission_id` 所选的账户权限校验恢复出的签名者地址。拒绝重复签名者，并要求签名者的权重之和达到权限阈值。对于 Active 权限，还需检查是否允许该交易类型。

### 示例

签名验证由全节点进行。在 java-tron 中，[`ECKey.signatureToAddress`](https://github.com/tronprotocol/java-tron/blob/master/crypto/src/main/java/org/tron/common/crypto/ECKey.java) 用于恢复签名者地址，[`TransactionCapsule.validateSignature` 和 `checkWeight`](https://github.com/tronprotocol/java-tron/blob/master/chainbase/src/main/java/org/tron/core/capsule/TransactionCapsule.java) 用于检查账户权限和签名权重。

### 签名规范化

采用 secp256k1 曲线的 ECDSA 签名存在延展性：对于有效签名 $(r, s)$，$(r, n - s)$ 对同一公钥和消息仍然有效，其中 $n$ 为曲线阶数。

以太坊的 [EIP-2](https://eips.ethereum.org/EIPS/eip-2) 要求交易签名采用 low-S 值，即 $s \leq n/2$。

在 TRON 中，交易 ID 根据序列化后的 `raw_data` 计算，不包含签名。java-tron 的交易验签流程不强制要求 low-S。不过，java-tron 和 wallet-cli 都会在签名时将签名规范化为 low-S。
