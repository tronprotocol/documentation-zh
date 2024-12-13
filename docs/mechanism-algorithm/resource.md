# 资源模型

## 资源模型介绍

投票权、带宽和能量是TRON网络中的重要系统资源。其中投票权用于给超级代表投票；带宽是衡量保存在区块链数据库中的交易字节大小的单位，交易越大，消耗的带宽资源会越多。能量是衡量在TRON网络上TVM虚拟机执行特定操作所需的计算量的单位,由于智能合约交易都需要计算资源来执行，因此每笔智能合约交易都需要付费。

下文我们把投票权也称为TRON Power(TP)、带宽也称为Bandwidth Points，能量也称为Energy。

!!! note
    - 普通交易仅消耗Bandwidth points
    - 智能合约的操作不仅要消耗Bandwidth points，还会消耗Energy

## 投票权

任何账户在给超级代表投票前，都需要先获得投票权，即TRON Power(TP)。投票权可以通过质押TRX来获取。质押TRX除了可以获得带宽或者能量外，还将同时获得投票权，选民质押1TRX，将获得1TP。关于如何质押请参考[在TRON网络上质押](#tron)章节。

选民可以分批多次质押，多次质押获取到的投票权会被累加到选民账户内，选民可以通过[wallet/getaccount](../api/http.md/#walletgetaccount)接口查询账户拥有的投票权总数以及已使用的投票权数量。

+ 示例接口结果：
```
{
    "address": "TBEJewE3MWBbW9t7F4s875yvMHrhqBAZfB",
    "votes": [
        {
        "vote_address": "TFMehqCGCei9RrJLdM5eRFuwHY4CrYy6Xt",
        "vote_count": 7003
        },
        {
        "vote_address": "TE8dLwHkMrutMKULTZE41knERrT5XiLVeN",
        "vote_count": 7003
        },
        {
        "vote_address": "TYcvQx7rFuDgyauJmfxBxj7ppkAsSa3sJe",
        "vote_count": 7003
        }
    ],
...
}
```

## 带宽

交易以字节数组的形式在网络中传输及存储，一条交易消耗的 Bandwidth Points = 交易字节数 * Bandwidth Points费率。当前 Bandwidth Points费率 = 1.

如一条交易的字节数为200，那么该交易需要消耗 200 Bandwidth Points。

### 1. Bandwidth Points的来源

Bandwidth Points的获取分两种：

- 通过质押TRX获取的Bandwidth Points。
- 每个账号每天有固定免费额度的带宽，目前为600，由61号提案控制。

其中质押获取的带宽计算公式为:

`NetLimit = FrozenBandwidthAmount / TotalNetWeight * TotalNetLimit`

- FrozenBandwidthAmount: 为获取Bandwidth Points质押的TRX
- TotalNetWeight: 整个网络为获取Bandwidth Points质押的TRX 总额
- TotalNetLimit = 43_200_000_000

也就是所有用户按质押的TRX数量平分固定额度的Bandwidth Points。

!!! note
    由于网络中总质押资金以及账户的质押资金随时可能发生变化，因此账户拥有的 Bandwidth Points 不是固定值。

### 2. Bandwith Points的消耗

除了查询操作，任何交易都需要消耗 bandwidth points。


### 3. Bandwidth Points的计算规则

Bandwidth Points是一个账户1天内能够使用的总字节数。一定时间内，整个网络能够处理的Bandwidth为确定值。

如果交易需要创建新账户(如创建新账户交易，向未激活的账户转账TRX或者TRC10代币)，Bandwidth Points消耗如下：

1. 尝试消耗交易发起者质押获取的Bandwidth Points。如果交易发起者Bandwidth Points不足，则进入下一步
2. 尝试消耗交易发起者的TRX，这部分烧掉0.1TRX

如果交易是TRC-10 Token转账，Bandwidth Points消耗如下：

1. 依次验证发行Token资产总的免费Bandwidth Points是否足够消耗，转账发起者的Token剩余免费Bandwidth Points是否足够消耗，Token发行者质押TRX获取Bandwidth Points剩余量是否足够消耗。如果满足则扣除Token发行者质押获取的Bandwidth Points，任意一个不满足则进入下一步
2. 尝试消耗交易发起者质押获取的Bandwidth Points。如果交易发起者Bandwidth Points不足，则进入下一步
3. 尝试消耗交易发起者的免费Bandwidth Points。如果免费Bandwidth Points也不足，则进入下一步
4. 尝试消耗交易发起者的TRX，交易的字节数 * 1000 sun

如果是其它交易，Bandwidth Points消耗如下：

1. 尝试消耗交易发起者质押获取的Bandwidth Points。如果交易发起者Bandwidth Points不足，则进入下一步
2. 尝试消耗交易发起者的免费Bandwidth Points。如果免费Bandwidth Points也不足，则进入下一步
3. 尝试消耗交易发起者的TRX，交易的字节数 * 1000 sun

### 4. 带宽的自动恢复

账户的免费带宽和质押TRX获取的带宽消耗后，会在24小时内逐步恢复。
其中每次计算质押剩余可用带宽的等价公式为：

`AvailableNetUsage = NetLimit - LastUsage * (CurrentTime - LastUseTime) / RecoveryWindow(24h)`

当 `CurrentTime - LastUseTime >= 24h` 时 `AvailableNetUsage = NetLimit`，
其中NetLimit的公式就是上面质押获取带宽的计算公式。通过这个公式实现24小时的质押带宽恢复。

如果交易需要消耗质押带宽，当 `AvailableNetUsage >= NewCost `则可顺利消耗质押带宽，并设置新的
`LastUsage = AvailableNetUsage - NewCost， LastUseTime = CurrentTime`。

### 5. 账户带宽余额查询

首先调用节点HTTP接口`wallet/getaccountresource`来获取账户当前的资源状态，然后通过如下公式计算带宽余额：

```
免费带宽余额 = freeNetLimit - freeNetUsed
通过质押获取的带宽余额 = NetLimit - NetUsed
```

注：如果接口返回的结果中没有包含上述公式中的参数，表示该参数值为0。

## 能量

智能合约运行时执行每一条指令都需要消耗一定的系统资源，资源的多少用Energy的值来衡量。

### 1. Energy的获取与消耗

质押获取Energy，即将持有的TRX锁定，无法进行交易，作为抵押，并以此获得免费使用Energy的权利。具体计算与全网所有账户质押有关，可参考下面计算逻辑。

#### 质押获得能量

通过调用接口[wallet/freezebalancev2](../api/http.md/#walletfreezebalancev2)，或下面Wallet-cli指令:

```text
freezeBalanceV2 frozen_balance [ResourceCode:0 BANDWIDTH,1 ENERGY]
```

接口[wallet/getaccount](../api/http.md/#walletgetaccount)可以查询账户当前为获取Energy质押的TRX，示例返回：
```
{
  "address": "TBEJewE3MWBbW9t7F4s875yvMHrhqBAZfB",
  "balance": 26795494669,
  "frozenV2": [
        {
            "amount": 1002000000 // Bandwith
        },
        {
            "type": "ENERGY",
            "amount": 20001000000
        },
        {
            "type": "TRON_POWER"
        }
  ],
  ... ...
}
```

##### 质押获得的能量计算
通过质押TRX获取的能量公式为：
`Energy_Limit = 为获取Energy质押的TRX / TotalEnergyWeight * TotalEnergyLimit`
。
TotalEnergyWeight：整个网络为获取Energy质押的TRX总额
其中Total_Energy_Limit = 180000000000，由#19号提议决定，后续数值变动可以查看[Network Parameters](https://tronscan.org/#/sr/committee)。
也就是所有用户按质押的TRX数量平分固定额度的Energy。

具体账户的能量数值，可以调用接口[wallet/getaccountresource](../api/http.md/#walletgetaccountresource)查看，示例返回：
```
{
    ...
    "EnergyLimit": 1459402, // Dynamic changed as TotalEnergyWeight changes
    "TotalEnergyLimit": 180000000000, // Static value follow propsal #19
    "TotalEnergyWeight": 2466887064
}
```

账户获得的Energy Limit是会动态调整的，示例：

```text
如全网只有两个人A，B分别质押2TRX，2TRX。

二人质押获得的可用Energy分别是

A: 75_000_000_000 且energy_limit 为90_000_000_000

B: 75_000_000_000 且energy_limit 为90_000_000_000

当第三人C质押1TRX时。

三人质押获得的可用Energy调整为

A: 60_000_000_000 且energy_limit调整为72_000_000_000

B: 60_000_000_000 且energy_limit调整为72_000_000_000

B: 30_000_000_000 且energy_limit 为36_000_000_000

```

#### 能量的消耗

在执行合约时，逐条指令计算并扣除账户能量，账户能量消耗的优先级如下：

* 质押TRX获取的能量
* 燃烧TRX

首先会消耗交易发起者质押TRX获取的能量，如果消耗完这部分能量后还不够，会继续燃烧账户的TRX来支付交易所需的能量资源，按照每一个能量0.00021TRX的单价来支付。

如果合约中途由于抛出revert异常而退出，则仅扣除已经执行的指令所对应的能量，但是对于异常合约，比如合约执行超时，或因bug异常退出，会扣除本次交易最大可用的能量，用户可以通过设置交易的fee_limit参数来限定这笔交易最多可以消耗的能量费用上限。

#### 能量的恢复

账户的能量资源消耗后，会在24小时内逐步恢复。

其中每次计算质押剩余可用能量的等价公式为：

`EnergyLimit - LastUsage * (CurrentTime - LastUseTime) / RecoveryWindow(24h)`
当 `CurrentTime - LastUseTime >= 24h` 时 `Account_Left_Energy = EnergyLimit`，
其中EnergyLimit的公式就是上面质押获取EnergyLimit的计算公式。通过这个公式实现24小时的质押能量恢复。

#### 账户能量余额查询

首先调用节点HTTP接口wallet/getaccountresource来获取账户当前的资源状态，然后通过如下公式计算能量余额：

```
能量余额 = EnergyLimit - EnergyUsed
```

注：如果接口返回的结果中没有包含上述公式中的参数，表示该参数值为0。

### 2. 如何填写 feeLimit(用户必读)

***
*在本节范围内，将合约的开发部署人员，简称为“开发者”；将调用合约的用户或者其他合约，简称为“调用者”。*

*调用合约消耗的Energy能以一定比例折合成trx（或者sun），所以在本节范围内，指代合约消耗的资源时，并不严格区分Energy和 trx；仅在作为 数值的单位时，才区分Energy、trx和sun。*

***

合理设置feeLimit，一方面能尽量保证正常执行；另外一方面，如果合约所需Energy过大，又不会过多消耗调用者的trx。在设置feeLimit之前，需要了解几个概念：

1. 合法的feeLimit为0 - 15*10^9 之间的整数值，单位是sun，折合0 - 15000 trx；
2. 不同复杂度的合约，每次正常执行消耗不同的Energy；相同合约每次消耗的Energy基本相同[^1]，但由于动态能量模型机制，对于热门合约，不同时刻执行时可能需要的能量不同，具体请参考[动态能量模型章节](#_10)；执行合约时，逐条指令计算并扣除Energy，如果超过feeLimit的限制，则合约执行失败，已扣除的Energy不退还；
3. 目前feeLimit仅指调用者愿意承担的Energy折合的trx[^2]；执行合约允许的最大Energy还包括开发者承担的部分；
4. 一个恶意合约，如果最终执行超时，或者因bug合约崩溃，则会扣除该合约允许的所有energy；
5. 开发者可能会承担一定比例的Energy消耗（比如承担90%）。但是，当开发者账户的Energy不足以支付时，剩余部分完全由调用者承担。在feeLimit限制范围内，如调用者的Energy不足，则会燃烧等价值的trx。[^2]

开发者通常会有充足的Energy，以鼓励低成本调用；调用者在估算feeLimit时，可以假设开发者能够承担其承诺比例的Energy，如果一次调用因为feeLimit不足而失败，可以再适当扩大。

**示例**
下面将以一个合约C的执行，来具体举例，如何估算feeLimit：

- 假设合约C上一次成功执行时，消耗了18000 Energy，那么预估本次执行消耗的Energy上限为20000 Energy；
- 燃烧trx时，由于能量单价目前为210sun，所以 21 trx固定可以兑换100000 Energy；
- 假设开发者承诺承担90%的Energy，而且开发者账户有充足的Energy；

则，feeLimit的预估方法为：

1. A = 20000 energy * 210sun = 4_200_000 sun  = 4.2 trx,
2. 开发者承诺承担90%，用户需要承担10%，

那么，建议用户填写的feeLimit为 4_200_000 sun * 10% = 420_000 sun。

### 3. Energy的计算(开发者必读)

在讨论本章节前，需要了解：

1. tron为了惩罚恶意开发者，对于异常合约，如果执行超时（超过80ms），或因bug异常退出（不包含revert），会扣除本次的最大可用Energy。若合约正常执行，或revert，则仅扣除执行相关指令所需的Energy；
2. 开发者可以设置执行合约时，消耗Energy中自己承担的比例，该比例后续可修改。一次合约调用消耗的Energy，若开发者的Energy不足以支付其承担的部分，剩余部分全由调用者支付；
3. 目前执行一个合约，可用的Energy总数由 调用者调用时设置的feeLimit 和 开发者承担部分共同决定；

!!! note
    1. 若开发者不确定合约是否正常，请勿将用户承担比例设置为0%，否则在被判为恶意执行时，会扣除开发者的所有Energy。[^1]
    2. 因此建议开发者设置的用户承担的比例为10%~100%。[^2]

下面具体举例，详细描述合约可用Energy的计算方法。

**示例1**
如果一个账户A的balance是 100 TRX(100_000_000 SUN)，质押 10 TRX 获得了100000 Energy，未质押的balance是 90 TRX。
有一个合约C设置的消耗调用者资源的比例是100%，也就是完全由调用者支付所需资源。
此时A调用了合约C，填写的feeLimit是 30000000(单位是SUN, 30 TRX)。
那么A此次调用能够使用的Energy是由两部分计算出来的：

- A质押剩余的Energy

    这部分是根据账户A当前质押的TRX和当前质押所获得的Energy总量按比例计算出来的，也就是：1 Energy = (10 / 100000) TRX，还剩100000 Energy，价值10 TRX，小于feeLimit，则在本次调用中，可以使用所有的100000 Energy，价值的10 TRX。

- 按照能量单价换算出来的Energy

    如果feeLimit大于质押剩余Energy价值的TRX，那么需要使用balance中的TRX来换算。能量单价是： 1 Energy = 210 sun, feeLimit还有(30 - 10) TRX = 20 TRX，则这部分可用的Energy是 20 TRX / 210 sun = 95238 Energy

所以，A此次调用能够使用的Energy是 (100000 + 95238) = 195238 Energy

如果合约执行成功，没有发生任何异常，则会扣除合约运行实际消耗的Energy，一般都远远小于此次调用能够使用的Energy。如果发生了Assert-style异常，则会消耗feeLimit对应的所有的Energy。

Assert-style异常的介绍详见[异常介绍](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E6%9C%BA/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.md)

**示例2**
如果一个账户A的balance是 100 TRX(100000000 SUN)，质押 10 TRX 获得了100000 Energy，未质押的balance是 90 TRX。
有一个合约C设置的消耗调用者资源的比例是40%，也就是由合约开发者支付所需资源的60%。
开发者是D，质押 50 TRX 获得了500000 Energy。
此时A调用了合约C，填写的feeLimit是 200000000(单位是SUN, 200 TRX)。
那么A此次调用能够使用的Energy是于以下三部分相关：

- 调用者A质押剩余的Energy（X Energy）

    这部分是根据账户A当前质押的TRX和当前质押所获得的Energy总量按比例计算出来的，也就是：1 Energy = (10 / 100000) TRX，还剩100000 Energy，价值10 TRX，小于剩下的feeLimit，则在本次调用中，可以使用所有的100000 Energy，价值的10 TRX。

- 从调用者A的balance中，按照固定比例换算出来的Energy （Y Energy）

    如果feeLimit大于质押剩余Energy价值的TRX，那么需要使用A的balance中的TRX来换算。能量单价是： 1 Energy = 210 sun, feeLimit还有(200 - 10) TRX = 190 TRX，但是A的balance只有90 TRX，按90TRX来计算可用的energy为 90 TRX / 210 SUN = 428571 Energy。

- 开发者D质押剩余的Energy (Z Energy)

    开发者D质押剩余500000 Energy。

会出现以下两种情况：

- 当(X + Y) / 40% >= Z / 60%，A此次调用能够使用的Energy是 X + Y + Z Energy。
- 当(X + Y) / 40% < Z / 60%，A此次调用能够使用的Energy是 (X + Y) / 40% Energy。

若A此次调用能够使用的Energy是 Q Energy

同上，如果合约执行成功，没有发生任何异常，消耗总Energy小于Q Energy，如消耗 500000 Energy ，会按照比例扣除合约运行实际消耗的Energy，调用者A消耗 $500000 * 40\% =200000$ Energy，开发者D消耗 $500000 * 60\% = 300000$ Energy。

一般实际消耗Energy都远远小于此次调用能够使用的Energy。如果发生了Assert-style异常，则会消耗feeLimit对应的所有的Energy。Assert-style异常的介绍详见[异常介绍](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E6%9C%BA/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.md)

注意：
开发者创建合约的时候，consume_user_resource_percent不要设置成0，也就是开发者自己承担所有资源消耗。
开发者自己承担所有资源消耗，意味着当发生了Assert-style异常时，会消耗开发者质押的所有Energy。为避免造成不必要的损失consume_user_resource_percent建议值是10-100。

## 动态能量模型
动态能量模型是波场网络的一个资源平衡机制，可以根据合约的资源占用情况动态调整每个合约的能量消耗量，从而使能量资源在链上的分配更加合理，防止网络资源过度集中在少数热门合约上，详情请参考[动态能量模型介绍](https://medium.com/tronnetwork/introduction-to-dynamic-energy-model-31917419b61a)。

### 工作原理
如果合约在一个维护周期(目前是6小时)内使用过多的能量，则在下一个维护周期内，用户向该合约发送相同的交易将产生更多的额外能量消量。当合约合理使用资源时，用户调用该合约所产生的能量消耗将逐渐恢复正常。

每一个合约有一个能量消耗放大系数 `energy_factor`，表示该智能合约交易的能量消耗相对于基础能量消耗的增加倍数，初始值是0。合约的`energy_factor`为0时，表示该合约在合理的使用资源，调用该合约不会有额外的能量消耗。当`energy_factor`大于0时，表示该合约已经是热门合约，调用该合约时将消耗额外的能量。合约的能量消耗放大系数可以通过 [getcontractinfo](https://developers.tron.network/reference/getcontractinfo) 接口查询。

合约调用交易最终需要消耗的能量的计算公式为：

```
合约交易能量消耗量 = 合约调用交易产生的基础能量消耗 * （1 +  energy_factor）
```

动态能量模型引入了如下三个TRON网络参数，它们共同控制合约的`energy_factor`字段：

* `threshold`：合约基础能量消耗的阈值，如果合约在一个维护周期中的基础能量消耗超过这个阈值，下一个维护周期，该合约的能量消耗量就会增加。
* `increase_factor`：合约在某个维护周期的能量消耗超过阈值，则在下一个维护周期，`energy_factor`就会根据increase_factor增加一定的比例。
* `max_factor`：合约`energy_factor`的最大值

另外还有一个变量`decrease_factor`用于降低合约的`energy_factor`：

* `decrease_factor`：`increase_factor`的四分之一，合约基础能耗降低到阈值以下后`energy_factor`会根据`decrease_factor`减少一定比例。

当合约的基础能量消耗量在一个维护周期内超过了`threshold`，那么在下一个维护周期它的`energy_factor`将增加，但最大不会超过`max_factor`，计算公式为：

```
energy_factor = min((1 + energy_factor) * (1 + increaese_factor)-1, max_factor)
```

当合约的基础能量消耗量在一个维护周期内下降到`threshold`及以下后，那么在下一个维护周期`energy_factor`就会降低，但最小值不会低于0，计算公式如下:

```
energy_factor = max((1 + energy_factor) * (1 - decrease_factor)- 1, 0)
```

动态能量模型在主网已经开启，相关参数设置如下：

* threshold：5,000,000,000
* increase_factor：0.2
* max_factor：3.4

由于热门合约在不同的维护周期的能量消耗是不一样的，所以在调用合约时要为交易设置合适的feelimit参数。


## 在TRON网络上质押


### 如何质押获取系统资源

能量和带宽资源由帐户所有者通过质押来获取，请使用`wallet/freezebalancev2`HTTP API完成质押操作、或者使用[Stake2.0 Solidity API](https://developers.tron.network/docs/stake-20-solidity-api)通过合约完成质押操作。

TRON通过质押机制分配网络资源。质押TRX除了可以获取带宽或者能量资源外，还将同时获得与质押量等量的投票权（TRON Power，简称TP），质押1TRX，获得1TP。质押获取到的带宽或者能量资源用于支付交易费用，获取到的投票权用于给超级代表投票以获取投票奖励。

解质押操作会释放对应的资源。

### 如何代理资源

账户在通过质押获取到能量或者带宽资源后，可以通过代理操作`delegateresource`将资源代理给其它地址，也可以通过取消代理操作`undelegateresource`收回分配出去的资源，代理资源需要注意以下情况：

- 只有能量和带宽可以被代理给其他地址，投票权无法被代理
- 只有Stake2.0 质押获取且未使用的资源可以代理给其它地址
- 只能代理给一个已激活的外部账户地址，不能代理给合约地址

可以通过`wallet/getcandelegatedmaxsize`接口查询账户某种资源的可供代理份额。代理资源时可采用`时间锁`，如果采用了时间锁，完成资源代理后，需要等待3天后才能取消对该地址的资源代理， 锁定期间，如果用户对同一个地址再次进行了资源代理，将重置3天等待时间。如果不采用时间锁，资源代理后，可立刻取消代理。

### 如何解质押

完成TRX质押后可随时解质押，解质押后需要等待14天，才可以将解质押的本金提取到自己的账户中，14天是TRON网络[第70号参数](https://tronscan.org/#/sr/committee)，可以被网络治理提议投票修改。请使用 `unfreezebalancev2` API完成解质押操作。

可多次分批解质押，但只允许最多同时进行32笔解质押操作，也就说当用户发起第一笔解质押，在这笔解质押的资金达到可提取状态之前，只能再发起31笔解质押操作。可通过`getavailableunfreezecount`接口查询剩余解质押次数。

已经代理出去的资源对应的TRX不可被解质押，解质押除了会失去等量的资源份额外，还将失去等量的TP资源。

在执行解质押时，如果存在未领取的投票奖励，会自动将投票奖励提取到账户内，如果存在已过锁定期的之前解质押的本金，那么本次解质押操作还将同时将已过锁定期的解质押本金提取到账户内，可通过`gettransactioninfobyid` API 查询一笔交易中提取到的投票奖励`withdraw_amount` 及提取到的已过锁定期的本金数量`withdraw_expire_amount` 。

#### 投票权资源回收

解锁在Stake2.0阶段质押的TRX后，会失去等量的投票权，系统优先回收账户内空闲的投票权，只有空闲的投票权不够回收时， 才会根据需要撤销一部分账户投票，如果用户投票给了多个超级代表， 将按照比例从每个超级代表撤销一定数量的投票，并将对应的投票权回收。从每个SR撤销的投数的计算公式为：

```
从当前超级代表撤销的票数 = 总撤票数 * (给当前超级代表的投票数 / 该账户总投票数)
```



举个例子，假设A总共质押了2,000TRX，并获取到2,000 TRON Powner，其中的1000 TRON Power投票给了2个超级代表，分别为600票和400票，账户中剩余1000 TRON Power。此时，A解质押1,500TRX，这意味着需要从A账户中回收1,500 TRON Powner, 在这种情况下，会优先回收A账户中空闲的1000 TRON Power，另外会分别从2个超级代表撤销300票和200票，然后回收这500 TRON Powner。这里撤票的计算方式如下：

- 超级代表1撤票数 = 500 \* (600 / 1,000) = 300
- 超级代表2撤票数 = 500 \* (400 / 1,000) = 200

目前TRON网络使用的是Stake2.0质押机制，但Stake1.0 质押获得的资源和投票继续有效，在Stake 1.0质押的TRX，仍然可以通过 Stake1.0 API `wallet/unfreezebalance`赎回，但需要注意的是，如果解质押Stake 1.0质押的TRX，会撤销账户所有的投票。

### 如何取消全部解质押
Stake2.0支持在用户解质押TRX后随时取消全部解质押，这样会使资产再次用于质押以获取相应的资源，而不必等待解质押本金过了锁定期后，将本金提取到账户内，再进行质押。请使用 `cancelallunfreezev2`API完成取消全部解质押操作。

在执行取消解质押时，会将所有未完成的解质押的本金重新用于质押，获取的资源类型与之前质押时相同。如果存在已过锁定期的解质押的本金，那么本次取消解质押操作会同时将已过锁定期的解质押本金提取到账户内，用户可通过`gettransactioninfobyid`接口查询本次交易取消的解质押本金数额 `cancel_unfreezeV2_amount`，以及提取到的已过锁定期的本金数量`withdraw_expire_amount` 。

### API

下表为质押模型相关接口及其说明：

| API                                                                                 | 描述                       |
| ----------------------------------------------------------------------------------- | ------------------------ |
| wallet/freezebalancev2                                     | 质押                       |
| wallet/unfreezebalancev2                                  | 解质押                      |
| wallet/delegateresource                                   | 资源代理                     |
| wallet/undelegateresource                                 | 取消资源代理                   |
| wallet/withdrawexpireunfreeze                        | 提取已过锁定期的解质押本金            |
| wallet/getavailableunfreezecount               | 查看剩余解质押次数                |
| wallet/getcanwithdrawunfreezeamount            | 查看可提取的已过锁定期的解质押本金        |
| wallet/getcandelegatedmaxsize                        | 查看可代理的资源份额数量             |
| wallet/getdelegatedresourcev2                        | 查看某地址代理给目标地址的资源情况        |
| wallet/getdelegatedresourceaccountindexv2 | 查看某地址资源代理情况与资源被代理情况      |
| wallet/getaccount                                        | 查看账户质押情况、资源份额、解质押情况、投票情况 |
| wallet/getaccountresource                              | 查看资源总量、已使用量、可用数量         |
| wallet/cancelallunfreezev2                              | 取消全部解质押         |
