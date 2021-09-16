import json
from urllib import parse
import requests
import datetime
import re
import yaml
import os

session = requests.Session()
schools = {
    "沙河": {"name": "沙河校区", "value": "1", "default": 0, "imgdata": ""},
    "西土城": {"name": "西土城校区", "value": "2", "default": 0, "imgdata": ""},
}


def login(username: str, password: str):
    session.cookies.clear()
    resp = session.get("https://auth.bupt.edu.cn/authserver/login")
    matchLT = re.findall(
        r'<input type="hidden" name="lt" value="(.*)" />', resp.text)
    if len(matchLT) == 0:
        print("登录 CSRF 加载错误")
        return ""
    lt = matchLT[0]

    resp = session.post(
        "https://auth.bupt.edu.cn/authserver/login?service=https%3A%2F%2Fme.bupt.edu.cn%2Fsite%2Flogin%2Fcas-login",
        data={
            "username": username,
            "password": password,
            "lt": lt,
            "execution": "e1s1",
            "_eventId": "submit",
            "rmShown": 1,
        })

    matchUserInfo = re.findall(
        r'<div class="login_info">\s*<span>\s*([^\s]*)\s*</span>\s*<a href=".*" title="退出登录">',
        resp.text
    )
    if len(matchUserInfo) != 0:
        return matchUserInfo[0]
    return ""


def getCollege():
    resp = session.get("https://service.bupt.edu.cn/site/user/get-name")
    return resp.json()["d"]["college"]


def leave(
        username: str,
        password: str,
        phone: str,
        position: str,
        reason: str,
        school: object,
        teacher: object
):
    name = login(username, password)
    if name == "":
        print(username, "登录失败")
        return
    print(name, "登录成功")

    college = getCollege()

    date = datetime.datetime.now().replace(hour=0, minute=0, second=0,
                                           microsecond=0).isoformat(timespec="microseconds")[:-7] + "+08:00"
    print(f"date={date}")
    beginTime = datetime.datetime.utcnow().replace(
        microsecond=0).isoformat(timespec="seconds") + ".000Z"
    endTime = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0).astimezone(
        tz=datetime.timezone.utc).isoformat(timespec="microseconds").replace("000+00:00", "Z")
    print(f"begin={beginTime}")
    print(f"end={endTime}")
    data1 = {"data": {"app_id": "578", "form_data": {
        "1716": {"User_5": name, "User_7": username, "User_9": college, "User_11": phone,
                 "SelectV2_58": [schools[school]],
                 "UserSearch_60": teacher,
                 "Calendar_62": date, "Calendar_50": beginTime,
                 "Calendar_47": endTime, "Input_28": position, "MultiInput_30": reason,
                 "Radio_52": {"value": "1", "name": "本人已阅读并承诺"}, "Validate_63": "", "Alert_65": "", "Validate_66": "",
                 "Alert_67": "", "Variate_74": "否", "DataSource_75": ""}}}}
    data = {
        "data": {
            "app_id": "578",
            "node_id": "",
            "form_data": {
                "1716": {
                    "Alert_67": "",
                    "Count_74": {"type": 0, "value": 1},
                    "Input_28": "1",
                    "Valudate_66": "",
                    "User_5": name,
                    "User_7": username,
                    "User_9": college,
                    "User_11": phone,
                    "Input_28": position,
                    "Radio_52": {
                        "value": "1",
                        "name": "本人已阅读并承诺",
                    },
                    "Radio_73": {
                        "value": "1",
                        "name": "是",
                    },
                    "Calendar_47": endTime,
                    "Calendar_50": beginTime,
                    "Calendar_62": date,
                    "Calendar_69": date,
                    "SelectV2_58": [schools[school]],
                    "MultiInput_30": reason,
                    "UserSearch_60": teacher,
                    # "UserSearch_73": teacher,
                }
            }
        }
    }

    resp = session.post(
        "https://service.bupt.edu.cn/site/apps/launch",
        data="data=" +
             parse.quote(str(data1["data"]).replace("'", '"').replace(" ", "")),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38",
            # "refer": "https://service.bupt.edu.cn/v2/matter/start?id=578",
            "x-requested-with": "XMLHttpRequest",
            # "accept": "application/json, text/plain, */*",
        }
    )
    resp.encoding = "utf-8"
    print(resp.text)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "users.txt")) as f:
        users = yaml.load_all(f, Loader=yaml.FullLoader)
        for u in users:
            try:
                leave(
                    username=u["username"],
                    password=u["password"],
                    phone=u["phone"],
                    position=u.get("position", "实验室"),
                    reason=u.get("reason", "科研"),
                    school=u.get("school", "西土城"),
                    teacher={
                        "uid": u.get("teacher_uid", 0),
                        "name": u.get("teacher_name", ""),
                        "number": u.get("teacher_number", "")
                    }
                )
            except Exception as e:
                print(e.print_exc())
