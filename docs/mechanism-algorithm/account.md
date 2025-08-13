# 账户模型

## 账户模型介绍

TRON采用账户模型，账户的唯一标识为地址（address），对账户操作需要私钥签名。每个账户可以拥有TRX、TRC10 Token、带宽、能量等各种资源。通过发送交易可以增减TRX或者TRC10 Token余额,可以发布并拥有智能合约，也可以调用自己或者他人发布的智能合约。可以申请成为超级代表并被投票，也可以对超级代表进行投票等等。TRON所有的活动都围绕账户进行。

## 创建账号的方式

1. 首先用一个钱包应用(推荐[TronLink](https://www.tronlink.org/))生成一对私钥和地址，然后由已有老账户往新创建的账户发送TRX或其他Token完成账户创建的流程。

2. 通过调用CreateAccount内置合约，完成创建账户

如果账户有足够的通过质押TRX获得的带宽，那么创建账户只会消耗带宽，否则，创建账户会烧掉0.1个TRX。

## 生成密钥对算法

TRON的签名算法为ECDSA，选用曲线为SECP256K1。其私钥为一个随机数，公钥为椭圆曲线上一个点。生成过程为：首先生成一个随机数`d`作为私钥，再计算`P = d × G`作为公钥，其中`G`为椭圆曲线的基点，基点是公开的。

私钥是一个32字节的大数，公钥由2个32字节的大数组成，分别是上述`P`点的横坐标和纵坐标。

## TRON地址的生成

1. 用公钥`P`作为输入，计算SHA3得到结果`H`，SHA3选用Keccak256。
2. 取`H`的最后20字节，在前面填充一个字节`0x41`得到`address`。
3. 对`address`进行base58check计算得到最终地址。

### Base58Check计算过程

1. 计算校验码
    1. 对`address`进行SHA256哈希运算，得到`h1`  
    2. 对`h1`再次进行SHA256运算，得到`h2`  
    3. 取`h2`的前4字节作为校验码`check`

2. 拼接数据  
将`check`拼接到`address`之后，得到`address||check`

3. Base58编码  
对`address||check`进行Base58编码，Base58的字符表为：`"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"`  ，排除了易混淆字符：`0`(阿拉伯数字0) 、`O`(大写字母O)、`I`(大写字母I)、`l`(小写字母l)。

### TRON地址特性
Base58编码原理是将以256为基数的大整数转换为以58为基数表示，再映射到字符表。由于`address||check`首字节固定为`0x41`，其十进制值`N`满足：`65 × 256²⁴ ≤ N < 66 × 256²⁴`。
   
- 长度为`34`位：由于`58³⁴ > 66 × 256²⁴`表明`34`位足够，`58³³ < 65 × 256²⁴`表明`33`位不够，所以所以长度只能是`34`位
- 首字母为`T`：首先长度已经确定是`34`位，并且由于`27 × 58³³ > 66 × 256²⁴`表明第一位必须小于27， `26 × 58³³ < 65 × 256²⁴`表明第一位必须大于等于26，所以最高位只能是`26`，而`26`对应base58字符表的`T`(`0`对应`'1'`)


## 签名

### 算法
1. 取交易的rawdata，转成byte[]格式，记为`data`

2. 对`data`进行sha256运算得到交易的hash值，记为`hash`。

3. 用交易合约中的地址对应的私钥`d`，对`hash`进行签名，签名算法为ECDSA算法（选用的曲线为SECP256K1）。签名结果包含`r`，`s`，`v`三个值：  
    1. 计算`r`值：随机生成一个临时私钥`k`，计算临时公钥`K = k × G`（`G`：曲线基点），`r = K_x mod n`，即`K`的横坐标模`n`，其中`n`是曲线阶数（`n`和`G`满足`n × G = O`，`O`是有限域上椭圆曲线群的零点）。`r`为32个字节。
    2. 计算`s`值：先计算临时私钥`k`对n的模逆`k⁻¹`，即`k⁻¹`满足`k⁻¹ × k = 1 mod n`，再通过交易的`hash`、用户的私钥`d`、`r`值计算`s`值，`s = (k⁻¹ × (hash + d × r)) mod n`。`s`为32个字节。
    3. 计算`v`值：`v`值是恢复标志符，由于`r`值有取模运算以及椭圆曲线的对称性，如果只有`r`值，一个`r`最多可以恢复出四个`K`。`v`值的取值范围是`0、1、2、3`四个整数，历史上为了和以太坊保持一致，最后的`v`值会在`0、1、2、3`的基础上再加`27`，即最后`v`值的取值范围是`27、28、29、30`。有了确定的`v`，就可以恢复出唯一的`K`。`v`为1个字节。  

4. 将签名结果`r`，`s`，`v`拼接后添加到交易中，拼接顺序为`v || r || s`。

### 示例

```
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    ECDSASignature signature = myKey.sign(hash);
    ByteString bsSign = ByteString.copyFrom(signature.toByteArray());
    transactionBuilderSigned.addSignature(bsSign);
}
```

## 验签
全节点(Fullnode)收到交易后会进行验签，由`hash` 和 `r`、`s`、`v`恢复出公钥([生成密钥对算法](#_4)中的`P`)，再通过base58check编码生成一个TRON地址，与合约中的地址进行比较，相同则验签通过。


### 算法

1. 恢复公钥点`K`：通过签名中的`v`和`r`可以唯一恢复出临时公钥点`K`。

2. 推导公钥`P`：      
    1. 已知签名方程：  
     `s = k⁻¹(hash + d × r) mod n`  
    2. 两边同乘`k`：  
     `s × k = (hash + d × r) mod n`  
    3. 两边再同乘曲线的基点`G`（利用`K = k × G`和`P = d × G`）：    
     `s × K = hash × G + r × P`  
    4. 因`s`、`K`、`hash`、`G`、`r`均已知，可求得`P`

3. 生成TRON地址：同[TRON地址的生成](#tron)

4. 地址验证：比对生成的TRON地址与交易合约中的地址是否一致。

### 示例
验证签名由全节点进行，[ECDSA算法的验签](https://github.com/tronprotocol/java-tron/blob/master/crypto/src/main/java/org/tron/common/crypto/ECKey.java)可参考java-tron，核心函数为`signatureToAddress`。


## 账户发起交易
以上是TRON账户模型的理论知识，对于开发者，账户发起交易(构建/签名/广播)建议使用官方sdk(Trident/TronWeb)，详细信息见[开发者文档](https://developers.tron.network/docs/create-offline-transactions-with-trident-and-tronweb)。

