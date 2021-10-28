# ranger+fzf 终端文件管理器+模糊搜索
  ## ranger 的安装
```zsh
brew install ranger
```

  ## ranger配置文件的导出
ranger 默认没有导出配置文件，需要命令导出,all(导出全部)
```zsh
ranger --copy-config=all
creating: /Users/glimmer/.config/ranger/rifle.conf
creating: /Users/glimmer/.config/ranger/commands.py
creating: /Users/glimmer/.config/ranger/commands_full.py
creating: /Users/glimmer/.config/ranger/rc.conf
creating: /Users/glimmer/.config/ranger/scope.sh

> Please note that configuration files may change as ranger evolves.
  It's completely up to you to keep them up to date.

> To stop ranger from loading both the default and your custom rc.conf,
  please set the environment variable RANGER_LOAD_DEFAULT_RC to FALSE.
  
```
  
  
  ## 修改环境变量，声明不使用ranger的默认配置
`echo "export RANGER_LOAD_DEFAULT_RC=FALSE">> ~/.zshrc` 
  ## 设置ranger的默认编辑器为neovim
`echo "export EDITOR='nvim'">> ~/.zshrc` 


  ## ranger配置文件介绍
```
/Users/glimmer/.config/ranger/rifle.conf          打开哪个文件用哪个应用程序，就是默认打开方式
/Users/glimmer/.config/ranger/commands.py         命令，可以自己修改添加
/Users/glimmer/.config/ranger/commands_full.py    
/Users/glimmer/.config/ranger/rc.conf             主要配置文件,主要配置内容，改键，快捷方式等
/Users/glimmer/.config/ranger/scope.sh            预览脚本，表示pdf video 图片等的预览方式设置
```

  ## ranger的常规使用
