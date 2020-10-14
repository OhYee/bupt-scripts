//go:generate bash -c "GOOS=linux GOARCH=mipsle GOMIPS=softfloat go build -o bupt_bath"

package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"regexp"
	"strings"
	"time"
)

const (
	UserAgent   = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
	ContentType = "application/x-www-form-urlencoded"
)

var (
	idReg, _   = regexp.Compile("<div class=\"mt-3\">学工号： (\\d+)</div>")
	infoReg, _ = regexp.Compile("<div class=\"alert alert-info\">(.*)</div>")
	DEBUG      = false
)

// Get 请求到指定链接
func Get(url string, userAgent string, cookie string) (status int, body []byte, err error) {
	client := http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return
	}

	req.Header.Set("User-Agent", userAgent)
	req.Header.Set("Cookie", cookie)

	resp, err := client.Do(req)
	if err != nil {
		return
	}
	defer resp.Body.Close()
	status = resp.StatusCode
	body, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return
	}
	return
}

// Post 请求到指定链接
func Post(url string, data url.Values, userAgent string, cookie string) (status int, body []byte, err error) {
	client := http.Client{}
	req, err := http.NewRequest("POST", url, strings.NewReader(data.Encode()))
	if err != nil {
		return
	}

	req.Header.Set("User-Agent", userAgent)
	req.Header.Set("Cookie", cookie)
	req.Header.Set("Content-Type", ContentType)

	resp, err := client.Do(req)
	if err != nil {
		return
	}
	defer resp.Body.Close()

	status = resp.StatusCode
	body, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return
	}

	return
}

// Send 发送预约请求
func Send(period string, token string) (status int, id string, info string, err error) {
	values := make(url.Values)
	values.Set("period", period)

	status, body, err := Post("http://wx.bupt.edu.cn/bathroom/submit", values, UserAgent, token)
	if err != nil {
		return
	}
	if DEBUG {
		fmt.Printf("%s\n", body)
	}

	_id := idReg.FindSubmatch(body)
	if len(_id) > 1 {
		id = string(_id[1])
	}
	_info := infoReg.FindSubmatch(body)
	if len(_info) > 1 {
		info = string(_info[1])
	}

	return
}

// Keep 用户 token 保活
func Keep(token string) (status int, id string, err error) {
	status, body, err := Get("http://wx.bupt.edu.cn/bathroom/index", UserAgent, token)
	if err != nil {
		return
	}
	if DEBUG {
		fmt.Printf("%s\n", body)
	}

	_id := idReg.FindSubmatch(body)
	if len(_id) > 1 {
		id = string(_id[1])
	}

	return
}

func read(file string) (tokens []string, err error) {
	tokens = make([]string, 0)
	data, err := ioutil.ReadFile(file)
	if err != nil {
		return
	}
	temp := strings.Split(string(data), "\n")
	for _, item := range temp {
		if item != "" {
			tokens = append(tokens, item)
		}
	}

	return
}

func main() {
	var debug bool
	var tokenFile string
	var submit bool
	flag.BoolVar(&debug, "debug", false, "调试模式")
	flag.BoolVar(&debug, "d", false, "调试模式")
	flag.BoolVar(&submit, "submit", false, "预约模式")
	flag.BoolVar(&submit, "s", false, "预约模式")
	flag.StringVar(&tokenFile, "tokens", "", "Token 文件路径")
	flag.StringVar(&tokenFile, "t", "", "Token 文件路径")
	flag.Parse()

	DEBUG = debug

	period := time.Now().AddDate(0, 0, 1).Format("2006-01-02") + " 21:00:00"

	tokens, err := read(tokenFile)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(time.Now().Format("2006-01-02 15:04:05"))

	if submit {
		for _, token := range tokens {
			count := 100
			for count >= 0 {
				count--

				status, id, info, err := Send(period, token)
				if status != 200 || id == "" {
					fmt.Printf("Status %d, ID %s Info %s\n%s\n", status, id, info, err)
				} else {
					fmt.Println(id, info)
					break
				}
				time.Sleep(time.Second * 1)
			}
		}
	} else {
		for _, token := range tokens {
			status, id, err := Keep(token)
			if id == "" {
				fmt.Printf("Status %d, ID %s\n%s\n", status, id, err)
			} else {
				fmt.Println(id, "ok")
			}
		}

	}
	fmt.Printf("Finished at %s\n\n\n", time.Now().Format("2006-01-02 15:04:05"))
}
