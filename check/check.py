import requests
import datetime
import re
import json
import os

session = requests.Session()

oldKeys = [
    "ismoved",    "jhfjrq", "jhfjjtgj", "jhfjhbcc", "sfxk", "xkqq", "szgj", "szcs", "zgfxdq", "mjry", "csmjry", "uid",  "tw", "sfcxtz", "sfyyjc", "jcjgqr", "jcjg", "sfjcbh", "sfcxzysx", "qksm", "remark", "address", "area", "province", "city", "geo_api_info",  "sfzx", "sfjcwhry", "sfcyglq", "gllx",
    "glksrq", "jcbhlx", "jcbhrq", "sftjwh", "sftjhb", "fxyy", "bztcyy", "fjsj", "sfjchbry", "sfjcqz", "jcqzrq", "jcwhryfs", "jchbryfs", "xjzd", "sfsfbh", "jhfjsftjwh", "jhfjsftjhb", "szsqsfybl", "sfygtjzzfj", "gtjzzfjsj", "sfsqhzjkk", "sqhzjkkys", "created_uid", "gwszdd", "sfyqjzgc", "jrsfqzys", "jrsfqzfy"
]
defaultKeys = [
    "date", "created", "id",
]


def login(username: str, password: str):
    resp = session.post("https://app.bupt.edu.cn/uc/wap/login/check", data={
        "username": username,
        "password": password,
    })

    if resp.json()["e"] == 0:
        return True
    else:
        print(resp.text)
        return False


def check(username: str, password: str):
    if login(username, password):
        print(username, "登录成功")
    else:
        print(username, "登录失败")
        return

    resp = session.get("https://app.bupt.edu.cn/ncov/wap/default/index")
    matchDefault = re.findall(r'var def = (.*);\n', resp.text)
    if (len(matchDefault) == 0):
        print("获取默认信息失败")
        return
    default = json.loads(matchDefault[0])

    matchOld = re.findall(r'oldInfo: (.*),\n', resp.text)
    if (len(matchOld) == 0):
        print("获取上次信息失败")
        return
    oldInfo = json.loads(matchOld[0])

    realnames = re.findall(r'realname: "(.*)",', resp.text)
    realname = "获取名称失败"
    if len(realnames) > 0:
        realname = realnames[0]

    data = {}
    for k in oldInfo:
        data[k] = oldInfo.get(k, "")
    for k in defaultKeys:
        data[k] = default.get(k, "")

    resp = session.post(
        "https://app.bupt.edu.cn/ncov/wap/default/save", data=data)

    j = resp.json()
    if j.get("e", 1) == 0:
        print(realname, "填报成功", oldInfo.get("address", ""))
    else:
        print(realname, "填报失败", j.get("m", ""))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "users.txt")) as f:
        users = f.read().split("\n")
    for u in users:
        try:
            if u != "":
                username, password = u.split(" ")
                check(username, password)
        except Exception as e:
            print(e)
