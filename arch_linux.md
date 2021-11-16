# arch linux 的安装

## 1.镜像的下载和启动盘的设置

### A.下载地址  
https://wiki.archlinux.org/title/Installation_guide  
https://archlinux.org/download/
### B.iso镜像校验  
```
brew install gnupg
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 4AA4767BBC9C4B1D18AE28B77F2D434B9741E8AC
gpg --search-keys 4AA4767BBC9C4B1D18AE28B77F2D434B9741E8AC
gpg --keyserver-options auto-key-retrieve --verify archlinux-2021.10.01-x86_64.iso.sig
gpg --auto-key-locate clear,wkd -v --locate-external-key pierre@archlinux.de
```  

### C.启动盘的制作
macos上制作启动盘,要先卸载u盘
```
diskutil list
sudo diskutil umount /dev/disk2s
diskutil list
刻录镜像到u盘 注意这里的rdisk2即为disk2，r带上是为了提高速度，表示裸设备
sudo dd if=/Users/glimmer/Downloads/archlinux-2021.10.01-x86_64.iso/archlinux-2021.10.01-x86_64.iso of=/dev/rdisk2 bs=1m
diskutil list
推出设备
diskutil eject /dev/disk2
```

## 2.安装
### A.安装前的一些设置  
进入arch linux启动盘后在选择安装选项时按e可以编辑特定选项（非必须），如屏幕分辨率，如：
nomodeset video=800****450

进入arch linux后设置字体大小（非必须），如
setfont /usr/share/kbd/consolefonts/LatGrkCyr-12*22.psfu.gz

设置esc和capslock按键互换(更改键位),
```

vim keys.conf
keycode 1 = Caps_Lock
keycode 58 = Escape
#执行命令
loadkeys keys.conf

```

### B.查看网络链接     
安装arch linux需要互联网链接  
  
```
#查看网络链接  
ip link

#开启无限网络链接
ip link set wlan0 up

#扫描无线网络(亦可以使用wifi-menu，不过可能已经不在安装包里，wifi-menu不支持企业级协议**** 不支持wpa2)
iwlist wlan0 scan

#查看ESSID
iwlist wlan scan | grep ESSID

#通过wpa_passphrase命令来输入wifi网络密码(支持企业级协议)
wpa_passphrase 网络 密码 > 文件名

#通过配置文件链接网络(并运行在后台)
wpa_supplicant -c 文件名 -i  wlan0 & 

#需要获取动态分配的ip地址，否则没拿到ip无法链接网络
dhcpcd &

#测试网络
ping baidu.com

#设置时间同步(通过systemd-timesyncd，经常断网的情况可以考虑使用chrony,不过要安装下载并配置服务，详情可看archlinux wiki)
timedatectl set-ntp true

#此命令会启用2个服务systemd-timesyncd(用于ntp时间同步) systemd-timedated(只在timedatectl命令使用时启用)
前者的配置文件在/etc/systemd/timesyncd.conf 不配置会使用默认的时间服务器同步时间
查看状态
timedatectl status
timedatectl show
timedatectl show-timesync --all
timedatectl timesync-status
#设置硬件时钟为utc (rtc no 即为utc)
timedatectl set-local-rtc 0
#以系统时间为基准，修改硬件时间
sudo hwclock --systohc
```

### C.磁盘及分区设置  

```   
#查看分区情况
fdisk -l

#对特定磁盘做分区
fdisk /dev/xxx
#m 帮助
#p 打印分区情况
#g 创建空白gpi（efi）分区表
#o 创建空白mbr分区
#n 创建分区
#w 保存分区信息

#根据引动类型创建分区
ls /sys/firmware/efi/efivars 
如果命令结果显示了目录且没有报告错误，则系统以 UEFI 模式引导。 如果目录不存在，则系统可能以 BIOS 模式 (或 CSM 模式) 引导。如果系统未以您想要的模式引导启动，请参考您的主板说明书。  

#gpi（uefi）需要至少三个分区
n
/boot 1024M 即最好设置1G大小
/swap 如果开启休眠，8g以内内存的2倍，64g以内内存的1.5倍，64g以上不建议使用休眠
      如果没有开启休眠，8g以内跟内存一样大小，8g以上则设置为8g，64g以上设置为16g
/root 剩余的所有空间
/home 设置家目录，重装的时候保留，避免要备份数据


#mbr需要至少2个分区
/swap 如果开启休眠，8g以内内存的2倍，64g以内内存的1.5倍，64g以上不建议使用休眠
      如果没有开启休眠，8g以内跟内存一样大小，8g以上则设置为8g，64g以上设置为16g
/root 剩余的所有空间
/home 设置家目录，重装的时候保留，避免要备份数据

#分区完成后记得保存
p  
w

#设置分区的文件格式并启用
mkfs.fat -F32 /dev/xxx1   #注意有些分区格式必须是fat32，比如你想装windows和linux共存的情况，而macos则为hfs+
mkfs.ext4 /dev/xxx1       #linux分区一般为ext4
mkswap /dev/xxx2          #设置交换分区
swapon /dev/xxx2          #设置交换分区
  
``` 
    
### D.配置pacman的更新源    

```
vim /etc/pacman.conf
#取消掉Color的注释
#Color   #安装程序时候提示报告用彩色显示

vim /etc/pacman.d/mirrorlist
#将中国大陆的服务器放到最前边
#注意这里有多个

```

### E.挂载系统盘，方便从原来的u盘上的根目录切换到系统盘上的根目录  

```
mount /dev/xxxroot /mnt       #挂载根目录
ls /mnt    #检查是否为空
mkdir /mnt/boot
mount /dev/xxxboot /mnt/boot  #挂载boot目录

```

### F.pacstrap脚本安装arch 的基础软件 linux内核 linux固件到/mnt目录中   
`pacstrap /mnt base linux linux-firmware base-devel` 

### G.生成系统的挂载文件,让系统重启后自动挂载  
`genfstab -U /mnt >> /mnt/etc/fstab ` 

