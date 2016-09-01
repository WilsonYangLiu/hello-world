## 初始化，内容在~/.gitconfig
git config --global user.name "WilsonYangLiu"
git config --global user.email "lweixin316@gmail.com"
git config --global color.ui auto

## 添加密钥，id_rsa 为私钥，id_rsa.pub 为公钥
ssh-keygen -t rsa -C "lweixin316@gmail.com"

## 将公钥的内容添加到 Github 中
cat ./.ssh/id_rsa.pub

## GitHub 进行认证和通信
ssh -T git@github.com

## 举个栗子
git clone git@github.com:WilsonYangLiu/hello-world.git
cd hello-world/

git status

git add hello-world.py
git commit -m "Add hello world script by python"

git log

git push
