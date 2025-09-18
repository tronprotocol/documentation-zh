# java-tron 发布包签名校验

本文档旨在指导开发者如何对 TRON 的 java-tron 可执行文件进行签名校验，以确保所获取文件的**可靠性**和**完整性**。签名校验过程需要提供三个关键信息：待验证的可执行文件、文件的数字签名以及用于签名的私钥所对应的公钥。校验原理是根据可执行文件的内容和其签名反向推导出签名的公钥，并与  [java-tron](https://github.com/tronprotocol/java-tron) 公示的公钥进行比对。如果两者一致，则表明您获取的 java-tron 可执行文件是与 GitHub 上发布的一致且未被篡改的。

TRON 针对 java-tron 发布包的签名方式有所调整：

* **2023 年 1 月 3 日及之后发布的新版本**：采用 **GPG 方式**进行签名和验签。
* **2023 年 1 月 3 日之前发布的版本**：采用**指定 TRON 账户的公私钥方式**进行签名和验签。

本文将详细介绍这两种签名验证流程。


## GPG 签名验证流程

对于 2023 年 1 月 3 日之后发布的 java-tron 版本，您需要使用 GPG 进行签名验证。java-tron 可执行文件及其对应的签名文件会一并发布在 [GitHub Releases](https://github.com/tronprotocol/java-tron/releases) 页面。请按照以下步骤进行 GPG 签名验证。

### 1. 安装 GPG

如果您已经安装了 GPG，可以跳过此步骤。否则，请根据您的操作系统执行以下命令进行安装：

* **macOS**:
    ```shell
    brew install gpg
    ```
* **Debian、Ubuntu 或其他 Linux 发行版**:
    ```shell
    sudo apt install gpg
    ```

### 2. 导入公钥

如果您之前已经导入过公钥，请跳过此步骤，公钥只需导入一次。

首先，从 [java-tron GitHub 仓库](https://github.com/tronprotocol/java-tron?tab=readme-ov-file#integrity-check) 获取 java-tron 发布包 GPG 签名的**公钥 Hash** 和 **UID**。例如：

```text
pub: 1254 F859 D2B1 BD9F 66E7 107D F859 BCB4 4A28 290B
uid: build@tron.network
```

然后，根据公钥 Hash 将公钥从 GPG 公钥服务器导入到本地：

```
gpg --recv-keys "1254 F859 D2B1 BD9F 66E7 107D F859 BCB4 4A28 290B"
```

如果公钥导入成功，您将看到类似如下的输出：

```
gpg: 密钥 785FB96D2C7C3CA5：公钥 “build_tron <build@tron.network>” 已导入
gpg: 处理的总数：1
gpg: 已导入：1
```

### 3. 验签

假设您要验证的可执行文件为 `FullNode.jar`，其对应的签名文件为 `FullNode.jar.sig`。执行以下命令进行验签：

```
gpg --verify FullNode.jar.sig FullNode.jar
```

如果签名验证通过，您将看到如下字样：

```
gpg: 签名建立于 五  1/ 6 12:21:51 2023 CST
gpg:               使用 RSA 密钥 1254F859D2B1BD9F66E7107D F859BCB44A28290B
gpg: 完好的签名，来自于 “build_tron <build@tron.network>” [未知]
gpg: 警告：此密钥未被受信任签名认证！
gpg:       没有证据表明此签名属于其声称的所有者。    
主密钥指纹： 07B2 3298 AEA4 E006 BD9A  42DE 785F B96D 2C7C 3CA5
子密钥指纹： 1254 F859 D2B1 BD9F 66E7  107D F859 BCB4 4A28 290B
```

如果验证失败，则会显示 `已损坏的签名，来自于 “build_tron <build@tron.network>”` 字样。


## TRON 地址签名验证流程

对于 2023 年 1 月 3 日之前发布的 java-tron 版本，其发布包均由 TRON 账户 `TKeAcHxgErbVXrG3N3TZiSV6AT566BHTj2` 进行签名。签名步骤如下：

1.  首先计算发布包可执行文件的 SHA256 哈希值。
2.  然后使用该 TRON 账户的私钥对 SHA256 哈希值进行签名。

发布包的 SHA256 哈希值和签名结果可在本文档的 [历史版本签名信息](#_1)章节中查看，也可以在 [GitHub Releases 页面](https://github.com/tronprotocol/java-tron/releases) 查看。

在这里，我们使用 TRON 上流行的 JavaScript 库 [tronweb](https://tronweb.network/docu/docs/intro/) 来演示验证签名的流程。 TronWeb 提供了 `Trx.verifySignature` 接口来验证签名。验证通过将返回 `true`，否则返回 `false`。请按照以下流程进行验证。

### 1. 安装 TronWeb

如果您已经安装了 TronWeb，可以跳过此步骤。否则，请参照以下命令进行安装：

```
npm install -g tronweb
```

### 2. 验证发布包的完整性

为了确保发布包的完整性，您需要检查其 SHA256 哈希值是否与发布信息中提供的哈希值一致。

以 `Odyssey-3.7` 版本为例：

* 发布包文件名为：`FullNode.jar`
* 发布包的 SHA256 为：`2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e`
* 签名为：`21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b`

在您的系统上执行以下命令来计算 `FullNode.jar` 的 SHA256 哈希值：

* **macOS**:
    ```
    shasum -a 256 FullNode.jar
    ```
* **Debian、Ubuntu 和其他 Debian 衍生版系统**:
    ```
    sha256sum FullNode.jar
    ```
将命令输出的哈希值与发布信息中提供的哈希值进行比对。

### 3. 检查发布包签名

使用 TronWeb 的 `Trx.verifySignature` 接口验证发布包的签名。在命令行中执行以下 JavaScript 代码：

```
# Trx.verifySignature(SHA256, ADDRESS, SIGNATURE));
node -e 'console.log(require("tronweb").Trx.verifySignature(
    "2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e",
    "TKeAcHxgErbVXrG3N3TZiSV6AT566BHTj2",
    "21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b"
  ))'
```

如果签名验证通过，将输出 `true`；否则，输出 `false`。


### 历史版本签名信息

#### Odyssey-3.7

```text
FullNode sha256sum: 2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e
FullNode signature: 21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b
SolidityNode sha256sum: fcdea8b3e511306218ba442fb0828f0413574012d646c39c212a59f6ba5844bc
SolidityNode signature: 6dcad6e02f17467e5cfebeefa0f9963da08e7da10feebefdec47d689fecc30f104c9b7f5e784b883e7ceb786fe55188356c42c306d727fb7819eed2a71f788361c
```

#### GreatVoyage-4.0.0

```text
FullNode sha256sum: d3f8f9fde64bdefaadae784d09de97172e5e8a3fe539217e12b89963983a530d
FullNode signature: e788dbaf2fe35f099f65b2403cfb0d7cbe7f4611f8c5ff8151e4bd84ae468d2e541043c9cde9e74500003027ae9f25cdda81a9bcd60abb45ca7a69f965f4dcc71c
SolidityNode sha256sum: adddf88423c6c31f1f25ed39b10779c24dd7cdcf37f2325c02b2f2ecfc97e1f6
SolidityNode signature: e3b9859f178f7851dedb7a0a8deb715e5f1e3af10b1064c36f2727ec2b8825510df4fd7b09d7d049204e5df3e8d5b87778e83a15ca96ce786f7977a6cb48bca91b
```

#### GreatVoyage-4.1.1

```text
FullNode sha256sum: 30e716b86b879af1e006c2b463903ae3835e239e32e2b01c2a1b903a153897fe
FullNode signature: 5faee65a448bb9aa77835992ca3d24e50d8a76b7934f80664ad38e83179c8114278fdef4494de7231f8e40de86461676a7aa4a54c795f4c692e91d90e156ec471b
SolidityNode sha256sum: 10a160181053b421109ecace74df5fc0f8860bc8a70181add65fd9a292c35a44
SolidityNode signature: 1d1413b13adf7778f9a720294eca066ac728ad636d166505276f5ff1f63973c100c04778f937f240f10107edb7de477604857867fc4dbdb68238169c978fc3da1b
```

#### GreatVoyage-v4.1.2

```text
FullNode sha256sum: 4ded44b6c1a3dbd25212e14ab413142b5463dcbf30a528f83ded529048542547
FullNode signature: 57a094c1b8a5ec301ef913eb718de2498b5695eb999530863df05252ba8919ba6866c8490e29d36f7dbf34537c898ece5ef0111efb134419c3a5fd6fc9ec03b81c
SolidityNode sha256sum: 3db36cadbd1f7641aafc8164983f28df4b7ceff8174e090327ed407012cf12cb
SolidityNode signature: d07604f6811cbed628dd6e5c07880c2fdd3025848fd5365925531c7748467d5228fea2e18326864acc27f3b51c73b364fa44c450d8ec4b5080a7ddb7566724701c
```

#### GreatVoyage-v4.1.3(Thales)

```text
FullNode sha256sum: c5fb99ad5b024bb7877118f30fb6065f6e6febd11a3cfa241521cbed73cca181
FullNode signature: d80ec371e791c4316925d80ff3400cf51b14c8a4d4c696b7817c517eb094823622932b45b9b37f9e9657513c3eddb1134fbbb1ee56727c0957e8a3b40c67409b1c
SolidityNode sha256sum: 4b941d71b561a8b2e0b97d7498823d900eaf287910eea1eaafc649f5aad14036
SolidityNode signature: f8a8e8d411b009d02986cad1e19e745f8107384a274f146bcae60c570111b13556ff9ab528eb5d1fb4734bd4ef488ade4038781d06ab6420e35f28be6135fe9b1c
```

#### GreatVoyage-v4.2.0(Plato)

```text
FullNode sha256sum:
bbf103432be016b582452137b4862140af15ccf7c5daa9be738450705317fdb8
FullNode signature:
326701699a5eb8d497eb454b5b74c1559961417fb6f262b4e6314052d73f5977312e0450937fa485236f51f706b434acf8659ce1325d704097c5748629e736ef1c
SolidityNode sha256sum:
1db544cbca9dc814683ccf9bef28f7d6ca4469289052230394aaf4e3bcd08615
SolidityNode signature:
47fea27df940db0d2a4c0abf6d06969882c027bc4f17449205a28ae5cd25b8ba5339e21f105fe1c25e799d0f4ffea64a15046b9baf5b54341411b5180da439011b
```

#### GreatVoyage-v4.2.1(Origen)

```text
FullNode sha256sum:
9888710c915a4027f1bc3dcb1d5d983e0c00d4c438f6fa307d412f62ff6862ea
FullNode signature:
6e7d8ef9d033ebf9213118b7511f4ecc5def97442844fbd34de3ef76dd417a0d45da3e2e70fc213475d7fc0a44df1c54732874d858ec980159c5dbffc975680a1c
SolidityNode sha256sum:
c70edffa3022e9c25bf845ee978e3500c3ada89b473d895a715acf1738b83f10
SolidityNode signature:
0e366acce33bb7c6b02fa143a57d9380c94d3513a9fba8692efe2862a8f7df93156edbddd075f1844f2f81398b14f2db6a03e21f0f6b8ab25649fae4dc16ae731b
```

#### GreatVoyage-v4.2.2(Lucretius)

```text
FullNode sha256sum:
8a7f8143b3351ea6b5d8e3dfc857b09256d363d4907ba3ab0288f67f77c2a58f
FullNode signature:
71c6300ace5cbf16d78a32aa4602c3f129cb768e32acffaecd17b4134b5955bf37efda1d27025e894e521184a21174e5eddf4e7d1f86761657827795cbddfcfd1c
SolidityNode sha256sum:
2d0d5334a232b7b74df8ed3211d9e0ac957894f81e9172010732f2159da261ad
SolidityNode signature:
0696f8cb3c65324c4b04f9ecf89d939bf7e1b955144e3fe75eeca6bd4c639e463afbe24e31ae38a6889d4d0649ae03fafeeb7c337b34a36fbac33962f64651671b
```

#### GreatVoyage-v4.2.2.1(Epictetus)

```text
FullNode sha256sum:
8bd040a8db16ccba3e957ed3558b82d145928153a53f9688302849658a72f9bc
FullNode signature:
3137a8ba8fa5556e4c4a7597aec8f5f46ebb79a64edcf9e2925d2e3314afde3e0f42fd4080e5e4f4d3d1eff263d30478b0322e6dbcc71c43b534f614004b5c561b
SolidityNode sha256sum:
ee8abd39732e4901828a61124880f1d2eab62f7f3d97150f1e1921bf7da10e54
SolidityNode signature:
092b08184677449dd283a31cc486f994166cd9f5ad312a9c80d3e06689ec540774ac9a1334dffeb6412039ed70ee912ead39c4025dd69b688ea9df4dd831b5771c
```

#### GreatVoyage-v4.3.0(Bacon)

```text
FullNode sha256sum:
b5e993800cea5ca040758dd6b3c7438def03cbf1358468beb76ea45399a59298
FullNode signature:
8da6ac58129d78d948810e4bc7372dd8aef5232bfbc4c33ad8fb21e88314e3d97dd77509e0f03a98da32679495152ccd4a9d07541589822e5cf5d3d4f61877191b
SolidityNode sha256sum:
446a4736901958a450e4e95aaca99a63957163854fb32d25eed84600e6996668
SolidityNode signature:
c27ffde8ce88ee14689e15a9d5c3fb2d2a9d180ea43b45046131df8ac5481fae2588621b395ad7031ed49d65ddd020b3ce084537e3f527d8a5a979f8c65265561c
```

#### GreatVoyage-v4.4.0(Rousseau)

```text
FullNode sha256sum:
bf7f962846f75139dd89ac6da32074cad33b2e172c0749abbed8773cc1ab1a37
FullNode signature:
56ed97f3451e3d731f799bad952750d56aa78a9a91a2688b4d6b956328ede7e01bae78037ad6ef1f9c682b566e954dfb958271f006e5cf0dcace5768d76fda6e1b
SolidityNode sha256sum:
9dac37763ddf75c07335ec070f837b63ee46b698066dd25c4756ad40f8750d5f
SolidityNode signature:
cc4325c085719e3e5045b5c6c2553d7adc9c735419618f7afad06c3a532da0ed46906ae9b2dadb15d7f94150268d5ecdc7fd2741693991586d50da30a8d917071b
```

#### GreatVoyage-v4.4.1(Protagoras)

```text
FullNode sha256sum:
4a32918849dc8a7fedcb637ff4939389363726cb16c6a581e39253260668ee04
FullNode signature:
fd747f61705ef045143bd2d55b278ca347904323711e2e86b11cf1dd203f198443ab1a399767a570005bd5b2ea283187ccc41557ffb79c959b018e8d798b96f81c
SolidityNode sha256sum:
b6a06d3b19f41591bd8c01f35e78b316ab8e9ad4c0740128fc95ba52d3106f34
SolidityNode signature:
d2836bda30fd25c89494ae7a12b5357bc9e725c9e2c655fb0a9158a4bee881693ea869defe650b0b4f190458a5268f1c121e73c8305cc81a408e62fca0d234c51b
```

#### GreatVoyage-v4.4.2(Augustinus)

```text
FullNode sha256sum:
70eba12350fa21e1b261927093090e7bdf0765592d19433c594149bd3707ef0a
FullNode signature:
14430f463e6fab3dd247aca6267b6aaf2f1869b455d95aee297208bd1561c6c67559d9c535e63e74bbef604141cc4ceec78367a75e6ca4d4ceb6513019329c9b1b
SolidityNode sha256sum:
f08438e093cc1091859f0ee9dbc7e79b0d5d9068facd4e6485374baa3acf59d1
SolidityNode signature:
f3935dfe4af9601cf102c975ed2eebbd4b42160e8746c0d0b21ffbd2fbd4b6f374257b1bc0e948909a9ef343d2cc70671961c8f7a992b6cd123f9ad3c8c323391c
```

#### GreatVoyage-v4.4.3(Pythagoras)

```text
FullNode sha256sum:
c07637a1a4a9a289218554f4714caef90032e267b068411c7dd818d4af45e39f
FullNode signature:
2bf8d65adf556fe2c04b739c1f4e6e73058914cf642a7806ff85e57be2ff122e35cbf3d67b0bc8bad4fb827198ffd8e06f60111a167ecb0b3db0d8e571b8c67b1c
SolidityNode sha256sum:
64f4614160b9330d0a9e984686b66fa16e9aecf7ae16e32b8cc7c32f52694eef
SolidityNode signature:
dc0f910555a23667d682a6775588de90592ede44f76a32b12ea8f89fa7dcc937274cc3a44b20da49726323cc9f476d42caa318c338858474f02bf98cc398bca81c
```

#### GreatVoyage-v4.4.4(Plotinus)

```text
FullNode sha256sum:
0264d382489dae5bf1d340030c1892b0a7aeb9364cb9380c034e159c9eb9a269
FullNode signature:
70cdece8c3510ce4d7d84d5d2c8b53895397c0134d73d681b6b41d4de80d74ce2c2760fdf080ff0ce8c0989246377fca529cb1a2e85e1936755abef4be64f0971b
SolidityNode sha256sum:
b58e7b8b0f97eb2a7a0ce5c5aeb2ce070192ca82c96adc8568aabe4f3407d873
SolidityNode signature:
26da2e507bbd7e82e0170039cc1c0e42332fb2dfc755aeb385240f0a93125b6c0f1e943ccf1a4e9bfec7fdd4d8a26375a38e030e0b8b69af3e2c181bf08444111b
```

#### GreatVoyage-v4.4.5(Cicero)

```text
FullNode sha256sum:
8115e887e5af5768e8ab967f8e7bc024af94bda31be7f3dbc30934b42489d988
FullNode signature:
1a02f26eb6065efe5697123528f32ea352d813f9e5acf5936407ad8899c4019539e31b257cafe34b9f8045602f5a4f381b3dd8252a30bb9daf52aeeb078b54711b
SolidityNode sha256sum:
95884a07dcbb1531ec7ae20b7162cab3bb9c4bd2e300447c01c4772e02b24a20
SolidityNode signature:
8adab9501bbb2a3d9f3055c91e819f86081df9b92228a86afb7f0a27165a42690dbeb50f0f1fd1f7180b51809a291c5ff3860e49f888cf0ba87b401d3dda6e271c
```

#### GreatVoyage-v4.4.6(David)

```text
FullNode sha256sum:
eaf213f6e6cd9913f9f27bf72a42209c1a0f0fce9841c1d6bd680d879d7d6f85
FullNode signature:
064abe833436b3a2e9b66406abf81d12a20f9d28ef669abe7c87c0d750e58cf10c1e65de6fbd0fc368022f93e4c330b42ea9775ead91962480436985c90ad3b11c
SolidityNode sha256sum:
c3e9ccc1a4d2aac4c081ae01db86a0901b6f3506e3f8a953315e47ae274a98c1
SolidityNode signature:
a03d5d6f0e6c6b869f2e545d8c3ff8a4fed569508e9abe4219271d8bf25dfb015e242add8fd2ab6b8b412dd6b393639517957877e8eb7c07ff43a1351a88d62f1b
```

#### GreatVoyage-v4.5.1(Tertullian)

```text
FullNode sha256sum:
db3c75d7854dcf241558c2942b9a582f478c00a88b6f7a7e5ff8a653a8d4c59a
FullNode signature:
61ba205f28c3bc7fa228c27e4e3b4d460ef4fad75ca1d38d82540d45eea2d3d720196b607cd45c560db7a749d05bfe8089c61fba5843e98d61fec90f1591f2861b
SolidityNode sha256sum:
537a81bd781d416229de5e0875247160f2569c378c8eed703203d0acca5be5f1
SolidityNode signature:
a736f9de5425562a2af188c547245f9b4da6d793728bc767242e3df75fa104f61ce978b62fc5cea7f6008bdb51faa9510ff5633702cdb1ddca29cb06a18920d21c
```

#### GreatVoyage-v4.5.2 (Aurelius)

```text
FullNode sha256sum:
60e959ccde3ff90c10b503bb25edf37684845e358df2ad64b2b330712b30c177
FullNode signature:
f2f4b6050e639047857c5b5331eb006dcc9c1e0427bac4ae3d934f7436080785472ead691aa16e6a5aed3c2932fb279ce8ab3580449071b878e0d31fdf01f0371c
SolidityNode sha256sum:
4783b8abef12a6c7b8319f3e8960c1d3126edcc521ac1fc3429fe2870cab91b0
SolidityNode signature:
afb5db2467ce9f5445679df53e2fecfaed3c4a2d0ca2ba88b65e621aa2d37a9e6aab06b30052a9381087d0164cb5c347d710b2b1c59e6f7c7107deacfd1cfc961b
```

#### GreatVoyage-v4.6.0 (Socrates)

```text
FullNode sha256sum:
598589d428085e25c838552970844b0ba00248ad92873bd2ad25b35f37db7a5b
FullNode signature:
d3bcfa1bea64b7e58cb94603563cb0c5e47bc20316f61b0dfc966fb64ae846f21b8f917a63328416993f524f4de55ddf5083f163b1fe1b811a9a6f4532725c8e1c
SolidityNode sha256sum:
ee37a425a84677063b6ea44ed073b8260e336586a61debc10ce0b1544bf7db6a
SolidityNode signature:
332c273ef1cdae8dc39c76a83b38750a74b3dd1b915e49698e4ae6870cfed49a1449e8d8db995c7a6be2295e2603efedb0f3e8e906ac7681583c5023b28a521d1b
```