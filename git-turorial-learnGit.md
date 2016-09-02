# Git turotial

## Chapter 1

#### 1. 创建并初始化仓库  

	mkdir git-turorial
	cd git-turorial/
	git init

#### 2. 查看仓库的状态  

	git status

#### 3. 例子：添加文件  

	touch README.md
	git status
	git add README.md
	git status
	git commit -m "First commit"

#### 4. 文件中添加内容  

	vi README.md
	git status
	git add README.md
	git status
	git commit
	
#### 5. 查看提交日志 

	git log
	git log --pretty=short
	git log README.md
	git log -p README.md

#### 6. 查看更改前后的差别，即工作树、暂存区、最新提交之间的差别  

	vi README.md
	
	# 工作树与暂存区的差别
	git diff
	
	# 工作区与最新提交之间的差别
	git add README.md
	git diff HEAD
	git commit -m "Add index"

## Chapter 2

#### 1. 创建分支  

	git checkout -b feature-A
	git branch
	git add README.md
	git commit -m "Add feature-A"

#### 2. 合并分支  

	git checkout master
	git merge --no-ff feature-A
	git log --graph

#### 3. 历史版本回溯  

	git reset --hard [回溯到feature-A创建前，值填写对应的哈希值]
	git checkout -b fix-B
	vi README.md
	git add README.md
	git commit -m "Fix-B"

	git reflog
	git checkout master
	git reset --hard [推进历史到feature-A合并后的状态，填写从git reflog中对应状态的哈希值]

	git merge --no-ff fix-B

	# 有冲突，编辑文档解决冲突
	vi README.md
	git add README.md
	git commit -m "Fix conflict"

#### 4. 修改 commit 提交信息

	git commit --amend
	git log --graph

#### 5. Here has an error. [status: fixed]  

	git checkout -b feature-C
	git commit -am "Add feature-C"
	
	# 修正错误
	vi README.md
	git diff
	git commit -am "Fix typo"
	git log --graph

	# 更改历史
	git rebase -i HEAD~2
	git log --graph

	git checkout master
	git merge --no-ff feature-C
	git log --graph

#### 6. 推送到远程仓库

	git remote add origin git@github.com:WilsonYangLiu/git-turorial.git
	git push -u origin master

	git checkout -b feature-D
	git push -u origin feature-D

#### 7. 从远程仓库获取

[I am programer B! I'll add something]  

	git clone git@github.com:WilsonYangLiu/git-turorial.git
	git branch -a 

	git checkout -b feature-D origin/feature-D
	vi README.md
	git commit -am "Add feature-D"

	git push

[I am programer A!]

	# in any branch. Here i am in master!
	git pull origin feature-D
	git log --graph
