#!/bin/bash
export PYTHONPATH="/usr/lib/python38.zip:/usr/lib/python3.8:/usr/lib/python3.8/lib-dynload:/home/ubuntu/.local/lib/python3.8/site-packages:/usr/local/lib/python3.8/dist-packages:/usr/lib/python3/dist-packages"
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

date '+%Y-%m-%d %H:%M:%S' >> $SHELL_FOLDER/log.log
python3.8 $SHELL_FOLDER/leave.py 1>>$SHELL_FOLDER/log.log 2>>$SHELL_FOLDER/error.log