### H.切根配置及安装软件  
```
#切根
arch-chroot /mnt

#设置时区
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#同步系统时间
hwclock --systohc
以生成 /etc/adjtime
这个命令假定已设置硬件时间为 UTC 时间

#切根，配置本地化
exit   #切换回u盘根目录,因为新装的系统无法使用vim
vim /mnt/etc/locale.gen #取消注释
#en_US.UTF8 UTF-8
arch-chroot /mnt
locale-gen             #生成本地化文件

#语言配置
exit
vim /mnt/etc/locale.conf
LANG=en_US.UTF-8

#设置系统键盘布局
vim /mnt/etc/vconsole.conf
keycode 1 = Caps_Lock
keycode 58 = Escape

#配置主机名
vim /mnt/etc/host
archglimmer

vim /mnt/etc/hosts
127.0.0.1 localhost
::1 localhost
127.0.0.1 archglimmer.localdomain archglimmer


#更改系统密码
arch-chroot /mnt
passwd

#安装grub引导，方便安装多个系统
pacman -S grub efibootmgr intel-ucode os-prober  #注意intel-ucode如果为amd芯片要换成amd-ucode ，refind亦可以替代grub，不过需要uefi支持， os-probe用于在电脑上寻找其他操作系统 注意如果是mbr则只需要grub ucode，按需要安装os-prober

mkdir /boot/grub
#生成grub配置
grub-mkconfig > /boot/grub/grub.cfg
或者
grub-mkconfig -o /boot/grub/grub.cfg

uname -r
#如果引导是gpt（uefi）
grub-install --target=x86_64-efi --efi-dirctory=/boot
#如果引导是mbr，sda为整个硬盘名
grub-install --target=i386-pc /dev/sda


#安装需要的基础软件，其中wpa_supplicant用于上网，dhcpcd用于获取dhcp分配的地址
pacman -S neovim vi zsh wpa_supplicant dhcpcd

#退出系统
exit

#关闭指定程序
killall spa_supplicant dhcpcd
#还可能需要取消挂载
umount -R /mnt

#重启
reboot

```


## 3.系统的配置及软件的安装
  
### A.更新系统
`pacman -Syyu` 

### B.安装软件
```
#base-devel中包含很多基础命令，如sudo sed which等
pacman -S man base-devel
```


### C.添加用户并设置其用户组为wheel  
（wheel组可以使用所有命令，其他则不可以使用su命令）

```
#m,参数创建用户目录，G参数设置其用户组
useradd -m -G wheel glimmer
#创建用户密码
passwd glimmer
```

visudo 默认编辑sudo文件的命令，其通过vi对sudo进行编辑，可以修改编辑器，让其默认使用nvim
mv /usr/bin/vi /usr/bin/vi.backup
ln -s /usr/bin/nvim /usr/bin/vi

visudo 修改sudo文件，让wheel组可以操作所有命令,让glimmer用户可以执行sudo命令
删掉前边的注释
```
# %wheel ALL=(ALL) ALL
```
sudo文件亦可以设置用户执行sudo命令免密码

### D.安装显示服务器
显示服务器是任何图形用户界面（尤其是窗口系统）中的关键组件。它是图形用户界面（GUI）的基本组件，位于图形界面和内核之间。因此，借助显示服务器，您可以将计算机与GUI一起使用。没有它，您将只能使用命令行界面。
显示服务器有xorg或者wayland
以xorg为例
```
sudo pacman -S xorg xorg-server
```

### E.安装桌面环境
Gnome kde xfe xfce  dde deepin bspmw(加tiling)等为桌面环境 
窗口管理器有i3 dwm（动态窗口管理器） openbox（只支持特定桌面）等，其没有桌面环境desktop environment 即DE，仅有wm windows manager。
登陆管理器有xdm sddm lightdm等，其作用仅仅只是在你开机后，让你输入用户名和密码登陆，然后引导进入桌面，至此任务完成，之后就交给kde或i3，dwm管理桌面了。你可以不需要DM，直接通过startx脚本命令进入桌面。


以国人的deepin深度桌面为例
```
sudo pacman -S deepin deepin-extra
#安装displaymanager 显示管理器（登陆管理器）
#检查deepin是否已经包含lightdm ，默认自带
pacman -Qs lightdm
vim /etc/lightdm/lightdm.conf
#取消注释
#greeter-session=example-gtk-gnome
#将内容改成
greeter-session=lightdm-deepin-greeter

#通过systemd让系统开机启动lightdm
systemctl enable lightdm
systemctl start lightdm

```

### F.安装AUR帮助工具和配置字体，安装其他软件

AUR  

AUR的全称是Arch User Repository,使用它可以在Arch Linux/Manjaro系统中安装和更新软件包。
AUR是Arch Linux/Manjaro用户的社区驱动存储库，创建AUR的目的是使共享社区包的过程更容易和有条理，它包含包描述（PKGBUILDs），允许使用makepkg从源代码编译包，然后通过pacman安装它。
AUR 中的包是以 PKGBUILD 的形式存在的，需要手动过程来构建。

yay  

Yay是用Go编写的Arch Linux AUR帮助工具，它可以帮助你以自动方式从PKGBUILD安装软件包， yay有一个AUR Tab完成，具有高级依赖性解决方案，它基于yaourt、apacman和pacaur，同时能实现几乎没有依赖、为pacman提供界面、有像搜索一样的yaourt、最大限度地减少用户输入、知道git包何时升级等功能。  
要从PKGBUILD构建包，请使用以下命令(不推荐使用这种方法，因为可能有部分包无法下载，建议使用中文社区仓库)： 
```
pacman -S git
git clone https://aur.archlinux.org/yay.git --depth=1
cd yay
makepkg -si
```

这将安装在你的系统上并从下载的repo文件构建yay包。
或者如果安装了中文社区仓库可以使用以下命令  
`pacman -S yay
`   
可能安装回有报错，那么（未见有此情况）  
`sudo pacman -S fakeroot make  
`  
#从pacman中查询安装了的软件   

`pacman -Qs yay
`  
  



使用arch linux中文社区仓库安装yay  

```
sudo vim /etc/pacman.conf
#添加内容
[archlinuxcn]
Server = https://repo.archlinuxcn.org/$arch
Server = https://opentuna.cn/archlinuxcn/$arch
Server = https://mirrors.163.com/archlinux-cn/$arch
Server = https://mirrors.aliyun.com/archlinuxcn/$arch

sudo vim /etc/pacman.d/mirrorlist
#添加镜像
Server = http://mirrors.163.com/archlinux/$repo/os/$arch
Server = http://mirrors.dgut.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.dgut.edu.cn/archlinux/$repo/os/$arch
Server = http://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

之后安装 archlinuxcn-keyring 包以导入 GPG key。安装 archlinuxcn-mirrorlist-git 包可以获得一份镜像列表，以便在 pacman.conf 中直接引入。
sudo pacman -Syy
sudo pacman -Syu
sudo pacman -S archlinuxcn-keyring
sudo pacman -S archlinuxcn-mirrorlist-git

然后执行
pacman -S yay
```



#通过yay安装程序  
```
yay -S google-chrome
yay -S chromium
# chrome的flash支持
pepper-flash
yay -S bc
```  
  

