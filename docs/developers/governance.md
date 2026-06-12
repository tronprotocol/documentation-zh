# 网络治理

TRON 网络的治理主要通过修改 [网络参数](https://tronscan.org/#/sr/committee) 来实现，这一过程也被称为 **网络升级**。  
任何人都可以在社区中提出对网络参数的修改建议，但只有 **超级代表（SR）** ，**超级代表合伙人** ，以及 **超级代表候选人** 才能在链上正式提交投票请求。在投票有效期内，超级代表将对提案进行表决。当投票截止时间到达且支持票数达到要求时，提案即自动生效。

您可以在 [这里](https://github.com/tronprotocol/tips/tree/master/proposal) 查看历次已完成的提案和投票记录。



## 提案投票流程

1. [发起提案的讨论](#initiate-proposal-discussion)  
2. [社区讨论](#community-discussion)  
3. [发起投票请求](#submit-voting-request)  
4. [投票和生效](#voting-and-implementation)  



## 发起提案的讨论 { #initiate-proposal-discussion }

任何 TRON 网络参与者都可以发起 TIP 投票的讨论。  
请在 [TIP 仓库](https://github.com/tronprotocol/tips/issues) 中创建一个 **Issue**，详细说明提案内容，包括：

- 提案动机  
- 计划修改的网络参数及其数值  
- 技术规范  
- 修改后的预期影响  

新的提案讨论可参考这个 [示例](https://github.com/tronprotocol/tips/issues/789)。

### 规范要求

#### 标题
为了便于传播与社区参与，建议为提案设计一个简洁明确的名称，并写在标题最前面，例如：

```
Proposal: Change the unit price of Energy to 100 sun
```

#### 主体内容
在 Issue 正文中，应包含以下主要部分：

```
## Simple Summary
简要说明该提案修改的 TRON 网络参数及数值，并概括预期作用。

## Motivation
描述提出该提案的动机，即当前存在的问题，以及为什么需要修改某些网络参数。

## Timeline
说明发起提案投票的日期，以及预估的提案生效时间。
一般来说，Issue 提出后会留出约两周的时间供社区讨论，因此正式的投票请求应在两周后启动。

## How to Initialize the Voting Request
明确说明在链上发起提案投票请求的命令。

## Technical Specification / Background
详细描述提案的技术规范或背景信息。
```

## 社区讨论 { #community-discussion }

在 TIP 讨论发起后，发起人应积极推动社区用户参与讨论，收集意见和反馈，并根据讨论结果对提案内容进行适当修改与更新。


## 发起投票请求 { #submit-voting-request }

若社区已充分讨论并形成基本共识，**超级代表** ，**超级代表合伙人**，或 **超级代表候选人**会在链上正式提交投票请求。


## 投票和生效 { #voting-and-implementation }

- 链上投票的有效期为 **3 天**。  
- 在此期间，所有超级代表均可对 TIP 进行投票。  
- 投票截止后，如果获得的超级代表赞成票数 **大于或等于 18 票**，该提案即视为通过并自动生效。
