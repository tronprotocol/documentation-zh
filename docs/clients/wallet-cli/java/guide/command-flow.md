# 命令行操作流程

下面通过一个完整的交互式会话，演示构建并运行 wallet-cli、创建和备份钱包、查询账户，以及发行和转移资产。

```console
$ cd wallet-cli/java
$ ./gradlew build
$ ./gradlew run
> RegisterWallet             # 先两次提示输入密码，再询问助记词长度
> login                      # 提示输入密码
> getAddress
GetAddress  successful !!
address = TRfwwLDpr4excH4V4QzghLEsdYwkapTxnm   # 请备份它！
> BackupWallet               # 提示输入密码
BackupWallet  successful !!
1234567890123456789012345678901234567890123456789012345678901234  # 请备份它！！！（BackupWallet2Base64 输出的是同一把密钥的 base64 编码）
> getbalance
Balance = 0 SUN = 0.000000 TRX
> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
> getaccount TRfwwLDpr4excH4V4QzghLEsdYwkapTxnm
# 余额输出节选：9999900000
"assetV2": [
    {
        "key": "1000001",
        "value": 74999999999980000
    }
]
  # （assetIssue 消耗 1000 trx）
  # （你可以查询任意账户的 trx 余额和其他资产余额）
> TransferAsset TWzrEZYtwzkAxXJ8PatVrGuoSNsexejRiM 1000001 10000
```

## 另请参见

- [getting-started](getting-started.md)——更简短的快速上手
- [commands/transfer-trc10](../commands/transfer-trc10.md)——`AssetIssue` / `TransferAsset` 的细节