#推荐软件tlp，电池管理软件，可以设置电池管理策略  
TLP 提供优秀的 Linux 高级电源管理功能,不需要您了解所有技术细节。默认配置已经对电池使用时间进行了优化，只要安装即可享受更长的使用时间。除此之外，TLP 也是高度可配置的，可以满足您的各种特定需求。
配置可查看https://wiki.archlinux.org/title/TLP_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)  但东芝的硬件不支持，所以没有装
`yay -S tlp
`  
电池管理器还有一个xfce4-power-manager（dwm需要这个在autostart脚本中启动）
`sudo pacman -S xfce4-power-manager`   
电池管理还需要一个acpi，acpitool工具（dwm的autostart脚本中的底部bar是通过这个来实现的）  
```
pacman -S acpi
yay -S acpitool
```

laptop还可以考虑安装一个laptop-mode-tools（按需要安装,需要一定的配置）  
是一个 Linux 系统下的笔记本电源管理软件。它是让内核开启笔记本电脑模式功能的主要方法，能让硬盘降速。另外，它允许你通过一个简单的配置文件调整一些其他的节能相关的设置。与 acpid 和 CPU frequency scaling 结合使用，LMT 提供给了大多数用户一个完整的笔记本电脑电源管理方案。  
```
yay -S laptop-mode-tools
```

<++>


#安装输入法（fcitx-configtool是fcitx的配置工具，可以不安装）   

`yay -S fcitx fcitx-im fcitx-googlepinyin fcitx-configtool
`  

根据需要设置首选输入法
要在 Gtk/Qt 程序中要修改如下几个参数，具体看wiki文档：   
```
在 /etc/X11/xinit/xinitrc 或者 ~/.xinitrc文件中添加：   
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"
```  
如果fcitx没有自动启动,则在~/.xinitrc文件中添加：
fcitx &
或者在dwm的自启动脚本中添加



#locale本地化设置和安装字体(否则显示为方块字体)  
```
vim /etc/locale.gen
#取消掉两个注释  
en_US.UTF-8 UTF-8  
zh_CN.UTF-8 UTF-8
```  
  



编辑完成以后,通过下面的命令生成 Locale：   
`locale-gen  
`  
  

想要显示正在使用的 Locale 和相关的环境变量，运行：    

`locale  
`  
  
要使用的区域设置（从前面生成的区域设置中选择）设置在 locale.conf 文件中。每一个 locale.conf 文件都必须包含一些环境变量赋值语句，其格式与 locale 命令输出的格式相同。   
```
要查看已经生成的区域设置：  
$ localedef --list-archive
或者  
$ localectl list-locales
要设置整个系统使用的区域设置，需要在 /etc/locale.conf 中写入 LANG 变量，以下的 zh_CN.UTF-8 应为 /etc/locale.gen 中某个未注释条目的第一列(最好设置为en_US.UTF-8 UTF-8 避免ssh等远程链接时出现乱码等现象)：    
vim /etc/locale.conf
LANG=zh_CN.UTF-8
或者使用  
localectl set-locale LANG=zh_CN.UTF-8
locale.conf 的变更会在下次登录时生效

一般设置为以下则可  
LANG=zh_CN.utf8
然后为了保持终端中的输出为英文，而非中文，需要修改bashrc或者zshrc，添加下边代码，在打开终端的时候临时修改LANG的值
export LANG=en_US.UTF-8

locale.conf的配置参考（全英文）  
LANG=en_US.UTF-8
LC_ADDRESS=en_US.UTF-8
LC_IDENTIFICATION=en_US.UTF-8
LC_MEASUREMENT=en_US.UTF-8
LC_MONETARY=en_US.UTF-8
LC_NAME=en_US.UTF-8
LC_NUMERIC=en_US.UTF-8
LC_PAPER=en_US.UTF-8
LC_TELEPHONE=en_US.UTF-8
LC_TIME=en_US.UTF-8
完全支持中文环境，但是以英文作为用户界面
LANG=zh_CN.utf8
LC_MESSAGES=en_US.utf8
LC_CTYPE=”zh_CN.UTF-8″
LC_NUMERIC=”zh_CN.UTF-8″
LC_TIME=”zh_CN.UTF-8″
LC_COLLATE=”zh_CN.UTF-8″
LC_MONETARY=”zh_CN.UTF-8″

```  
  




常用字体 

`yay -S adobe-source-code-pro-fonts nerd-fonts-source-code-pro noto-fonts(思源宋体)
`  
  

中文字体    

`yay -S wqy-bitmapfont wqy-microhei wqy-microhei-lite wqy-zenhei adobe-source-han-mono-cn-fonts adobe-source-han-sans-cn-fonts adobe-source-han-serif-cn-fonts
`   
  


emoji   
  
`yay -S ttf-linux-libertine ttf-inconsolata ttf-joypixels ttf-twemoji-color noto-fonts-emoji ttf-liberation ttf-droid
`  
  




## 4.dwm极简窗口管理器的安装与配置  

### A.安装显示服务器  

`pacman -S xorg xorg-server xorg-xinit
`    

### B.启动dwm的方式  

#### (1)通过startx启动dwm（startx配合xorg-xinit） 

`pacman -S xorg-xinit
`  
  

xinit 程序手动启动 Xorg 显示服务器。
xinit 通常用在启动 X 时执行窗口管理器 或 桌面环境。虽然可以使用 xinit 在无窗口管理器的情况下启动图形程序，大部分图形程序都需要一个兼容 EWMH 的窗口管理器。显示管理器 启动 Xorg 并读取 xprofile。

startx -》 xinit -》 ~/.xinitrc (如果没有则默认读取/etc/X11/xinit/xinitrc) -》 根据xinitrc内容启动窗口管理器或者显示管理器  

vim ~/.xinitrc  

#登陆后执行打开dwm窗口管理器  

exec dwm  

chmod a+s ~/.xinitrc  

#那么通过命令startx则可以打开dwm窗口管理器  
  



#### (2)通过登陆管理器lightdm启动dwm
选择一：lightdm -> 登陆管理器 -》/etc/lightdm/Xsession -> /usr/share/xsession/xxx.desktop 选择x桌面会话 -》 创建x桌面
选择二：lightdm -> 登陆管理器 -》/lightdm根据配置文件检查session的存放目录 -》 /etc/lightdm/Xsession 执行本地化脚本操作 -》激活session服务 -> /usr/share/xsession/xinit.desktop 选择x桌面会话 -》 通过xinit-helper 读入~/.xinitrc文件 -》 创建x桌面
注意：xinit-xsession会在/usr/share/xsession中添加xsession会话服务xinitrc.desktop，服务器会通过xinit-helper执行xinitrc文件中的内容

安装包  
`pacman -s xorg-xinit lightdm lightdm-gtk-greeter xinit-xsession
`  

