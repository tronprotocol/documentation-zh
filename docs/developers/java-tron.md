# 开发者指南

非常感谢您帮助我们开发java-tron源代码！我们欢迎来自任何人对java-tron给予的的贡献，即使是很小的修复，我们也表示感激。

GitHub可以用于跟踪问题、贡献代码、提出建议、请求新功能以及管理文档。如果您想参与java-tron开发，请遵循如下Github代码提交流程：

* Fork java-tron仓库 
* 修改代码 
* 提交改动 
* 发送一个pull request
* 维护者审查并合并到主分支

对于小的修复，您可以直接发送一个pull request (PR)，但请确保PR中包含详细的描述。对于复杂的改动，您需要向[TIP仓库](https://github.com/tronprotocol/tips)提交一个issue，以详细说明您的动机和实现计划等。关于如何提交TIP issue，请参见[TIP规范](tips.md)。

我们鼓励java-tron开发者尽早提交PR，即使没有完全开发完成，也可以先提交PR，这样可以让其它开发者了解到这个PR对应的TIP Issue已经处于`In Progress`状态。

java-tron开发者应基于`develop`分支进行开发并提交PR，审查者将根据[代码审查指南](#_4)对提交的PR进行审查。


## 分支管理
java-tron项目分支只有master、develop、`release-*`、`feature-*`、`hotfix-*`分支：

* ``develop`` 分支

    develop分支只能合并其他Fork的分支、`release-*`分支。当决定要发一个新版本的时候，需要从develop分支拉出一个`release-*`分支。
    
* ``master`` 分支

    master分支只能在发布新版本时合并`release-*`分支、`hotfix-*`分支。
    
* ``release`` 分支

    `release-*`分支是准备发版前定版的分支，它是从`develop`分支拉出来的一个分支，此分支经过回归测试之后，最终合并到`master`，同时这个分支永久保留在仓库中。如果遇到`release-*`分支有bug，后续修复bug的代码直接合并到`release-*`分支上。通过回归测试后，将`release-*`分支合并回`develop`分支。`release-*`分支实际上为每次的发版保留了一个快照。

- ``feature`` 分支

    `feature-*`分支是重要的功能特性分支，它是从`develop`分支拉出来的一个分支。`feature-*`分支开发完成之后合并回`develop`分支，并且`feature-*`支是可以被维护的。

- ``hotfix`` 分支

    从`master`分支拉出来，合并回master分支和`develop`分支。`hotfix`分支只能合并Fork仓库的PR（一定是用于修复bug的PR）。`hotfix`分支只用来版本上线之后发现的bug修复。
    
## 代码提交流程

如果您想为java-tron贡献代码，应该遵循以下步骤：

* Fork java-tron代码仓库

    从 [https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) 项目中Fork一个新的repository到自己个人的代码仓库中，然后使用如下命令将代码克隆到本地:
    
    ```
    $ git clone https://github.com/yourname/java-tron.git

    $ git remote add upstream https://github.com/tronprotocol/java-tron.git   （备注：upstream指的是上游的项目仓库，即tronprotocol中的repository，upstream可以任意命名，但是习惯上命名为upstream）
    ```
    
* 在Fork的仓库中修改代码 
    
    开发新功能之前先将个人Fork的仓库和上游仓库进行同步：
    
    ```
    git fetch upstream 
    git checkout develop 
    git merge upstream/develop --no-ff   (添加--no-ff可以关闭默认的快速合并模式)
    ```
    
    从自己仓库的develop分支拉出一个新的分支用于本地开发，请参考[分支命名规范](#_8)。

    ```
    git checkout -b feature/branch_name develop
    ```

    编写新的代码,完成之后提交commit，请参考[commit规范](#commit)。
    ```
    git add .
    git commit -m 'commit message'
    ```
     
    提交新的分支到个人远端仓库：
     
    ```
    git push origin new_feature
    ```

* Push代码

    从你自己的仓库向`tronprotocol/java-tron`提交一个推送代码请求 Pull Request（PR）。建议选择红框的选项，将tronprotocol的分支选成base分支，将个人的Fork仓库的分支选成compare分支。
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/javatron_pr.png)



## 代码审查指南
将代码合并到java-tron的唯一方法是发送一个pull repuest（PR），而提交的PRs需要被审查通过后，才可以合并到主分支。下面将详细介绍我们对代码提交者和代码审查者的期望。

### 审查流程
对于任何PR，我们需要判断是否值得将其包含在主分支中。为了做出决定，我们必须了解这个PR是做什么的。如果PR的提交者对PR没有提供足够的描述内容或PR的代码改动太大，任何人都可以要求PR提交者给予适当的解释与说明。

审查者应该检查PR的代码风格以及功能的完整性，并在GitHub中给予评论。审核者应该一直跟进PR，直至满足要求，然后批准PR。最后由java-tron维护者将批准的PR合并到主分支。

当与PR提交者沟通时，请注意，要懂得礼貌和尊重。

### 功能检查
对于修复问题的PRs，审查人员应该尝试重现问题，并验证PR确实修复了问题。为了帮助审查者可以快速的检查问题的修复情况，PR提交者可以包含一个单元测试，这个单元测试会在没有代码更改的情况下失败，而在包含了更改代码的情况下通过。

对于添加新功能的PRs，审核人员应该尝试使用该功能并对使用的感受给出评论。例如:一个PR添加了一个新的命令行参数，那么审查者应该使用该参数，并对该参数是否有用给出自己的意见。

任何一个PR，只要改动代码，都应提供足够的单元测试，以保证基础功能正常。评审者应该验证单元测试是否覆盖了新代码。

### 代码规范
我们希望遵循一个共同的开发流程和代码规范。为此，我们有以下建议。

1. 使用代码规范工具来检查代码
2. 在提交之前检查代码
3. 标准化的测试 

`Sonar`检查和`Travis CI`持续集成检查将在PR提交后自动触发，一旦所有检查通过，**java-tron**维护者将审查该PR，并在必要时给予反馈修改。一旦通过，我们将关闭该PR，并将其合并到`develop`分支。

我们很高兴收到推送代码请求，并尽最大努力以及最快的速度审查它们。一个不确定的错别字是否值得提交一个推送请求？
请去处理它! 我们会很感谢你的贡献。

如果你的推送代码请求在第一次尝试时没有被接受，请不要灰心，因为这可能是一个疏忽。请尽可能多地解释描述你的代码，让我们更容易理解。

请确保你的提交遵循以下编码准则：

- 代码必须符合: [Google Code Style](https://google.github.io/styleguide/javaguide.html)
- 代码必须通过静态代码分析Sonar检测
- 拉取代码必须以`develop`分支为基础


### 分支命名规范
分支命名应遵循如下规范：

1. `master`分支和`develop`分支固定为"master"和"develop"
2. 版本开发分支名称为版本号，由项目负责人指定，例如：Odyssey-v3.1.3，3.1.3等
3. `hotfix`分支以`hotfix/`作为前缀，名称为Bug简单描述，多个单词用连接符"-"进行连接，例如：hotfix/typo，hotfix/null-point-exception等
4. `feature`分支以`feature/`作为前缀，名称为该新特性的简要描述，多个单词用连接符"-"进行连接，例如：feature/new_resource_model等

### Pull Request规范
Pull Request应遵循如下规范：

1. 一个PR只围绕一件事
2. 避免代码改动量特别大的PR
3. PR标题——概述此次PR的目标
4. PR说明——面向未来的Reviewer
5. 如果需要反馈，请详述需要哪些反馈


#### Commit描述规范
提交PR时提供的描述内容应遵循以下规范，可以使用如下模板对PR内容进行说明：
```
<commit type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```
消息头是对更改的简要描述，其中包含`commit type`、`scope`和`subject`。

`commit type` 描述了该提交的更改类型:

* feat     ：新功能
* fix      ：bug修改
* docs     ：文档修改
* style    ：格式化，如缺少分号等，没有代码更改
* refactor ：重构代码
* test     ：添加或重构测试代码，没有生产代码更改
* chore    ：其它，如分配任务等，没有生产代码更改

`scope`（可选）描述了提交的更改所在位置。例如:`protobuf`、`api`、`test`、`docs`、`build`、`db`、`net`等。如果没有合适的作用域，可以使用*代替。

`subject`是对Commit目的的简短描述，规范如下：

1. commit主题不超过50个字符
2. 以动词开头，使用第一人称现在时，比如change，而不是changed或changes
3. 首字母小写
4. 结尾不加句号（.）
5. 避免无意义的commit，推荐大家学习git rebase命令的使用

消息体使用祈使句，动词开头，第一人称现在时。主体应该包括代码修改的动机，并与修改之前进行对比。下面是一个PR commit的例子：
```
feat(block): optimize the block-producing logic

1. increase the priority that block producing thread acquires synchronization lock
2. add the interruption exception handling in block-producing thread

Closes #1234
```
如果此次提交是为了修改一个issue，则需要在页脚中引用该issue，以关键字`Closes`开头，例如`closes#1234`，如果修改了多个错误，则用逗号分隔它们，例如`Closes #123, #245, #992`。



### 特殊情况及应对方法
作为审查人员，当遇到如下特殊情况时，请根据建议进行PR处理。

* PR提交者没有继续跟进: 可以过段时间(例如，几天后)再联系他们，如果还是没有进一步的回应，可以关闭该PR或者自己继续完成提交者未完成的工作。
* PR提交者坚持在修复bug的同时进行代码重构: 我们可以容忍在任何更改的同时进行小的重构。如果您认为代码改动量太大，或者PR改动不清晰，可以联系PR提交者，请求以独立PR的形式提交重构代码，或者在同一PR中以独立提交的形式提交重构代码，这样可以使代码修改意图更清晰，更方便审查者审阅。
* PR提交者一直拒绝您的反馈: 可以关闭PR。

## 行为准则
在贡献的同时，请保持尊重性和建设性，使参与我们项目的每个人都有一种积极的项目体验。

有助于创造积极环境的行为包括:

* 使用友好和包容的言语
* 尊重不同的观点和经验
* 善于接受建设性的批评 
* 专注于有助社区发展的事情
* 对其他社区成员表示友好

不可接受的行为包括:

* 低俗用语
* 恶意攻击，侮辱性/贬损性评论，以及个人或政治攻击 
* 公开或私下骚扰 
* 未经明确许可发布他人的私人信息 
* 其他被认为不合适的行为
