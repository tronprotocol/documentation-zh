# 账户模型

## 账户模型介绍

TRON 采用账户模型进行记账。网络中的所有活动，如转账、投票、部署合约等，都围绕账户展开。

* **唯一标识**：每个账户的唯一标识是其地址 (Address)，通常以 `T` 开头。
* **权限控制**：对账户的任何操作（如转账）都需要对应的**私钥**进行签名。
* **账户资产与能力**：每个账户可以拥有和管理多种资源，包括：

    * **资产**：TRX、TRC-10、TRC-20、TRC-721/TRC-1155 NFT 等。 
    * **网络资源**：带宽和能量。
    * **权限与活动**：发起交易、部署和调用智能合约、参与超级代表选举（投票或成为候选人）等。

## 创建账号的方式

创建一个新的TRON账户主要有两种方式：

**方式一：链下生成与激活**

* 生成地址：使用钱包应用（如 [TronLink](https://www.tronlink.org/)）生成一对私钥和地址。
* 激活账户：此时账户仅存在于理论上，需要被“激活”才能在链上使用。激活方式是从一个已存在的账户向这个新地址发送任意数量的 TRX 或 TRC-10 代币。交易成功后，新账户即在TRON网络上被创建。

**方式二：通过内置合约创建**

* 开发者可以调用 `CreateAccount` 内置合约，完成创建账户。

**账户的创建成本:**

1. 创建并激活一个新账户需支付的 1 TRX 创建账户的费。
2. 除此之外，如果账户拥有足够的带宽（包括质押 TRX 获得的带宽或他人代理的带宽），那么创建账户只会消耗带宽，否则，创建账户需要支付 0.1 个TRX带宽费用。

## 生成密钥对算法

TRON的签名算法为ECDSA，选用曲线为SECP256K1。其私钥为一个随机数，公钥为椭圆曲线上一个点。生成过程为：首先生成一个随机数`d`作为私钥，再计算`P = d × G`作为公钥，其中`G`为椭圆曲线的基点，基点是公开的。

私钥是一个32字节的大数，公钥由2个32字节的大数组成，分别是上述`P`点的横坐标和纵坐标。

## TRON地址生成

1. 用公钥P作为输入，计算SHA3得到结果H，SHA3选用Keccak256。
2. 取H的最后20字节，在前面填充一个字节0x41得到address。
3. 对address进行base58check计算得到最终地址。

### Base58Check计算过程

1. 计算校验码
    a. 对`address`进行SHA256哈希运算，得到`h1`  
    b. 对`h1`再次进行SHA256运算，得到`h2`  
    c. 取`h2`的前4字节作为校验码`check`
2. 拼接数据  
将`check`拼接到`address`之后，得到`address||check`
3. Base58编码  
对`address||check`进行Base58编码，Base58的字符表为：`"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"`  ，排除了易混淆字符：`0`(阿拉伯数字0) 、`O`(大写字母O)、`I`(大写字母I)、`l`(小写字母l)。

### TRON地址特性

Base58编码原理是将以256为基数的大整数转换为以58为基数表示，再映射到字符表。由于`address||check`首字节固定为`0x41`，其十进制值`N`满足：`65 × 256²⁴ ≤ N < 66 × 256²⁴`。

- 长度为`34`位：由于`58³⁴ > 66 × 256²⁴`表明`34`位足够，`58³³ < 65 × 256²⁴`表明`33`位不够，所以所以长度只能是`34`位
- 首字母为`T`：首先长度已经确定是`34`位，并且由于`27 × 58³³ > 66 × 256²⁴`表明第一位必须小于27， `26 × 58³³ < 65 × 256²⁴`表明第一位必须大于等于26，所以最高位只能是`26`，而`26`对应base58字符表的`T`(`0`对应`'1'`)

## 签名说明

### 算法

1.  取交易的rawdata，转成byte[]格式，记为`data`（以Java中类型为例：`byte[]`）。
2. 对`data`进行sha256运算得到交易的hash值，记为`hash`。
3. 用交易合约中的地址对应的私钥`d`，对`hash`进行签名，签名算法为ECDSA算法（选用的曲线为SECP256K1）。签名结果包含`r`，`s`，`v`三个值：  

    * 计算`r`值：随机生成一个临时私钥`k`，计算临时公钥`K = k × G`（`G`：曲线基点），`r = K_x mod n`，即`K`的横坐标模`n`，其中`n`是曲线阶数（`n`和`G`满足`n × G = O`，`O`是有限域上椭圆曲线群的零点）。`r`为32个字节。
    * 计算`s`值：先计算临时私钥`k`对n的模逆`k⁻¹`，即`k⁻¹`满足`k⁻¹ × k = 1 mod n`，再通过交易的`hash`、用户的私钥`d`、`r`值计算`s`值，`s = (k⁻¹ × (hash + d × r)) mod n`。`s`为32个字节。
    * 计算`v`值：`v`值是恢复标志符，由于`r`值有取模运算以及椭圆曲线的对称性，如果只有`r`值，一个`r`最多可以恢复出四个`K`。`v`值的取值范围是`0、1、2、3`四个整数，历史上为了和以太坊保持一致，最后的`v`值会在`0、1、2、3`的基础上再加`27`，即最后`v`值的取值范围是`27、28、29、30`。有了确定的`v`，就可以恢复出唯一的`K`。`v`为1个字节。  

4. 将签名结果`r`，`s`，`v`拼接后添加到交易中，拼接顺序为`v || r || s`。

#### Java 代码示例

```java
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    ECDSASignature signature = myKey.sign(hash);
    ByteString bsSign = ByteString.copyFrom(signature.toByteArray());
    transactionBuilderSigned.addSignature(bsSign);
}
```

### 签名验证

Fullnode 节点收到交易后，会使用交易中的哈希和签名，通过 ECDSA 的恢复机制（ecrecover）计算出一个公钥，并由此推算出地址。如果该地址与交易中指定的发起方地址匹配，则验签通过。

#### 算法

1. 恢复公钥点 K：通过签名中的 v 和 r 可以唯一恢复出临时公钥点 K。
2. 推导公钥 P：

   - 已知签名方程：
      `s = k⁻¹(hash + d × r) mod n`
   - 两边同乘 k：
      ` s × k = (hash + d × r) mod n`
   - 两边再同乘曲线的基点 G（利用 `K = k × G` 和 `P = d × G`）：
      ` s × K = hash × G + r × P`
   - 因 `s、K、hash、G、r` 均已知，可求得 `P`

3. 生成 TRON 地址：[同 TRON 地址的生成](#tron)。
4. 地址验证：比对生成的 TRON 地址与交易合约中的地址是否一致。

#### 示例
验证签名由全节点进行，[ECDSA 算法的验签](https://github.com/tronprotocol/java-tron/blob/master/crypto/src/main/java/org/tron/common/crypto/ECKey.java)可参考 java-tron，核心函数为`signatureToAddress`。

### 签名规范化
ECDSA 签名（采用secp256k1曲线）存在延展性，即对于签名$(r, s)$, 其中 $r, s \in [1, n-1]$,  $(r, n - s)$ 仍然是合法的签名。由于比特币和以太坊签名会影响交易id,  分别在[BIP-62](https://github.com/bitcoin/bips/blob/master/bip-0062.mediawiki)  和 [EIP-2]( https://eips.ethereum.org/EIPS/eip-2) 要求签名必须规范化，即 $s \leq n/2$。 但对于TRON 网络，交易id并不包含签名信息，所以并不需要对签名规范化作严格的限制，验签也不需要对签名作规范化判断。虽然没有严格限制，但是目前`java-tron`和`wallet-cli`都对签名做了规范化处理。