#可以选择其他好看的greeter，就是登陆的页面
可以对lightdm-gtk-greeter进行背景图片及头像的设置
```
sudo pacman -S lightdm-gtk-greeter-settings
sudo pacman -S archlinux-artwork
# /usr/share/archlinux/icons/archlinux-icon-crystal-64.svg
sudo lightdm-gtk-greeter-settings #将头像设置成上边的路径
```



这里按选择二操作
```
设置xinitrc文件
vim ~/.xinitrc
exec dwm
chmod a+x ~/.xinitrc

如果使用登陆管理器如lightdm，那么要设置lightdm默认启动
#默认可能有其他登陆管理器，需要禁用掉，比如gdm
systemctl disable gdm
#启用lightdm作为默认的登陆管理器
systemctl start lightdm #测试是否可正常操作
#lightdm登陆成功后会执行Xsession脚本，查找desktop文件（xinitrc.desktop），指出可选的x会话桌面
#测试成功后执行以下命令，让其可以默认启动
systemctl enable lightdm

```




### C.安装dwm

dwm是一个简单的动态窗口管理器。

dmenu是一个X下的快速、轻量级的软件启动器，它从stdin读取任意文本，并创建一个菜单，每一行都有一个菜单项。 然后，用户可以通过方向键或键入名称的一部分来选择一个项目，该行就会被输出到stdout。 dmenu_run是 dmenu 发行版附带的包装器，可将其用作应用程序启动器。
	
注意dwm一样需要字体支持

官方的安装方式（不建议需要大量个人的配置）

git clone https://git.suckless.org/dwm --depth=1

cw用户的安装（已经配置好相应的设置，做适当修改即可,其已经包含dmenu配置）
```
git clone https://github.com/theniceboy/dwm.git --depth=1
git clone https://github.com/theniceboy/dmenu.git --depth
cd dwm
#修改config.h 和config.mk文件中的内容(如脚本的位置，编译器的位置等，以及按键的设置)
sudo make clean install
cd dmenu
#修改config.h 和.mk文件中的内容
sudo make clean install
#cw作者写的脚本，可做特定常用操作
https://github.com/theniceboy/scripts.git
cd scripts
#对其做适当的修改


```


### D.配置dwm

dwm的配置
```
cd ~/dwm
vim config.mk
vim config.h


```


patch的安装
```
将patch包放置到dwm目录下，然后执行
patch < xxxx.diff
sudo make clean install


```


scripts脚本的简介及执行流程
#见autostart.sh


gtk和qt主题设置（让其保持一致）

yay -S nordic-darker-theme
sudo pacman -S papirus-icon-theme

yay -S adapta-gtk-theme
yay -S arc-icon-theme
gtk和qt是linux下程序的不同的gui开发工具，由于不同程序使用不同的gui开发工具，会导致按键显示等的不同，人为让其保持一致。
设置gtk主题及图标

通过lxappearance可以设置gtk程序的主题和图标。

sudo pacman -S lxappearance
设置管理员和普通用户的主题
sudo lxappearance

设置 qt 主题和图标
通过qt5ct可以设置qt程序的主题和图标。

sudo pacman -S qt5ct
使用qt5ct需要在~/.xinitrc文件中添加以下代码：

export QT_QPA_PLATFORMTHEME=qt5ct
安装qt5-styleplugins可以将qt程序设置为gtk风格。

yay -S qt5-styleplugins
或者
pacman -S qt5-styleplugins

分别设置管理员及普通用户的主题
sudo qt5ct
qt5ct




### E.安装st（简单的终端模拟器）  

  
官方安装（不建议，需要大量个人的配置）  
  

git clone https://git.suckless.org/st  
sudo make clean install

cw用户的安装（已经配置好相应的设置，做适当修改即可)
https://github.com/theniceboy/st.git

### F.安装声音管理器 (dwm,依赖工具)  
 
sudo pacman -S alsa-utils  
解除静音  
$ amixer sset Master unmute
$ amixer sset Speaker unmute
$ amixer sset Headphone unmute  
或者通过  
$ alsamixer  
测试声卡是否工作：
$ speaker-test -c 2  
$ speaker-test -c 8

sudo alsactl store  
在引导时读取 /var/lib/alsa/asound.state ，并在关机时写入更新后的值，前提是已经运行 alsactl store 生成了配置文件
sudo systemctl enable alsa-restore.service    

#安装声音管理器
sudo pacman -S pulseaudio pulseaudio-alsa 
sudo pacman -S pavucontrol
执行命令查看声音输出是否正常
pavucontrol 

#安装本地音频服务器和音频客户端
sudo pacman -S mpd ncmpcpp deadbeef-git
#注意mpd ncmpcpp支持conky中显示资源状态，除此外没啥用。倒不如deadbeef。
复制对应应用的对应的配置文件到~/.config/ 下
#启用mpd服务
systemctl start mpd --user
systemctl enable mpd --user
#运行音乐播放器ncmpcp
ncmpcpp  
注意F1查看帮助，enter为播放音乐，空格按键不可用
#运行音乐播放器deadbeef(此播放器不需要mpd支持)
dmenu中查找deadbeef，运行，添加播放目录即可。

### G.安装截图工具flameshot(dwm,依赖工具)  

sudo pacman -S flameshot  
修改~/.xinitrc
exec dbus-launch dwm


### .安装compont（毛玻璃特效）
### .picom的安装与使用(桌面背景管理)  

安装网络软件包 dhcpcd, netctl, networkmanager 三选一
# pacman -S dhcpcd  # systemctl enable dhcpcd
# pacman -S netctl iw wpa_supplicant dialog
# pacman -S rp-pppoe #pppoe-setup #systemctl enable adsl
pacman -S networkmanager nm-connection-editor  network-manager-applet rp-pppoe
systemctl enable NetworkManager
network-manager-applet 是 NetworkManager 的前端UI管理工具，可以通过 nm-applet 启动。


su命令知识点回顾  
su root #表示切换到root用户，保留原来的环境变量，home目录仍为原来的目录而非root用户目录  
su - root #表示切换到root用户，更换到root的环境变量，home目录为/root  
root用户如何运行普通用户安装的软件，普通用户如何运行root用户安装的软件  
将普通用户安装的软件放置到自己的环境变量中，然后就可以执行了。或者sudo -u user command 到指定用户执行，或者su -c command user 命令。  
  

如何设置默认编辑器  
update-alternatives --config editor $更换默认编辑器  



