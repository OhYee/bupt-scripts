#!/bin/bash
# 运行该文件将相关定时任务追加至 crontab 中

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

crontab -l > ./crontab.temp
echo "
# bupt
30 0 * * * /bin/bash $SHELL_FOLDER/check/check.crontab.bash
30 6 * * * /bin/bash $SHELL_FOLDER/check/check.crontab.bash
0  7 * * * /bin/bash $SHELL_FOLDER/leave/leave.crontab.bash
" >> ./crontab.temp
crontab ./crontab.temp
rm crontab.temp

crontab -l