curl 是一个利用 URL 语法在命令行下工作的文件传输工具。它支持文件上传和下载，所以是综合传输工具，但按传统，习惯称 curl 为下载工具。其语法格式及常见参数含义如下，

```
# 语法
curl [option] [url]

# 最简单的使用，获取服务器内容，默认将输出打印到标准输出中(STDOUT)中。
curl http://www.centos.org

# 添加-v 参数可以看到详细解析过程，通常用于 debug
curl -v http://www.centos.org

# curl 发送 Get 请求
curl URL
curl URL -O 文件绝对路径
 
# curl 发送 post 请求

# 请求主体用 json 格式
curl -X POST -H 'content-type: application/json' -d @json 文件绝对路径 URL
curl -X POST -H 'content-type: application/json' -d 'json 内容' URL
# 请求主体用 xml 格式
curl -X POST -H 'content-type: application/xml' -d @xml 文件绝对路径 URL
curl -X POST -H 'content-type: application/xml' -d 'xml 内容' URL
 
# 设置 cookies
curl URL --cookie "cookie 内容"
curl URL --cookie-jar cookie 文件绝对路径
 
# 设置代理字符串
curl URL --user-agent "代理内容"
curl URL -A "代理内容"
 
# curl 限制带宽
curl URL --limit-rate 速度
 
# curl 认证
curl -u user:pwd URL
curl -u user URL
 
# 只打印 http 头部信息
curl -I URL
curl -head URL

# 末尾参数
--progress  显示进度条
--silent    不现实进度条

# 不需要修改 /etc/hosts，curl 直接解析 ip 请求域名
# 将 http://example.com 或 https://example.com 请求指定域名解析的 IP 为 127.0.0.1
curl --resolve example.com:80:127.0.0.1 http://example.com/
curl --resolve example.com:443:127.0.0.1 https://example.com/
```

curl 可以很方便地完成对 REST API 的调用场景，比如：设置 Header，指定 HTTP 请求方法，指定 HTTP 消息体，指定权限认证信息等。通过 -v 选项也能输出 REST 请求的所有返回信息。curl 功能很强大，有很多参数，这里列出 REST 测试常用的参数：

```
-X/--request [GET|POST|PUT|DELETE|…]  指定请求的 HTTP 方法
-H/--header                           指定请求的 HTTP Header
-d/--data                             指定请求的 HTTP 消息体（ Body ）
-v/--verbose                          输出详细的返回信息
-u/--user                             指定账号、密码
-b/--cookie                           读取 cookie  

# 典型的测试命令为：
curl -v -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/user -d'{"username":"admin","password":"admin1234"}'...

# 测试 get 请求
curl http://www.linuxidc.com/login.cgi?user=test001&password=123456

# 测试 post 请求
curl -d "user=nickwolfe&password=12345" http://www.linuxidc.com/login.cgi

# 请求主体用 json 格式
curl -X POST -H 'content-type: application/json' -d @json 文件绝对路径 URL
curl -X POST -H 'content-type: application/json' -d 'json 内容' URL
 
# 请求主体用 xml 格式
curl -X POST -H 'content-type: application/xml' -d @xml 文件绝对路径 URL
curl -X POST -H 'content-type: application/xml' -d 'xml 内容' URL

# 发送 post 请求时需要使用-X 选项，除了使用 POST 外，还可以使用 http 规范定义的其它请求谓词，如 PUT,DELETE 等
curl -XPOST url

#发送 post 请求时，通常需要指定请求体数据。可以使用-d 或--data 来指定发送的请求体。
curl -XPOST -d "name=leo&age=12" url

# 如果需要对请求数据进行 urlencode,可以使用下面的方式：
curl -XPOST --data-urlencode "name=leo&age=12" url

# 此外发送 post 请求还可以有如下几种子选项：
–data-raw
–data-ascii
–data-binary
```

使用 curl 和 Jenkins REST API

```
# To retrieve the job config.xml
curl -X GET '<jenkinshost>/job/<jobname>/config.xml' -u username:API_TOKEN -o <jobname>.xml

# to use this config to create a new job
curl -s -XPOST '<jenkinshost>/createItem?name=<jobname>' -u username:API_TOKEN --data-binary @<jobname>.xml -H "Content-Type:text/xml"

# get all jenkins jobs
curl -X GET '<jenkinshost>/api/json?pretty=true' -u username:API_TOKEN -o jobs.json

# get jenkins view
curl -X GET '<jenkinshost>/view/<viewname>/api/json' -u username:API_TOKEN -o view.json
```