archlinux 报错  
无法启动加载/保存屏幕背光亮度  
[SOLVED] Failed to start Load/Save Screen Backlight Brightness  
添加下列内容到/etc/default/grub  
GRUB_CMDLINE_LINUX_DEFAULT="quiet acpi_backlight=vendor"  
更新grub  
sudo grub-mkconfig -o /boot/grub/grub.cfg  

每次启动grub后就会出现/dev/sda1: clean, ***/*** files, ***/*** blocks，然后正常进入系统，请教哪里出了问题，能不能让系统不显示它？

f1等功能键要按fn才能起作用  
bios中设置


安装显卡驱动(xorg会自动选择显卡驱动)
#查看当前的显卡
$ lspci | grep -e VGA -e 3D
#查找可用的显卡驱动
$ pacman -Ss xf86-video  
选择适合的显卡驱动安装
$ pacman -S xf86-video-amdgpu



lspci 是一个用来显示系统中所有PCI总线设备或连接到该总线上的所有设备的工具。可以用于查看硬件信息。lshw也是这种类型的工具
pacman -S pciutils
pacman -S lshw

以查看显卡信息为例子
lscpi|grep -i vga 
00:02.0 VGA compatible controller: Intel Corporation Mobile GM965/GL960 Integrated Graphics Controller (primary) (rev 0c)
根据前边的序号继续查看详细信息
lspci -v -s 00:02.0
Kernel modules: i915, intelfb
根据显示的内核模块信息查看内核模块信息
modinfo i915

查看驱动模块
lshw -numeric -C display
lshw -c video|grep configuration
modinfo i915


设置背光亮度
如果是intel显卡模块，可以使用xorg-xbacklight，radeon不支持需要安装acpilight，acpilight命令和xorg-xbacklight命令一样
pacman -S xorg-xbacklight
#获取当前的亮度
xbacklight -get
设置亮度
xbacklight -set 30
增加亮度
xbacklight -inc 10
减少亮度
xbacklight -dec 10


clight 通过摄像头传感器等感知亮度
pacman -S clight
打开软件
clight
sudo systemctl enable clightd.service

最好用的方式
pacman -s xfce4-power-manager
xfce4-power-manager &
设置电源及亮度显示方式，以及启用亮度按键，通过界面调节
xfce4-power-manager -c

触摸板的安装
一般可能会自动安装xf86-input-libinput
pacman -S xf86-input-libinput
xinput list #查看所有输入设备
xinput可以设置鼠标或者触摸板按键映射，触摸板灵敏度等
配置方法
cp /usr/share/X11/xorg.config.d/40-libinput.conf /etc/X11/xorg.conf.d/40-libinput.conf
#修改40-libinput.conf touchpad的内容描述，并且只保留touchpad的内容如下,或者复制git@github.com:bbbglimmer/keyboard_touchpad中的40-libinput.conf
```
Section "InputClass"
        Identifier "libinput touchpad catchall"
        MatchIsTouchpad "on"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
        Option "SendEventsMode" "disabled-on-external-mouse"
        Option "Tapping" "True"
        Option "DisableWhileTyping" "True"
        Option "ClickMethod" "clickfinger"
        Option "TappingDrag" "True"
        Option "AccelProfile" "adaptive"
        Option "AccelSpeed" "0.26"
        Option "NaturalScrolling" "True"
EndSection

```

<++>

触摸板手势支持可以通过libinput-gestures来实现
pacman -S libinput-gestures



摄像头的安装
如果是usb摄像头或者内置摄像头，系统一般自动识别加载
usb工具usbutils
pacman -s usbutils
lsusb -v|grep -i "14 video"
如果有信息输出表示有webcame
可以安装cheese来查看摄像头，但是比较大
pacman -S cheese

图片工具

在命令行中显示图片ranger，配合seebye/ueberzug

图片管理工具


复制黏贴的实现

u盘自动挂载的实现

github克隆zsh ohmyzsh ohmytumx nvim配置等

安装zsh和zsh-completions
pacman -S zsh zsh-completions

初始配置zsh，安装完后运行zsh会进入zsh的初始化配置
zsh
如果想再次进入初始化配置
autoload -Uz zsh-newuser-install
zsh-newuser-install -f

安装ohmyzsh
sh -c "$(curl -fsSL https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh)"
脚本会执行并备份当前的配置到/home/glimmer/.zshrc.pre-oh-my-zsh文件中
需要添加ohmyzsh模版文件到.zshrc文件中并添加插件等

安装主题
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
在zshrc中配置主题
ZSH_THEME="powerlevel10k/powerlevel10k"
然后关闭终端重新打开则进入powerlevel10k主题的配置

ohmyzsh安装插件
ohmyzsh插件库：https://github.com/ohmyzsh/ohmyzsh/wiki/External-themes  
修改.zshrc内的插件内容
git z sudo extract tmux zsh-syntax-highlighting zsh-autosuggestions
z是cd的快捷方式插件
sudo 按两下escape可以打上sudo命令
extract命令用于解压缩    ohmyzsh自带不用安装
tmux tmux的插件   设置终端参数，在使用ssh链接远程服务器的时候会打开tmux避免远程服务器网络差断开后进程关闭的情况  
syntax 高亮语法插件
autosuggestions 命令自动建议插件

通过git下载相应的插件
git clone https://github.com/rupa/z.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/z
git clone --depth=1 https://github.com/hcgraf/zsh-sudo
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

tmux插件ohmyzsh已经自带但用户要安装tmux，否则会报错
pacman -S tmux

安装ohmytmux美化及优化tmux
git clone https://github.com/gpakosz/.tmux.git /Users/glimmer/.oh-my-tmux
ln -s -f /Users/glimmer/.oh-my-tmux/.tmux.conf ~/.tmux.conf
cp /Users/glimmer/.oh-my-tmux/.tmux.conf.local ~/.tmux.conf.local

根据自己的实际情况，配置tmux.conf.local
根据ohmytmux配置文件tmxu.conf查看定义的快捷键
并通过tmux的插件程序tpm安装插件。


