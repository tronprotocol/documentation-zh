# 波场共识机制 DPoS

## 概述

区块链是一个分布式的记账系统，在一个区块链系统中可以有成千上万的节点，他们各自独立保存一份相同的账本，而新的交易数据想要被写入帐本，需要获得这些节点的认可。在不可信的分布式环境中实现这一目标是一个很复杂的系统工程。区块链系统正常运行，即区块链中各节点总能保存同一份账本，前提是系统中绝大部分的节点是诚实可靠的。为了保证诚实可靠的节点能够共同监督交易数据写入账本，每个区块链系统都需要构建自己的共识，共识就相当于区块链的宪法。共识保证了即便是在不可信的分布式环境下，只要绝大多数节点遵守共识的规定，就一定能获得确定可信结果。因此共识的意义在于，区块链中的诚信节点可以最终达成账本的一致只要他们严格遵守这份共识。

共识有多种类型，目前使用最多的是POW、POS、DPOS，当然不同的区块链系统中都会有一些特有的具体实现上的不同。本文主要介绍波场的共识就是基于DPOS的，同时向大家说明一下DPOS中的基本组件和机制。

DPoS共识的作用是在区块链系统中选出记账人，记账人验证交易数据并进行记账，进而向区块链网络中的其他节点广播新的账目，并获得其他节点对于新账目的认可。DPOS作为共识的一类特定实现是这样的：

DPOS共识在区块链系统中根据节点获取选票的多少确定出部分节点作为记账。首先区块链系统开始启动运行的时候，会发行一定数量的通证，然后将通证分给区块链系统中的节点，节点可以凭借一部分通证申请成为这个区块链系统记账人的候选人，区块链系统中任何持有通证的节点都可以为这些候选人进行投票，每经过一段时间t会统计所有候选人获得的选票数量，选票数量排在前面的N个节点会成为下一段时间t内的记账人，再经过t的时间，又会重新统计一遍新的记账人，以此类推循环往复。

下面结合波场中的实现具体说明：

## 定义
* 波场：指波场的区块链网络。本文不区分波场、波场区块链、波场区块链系统等概念。

* 波场币：指由波场区块链系统发行并在系统中流转的权益通证，代号是TRX。

* 记账候选人：指波场中有成为记账人资格的节点。

* 记账人：指波场中获得记账资格的节点，通常DPOS共识中将记账人称为超级代表，波场也将记账人称为super node，super representative（简称SR），波场设定记账人的数量是27个。下文不区分记账人、witness、supernode、SR等概念。

* 记账：指验证交易并将交易记录成账目的过程，由于波场中的账目是用区块承载的，因此记账的过程也被称为生产区块，下文不区分记账和生产区块。

* 记账顺序：即出块顺序。按照27个记账人得票多少的降序作为记账顺序。

* 槽位：在TRON中，每3秒钟被计为一个slot，正常情况下每个产块的SR都会在对应的slot时间内产块。因此，TRON 的平均产块间隔为3秒左右。如果因某些原因SR没有产块，则对应的slot会空置，下一个SR会在接下来的slot内产块。遇到维护期时，产块会跳过2个slot。

* 出块轮：波场设定每6个小时作为一个出块轮，称为一个Epoch。每个出块轮最后的2个出块时间是一个维护期。每个出块轮的维护期决定下一个出块轮的出块顺序。

* 维护期：波场设定是2个区块时间，即6秒钟。这段时间用于统计候选人得票数。因为24个小时有4个出块轮，自然就有4个维护期，维护期中不进行区块生产，主要用来确定下个出块轮的出块顺序。

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/sequence.png)

## 记账流程

区块链系统的记账人，他们收集区块链网络中新产生的交易，并对这些交易的合法性进行验证，然后把这些交易打包在一个区块中，作为新的一页账记录在账本上，然后将账页在整个区块链网络中进行广播，其他的节点收到新的账页，也会验证账页中交易数据的合法性，并添加到自己的账本中。记账人一直重复这个过程，这样只要区块链系统中新的交易数据都会记录在账本里面。

## 超级节点选举机制

- 选票

波场中设定拥有一个TRX就可以拥有一张选票的权利。

- 投票过程

