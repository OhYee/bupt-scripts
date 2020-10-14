# Go 语言版浴室预约脚本

该版本是为了编译出可以在路由器运行的自动预约程序而写的

Go 交叉编译见 [将 Go 程序编译至 OpenWRT](https://www.oyohyee.com/post/note_compile_go_to_openwrt)

## 使用

```
-d    调试模式
-debug
      调试模式
-s    预约模式
-submit
      预约模式
-t string
      Token 文件路径
-tokens string
      Token 文件路径
```

使用`-t`指定存储用户信息的文件，一行一个，内容为对应用户在预约系统的 cookies 字段

默认运行为保持 Token 模式，程序会按顺序访问对应页面，保持 Token 有效（建议每小时运行一次）**目前该保活机制已失效**

添加`-s`参数，使用预约模式。默认会预约次日 21:00:00 浴室 2 楼