```


配置neovim
#下载我自己的配置文件
git clone
#安装或者更新软件
#为coc安装pynvim
pacman -S python-pip
pip install pynvim
pip install debugpy
pacman -S nodejs npm ctags fzf the_silver_searcher ripgrep ranger figlet xclip
yay -S ccat
sudo npm install -g yarn
# instant-markdown的依赖
sudo npm install -g instant-markdown-d
vim-plug 更新插件
:PlugInstall

安装coc.nvim
cd ~/.config/nvim/plugged/coc.nvim/
yarn install
yarn build
检查coc的环境状况，更新插件
:checkhealth



#安装并更新xclip的配置
xclip 使终端可以使用黏贴版
pacman -S xclip
然后修改st终端相应的代码，绑定快捷键，使其支持xclip
neovim上相应的xclip设置已经更新到init.vim文件中，默认可用。

#检查各样功能及插件是否正常可用

#安装ranger和fzf
#配置ranger和fzf
git clone git@github.com:bbbglimmer/myrangerconfig.git
git clone git@github.com:bbbglimmer/myfzfconfig.git
修改相应的路径并测试即可
更新zshrc和init.vim文件另ranger和fzf可以在zsh和neovim中正常可用


# 使用trash来代替rm命令
sudo pacman -S trash-cli
# 添加以下内容到zshrc文件中去
你可以给 rm 设置一个别名来提醒你不要使用它：
alias rm='echo "This is not the command you are looking for."; false'
如果你真的要用 rm，那就在 rm 前加上斜杠来取消别名：
\rm file-without-hope
注意，Bash 别名是有在交互式界面才有效，所以使用这个别名不会影响使用 rm 的脚本。
从 home 分区移动到回收站的文件在这：
~/.local/share/Trash/
修改ranger快捷键绑定让ranger支持垃圾箱（已经更新ranger配置文件）


通过udevadm和hwdb来修改esc和capslock按键，实现终端和虚拟终端以及图形界面的按键互换（此方法为最优）  
```
git clone git@github.com:bbbglimmer/keyboard_touchpad.git ~/.config/keyboard_touchpad

cp ~/.config/keyboard_touchpad/60-keyboard.hwdb /etc/udev/hwdb.d/60-keyboard.hwdb
#以下修改触摸板的功能跟触摸板安装区域内容一致
cp ~/.config/keyboard_touchpad/40-libinput.conf /usr/share/X11/xorg.config.d/40-libinput.conf
```

<++>


快捷键处理软件脚本leftaltkeybind，实现alt按键作为功能键（此方法暂时最优，因为xkeysnail会导致触摸板不可用，但此方法会导致像st等原本绑定alt的快捷键不可用）
alt+hjkl 等于上下左右移动
alt+c/v  等于复制粘帖
alt+u/e  等于滚动屏幕
安装依赖
`sudo pacman -S python-evdev` <++>
`sudo yay -S python-inotify-simple` <++>

安装leftaltkeybind脚本及服务
```
git clone git@github.com:bbbglimmer/leftaltkeybind ~/.config/leftaltkeybind

cp ~/.config/leftaltkeybind/leftaltkeybind.service /etc/systemd/system/leftaltkeybind.service 
systemctl start leftaltkeybind
systemctl enable leftaltkeybind

```

安装feh 使桌面有壁纸
`sudo pacman -S feh` <++>
修改dwm启动后自动执行的脚本
`nvim /script/autostart.sh` 
使其开机启动


安装picom （可能由于我图片太高清导致渲染期间太吃内存，电脑会变慢）
```
安装 picom-jonaburg-git或者picom，两者会冲突，建议前者，比较好用
yay -S picom-jonaburg-git
sudo pacman -S picom
mkdir -p ~/.config/picom
cp /etc/xdg/picom.conf ~/.config/picom

修改里边的内容(不建议，建议直接用别人的脚本)
blur-background = true;
blur-strength = 7;
backend = "glx";

或者直接用别人设置好的
https://github.com/ayamir/dotfiles/blob/master/nord/.config/picom/picom.conf
运行picom测试是否可行
修改启动脚本让它自动启用
```

安装dunst实现简单的消息提示管理 
复制配置到.config目录下

安装conky实现桌面式资源状态显示
复制配置到.config目录下



安装锁屏管理器：betterlockscreen, xautolock（用于自动锁屏）

#安装betterlockscreen
yay -S betterlockscreen

#配置
更新缓存的锁屏壁纸
betterlockscreen -u ~/Wallpapers/image.png --fx dim,pixel
更换锁屏壁纸及壁纸的样式
betterlockscreen -w pixel
锁屏,并设置锁屏桌面为模糊 变暗或者像素化
betterlockscreen -l blur 
或者
betterlockscreen -l dim
betterlockscreen -l pixel

#设置为服务，让系统在休眠或者挂起的时候会执行锁屏操作

# # move service file to proper dir (the aur package does this for you)
# 如果是yay安装则不用复制,已经放到指定目录中
# cp betterlockscreen@.service /usr/lib/systemd/system/
# enable systemd service
systemctl enable betterlockscreen@$USER
# disable systemd service
# systemctl disable betterlockscreen@$USER

# 让系统定时锁定屏幕并且在排除特定应用在使用过程中的锁屏，需要设置脚本中的程序
pacman -S xautolock

开机启动脚本中执行
xautolock -time 5  -locker "~/scripts/lockscreen.sh"

编辑脚本~/scripts/lockscreen.sh
排除不锁屏程序在焦点时不锁定屏幕。




安装pdf 阅读器：zathura（vim风格）, evince
安装
pacman -S zathura
pacman -S zathura-pdf-mupdf

pacman -S evince

安装浏览器主页，让浏览器打开标签时默认打开自己设定的主页
复制startpage到~/ 目录下然后设定浏览器标签即可，或者安装chrome插件custom new tab url
startpage来自https://github.com/migueravila/Bento

安装文件管理器：thunar 或者 nemo
sudo pacman -S thunar thunar-archive-plugin thunar-media-tags-plugin thunar-volman

thunar增加smaba服务
sudo pacman -S gvfs-smb

终端下的视频播放器
smplayer
gui视频播放器
bomi
yay -S bomi

vlc-git
sudo pacman -S vlc-git

gui图片图像查看器
xnview
yay -S xnviewmp

gui复杂图片图像编辑
gimp

办公软件
wps
yay -S wps-office-cn
yay -S wps-office-mui-zh-cn
yay -S ttf-wps-fonts

mardown软件
typora
sudo pacman -S typora


通讯软件的安装
deepin-wine-tim 依赖Multilib仓库中的一些32位库，Archlinux 默认没有开启 Multilib仓库，需要编辑/etc/pacman.conf，取消对应行前面的注释(Archlinux wiki):
#[multilib-testing]
#Include = /etc/pacman.d/mirrorlist

qq
yay -S deepin-wine-tim
/opt/apps/com.qq.office.deepin/files/run.sh

微信
yay -S deepin-wine-wechat
/opt/apps/com.qq.weixin.deepin/files/run.sh

qq或者微信需要通过打开其desktop文件打开软件，所以需要安装rofi
rofi的安装
sudo pacman -S rofi
配置.config/rofi的配置文件即可

邮箱(没有特别好用的邮箱客户端，thunderbird可以使用一下但是效果也不是特别好)
通过在我自定义的主页中快捷跳到制定邮箱网页即可,然后可以在chrome中设置邮箱邮件提醒


自动挂载工具
udiske
yay -S udiskie 
在开机脚本中添加内容(因为是针对每用户的，所以每个用户都要执行)
udiskie --tray &

让系统支持ntfs
sudo pacman -S ntfs-3g

bluthooh蓝牙管理
https://wiki.archlinux.org/title/Bluetooth_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)





golang isp配置按原来的设置一下看是否可用



配置文件介绍
当 Zsh 启动时，它会按照顺序依次读取下面的配置文件：

/etc/zsh/zshenv
该文件应该包含用来设置PATH 环境变量以及其他一些环境变量的命令；不应该包含那些可以产生输出结果或者假设终端已经附着到 tty 上的命令。
~/.zshenv
该文件和 /etc/zsh/zshenv 相似，但是它是针对每个用户而言的。一般来说是用来设置一些有用的环境变量。
/etc/zsh/zprofile
这是一个全局的配置文件，在用户登录的时候加载。一般是用来在登录的时候执行一些命令。请注意，在 Arch Linux 里该文件默认包含一行配置，用来加载 /etc/profile 文件，详见 #全局配置文件。
/etc/profile
在登录时，该文件应该被所有和伯克利（Bourne）终端相兼容的终端加载：它在登录的的时候会加载应用相关的配置（/etc/profile.d/*.sh）。注意在 Arch Linux 里，Zsh 会默认加载该文件。
~/.zprofile
该文件一般用来在登录的时候自动执行一些用户脚本。
/etc/zsh/zshrc
当 Zsh 被作为交互式终端的时候，会加载这样一个全局配置文件。
~/.zshrc
当 Zsh 被作为交互式终端的时候，会加载这样一个用户配置文件。
/etc/zsh/zlogin
在登录完毕后加载的一个全局配置文件。
~/.zlogin
和 /etc/zsh/zlogin 相似，但是它是针对每个用户而言的。
/etc/zsh/zlogout
在注销的时候被加载的一个全局配置文件。
~/.zlogout
和 /etc/zsh/zlogout 相似，但是它是针对每个用户而言的.
在 Arch 源中的 zsh 所使用的文件路径和 Zsh 的 man 手册中默认的不同（详见 #全局配置文件）
/etc/profile 不是 Zsh 常规启动配置文件的一部分，但是 Arch 源中的 zsh 会在 /etc/zsh/zprofile 里面加载它。用户应该注意 /etc/profile 里面设置的 $PATH 环境变量会覆盖掉 ~/.zshenv 里面配置的任何 $PATH。为了防止这一点，请在 ~/.zshrc 当中设置 $PATH（不推荐替换掉 /etc/zsh/zprofile 里面的默认配置，因为这样会破坏其他提供了 /etc/profile.d 的软件包和 Zsh 的联动关系）
有时候你可能想提供一些所有 Zsh 用户共享的配置。在帮助手册 zsh(1) 提到的一些全局配置文件（例如 /etc/zshrc）的路径，在 Arch Linux 里是有一些不同的，因为其路径已经被编译为 [1] /etc/zsh/ 。

所以，Arch 源中 zsh 的全局配置文件会使用 /etc/zsh/zshrc 而不是 /etc/zshrc。类似的还有 /etc/zsh/zshenv、/etc/zsh/zlogin 和 /etc/zsh/zlogout。注意这些文件不是默认就被创建好的，你可以根据需要来创建它们。

唯一的例外是 zprofile，请使用 /etc/profile
```

