import re
from time import sleep, time
import requests
import datetime
import sys

DEBUG = False


def main(period, token):
    res = requests.post(
        "http://wx.bupt.edu.cn/bathroom/submit",
        data={
            "period": period
        },
        headers={
            "user-agent": "MicroMessenger",
        },
        cookies={
            "laravel_session": token
        },
    )
    
    if DEBUG or res.status_code == 200:
        print(res.text)
    
    print(res.status_code, re.findall(r'<div class="mt-3">学工号： (\d+)</div>', res.text),
          re.findall(r'<div class="alert alert-info">(.*)</div>', res.text))
    
    return res.status_code == 200


if __name__ == "__main__":
    today = datetime.date.today()
    tomorrow = today+datetime.timedelta(days=1)
    at = today+datetime.timedelta(days=2)
    
    period = "21:00:00"
    token = ""

    rePeriod = r'^\d\d:\d\d:\d\d$'
    date = at
    for arg in sys.argv:
        if ("today" == arg):
            date = today
        if ("tomorrow" == arg):
            date = tomorrow
        if re.fullmatch(rePeriod, arg):
            period = arg
        if "laravel_session" in arg:
            token = arg.split("=")[1]
        if arg == "debug":
            DEBUG = True
    print("task:", date, period, "\n", token)

    while 1:
        if main("{} {}".format(date, period), token):
            break
        sleep(1)
