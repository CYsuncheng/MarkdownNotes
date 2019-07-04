# Cookies and Session

## http无状态

OK，首先来明确下，这个状态的主体指的是什么？应该是信息，这些信息是由服务端所维护的与客户端交互的信息（也称为状态信息）； 因为HTTP本身是不保存任何用户的状态信息的，所以HTTP是无状态的协议。

## Cookie

Cookie是客户端保存用户信息的一种机制，用来记录用户的一些信息。如何识别特定的客户呢？cookie就可以做到。每次HTTP请求时，客户端都会发送相应的Cookie信息到服务端。它的过期时间可以任意设置，如果你不主动清除它，在很长一段时间里面都可以保留着，即便这之间你把电脑关机了。

### Cookie机制原理

客户端请求服务器时，如果服务器需要记录该用户状态，就使用response向客户端浏览器颁发一个Cookie。而客户端浏览器会把Cookie保存起来。当浏览器再请求服务器时，浏览器把请求的网址连同该Cookie一同提交给服务器。服务器通过检查该Cookie来获取用户状态。

## Session

与Cookie不同的是，session是以服务端保存状态的。<br />Session是在无状态的HTTP协议下，服务端记录用户状态时用于标识具体用户的机制。它是在服务端保存的用来跟踪用户的状态的数据结构，可以保存在文件、数据库或者集群中。在浏览器关闭后这次的Session就消失了，下次打开就不再拥有这个Session。其实并不是Session消失了，而是Session ID变了，服务器端可能还是存着你上次的Session ID及其Session 信息，只是他们是无主状态，也许一段时间后会被删除。<br />实际上Cookie与Session都是会话的一种方式。它们的典型使用场景比如“购物车”，当你点击下单按钮时，服务端并不清楚具体用户的具体操作，为了标识并跟踪该用户，了解购物车中有几样物品，服务端通过为该用户创建Cookie/Session来获取这些信息。

### session机制原理

当客户端请求创建一个session的时候，服务器会先检查这个客户端的请求里是否已包含了一个session标识 - sessionId，

- 如果已包含这个sessionId，则说明以前已经为此客户端创建过session，服务器就按照sessionId把这个session检索出来使用（如果检索不到，可能会新建一个）
- 如果客户端请求不包含sessionId，则为此客户端创建一个session并且生成一个与此session相关联的sessionId<br />
sessionId的值一般是一个既不会重复，又不容易被仿造的字符串，这个sessionId将被在本次响应中返回给客户端保存。保存sessionId的方式大多情况下用的是cookie。

## Cookie与Session的区别

1. cookie数据存放在客户的浏览器（客户端）上，session数据放在服务器上，但是服务端的session的实现对客户端的cookie有依赖关系的；
2. cookie不是很安全，别人可以分析存放在本地的COOKIE并进行COOKIE欺骗，考虑到安全应当使用session；
3. session会在一定时间内保存在服务器上。当访问增多，会比较占用你服务器的性能。考虑到减轻服务器性能方面，应当使用COOKIE；
4. 单个cookie在客户端的限制是3K，就是说一个站点在客户端存放的COOKIE不能超过3K；
