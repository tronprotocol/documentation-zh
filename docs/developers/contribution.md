## 成为波场社区开发者

波场是个全球的，开源的去中心化应用的平台。

非常感谢你帮助我们开发源代码！我们欢迎和感激来自互联网的任何人的贡献，即使是很小的漏洞修复！

GitHub是用来追踪议题，贡献代码、建议、特性请求、文档等。

如果你想参与波场开发，请遵循流程：fork，fix，commit，send a pull request (PR)，以供波场主要维护者审查并且合并到主分支。如果你想提交更复杂的改动，为了保证你的改动符合我们的项目需求或者使你的改动更有效，请先通过我们的通信频道与我们的核心开发者确认。

我们鼓励尽早提交PR，这样可以让其他社区开发者知道你在开发的议题。未开发完成的PR需要被标注“进行中”状态。

** 社区开发者频道 **
  
* [Gitter](https://gitter.im/tronprotocol/allcoredev)   

查看 [波场开发者激励政策](incentives.md)

## 如何参与波场文档的书写

我们有两个文档仓库：  
[英文文档](https://github.com/tronprotocol/documentation-EN)     
[中文文档](https://github.com/tronprotocol/documentation-ZH)     

我们使用MkDocs框架来构建我们的文档项目。文档使用Markdown语言书写，通过在YAML配置文件中配置文档路径。

你可以在/docs/文件夹下，修改、添加文档。

## 如何参与TIP书写

波场优化提议(TIPs) 描述了波场平台的标准，包括协议说明、客户端接口、合约标准等等。

TIPS仓库路径是：[https://github.com/tronprotocol/TIPs](https://github.com/tronprotocol/TIPs)

你提交的第一个TIP PR应该是最终TIP的一个草案，必须要符合我们要求的格式。我们会审核你提交的TIP，并且会为之分配一个编号。请确保在TIP页头中附上论坛的地址或者一个公开的GitHub议题地址来让用户进行讨论。    
请参考：[TIP模板](https://github.com/tronprotocol/TIPs/blob/master/template.md)


## 如何参与java-tron代码书写

java-tron仓库路径是：[https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)  

**分支介绍：**

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

**开发一个新功能**  
  
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

**修复线上漏洞**  
     
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

## 报告安全问题  

我们高度重视所有与波场项目安全有关的问题。我们非常感谢你帮助我们增强波场项目的安全性。  
  
请在这里报告安全有关的问题 [https://hackerone.com/tronfoundation](https://hackerone.com/tronfoundation)  

我们会从核心开发人员中委派一人跟进问题。首先，我们会确认问题的有效性并且确认问题所影响的版本。其次，我们会去排查是否还有相似的问题存在。最后，我们会修复问题，并发布新的版本。  

当我们收到你的报告后，我们会及时通知你我们的处理进度。我们有可能会需要你提供更详细的问题信息。   

如果你对问题的修改有好的建议，请提交一个PR。  