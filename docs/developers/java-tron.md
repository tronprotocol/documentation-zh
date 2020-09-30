# Java-tron

java-tron仓库路径是：[https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)

<h2>分支介绍</h2>

``master``分支：
这个分支包含最近发布到生成环境的代码，并通过Tag进行标注release版本号，这个分支只能从其他分支合并，不能在这个分支直接修改。

``develop``分支：
这个分支是我们的主开发分支，包含所有要发布到下一个release的代码，这个分支只能从其他分支合并，不能在这个分支直接修改。

``feature``分支：
这个分支主要是用来开发一个新的功能，基于``develop``分支创建，一旦开发完成，就会将其合并回``develop``分支，并将其删除。

``release``分支：
预发布分支，当你需要发布的时候，基于``develop``分支创建一个release分支，允许小修复和最终版本元数据（版本号等）修改，从``develop``分支到``release``分支的关键点是开发完成反映新版本的期望状态。至少合并了所有针对要发布的功能，针对未来版本的所有功能不会被合并-他们必须等到Release分支创建完成后才可以被合并。完成release后，将其合并到``master``分支（需要打Tag）和``develop``分支，并将其删除。上线前最后的测试将在这个分支进行。

``hotfix``分支：
当我们在``master``分支发现bug的时候，需要基于``master``分支创建一个hotfix分支，完成hotfix后，将其合并到``master``分支（当做一个新的release）和``develop``分支，并将其删除。

<h2>开发一个新功能</h2>

当你开始开发新功能时，从``develop``分支创建一个feature分支，分支需要位于``origin/feature``下。
```text
$ git checkout -b feature/my-feature develop
# 切换到新分支'feature/my-feature'
```
完成的新功能将被合并到Develop分支，以便未来合并到Master分支。
```text
$ git commit -a -m "Bumped version number to 3.1.4"
# 提交
$ git checkout develop
# 切换到分支'develop'
$ git pull
# 更新分支
$ git checkout feature/my-feature
# 切换到分支'feature/my-feature'
$ git merge develop
# 合并分支'develop'，有冲突解决冲突
$ git push
# 提交代码到GitHub
# 在GitHub网站上发起一个Pull Request等待自动化检查和相关人员审核，合并成功后继续下面流程
$ git branch -d feature/my-feature
# 删除开发完成后的功能分支'feature/my-feature'
# 在GitHub网站上，同样删除分支'feature/my-feature'
```

<h2>修复线上漏洞</h2>

当你发现一个发布版的Bug时，从``master``分支（此时应该是最新release代码）创建一个hotfix分支，分支需要位于``origin/hotfix``下。
```text
$ git checkout -b hotfix/my-hotfix master
# 切换到新分支'hotfix/my-hotfix'
# 修改版本号
$ git commit -a -m "Bumped version number to 3.1.4"
# 提交
```

当修复完Bug后，需要将Hotfix分支合并到Master分支和Develop分支.
```text
$ git checkout master
# 切换到分支'master'
$ git pull
# 更新
$ git checkout hotfix/my-hotfix
# 切换到分支'hotfix/my-hotfix'
$ git merge master
# 合并Master分支代码，解决冲突后
$ git push
# 提交到GitHub，然后通过GitHub发起一个Pull Request等待自动化检查和相关人员审核，合并成功后继续下面流程
# 通过GitHub对Master分支代码打Tag

$ git checkout develop
# 切换到分支'develop'
$ git pull
# 更新
$ git checkout hotfix/my-hotfix
# 切换到分支'hotfix/my-hotfix'
$ git merge develop
# 合并Develop分支代码，解决冲突后
$ git push
# 提交到GitHub，然后通过GitHub发起一个Pull Request等待自动化检查和相关人员审核，合并成功后继续下面流程

$ git branch -d hotfix/my-hotfix
# 本地删除分支
# 在GitHub网站上，同样删除分支'feature/my-hotfix'
```

最后，请提交一个PR。

补充说明：如果你开发了新功能，请确保你在``/src/test``目录中添加了测试用例。
