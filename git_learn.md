# git的安装
<++>


```

ssh免密码登陆
那么push都只能用ssh模式（git@github.com），不能用https模式.
#检查是否已经配置过ssh key，如果没有私钥和公钥则没有配置过
ls -al ~/.ssh

#新建一个ssh key
ssh-keygen -t rsa -b 4096 -C "glimmmermail@163.com" # -b参数可以忽略 指定密钥位数，默认2048
#只要一直确认，不要给私钥密码登陆，太麻烦
#nvim id_rsa.pub将公钥中的内容添加到git仓库设置
选择setting -》 ssh and gpgkeys -》 new ssh key

验证
ssh -T git@github.com
#如果询问是否链接则确认即可。


github创建repo

git的全局环境配置（~/.gitconfig）
让github默认创建的分支为main
git config --global init.defaultBranch main 

#配置git户名及用户邮箱 （邮箱设置需要注意：要么不在github上的记录中，在的话要求设置为public否则无法上传代码）
git config --global user.email "glimmermail@163.com"
git config --global user.name "bbbglimmer"

git config --global --replace-all user.email "glimmermail@163.com"
git config --global --replace-all user.name "glimmer"


#配置git默认编辑器
git config --global core.editor nvim

#查看git配置参数及配置文件所在的位置
git config --list --show-origin

#查看git配置参数
git config --list

#查看git参数的值
git config <key>
git config --show-origin <key>


mkdir learngit
cd learngit

git init
touch README.MD

git add README.MD

git commit -m "first commit"

#查看当前的branch名称
git branch
#让当前分支重命名为main，如果设置了默认创建分支为main则可以忽略，否则系统会创建成master
git branch -m main
#如果之前已经定义过origin可能需要移除后重新添加git地址
git remote rm origin
git remote add origin git@github.com:bbbglimmer  # learngit/.git/config 中亦可以配置
git push -u origin main





```

<++>


git创建的用户名和邮箱号配置有什么用
远程仓库里需要记录这些提交记录是由谁来完成的；所以我们需要给本地的git设置用户名和邮箱，用于从本地仓库向远程仓库提交记录时，在远程仓库记录下这些操作是由谁来完成的。
首先，配置的用户名和邮箱对push代码到远程仓库时的身份验证没有作用，即不用他们进行身份验证；他们仅仅会出现在远程仓库的commits里。其次，按正常操作来说，你应该配置你的真实用户名和邮箱，这样一来在远程仓库的commits里可以看到哪个操作是你所为。最后，这个用户名和邮箱是可以随便配置的（不提倡），如果你配置的邮箱是github里真实存在的邮箱，则commits里显示的是这个邮箱对应的账号；如果配置的邮箱是一个在github里不存在的邮箱，则commits里显示的是你配置的用户名。


git怎么使用代理
通过在shell中设置全局代理
export export  ALL_PROXY="socks5://127.0.0.1:1086"
export http_proxy="http://127.0.0.1:1087"
export https_proxy="http://127.0.0.1:1087"

alias setproxy="export ALL_PROXY=socks5://127.0.0.1:1086" 
alias unsetproxy="unset ALL_PROXY"

通过在git全局配置中设置代理
http和https模式
git config --global http.proxy 'socks5://127.0.0.1:1087' 
git config --global https.proxy 'socks5://127.0.0.1:1087'
# 忽略服务器的ssl证书检查
git config --global http.sslVerify false

git config --global --unset http.proxy
git config --global --unset https.proxy

上述方法挂了全局代理，但是如果要克隆码云、coding等国内仓库，速度就会很慢。更好的方法是只对github进行代理，不会影响国内仓库：
git config --global http.https://github.com.proxy socks5://127.0.0.1:1080
git config --global https.https://github.com.proxy socks5://127.0.0.1:1080

ssh模式设置socks5代理
让ssh也使用代理（应该设置ALL_PROXY即可，不用设置这个，不确定）
nvim .ssh/config 或者~/.ssh/ssh_config
Host github.com
     HostName github.com
		 User git
     ProxyCommand nc -v -x 127.0.0.1:1086 %h %p



git clone后如何保持与原项目同步

如果你不是fork的项目的话：
git pull
即可。
如果你是fork的话，把原来的项目添加到：
git remote add ups [主项目地址]
然后：
git fetch ups && git merge ups/master



git clone depth=1 导致git push的时候报错：
提示了错误：shallow update not allowed
初步分析原因，提示的问题应该是浅拷贝，就是我们在git clone的时候，depth设置的太浅，没有全部的历史记录。
所以解决方法有3个
1）复制全部历史记录（与原来repo同步）然后再push
a 添加源库到本地github分支： git remote add github https://github.com/x/y.git
b 重新获取源库的数据: git fetch --unshallow github 或者
修改.git/config文件中的fetch = +refs/heads/master:refs/remotes/origin/master
为fetch = +refs/heads/*:refs/remotes/origin/*然后执行git fetch --all

c 强推git代码到自己的git服务器: git push -u origin master

2）直接删掉.git目录重新git init

3）由于已经提交了过多次并且不想丢失这些提交，可以使用
git filter-branch -- --all #这样就可以去掉克隆的提交的 grafted 标记了
然后就可以执行
git push -u origin master







