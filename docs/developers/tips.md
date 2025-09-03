# 波场改进提案(TIPs)

TRON Improvement Proposals(TIPs)是TRON网络改进提议，TIPs记录了TRON改进的整个过程，包括社区提出建议、讨论、采纳的过程记录。一个TIP是一个关于提议的设计文档，包含提议的基本原理和技术规范，社区用户可以通过阅读TIP文档了解提议的详细信息。 TIP是TRON社区治理的基本单位，任何人都可以自由提议，社区参与者会进行讨论，以确定是否应该将其发展为通用标准或纳入网络升级。TIP提出者负责在社区内鼓励其他开发者参与讨论，建立对该TIP的共识，同时还需要记录不同意见。 

## TIP类型
TIPs主要分为`Standard Track`和`Informational`两种:

* `Standard Track` :  描述影响波场实现的更改，如区块或交易有效性规则的更改、拟议的应用程序标准，或影响波场应用程序互操作性的任何改动。`Standard Track` TIPs还可以细分为以下几类：
    * `Core`: 需要共识分叉来实现的TIP，也有一些不需要共识，但需要核心开发者讨论的TIP
    * `Networking`: 对网络协议的改进
    * `Interface`: 对API/RPC规范和标准的改进
    * `TRC`：应用级标准，包括合约标准，如TRC-20
    * `TVM`：对TRON虚拟机的改进

* `Informational`: 描述有关TRON的设计问题，或向波场社区提供一般性的指导或信息，但不提出新特性

## TIP工作流程

在提交TIP之前，需要创建一个TIP issue供其他人讨论，，然后将issue链接添加到TIP标题中，TIP issue的格式与TIP内容一致，提交TIP流程如下：

