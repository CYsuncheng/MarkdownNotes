# PostMan 

## 接口断言
### 断言响应时间
``` javascript
pm.test("Response time is less than 200ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});
// 断言响应事件小于200ms
```

### 断言状态码
``` javascript
pm.test("Successful POST request", function () {
    pm.expect(pm.response.code).to.be.oneOf([200,202]);
});
// 断言状态码200-202区间
```

### 断言响应中包含某个字符串
``` javascript
pm.test("Body matches string", function () {
    pm.expect(pm.response.text()).to.include("ok");
});

// 断言响应中包含"ok"
```

### 断言响应中的字段等于某个值
``` javascript
pm.test("message test", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData["message"]).to.eql("ok");
});

// 断言响应中"message" = ok"
```

### 断言响应中的字段不等于某个值
``` javascript
var jsonData = JSON.parse(responseBody);
tests["message不为bad"] = jsonData["message"] != "bad";

// 断言响应中"message" != bad"
```

### 断言响应中的列表长度
``` javascript
pm.test("data list test", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData["data"].length).to.eql(41);
});

// 断言响应中"list"的字段长度
```

### 断言响应中的列表中第几个元素的字段值
``` javascript
pm.test("data list 0 test", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData["data"][0]["time"]).to.eql("2018-11-28 17:27:41");
});

// 断言响应中"list 0的"的time字段的值
```

## 测试前准备
发送请求之前往往需要准备数据,比如设置header中参数或者计算签名.
使用Pre-request Script可以编写一些准备数据。

[Postman 使用](https://mp.weixin.qq.com/s/7NpWxzXRUUf-JwIoeK0N7g)