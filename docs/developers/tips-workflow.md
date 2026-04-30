# TIP 规范与指南


**TRON Improvement Proposals (TIPs)** 记录了 TRON 网络从社区建议、讨论到最终采纳的整个改进过程。每个 TIP 都是一个详细的设计文档，涵盖了其基本原理和技术规范，旨在帮助社区用户全面了解其中内容。TIPs 是波场社区治理的核心单元，任何人都可以自由提出，并通过社区讨论来决定是否将其发展为通用标准或纳入网络升级。TIP 的提出者有责任在社区内鼓励开发者参与讨论，建立对该 TIP 的共识，并记录所有不同意见。


## TIP 类型

TIPs 主要分为 `Standard Track` 和 `Informational` 两种类型：

* **`Standard Track`**: 这类 TIP 描述了影响波场实现方式的变更，例如区块或交易有效性规则的修改、拟议的应用程序标准，或任何影响波场应用程序互操作性的改动。`Standard Track` TIPs 还可以细分为以下几类：
    * **`Core`**: 需要通过共识分叉（consensus fork）[^1]来实现的 TIP，也有一些不需要共识但需要核心开发者讨论的 TIP。
    * **`Networking`**: 针对网络协议的改进。
    * **`Interface`**: 针对 API/RPC 规范和标准的改进。
    * **`TRC`**: 应用层级标准，包括智能合约标准，如 TRC-20。
    * **`TVM`**: 对波场虚拟机 (TRON Virtual Machine) 的改进。
* **`Informational`**: 这类 TIP 描述了与波场设计相关的问题，或向波场社区提供一般性的指导或信息，但不提出新特性。


## TIP 工作流程

在提交 TIP 之前，建议先创建一个 TIP **issue** 供社区讨论，并将该 issue 的链接添加到 TIP 标题中。TIP issue 的格式应与 TIP 内容保持一致。提交 TIP 的具体流程如下：