波场中设定对候选人的投票过程是一笔特殊类型的交易，节点可以通过生成一笔投票交易对候选人进行投票。

- 统计票

每个维护期内，统计一次候选人的票数，将获得票数最多的27个候选人作为下一个出块周期的记账人。

## 产块机制
在一个出块轮中，27个记账人按照记账顺序依次生产区块。每个记账人只能在轮到自己产块时进行区块生产，记账人将多笔验证合法的交易数据打包到每个区块之中，同时每个区块都会将上个区块的哈希值（hash）作为本区块的父哈希值（parentHash）填入区块中，同时用自己的私钥对本区块的数据进行签名，将签名结果（witness_signature）也填入区块中，同时被填入区块的还有记账人的地址，区块高度，区块生成的时刻等数据。

通过每个区块保存了上个区块hash值的方式，从而在逻辑上将区块相互关联了起来，最后组成了一条链的结构。典型的区块链结构示意图如下所示：

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/blockchain_structure.png)


理想情况下，采用DPOS共识的区块链系统的记账过程就是按照事先计算好的记账顺序，由超级代表轮流依序产块（如下图a），但实际情况下，区块链网络是一个分布式的、不可信的复杂系统，体现在 1）由于网络链路环境不佳导致超级代表生产的区块并不会在有效时间内被其他的超级代表收到（如下图b1、b2）；
2）并不能保证某个超级代表运行始终正常（如图c）；
3）某些超级代表恶意生产分叉的区块企图将链分叉（如图d）。

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/longest_chain1.png)

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/longest_chain2.png)

前文已经提到区块链系统正常运行的基础是系统中绝大部分的节点是诚实可靠的，再进一步探讨这个问题，区块链系统安全的首要保证的是账本的安全，账本既不能被恶意写入不合法的数据，账本在各个节点上保存的副本也应该是一致的。如果从DPOS共识的角度上来看，记账过程是由超级代表完成，因此波场的安全取决于大部分超级代表的可靠性，波场设定了不可逆转区块，也称为固化块。同时为了抵抗少部分记账节点的恶意行为，波场采用基于最长链的原则确认为主链。

### 固化块原则
刚生产出来的区块处于未确认状态，至少被27个超级代表中的70%（27 * 70 = 19，向上取整)认可的区块才被认为是不可逆区块，一般称为固化块，此时固化块中包含的交易已经被整个区块链网络确认。此处对未确认状态区块"认可"的方式是超级代表在其之后生产后继区块，如图d中超级代表C生产的第103块，超级代表E在第103块的基础上生产了104‘,超级代表G、A、B分别生产的第105‘、106’、107‘实质上也是103块的后继区块，故也是对C生产的第103块的认可。可知，当高度为121的区块被生产出来的时候，第103块就成为固化块，因为此时103区块已经有了19个后继区块，此处需要强调的一点是：生产这19个区块的超级代表互不相同，并且和生产第103个区块的超级代表也不同。

### 最长链原则

当区块链产生分叉之后，诚实的超级代表总是选择在当前最长的那个分叉链上继续生产区块。

## 激励模型

为了保证区块链系统安全高效地运行，TRON设定激励模型，用于鼓励更多的节点加入到波场网络，从而扩大网络规模。波场网络每生成一个区块，都会授予16个TRX的区块奖励给生产该区块的超级代表，还会授予160个TRX的投票奖励给所有超级代表和超级合伙人(票数排名第28～127名的超级代表候选人也叫超级代表合伙人)，他们根据获得的投票数按比例瓜分投票奖励。同时，超级代表及合伙人还会将获得的奖励按照其设定的佣金比例扣除后，将剩余部分按照选民投票比例分发给选民。

## 基于提案对参数进行调整

DPOS的一个重要的特性是任何系统参数的调整都可以通过链上的提案发起，记账人通过对提案的投票来决定提案是否生效，这样的好处是在链上新增加一些特性不需要进行硬分叉升级。目前TRON网络的动态参数及其值，以及过往的提案，请参考[这里](https://tronscan.org/#/sr/committee)。


## 参考文档

- [The Basics of TRON’s DPoS Consensus Algorithm](https://medium.com/tronnetwork/the-basics-of-trons-dpos-consensus-algorithm-db12c52f1e03)