1. Fork Github [TIPs仓库](https://github.com/tronprotocol/TIPs)
2. 请参照 [TIP模板](https://github.com/tronprotocol/TIPs/blob/master/template.md)，在您的fork仓库中新建一个TIP
3. 提交一个 Pull Request 到波场TIPs仓库。


请您严格按照 [模板](https://github.com/tronprotocol/TIPs/blob/master/template.md) 要求使用`markdown`编写TIP，并确保在 TIP 标题中附上了TIP Issue链接或一个讨论论坛的地址，以使社区参与者可以对该提议进行充分的讨论。如果一个TIP是关于java-tron的新特性的开发，并且存在该新特性的开发PR，您需要在TIP和java-tron的PR中，互相引用彼此的github链接，以使新特性的需求分析和开发代码可追溯。

对于一个新的TIP，它的第一个PR提交后，该TIP处于草案版`Draft`状态，编辑者会审核该TIP，使其满足一定的格式标准，在合并之前会为之分配一个TIP编号。

当您认为该TIP已经成熟完善并且准备越过`Draft`阶段，您应该：

- 对于核心TIP，您需要联系波场核心开发人员将您的提议加入到下次核心开发者会议内容里，从而可以讨论您的提议。如果核心开发者决定采纳您的提议，TIP编辑者会更新您的TIP状态为已采纳`Accepted`。
- 对于其他类型的TIP，您可以提交一个PR，将该TIP的状态改为最终版`Final (non-Core)`，然后TIP编辑者会审核您的草案并且询问是否有人反对将您的提议状态改为最终版，如果TIP编辑者认为该TIP还不能达成初步的共识，他们可能会关闭您的PR，并且要求您继续修改草案内容。

### TIP状态
一个TIP可能经历如下的状态：

- `Draft`: 草案版，提议处于快速迭代与修改期
- `Last Call`: 待审核，提议已经完成初始迭代并且可以被他人审核
- `Accepted`: 当核心TIP的提出者已经解决了所要求的技术变更，并且该TIP处于`Last Call`状态至少2周，那么核心开发者需要决定是否将该TIP作为硬分叉的一部分加入到客户端的开发（此过程不属于TIP流程中的一部分）决定做出后，该TIP将进入`Final`状态。
- `Final (non-Core)`: 非核心类型TIP已处于`Last Call`状态至少2周，并且所有更改均已完成。
- `Final (Core)`: 核心开发者决定实现该TIP，将在接下来的版本中包含该TIP或已经在某个发布的版本中实现了该TIP。
- `Active`: 如果一个TIP可能永远不会被完成，那么它的状态可以为`Active`
- `Abandoned`:一个TIP已经不再被它的提交者跟踪维护，或者它可能不再是技术上的首选
- `Rejected`:破坏功能的TIP或被核心开发者拒绝的不会实现的`Core` TIP
- `Superseded`:之前是Final状态，但现在不再被认为是最优的方案
- `Deferred`:现在不被采纳，将来可能会被采纳的TIP



## TIP的组成
TIP 由标题序言和主体内容组成。
### TIP标题

TIP标题包含TIP编号、简短的描述性标题(限制为最多44个字符)、作者详细信息、讨论链接、TIP状态、TIP类型、创建时间等，具体格式请参考：
```

---
tip: <to be assigned>
title: <TIP title>
author: <a list of the author's or authors' name(s) and/or username(s), or name(s) and email(s), e.g. (use with the parentheses or triangular brackets): FirstName LastName (@GitHubUsername), FirstName LastName <foo@bar.com>, FirstName (@GitHubUsername) and GitHubUsername (@GitHubUsername)>
discussions-to: <URL>
status: <Draft | Last Call | Accepted | Final | Deferred>
type: <Standards Track (Core, Networking, Interface, TRC, VM) | Informational>
category (*only required for Standard Track): <Core | Networking | Interface | TRC | VM>
created: <date created on, in ISO 8601 (yyyy-mm-dd) format>
requires (*optional): <TIP number(s)>
replaces (*optional): <TIP number(s)>
---  

```

### TIP主体内容
TIP主体应包括以下部分:

* `Simple Summary`：对TIP的简短描述。
* `Abstract` ： 摘要，是一个简短的技术总结，是`Specification`部分的一个简洁、易理解的版本。人们可以通过只阅读`Abstract`来了解该TIP的主要功能。
* `Motivation`: (可选) 动机是TIP的一个重要部分，在`Motivation`中应该清楚地解释为什么现有的协议规范不足以处理该TIP所解决的问题。如果动机明显，这一部分可以省略。
* `Specification`：技术规范是描述新特性的语法和语义，并且应该足够详细
* `Rationale`：基本原理是描述设计的动机，以及为什么做出如此设计决策。它用来对`Specification`做补充。同时，`Rationale`还要描述其它的备选设计方案和相关工作，即它应包括对在TIP讨论过程中提出的重要反对意见或关注事项的说明。
* `Backwards Compatibility` ：(可选) 如果TIP的改动会引入向后不兼容的问题，那么TIP中应该包含`Backwards Compatibility`，来描述这些不兼容及其影响。TIP必须说明打算如何处理这些不兼容。
* `Test Cases` ：(可选) 对于影响共识的TIP来说，必须包含实现代码相关的测试用例。非核心TIP可省略此部分。
* `Implementation`：该部分内容可以在TIP被赋予`Accepted`状态之前不填写，但必须在TIP被赋予`Final`状态之前完成。当涉及到许多API细节的讨论时，“大体的共识和可运行的代码"是有必要的。


## 链接外部资源 
由于外部资源可能随时变化，比如链接失效、内容移动或修改，因此，TIP中不应该包括外部资源的链接。

## 链接其它TIPs
TIP 中可以引用其它TIPs，对其它TIP的引用应遵循 `TIP-N` 格式，其中 `N` 是所引用的TIP编号，并且需附上引用链接，链接必须是相对路径，这样才能使链接在TIP GitHub仓库以及各个Forks等处有效。例如，您可以使用`[TIP-1](/tips/TIP-1)`对`TIP-1`进行引用。

## 辅助文件 
图像、图表和其它辅助文件应该存放在TIP仓库的`assets`文件夹的子目录中，例如:`assets/TIP-N/` (N为TIP编号)。在TIP中链接图片时应使用相对路径，如：`../assets/TIP -1/image.png`。