1.  **Fork** GitHub [TIPs 仓库](https://github.com/tronprotocol/TIPs)。
2.  参照 [TIP 模板](https://github.com/tronprotocol/TIPs/blob/master/template.md)，在您的 Fork 仓库中新建一个 TIP。
3.  向波场 TIPs 仓库提交一个 **Pull Request (PR)**。

请您严格按照 [模板](https://github.com/tronprotocol/TIPs/blob/master/template.md) 要求使用 `markdown` 编写 TIP，并确保在 TIP 标题中附上 TIP Issue 链接或一个讨论论坛的地址，以便社区参与者能够充分讨论该 TIP 。如果一个 TIP 涉及 java-tron 的新特性开发并存在相关的开发 PR，您需要在 TIP 和 java-tron 的 PR 中互相引用彼此的 GitHub 链接，以确保新特性的需求分析和开发代码可追溯。

对于一个新的 TIP，其首次 PR 提交后，该 TIP 将处于 **`Draft`**（草案版）状态。编辑者将审核该 TIP 以确保其符合一定的格式标准，并在合并之前为其分配一个 TIP 编号。

当您认为该 TIP 已成熟完善并准备进入下一阶段时，您应该：

* 对于 **核心 TIP**，您需要关注并按照 [TRON Project Management Repository](https://github.com/tronprotocol/pm?tab=readme-ov-file#tron-core-devs-meetings-and-sr-meetings-overview) 仓库里的核心开发者会议流程，将您的 TIP 提交到议程中，以便在后续会议上进行讨论。如果核心开发者决定采纳您的 TIP ，TIP 编辑者会将您的 TIP 状态更新为 **`Accepted`**（已采纳）。
* 对于 **其他类型的 TIP**，您可以提交一个 PR，将该 TIP 的状态改为 **`Final (non-Core)`**（非核心最终版）。随后，TIP 编辑者将审核您的草案，并询问是否有反对意见。如果 TIP 编辑者认为该 TIP 尚未达成初步共识，他们可能会关闭您的 PR，并要求您继续修改草案内容。


### TIP 状态

一个 TIP 可能会经历以下状态：

* **`Draft`**: 草案版， TIP 处于快速迭代与修改阶段。
* **`Last Call`**: 待审核， TIP 已完成初始迭代并可供他人审核。
* **`Accepted`**: 当核心 TIP 的提出者已解决所需的技术变更，且该 TIP 处于 `Last Call` 状态至少 2 周后，核心开发者需决定是否将该 TIP 作为硬分叉的一部分加入客户端开发（此过程不属于 TIP 流程）。决定做出后，该 TIP 将进入 `Final` 状态。
* **`Final (non-Core)`**: 非核心类型的 TIP 已处于 `Last Call` 状态至少 2 周，并且所有更改均已完成。
* **`Final (Core)`**: 核心开发者决定实现该 TIP，将在接下来的版本中包含该 TIP 或已在某个发布的版本中实现了该 TIP。
* **`Active`**: 如果一个 TIP 可能永远不会被完成，那么它的状态可以为 `Active`。
* **`Abandoned`**: 一个 TIP 已不再被其提交者跟踪维护，或者它可能不再是技术上的首选方案。
* **`Rejected`**: 破坏功能的 TIP，或被核心开发者拒绝的不会实现的 `Core` TIP。
* **`Superseded`**: 之前是 `Final` 状态，但现在不再被认为是最优的方案。
* **`Deferred`**: 当前不被采纳，但将来可能会被采纳的 TIP。


## TIP 的组成

TIP 由标题序言和主体内容两部分组成。


### TIP 标题

TIP 标题包含 TIP 编号、简短的描述性标题（限制为最多 44 个字符）、作者详细信息、讨论链接、TIP 状态、TIP 类型、创建时间等。具体格式请参考：

```
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
```


### TIP 主体内容

TIP 主体应包括以下部分：

* **`Simple Summary`**: 对 TIP 的简短描述。
* **`Abstract`**: 摘要，是对 `Specification` 部分的一个简洁、易理解的技术总结。读者可以通过只阅读 `Abstract` 来了解该 TIP 的主要功能。
* **`Motivation`**(可选)：动机是 TIP 的一个重要部分。在 `Motivation` 中应清楚地解释为什么现有协议规范不足以处理该 TIP 所解决的问题。如果动机显而易见，此部分可以省略。
* **`Specification`**: 技术规范，详细描述新特性的语法和语义，应足够详细。
* **`Rationale`**: 基本原理，描述设计的动机以及做出如此设计决策的原因。它用于对 `Specification` 进行补充。同时，`Rationale` 还应描述其他备选设计方案和相关工作，并包括对 TIP 讨论过程中提出的重要反对意见或关注事项的说明。
* **`Backwards Compatibility`** (可选)：如果 TIP 的改动会引入向后不兼容的问题，那么 TIP 中应包含 `Backwards Compatibility`，描述这些不兼容及其影响。TIP 必须说明打算如何处理这些不兼容。
* **`Test Cases`**(可选)：对于影响共识的 TIP 来说，必须包含实现代码相关的测试用例。非核心 TIP 可省略此部分。
* **`Implementation`**: 此部分内容可以在 TIP 被赋予 `Accepted` 状态之前不填写，但必须在 TIP 被赋予 `Final` 状态之前完成。当涉及到许多 API 细节的讨论时，“大体的共识和可运行的代码”是必要的。


## 链接外部资源

由于外部资源可能随时变化（例如链接失效、内容移动或修改），因此，TIP 中不应直接包含外部资源的链接。


## 链接其他 TIP

TIP 中可以引用其他 TIP。对其他 TIP 的引用应遵循 `TIP-N` 格式，其中 `N` 是所引用的 TIP 编号，并需附上引用链接。链接必须是相对路径，以确保链接在 TIP GitHub 仓库以及各个 Fork 中均有效。例如，您可以使用 `[TIP-1](/tips/TIP-1)` 对 `TIP-1` 进行引用。


## 辅助文件

图像、图表和其他辅助文件应存放在 TIP 仓库的 `assets` 文件夹的子目录中，例如：`assets/TIP-N/` (N 为 TIP 编号)。在 TIP 中链接图片时应使用相对路径，如：`../assets/TIP-1/image.png`。

---

[^1]: **共识分叉 (consensus fork)**：指区块链网络中的节点对协议规则的更改达成不同意见，导致区块链历史分化的现象。