更改shell，注意要将~/.bashrc某些代码转移到~/.zshrc,以及将～/.bash_profile文件的代码转移到~/.zprofile
```
chash -l

chash -s /bin/zsh
或者
homectl update --shell=/bin/zsh glimmer #使用systemd-homed
```







日志的查看
journalctl -f -n xxx.service


alsactl restore 报错：  
alsactl[769]: alsa-lib parser.c:242:(error_node) UCM is not supported for this HDA model (HD-Audio Generic at 0xfd3c8000 irq 108)
alsactl[769]: alsa-lib main.c:1405:(snd_use_case_mgr_open) error: failed to import hw:0 use case configuration -6
alsactl[769]: alsa-lib parser.c:242:(error_node) UCM is not supported for this HDA model (HD-Audio Generic at 0xfd3c0000 irq 109)
alsactl[769]: alsa-lib main.c:1405:(snd_use_case_mgr_open) error: failed to import hw:1 use case configuration -6

解决方法：
nvim /usr/ib/systemd/system/alisa-restore.service
修改
alsactl -U restore
alsactl -U store




如何备份主引导
如何备份分区






修改/etc/passwd文件，为了避免格式错误，应该使用vipw
`vipw` 


.local文件夹
什么是~/.local文件夹
这设计到xdg目录（分为基础目录和用户目录）
可以查看这两个网站
https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

XDG base directories （xdgji基础目录，用来创建用户目录下的.config .local .local.share .local.state .cache等目录）
https://wiki.archlinux.org/title/XDG_Base_Directory
XDG user directories （xdg用户目录，用来创建用户的目录文件夹）
https://wiki.archlinux.org/title/XDG_user_directories_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
如果需要自己执行创建这些目录，可以执行下面的代码
```
pacman -S xdg-users-dirs
nvim ~/.config/user-dirs.dir 或者 /etc/xdg/user-dirs.defaults 配置创建目录的规则
执行命令
LC_ALL=C xdg-user-dirs-update --force  #可以强制创建英语目录
查询配置好的目录
xdg-user-dirs
```

<++>


这是Gnome最近的一项创新，紧随其后的是Ubuntu，将user-specific数据存储在固定目录中。根据这个document（https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html），有

存储用户数据的单个目录，默认为~/.local/share;

存储配置的单个目录，默认为~/.config;

一个包含non-essiential数据文件的目录，默认为~/.cache。

从历史上看，Unix程序可以自由地将数据传播到$ HOME目录，将其数据放入dot-files(以”.”开头的文件)或~/.vimrc和~/.vim等子目录中。新规范旨在使此行为更具可预测性。我怀疑这使得应用程序数据的备份更容易，除了给你的主目录外观更整洁外。并非所有应用程序都符合此标准。

在.local层次结构中，程序放置用户信息，例如电子邮件和日历事件。你可以手动删除这些数据，但是程序会失去它的状态;除非您打算这么做(例如，当您的配置出现问题时)，则不应删除或更改该目录中的文件。使用.cache时，如果您删除它们，程序应该能够恢复 – 重新下载或重新计算 – 所有文件，否则您可能会更加不小心。

