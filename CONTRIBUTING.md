# 贡献指南

感谢您抽出时间为 java-tron 的中文文档做出贡献。

无论您是修复错别字、更新过时信息还是添加新的教程，任何规模的贡献我们都表示欢迎和感谢。本指南旨在帮助您顺畅、轻松地提交贡献。

**注意**：由于本项目结构简单，我们目前仅维护 `master` 分支，不采用诸如 `develop` 或 `release` 分支策略等复杂的 Git 工作流。


## 如何贡献

### 报告问题 (Reporting Issues)

如果您在阅读文档时发现错误、失效链接或表述不清，请通过 Issues 告知我们。

1.  在提交 Issue 之前，请先搜索[已有的 issues](https://github.com/tronprotocol/documentation-zh/issues?q=is%3Aissue%20state%3Aclosed%20OR%20state%3Aopen) 以避免重复。
2.  对于简单的错别字或格式问题，我们建议直接通过 Pull Request 提交修复。
3.  对于其他内容问题，请清楚地描述您遇到的问题以及您预期的文档表述方式。
    * Ask a question

      欢迎随时提问任何与 `documentation-zh` 相关的问题，以解决您的疑惑。请在 GitHub Issues 中点击 **Ask a question**，并使用 [Ask a question](.github/ISSUE_TEMPLATE/ask-a-question.md) 模板。
    * Report an error

      如果您认为在 `documentation-zh` 中发现了错误，请在 GitHub Issues 中点击 **Report an error**，并使用 [Report an error](.github/ISSUE_TEMPLATE/report-an-error.md) 模板。
    * Request a feature

      如果您对 `documentation-zh` 有任何好的内容建议，请在 GitHub Issues 中点击 **Request a feature**，并使用 [Request a feature](.github/ISSUE_TEMPLATE/request-a-feature.md) 模板。

### 提交修改

如果您想修改文档，请遵循以下步骤。

* **Fork 仓库**

  访问 [tronprotocol/documentation-zh](https://github.com/tronprotocol/documentation-zh/) 并点击 **Fork**，在您的 GitHub 账号下创建一个 fork 仓库。

* **搭建本地环境**

  将您的 fork 仓库克隆到本地，并将官方仓库添加为 **upstream**。
    ```bash
    git clone https://github.com/yourname/documentation-zh.git

    cd documentation-zh

    git remote add upstream https://github.com/tronprotocol/documentation-zh.git
    ```

* **同步与修改**

  在进行新的修改之前，请将本地的 `master` 分支与上游仓库同步，并更新到您的 fork 仓库。
    ```bash
    git fetch upstream
    # `--no-ff` 表示关闭默认的快进合并模式
    git merge upstream/master --no-ff
    git push origin master
    ```

  创建一个新的分支进行修改。
    ```bash
    git checkout -b branch_name master
    ```

* **提交与推送**

  编写修改并在完成后提交新代码。
     ```bash
     git add .
     git commit -m '提交说明'
     ```

  将新分支推送到您的 fork 仓库。
     ```bash
     git push origin branch_name
     ```

* **提交 Pull Request (PR)**

  从您的 fork 仓库向 `tronprotocol/documentation-zh` 提交一个 Pull Request。请选择 `tronprotocol/documentation-en` 的 `master` 分支作为 **base branch**（目标分支），并选择您 fork 仓库中的对应分支作为 **compare branch**（比较分支）。

## 常见问题 (FAQ)

**问：我没有看到 `develop` 分支。我应该把 PR 提交到哪个分支？** 答：请直接将 PR 提交到 `master` 分支。审核通过后将会被合并。

**问：我想重写一个大的章节。可以直接提交 PR 吗？**

答：我们建议先开一个 Issue 来描述您的想法，在开始工作前确认方向。这有助于避免徒劳无功。

**问：我的修改多久会被合并？**

答：维护者会尽量在 3 个工作日内处理 PR。简单的错别字修复通常会合并得很快。

---

再次感谢您的贡献！