```
  zh 和 ctrl h (back删除按键亦可以)表示显示或者隐藏文件
  r  表示打开该文件的方式(open with)，可以通过数字选择打开方式
  R  文件内容修改或者变动后重载内容
  [] 左右中括号，在上级文件夹之间切换
  shift h 在历史记录文件夹当中上翻
  shift l 在历史记录中下翻
  g   跳转，按g可以查看所有设置的跳转（g for jump）
      gi  跳到github文件夹
      gh  跳到home目录
      ge  跳到etc目录
  o   表示排序方式 s 文件大小排序 c 修改日期排序 n 文件名排序 atime最后一次访问时间 ctime 文件属性权限变化（改变时间）  mtime文件修改时间
  /   :search   查找文件
  n N 查找文件的下一个和上一个（默认） 可以考虑自定义为=和-
  f   :scout -ftsea xxx  显示含有xxx的文件(这个是自定义),默认通过为zf过滤 比/查找文件更好用
  shift s  让终端真正进入某个文件夹
  q   退出ranger （可能还有别的快捷按键）
  
  ctrl f (自定义按键)fzf插件，查找要查找的文件，确认即跳到该文件目录下并展示
  yp  复制选定的文件的路径
  yn  复制文件名
  a.  复制去掉后缀的文件名
  
  shift v (自定义按键) 创建文件,如 :shell vim hello.py
  M   (自定义快捷键) :mkcd
  shift 1 调用shell
  cw  (自定义快捷键bulkrename快捷方式)重命名快捷键change word 表示:rename 
      bulkrename   多文件编辑名字
  
  a   重命名，在文件名字后边修改
  I   重命名，在开头处修改
  A   重命名，在文件类型后边修改
  
  v    全部选中
  空格 选中当前指定的文件
  
  yy 复制文件
  pp 粘贴文件 如果重复粘贴ranger会在重复文件后加下划线
  po 黏贴文件，如果有重复名字的文件则覆盖
  dd 剪切文件
  dD 删除文件或者文件夹
  w  进入ranger的任务管理器,按dd可以取消指定的任务
  
  dU 或者du 查看文件夹大小
  
  C  (自定义快捷按键) 压缩:compress  rar貌似有问题
  yy shift x 表示解压缩，意思是必须先复制要解压的文件，然后再执行解压。否则在原文件上解压 必须如此操作
  
  cp  (自定义快捷按键)让md文件转换为pdf
  
  ydv （自定义快捷按键）复制链接，ydv，粘贴链接，确认，可以下载youtube视频
  
  :help  帮助，按k表示查看所有快捷键
```  

  tu  新建ranger标签
  th  跳到上一个标签
  tl  跳到下一个标签
  预览文件如何快捷键浏览
  ctrl+e 上滚预览文件map <c-e> scroll_preview 5
  ctrl+u 下滚预览文件map <c-u> scroll_preview -5

  ## ranger插件plug的安装
  以cdump/ranger-devicons2（为文件类型添加图标）为例子
  [ranger-devicons](https://github.com/cdump/ranger-devicons2) 
  ```
1.Install a Nerd Font compatible font or patch your own, then set your terminal font

Clone:

2.git clone https://github.com/cdump/ranger-devicons2 ~/.config/ranger/plugins/devicons2
3.Add/change in your ~/.config/ranger/rc.conf 
default_linemode devicons2 

  ```

  ## ranger的自定义配置
  ranger添加自定义函数（添加到commands.py中）
  ```
  #如mkcd命令，创建文件夹并且进入该文件夹
  #可以在wiki custom commands找到相应推荐的命令,添加到commands.py中即可.
  推荐fzf_select 快速查找文件 compress extracthere 压缩解压缩 插件
  ```

  
  
  ### rc.conf文件上的一些配置
  1.对mkcd文件设置快件按键  
  2.fzf_select设置快件按键  
  3.快速查找快捷键  
  4.压缩解压缩快捷键  
  3.set vcs_aware true 让git信息显示，打勾表示已经同步，加号表示修改了，问号表示还没有追踪   
  
  
  ### 图片的预览
  查看ranger wiki里边的介绍,不同的系统操作不一样
  [图片预览设置](https://github.com/ranger/ranger/wiki/Image-Previews) 
  iterm2上图片预览设置
  ```
Add the following lines to your ~/.config/ranger/rc.conf:
    set preview_images true
    set preview_images_method iterm2
Restart ranger and navigate to an image file. \o/
  ```

  
  ### 视频pdf及其他文件的预览
  ```
  1.在scope.sh中设置
  2.找到handle_image()
  3.取消视频、pdf及相关文件的预览方式的注释
  ```

  
  
  ### youtube视频的下载
  ` brew install youtube-dl `
  在rc.conf中设置
  ```
  map ytv console shell youtube-dl -ic%space
  map yta console shell youtube-dl -xic%space
  ```

  
  
  ## ranger在macos上的使用
  macos中使用ranger查看文件夹大小会报错，如下,需要修改rc.conf
  ```
  du: illegal option -- -
usage: du [-H | -L | -P] [-a | -s | -d depth] [-c] [-h | -k | -m | -g] [-x] [-I mask] [file ...]
(END)
  
  
  # External Programs
map du shell -p du --max-depth=1 -h --apparent-size
map dU shell -p du --max-depth=1 -h --apparent-size | sort -rh

替换为命令du -shc *  用以表示统计当前文件夹下的文件及文件夹的各自大小及统计大小。替换如下：
#按名称排列，由a-z
map du shell -p du -shc *
#按文件大小顺序排列，由大到小
map dU shell -p du -shc * | sort -rh
  ```
  ## 让ranger重新打开时保持在上次打开的目录中
  ```
  alias ra='ranger --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"'
  ```

    
    
    
***
***
    
    
  # fzf的安装及在vim和ranger内的配置
  ### fzf的安装
  
  ```
  brew install fzf
  ```
  ### 安装the_silver_searcher允许文档查询及文本内容快速查询，命令为ag，fzf默认使用的为fd，所以还需要在fzf.zsh中修改，除此还可以考虑使用另外一个ripgrep(rg命令)  
  ```
  brew install the_silver_searcher
  ```

  
  ### 在安装完fzf后会提示安装fzf-completion以支持命令补全,执行下面的命令
  ```
  /usr/local/opt/fzf/install
  
  #执行完后会自动生成相应脚本，如需修改可在下面脚本中注释相应功能
  ~/.fzf.zsh
  ```


  ### 安装ccat以便支持查找过程代码高亮
  ```
  brew install ccat
  ```


  ### 终端zsh中使用fzf
  编辑fzf.zsh文件作为fzf在终端中的配置文件，
  并引入fzf.zsh配置文件到.zshrc中
  ```
  
  source /Users/glimmer/.oh-my-zsh/.fzf.zsh
  ```
  将fzf文件夹放到fzf.zsh所在目录中(fzf文件夹中包括相应文件的fzf相关命令,会在fzf.zsh中使用到部分，大部分没用)
  

  ### ranger中使用fzf
  在ranger的命令文件commands.py中添加fzf的命令。
  ```

class fzf_select(Command):
    """
    :fzf_select

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        import os.path
        if self.quantifier:
            # match only directories
            command = "find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -type d -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"

        else:
            # match files and directories
            command = "find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"

        fzf = self.fm.execute_command(command,
                                      universal_newlines=True,
                                      stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)


  ```

  在ranger的配置文件rc.conf中设置,通过ctrl+f在ranger中激活fzf。
  ```
  map <C-f> fzf_select
  ```


  ### vim中使用fzf
  安装fzf.vim让fzf支持在vim中使用
  
  在.vimrc中的vim-plug中添加插件
  ```
  Plug 'junegunn/fzf.vim'
  ```
  ```
  #设置fzf.vim的相应配置,如下



" ===
" === FZF
" ===
set rtp+=/usr/local/opt/fzf
" nnoremap <c-p> :Leaderf file<CR>
" noremap <silent> <C-p> :Files<CR>
noremap <C-p> :FZF<CR>
noremap <C-f> :Ag<CR>
"noremap <silent> <C-h> :MRU<CR>
noremap <C-t> :BTags<CR>
"noremap <silent> <C-l> :LinesWithPreview<CR>
noremap <C-l> :Lines<CR>
noremap <C-b> :Buffers<CR>
noremap q; :History:<CR>

"noremap <silent> <C-f> :Rg<CR>
"noremap <silent> <C-h> :History<CR>
""noremap <C-t> :BTags<CR>
"" noremap <silent> <C-l> :Lines<CR>
"noremap <silent> <C-w> :Buffers<CR>
"noremap <leader>; :History:<CR>

let g:fzf_preview_window = 'right:60%'
let g:fzf_commits_log_options = '--graph --color=always --format="%C(auto)%h%d %s %C(black)%C(bold)%cr"'

function! s:list_buffers()
  redir => list
  silent ls
  redir END
  return split(list, "\n")
endfunction

function! s:delete_buffers(lines)
  execute 'bwipeout' join(map(a:lines, {_, line -> split(line)[0]}))
endfunction

command! BD call fzf#run(fzf#wrap({
  \ 'source': s:list_buffers(),
  \ 'sink*': { lines -> s:delete_buffers(lines) },
  \ 'options': '--multi --reverse --bind ctrl-a:select-all+accept'
\ }))

noremap <c-d> :BD<CR>

let g:fzf_layout = { 'window': { 'width': 0.9, 'height': 0.8 } }

  ```
  
  ### fzf模糊搜索的基本使用及快捷键
  1.终端中的使用  
  在终端中通过输入 cd \ 按tab按键激活
  或者
  在vim中通过输入  vim \ 按tab按键激活
  或者通过命令fzf激活
  
	control+p 在终端中触发路径查找
	control+t 在终端中查找文件夹并且进入该文件夹
	control+r 在终端中查找历史记录


  2.ranger中使用fzf
  在ranger中通过快捷键ctrl+f激活fzf
  
  3.vim中使用fzf
  ```
  
"搜索文件
noremap <C-p> :FZF<CR>
"搜索文本内容
noremap <C-f> :Ag<CR>
"查找打开过的文件
noremap  <C-h> :MRU<CR>
"标签查找
noremap <C-t> :BTags<CR>
"文本内容查找
noremap <C-l> :Lines<CR>
"查找缓冲区内容
noremap <C-b> :Buffers<CR>
"查找执行过的命令
noremap q; :History:<CR>
"ctrl+d查看在vim终端中打开的文档，选中确认则关闭
noremap <c-d> :BD<CR>
  ```