让我分享一下我对.local目录的体验。我还发现我的磁盘分区(根分区)存储主目录没有足够的空间，在检查这些目录的内容后，我发现.local目录存储在70G以上的空间，然后我想删除它，但是担心删除可能会导致我的Ubuntu系统崩溃。所以我在谷歌搜索这个问题，它指示我在这里。但以前的答案不能解决我的问题，我只想在我的系统上得到两个结果：

删除.local目录中的一些内容，然后我可以拥有足够的磁盘空间来存储我的新文件;

我不希望我的系统崩溃，这意味着我不想直接从我的家.local目录中删除内容，这太危险了！

最后，我发现.local目录下的最大内容在这里：/home/myAccount/.local/share/Trash占用69G字节。我觉得它涉及到垃圾，所以我去垃圾桶：垃圾：///并清空垃圾，然后我发现69G字节的磁盘空间被释放！

所以我的结论是：

直接删除.local目录非常危险。

我们可以通过”Empty”垃圾箱安全地删除/home/myAccount/.local/share/Trash下的内容。





archlinux运行登记查看及设置，使用用systemd
查看默认运行级别
systemctl get-default
设置默认的运行级别
systemctl set-default multi-user.target
systemctl set-default graphical.target

切换当前运行级别
systemctl isolate multi-user.target
systemctl isolate graphical.tareget

查看当前的用户级别
who  #查看终端是什么来确认，如果为7及7以上则为图形界面，如果是1-6则为文本界面




安装v2raya作为ssr的客户端
https://v2raya.org/docs/prologue/installation/archlinux/
v2raya的功能依赖于v2ray内核，因此要安装v2ray内核
pacman -S v2ray
安装v2ray
yay -S v2raya 
systemctl status v2raya   #可能需要sudo命令执行
systemctl enable --now v2raya #可能需要sudo命令执行
http://localhost:2017 对v2raya进行设置
默认情况下 v2rayA 会通过核心开放 20170(socks5), 20171(http), 20172(带分流规则的http) 端口





u盘驱动和软件ntfs fat exfat等




nvim 可以更新配置为lua模式,更现代化


改用chromium
安装扩展

Adobe Acrobat
Custom New Tab URL
Google Translate
Lunar Reader - Dark
OneTab
PDF Viewer for Vimium C
Proxy SwitchyOmega
Tampermonkey
uBlock Origin
Vimium C
书签侧边栏



更改主页
https://github.com/bbbglimmer/Bento


bios(传统bios legacy或者叫csm兼容支持模块)和uefi（esp表示EFI系统分区（即 ESP）的挂载点）安装linux的区别
一般uefi配合gpt分区一起用，传统bios使用传统的mbr分区，但实际bios和uefi安装与分区模式没关系，只是由于硬件支持的问题有此建议。
建议都关闭secure boot安全启动，禁用快速启动
进入 Linux shell 环境执行 ls /sys/firmware/efi 验证当前是否处于 EFI 引导模式。如果你看到一系列文件和目录，表明你已经以 EFI 模式启动，而且可以忽略以下多余的提示；如果没有，表明你是以 BIOS 模式启动的，应当重新检查你的设置。
bios安装不需要单独划分并且设置/boot
uefi需要单独划分一个分区,文件格式为uefi 或者指定为fat32,然后初始化并且挂载到目录/boot/EFI
两者均需要安装grub，但两者的引导方式不同，所以要安装的引导工具不同,后者需要efibootmgr
https://linux.cn/article-8481-1.html


滚挂处理


linux解决环境污染的问题及deb包和rpm包的问题（debian ubuntu 和readhat的包）
前者可以通过brew实现
后者可以通过pacur实现



archlinux 启动过程
https://wiki.archlinux.org/title/Arch_boot_process_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

mbr和gpt分区的区别
均在磁盘前做标记，gpt在磁盘后亦做标记。
mbr最大4个主分区，一般为了扩展分区需要将一个主分区设置为扩展分区（只能有一个扩展分区），然后该扩展分区存放多个逻辑分区，实现分区扩展。
gpt没有主分区和扩展分区以及逻辑分区的说法，分区不做限制。
并且MBR最大仅支持2TB的硬盘。如果需要分区的硬盘容量超过2TB了，则需要使用GPT分区表类型，此分区表类型不受分区个数、硬盘大小的限制。
详细可以看一下：
https://blog.csdn.net/u011198997/article/details/78734628


分区备份(MBR和GPT统一这种处理方式最简单)
对于GPT和MBR，您可以使用“sfdisk”将设备的分区布局保存到具有-d/--dump 选项的文件中. 对设备 /dev/sda运行以下命令:
sfdisk -d /dev/sda > sda.dump
要稍后恢复此布局，可以运行：
sfdisk /dev/sda < sda.dump
具体可以查看这里
https://wiki.archlinux.org/title/Partitioning_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E5%A4%87%E4%BB%BD

关于dd及文件系统块大小问题设置
fdisk cfdisk默认可以根据硬件情况确定分区的块大小（旧版本默认为512字节，不确认这个信息是否正确,这个信息错误）
https://wiki.archlinux.org/title/Dd#Backup_and_restore_MBR
https://www.mail-archive.com/eug-lug@efn.org/msg12073.html
http://blog.tdg5.com/tuning-dd-block-size/
https://wiki.archlinux.org/title/Disk_cloning_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

硬盘只有扇区的概念，没有块的概念
fdisk -l /dev/sda 可以查看硬盘的磁头/扇区/柱面，旧的硬盘一般扇区为512字节，新的一般为4k（sectors size即为扇区）

文件系统有块大小这个说法
df -T #查看是什么文件系统
tune2fs -l /dev/sda1 |grep "Block size" #查看文件系统块大小
Block size:               4096

mkfs.ext4可以设定参数-b 设置块大小，默认为4k，可以设置64k，加快传输大文件的速度，但同时会导致浪费
block设置为4K，那么创建大量的1K小文件后，磁盘空间会被大量浪费。一个文件占用一个block，100G的小文件（都是1K大小），那么会占用400G的空间，浪费300G
所以要合理设置块大小。一般默认值4k即可。

dd一般设置bs为4k与文件系统块大小一致可能传输速度最块


dd命令克隆 和 备份磁盘
https://wiki.archlinux.org/title/Disk_cloning#Using_ddrescue



archlinux 查找二进制文件所在的包
sudo pacman -Ss pkgfile                                                                                                                         
extra/pkgfile 21-2 a pacman .files metadata explorer
sudo pacman -S pkgfile
sudo pkgfile -u更新本地文件列表
完成之后，每当你遇到只知道文件名但不知道应该安装哪个软件包的名字的时候，运行
pkgfile -s filename（此处为netstat）

pkgfile -s netstat                                                                                                                             
core/net-tools
community/munin-node
