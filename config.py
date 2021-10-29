# -*- coding: utf-8 -*-

import re
from xkeysnail.transform import *

# define_modmap({Key.CAPSLOCK: Key.ESC})

define_multipurpose_modmap(
    # Capslock is escape when pressed and released. Control when held down.
    {Key.CAPSLOCK: [Key.ESC, Key.LEFT_CTRL]
    # To use this example, you can't remap capslock with define_modmap.
)

#这里把f13再改成Ctrl+space
define_keymap(
    None, {
        K("M-l"): K("right"),
        K("M-k"): K("up"),
        K("M-h"): K("left"),
        K("M-j"): K("down"),
    })

# nvim /etc/systemd/system/xkeysnail.service
# [Unit]
# Description=xkeysnail
# [Service]
# Environment=DISPLAY=:0
# ExecStart=/usr/bin/xkeysnail -q /home/kujio/.config/xkeysnail/config.py
# Restart=always
# RestartSec=10
# [Install]
# WantedBy=multi-user.target
