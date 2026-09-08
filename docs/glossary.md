# 术语表

**energyUsage**

此次调用中，合约调用者消耗的Energy(不含 EnergyFee 对应的部分)

**energyFee**

此次调用中，合约调用者消耗的Energy中，需要TRX支付的数目(以 sun 为单位，1 TRX = 1,000,000 sun)

**originEnergyUsage**

此次调用中，合约开发者消耗的Energy的总量

**energyUsageTotal**

此次调用中，合约调用者和合约开发者消耗的Energy的总量

**FeeLimit**

用户在调用或者创建智能合约时，用于设定可使用的、通过销毁或质押 TRX 获得的 Energy 的上限，优先使用通过质押 TRX 获得的 Energy。

**CallValue**

用户在智能合约调用或创建时给智能合约本身的账户转账的trx数量，在判断feelimit的时候会抛去这部分的值。

**consume_user_resource_percent**

对于一个智能合约来说，付费是由两大部分组成的。一部分是合约开发者付费，另一部分是由合约调用者支付。这个值是调用者付费的比例，剩余部分（100 减去该值）由合约开发者承担。

**origin_energy_limit**

开发者设置的在一次合约调用过程中自己消耗的energy的上限，必须大于0。对于之前老的合约，没有提供设置该值的参数，会存成0，但是会按照1000万energy上限计算，开发者可以通过updateEnergyLimit接口重新设置该值，设置新值时也必须大于0

**net_usage**

本次合约消耗的Bandwidth(不包含NetFee对应的)

**net_fee**

本次合约因Bandwidth不足而消耗的TRX(以 sun 为单位，1 TRX = 1,000,000 sun)

**Bandwidth**

在波场网络发起交易会消耗带宽，消耗带宽的多少取决于交易的字节数大小。例如，交易大小为100个字节，那么广播交易的时候，需要消耗100单位的带宽。

**Energy**

Energy 是部署和运行智能合约所消耗的资源。在 TRON 虚拟机（TVM）中执行的每一条指令都会消耗固定且确定的 Energy，其数值由虚拟机的 Energy 计价表规定（例如一次 `SLOAD` 消耗 50 Energy，通过 `SSTORE` 新建一个存储槽消耗 20000 Energy）。合约执行的计算量越大，消耗的 Energy 越多。Energy 可以通过质押 TRX 获得，也可以通过销毁 TRX 支付。

**TRON Power(TP)**

每质押一个TRX，可以获得一个TP。 1个TP代表一个投票权。

**Super Representative(SR)**

按得票数排名前 27 的 witness，负责出块。
