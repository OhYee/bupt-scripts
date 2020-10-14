# 自动请假脚本

在`users.txt`中以 yaml 格式填入数据，每个用户包含以下字段
- username: 用户名
- password: 服务门户密码(默认身份证后 8 位)
- phone: 手机号
- position: 要去的地方(不填写默认实验室)
- reason: 出校原因(不填写默认科研)
- school: 校区(不填写默认西土城)
- teacher_uid: 辅导员 id(需要自己在相应页面按 F12 查看，虽然有查询接口，但是有重名概率)
- teacher_name: 辅导员姓名

每两个用户使用单独的一行`---`分割

```
username: "2019111111"
password: "11111111"
phone: "19999999999"
position: "实验室"
reason: "科研"
school: "西土城"
teacher_uid: 000
teacher_name: "xxx"
```