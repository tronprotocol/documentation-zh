**energyUsage**

此次调用中，合约调用者消耗的Energy的总量

**energyFee** 

此次调用中，合约调用者消耗的Energy中，需要TRX支付的数目(SUN为单位)

**originEnergyUsage** 

此次调用中，合约开发者消耗的Energy的总量

**energyUsageTotal** 

此次调用中，合约调用者和合约开发者消耗的Energy的总量

**Feelimit** 

用户在调用或者创建智能合约时，指定的最高可接受的trx费用消耗，包含消耗冻结获得资源的trx和消耗用户本身持有的trx两部分，优先使用冻结资源。

**CallValue**

用户在智能合约调用或创建时给智能合约本身的账户转账的trx数量，在判断feelimit的时候会抛去这部分的值。

**consume_user_resource_percent**

对于一个智能合约来说，付费是由两大部分组成的。一部分是合约开发者付费，另一部分是由合约调用者支付。这个值是调用者付费的比例
           
**origin_energy_limit**

开发者设置的在一次合约调用过程中自己消耗的energy的上限，必须大于0。对于之前老的合约，没有提供设置该值的参数，会存成0，但是会按照1000万energy上限计算，开发者可以通过updateEnergyLimit接口重新设置该值，设置新值时也必须大于0

**net_usage**

本次合约消耗的Bandwidth(不包含NetFee对应的)

**net_fee** 

本次合约因Bandwidth不足消耗的TRX

**Bandwidth**

在波场网路发起交易会消耗带宽，消耗带宽的多少取决于交易的字节数大小。例如，交易大小为100个字节，那么广播交易的时候，需要消耗100单位的带宽。  

**Energy**

合约的部署与运行需要消耗能量。能量代表CPU资源的消耗，1 Energy = 1 Microsecond (μs)。 例如，一个合约的执行需要100μs，那么需要消耗100单位的能量。  

**TRON Power(TP)**

每冻结一个TRX，可以获得一个TP。 1个TP代表一个投票权。  

**Super Representative(SR)**

目前正在出块的前27名节点。





