# 开发者指南

感谢您参与 **java-tron** 源代码的开发！  

无论是小的修复还是重要的功能改进，我们都非常感激您的贡献。  

在 GitHub 上，您可以用于：

- 跟踪问题  
- 贡献代码  
- 提出改进建议  
- 请求新功能  
- 协作维护文档  

如果您计划参与 **java-tron** 的开发，请遵循以下流程。



## 贡献流程概览

1. **Fork 仓库**  
   将 [java-tron 仓库](https://github.com/tronprotocol/java-tron) Fork 到您个人账号。
2. **修改代码**  
   基于规范的分支创建新分支并进行开发。
3. **提交改动**  
   使用清晰的 Commit 信息提交您的更改。
4. **创建 Pull Request (PR)**  
   将改动推送到您的 Fork 仓库，并向官方仓库提交 PR。
5. **代码审查与合并**  
   维护者将根据 [代码审查指南](#_6) 审核您的 PR，并在合格后合并至主分支。



## 提交规则

- **小修复**  
  可以直接发起 PR，但务必包含完整的描述。  
- **复杂改动**  
  请先在 [TIP 仓库](https://github.com/tronprotocol/tips) 提交 Issue，详细说明动机与实现方案。  
  参考 [TIP 规范](tips.md)。  
- **提前提交 PR**  
  我们鼓励开发者尽早提交 PR，即使功能尚未完成。这样其他开发者能及时获知相关的 TIP Issue 已进入 *In Progress* 状态。  
- **开发分支**  
  所有开发应基于 `develop` 分支进行，随后再提交 PR。  



## 分支管理

**java-tron** 仓库包含以下主要分支类型：

- **`develop` 分支**
    - 用于日常开发  
    - 只允许合并分叉分支与 `release-*` 分支  
    - 每次准备新版本时，从该分支拉取 `release-*`  
- **`master` 分支**  
    - 只在发布时使用  
    - 合并对象仅限 `release-*` 与 `hotfix-*`  
- **`release-*` 分支**  
    - 从 `develop` 拉取，用于版本定版和回归测试  
    - 回归完成后合并至 `master`  
    - 永久保留，作为发版快照  
    - Bug 修复直接合并到该分支，并同步回 `develop`  
- **`feature-*` 分支**  
    - 从 `develop` 拉取，用于新功能开发  
    - 功能完成后合并回 `develop`  
    - 可长期维护  
- **`hotfix-*` 分支**  
    - 从 `master` 拉取，用于紧急 Bug 修复  
    - 修复完成后合并回 `master` 与 `develop`  



## 代码提交流程

### 1. Fork 与克隆仓库
```
git clone https://github.com/yourname/java-tron.git
cd java-tron
git remote add upstream https://github.com/tronprotocol/java-tron.git
```
> `upstream` 代表官方仓库。命名可自定义，但习惯上使用 `upstream`。
### 2. 同步上游代码
```
git fetch upstream
git checkout develop
git merge upstream/develop --no-ff
```
> `--no-ff` 用于避免快速合并模式，确保提交历史清晰。
### 3. 创建开发分支
```
git checkout -b feature/branch_name develop
```
### 4. 提交改动
```
git add .
git commit -m "commit message"
```
### 5. 推送分支
```
git push origin feature/branch_name
```
### 6. 发起 Pull Request
从你自己的仓库向 `tronprotocol/java-tron` 提交一个推送代码请求 Pull Request（PR）。
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/javatron_pr.png)


建议选择红框的选项，将 `tronprotocol/java-tron` 的 `develop` 分支选成 base 分支，将个人的 Fork 仓库的分支选成 compare 分支。

## 代码审查指南
将代码合并到 **java-tron** 的唯一途径是 **Pull Request (PR)**。
所有 PR 必须经过审查后才能合并。

### 审查流程
- 审查者需理解 PR 的动机和改动
- 对于缺少描述或改动过大的 PR，审查者可要求补充说明
- 审查者检查代码风格、功能完整性与测试情况
- 查者应保持礼貌、尊重并及时跟进

### 功能验证
- **Bug 修复 PR**
    - 审查者应尝试复现问题并验证修复
    - 推荐提交者提供单元测试：未改动时应失败，改动后应通过

- **功能新增 PR**
    - 审查者应尝试使用新功能并提出意见
    - 所有新增代码需提供单元测试

### 代码规范要求
- 使用代码规范工具检查代码
- 在提交前自测
- 通过标准化测试

CI 工具：

- Sonar：静态代码分析
- Travis CI：持续集成检查

所有检查通过后，维护者将审查并合并至 `develop`。

> **编码规范**
>- 遵循 [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
>- 所有 PR 必须基于 `develop` 分支

## 分支命名规范
1. `master` 和 `develop` 固定命名
2. 版本开发分支以版本号和版本名命名（如 `GreatVoyage-v4.8.0(Kant)`）
3. `hotfix/*`：用于紧急修复（如 `hotfix/typo`）
4. `feature/*`：用于新功能开发（如 `feature/new-resource-model`）

## Pull Request 规范
1. 一个 PR 只处理一件事
2. 避免超大改动量
3. 标题：简要描述 PR 目标
4. 描述：面向 Reviewer，详细说明
5. 明确需要反馈的部分

## Commit 描述规范
推荐格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit 类型
- `feat`：新功能
- `fix`：Bug 修复
- `docs`：文档修改
- `style`：格式调整（无功能更改）
- `refactor`：代码重构
- `test`：测试代码改动
- `chore`：其他（如任务分配等）

### Subject 规范
1. 不超过 50 个字符
2. 使用动词开头，第一人称现在时（如 `change` 而非 `changed`）
3. 首字母小写
4. 结尾不加句号
5. 避免无意义 Commit

示例
```
feat(block): optimize the block-producing logic

1. increase the priority for acquiring synchronization lock
2. add interruption exception handling in block-producing thread

Closes #1234
```
## 特殊情况处理
- **提交者未跟进**
    - 等待数日后联系；如无回应，可关闭 PR 或由他人继续
- **提交者在修复 Bug 时顺带重构**
    - 小范围可接受
    - 大范围改动需拆分为独立 PR，或至少独立 Commit
- **提交者拒绝反馈**
    - 审查者可关闭 PR

## 行为准则
请保持尊重和建设性，共同营造积极的社区氛围。




