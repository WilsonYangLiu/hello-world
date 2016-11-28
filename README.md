# Hello would ![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg) ![License](https://img.shields.io/badge/license-MIT%20License-blue.svg)

1. 初始化，内容在~/.gitconfig

	git config --global user.name 'Wilson--Liu'  
	git config --global user.email '----@gmail.com'  
	git config --global color.ui auto  

2. 添加密钥，id_rsa 为私钥，id_rsa.pub 为公钥

	ssh-keygen -t rsa -C "----@gmail.com"

3. 将公钥的内容添加到 Github 中

	cat ./.ssh/id_rsa.pub

4. GitHub 进行认证和通信

	ssh -T git@github.com

5. 举个栗子

	git clone git@github.com:WilsonYangLiu/hello-world.git  
	cd hello-world/

	git status

	git add hello-world.py  
	git commit -m "Add hello world script by python"

	git log

	git push
