# TRC-10

TRON网络支持2种通证，一种是通过智能合约发行的TRC20协议的通证，一种是通过Tron公链内置的TRC10通证。

下面对TRC10通证进行说明。

## 如何发行TRC10通证

http接口：

```shell
wallet/createassetissue
作用：发行Token
demo：curl -X POST  http://127.0.0.1:8090/wallet/createassetissue -d '{
"owner_address":"41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
"name":"0x6173736574497373756531353330383934333132313538",
"abbr": "0x6162627231353330383934333132313538",
"total_supply" :4321,
"trx_num":1,
"num":1,
"precision":1,
"start_time" : 1530894315158,
"end_time":1533894312158,
"description":"007570646174654e616d6531353330363038383733343633",
"url":"007570646174654e616d6531353330363038383733343633",
"free_asset_net_limit":10000,
"public_free_asset_net_limit":10000,
"frozen_supply":{"frozen_amount":1, "frozen_days":2}
}'

参数说明：
owner_address发行人地址
name是token名称
abbr是token简称
total_supply是发行总量
trx_num和num是token和trx的兑换价值
precision是精度，也就是小数点个数
start_time和end_time是token发行起止时间
description是token说明，需要是hexString格式
url是token发行方的官网，需要是hexString格式
free_asset_net_limit是每个token拥护者能使用本token的免费带宽
public_free_asset_net_limit是Token的总的免费带宽
frozen_supply是token发行者可以在发行的时候指定质押的token

返回值：发行Token的Transaction
```

## 参与TRC10通证

http接口：

```shell
wallet/participateassetissue
作用：参与通证发行
demo：curl -X POST http://127.0.0.1:8090/wallet/participateassetissue -d '{
"to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"amount":100,
"asset_name":"3230313271756265696a696e67"
}'

参数说明：
to_address是Token发行人的地址，需要是hexString格式
owner_address是参与token人的地址，需要是hexString格式
amount是参与token发行的TRX数量
asset_name是token的名称，需要是hexString格式

返回值：参与token发行的transaction
```

## TRC10通证转账

http接口：

```shell
wallet/transferasset
作用：转账Token
demo：curl -X POST  http://127.0.0.1:8090/wallet/transferasset -d '{
  "owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292",
  "to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
  "asset_name": "0x6173736574497373756531353330383934333132313538",
  "amount": 100
}'

参数说明：
  owner_address是token转出地址，需要是hexString格式
  to_address是token转入地址，需要是hexString格式
  asset_name是token名称，需要是hexString格式
  amount是token转账数量

返回值：token转账的Transaction
```
