# 版本发布

## 二进制一致性检验

自版本 3.7 之后的所有发布文件将由 Tron 账户 `TKeAcHxgErbVXrG3N3TZiSV6AT566BHTj2` 对文件一致性进行签名。

### 签名验证

这里介绍如何通过 tronweb 验证签名。

```js
const Trx = require('tronweb').Trx;

console.log(Trx.verifySignature(SHA256, ADDRESS, SIGNATURE));
```

例如 `FullNode.jar` 发布时附带 SHA256 hash `2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e`,
并提供 Tron 签名  `21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b`.

验证已发布文件的完整性：

```shell
# 首先验证 sha256 哈希值

sha256sum FullNode.jar  # or shasum -a 256 FullNode.jar (macOS)
# 2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e  FullNode.jar

# 然后检查 Tron 签名

npm install -g tronweb
node -e 'console.log(require("tronweb").Trx.verifySignature(
    "2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e",
    "TKeAcHxgErbVXrG3N3TZiSV6AT566BHTj2",
    "21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b"
  ))'
# true
```
