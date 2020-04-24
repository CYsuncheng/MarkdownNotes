# Docker 命令

<a name="8wMZe"></a>
## 常用命令
**下载镜像**<br />`docker pull jenkins/jenkins`<br />**查看已下载的镜像**<br />
<br />`docker image`<br />![image.png](https://cdn.nlark.com/yuque/0/2020/png/125389/1587725556468-8f6c329f-90fa-4c27-b98e-f7375ec84b3e.png#align=left&display=inline&height=271&margin=%5Bobject%20Object%5D&name=image.png&originHeight=542&originWidth=1696&size=334038&status=done&style=none&width=848)<br />那么，其中的每个字段又是什么意思呢？

| 字段名 | 含义 |
| :--- | :--- |
| `REPOSITORY` | `REPOSITORY` |
| `TAG` | 镜像的版本号，用来指定下载的版本 |
| `IMAGE ID` | 镜像的唯一标识ID |
| `CREATED` | 镜像的制作时间 |
| `SIZE` | 镜像的所占的磁盘空间 |

**删除镜像**<br />`docker rmi jenkins/IMAGE ID`<br />**下载指定版本的镜像**<br />`docker pull jenkins:3.1.x`<br />**将镜像打包成一个tar包**<br />`docker save jenkins:2.60.3 > myjenkins.tar`<br />![image.png](https://cdn.nlark.com/yuque/0/2020/png/125389/1587725713355-99f6fd6d-5e9c-48c5-bb73-94e46522855c.png#align=left&display=inline&height=84&margin=%5Bobject%20Object%5D&name=image.png&originHeight=168&originWidth=1688&size=114474&status=done&style=none&width=844)<br />**将打包的镜像加载出来**<br />`docker load < myjenkins.tar`<br />![image.png](https://cdn.nlark.com/yuque/0/2020/png/125389/1587725726846-9c314c54-bf7c-4e21-9654-c46369b019d7.png#align=left&display=inline&height=231&margin=%5Bobject%20Object%5D&name=image.png&originHeight=462&originWidth=1704&size=306281&status=done&style=none&width=852)<br />**给镜像加tag号**<br />`docker tag jenkins:latest jenkins:3.6.0`<br />![image.png](https://cdn.nlark.com/yuque/0/2020/png/125389/1587725772719-30fb7e02-04ae-41e1-855d-88bc14e9f9b1.png#align=left&display=inline&height=389&margin=%5Bobject%20Object%5D&name=image.png&originHeight=778&originWidth=1720&size=438232&status=done&style=none&width=860)<br />**给镜像改名称**<br />`docker tag jenkins:latest testjenkins`<br />![image.png](https://cdn.nlark.com/yuque/0/2020/png/125389/1587725811111-dd367c38-7b15-4a8e-9c45-205a6080929b.png#align=left&display=inline&height=165&margin=%5Bobject%20Object%5D&name=image.png&originHeight=330&originWidth=1720&size=197969&status=done&style=none&width=860)<br />**push镜像到镜像仓库**<br />`docker tag jenkins gaofei_com/jenkins`<br />`docker push`
<a name="MLeEM"></a>
## 容器命令
**容器运行命令参数**
```
1. --name 指定容器名称
2. -d 后台运行
3. -port 指定端口映射规则
4. --network 指定容器运行的网路模式
5. -v 指定需要挂载的数据卷
6. -env  指定需要传递给容器的环境变量
```
**容器管理命令参数**
```
1. docker run --name={your_name} --d {image_name}  (运行容器)
2. docker ps -s -a  {查看当前所有容器}
3. docker stop {container_name}  (停止容器)
4. docker kill (container_name) {杀死容器}
5. docker rm -f {container_name/id}  (删除容器)  
6. docker ps -s (-s表明size)
```
接下来我们继续使用Jenkins进行一个实战的演练<br />

```
#启动运行容器
docker run -d --name=myjenkins jenkins/jenkins
#查看当前运行中的容器
docker ps
```
`docker ps`也是我们常用的一个命令，下面是`docker ps`后显示的启动容器信息，其中每个字段都有自己的含义<br />![image.png](https://cdn.nlark.com/yuque/0/2020/png/125389/1587725984930-d22c3704-8dba-4518-a385-b04fb8a0c5bd.png#align=left&display=inline&height=93&margin=%5Bobject%20Object%5D&name=image.png&originHeight=186&originWidth=1708&size=134868&status=done&style=none&width=854)

| 字段名 | 含义 |
| :--- | :--- |
| `CONTAINER ID` | 容器ID(和image ID无关) |
| `IMAGE` | 启动容器的镜像 |
| `COMMAND` | 容器的启动命令 |
| `CREATED` | 创建时间 |
| `STATUS` | 当前状态 |
| `PORTS` | 容器对外暴露的端口号 |
| `NAMES` | 容器名称 |

`CONTAINER ID`:容器ID(和image ID无关)<br />如何删除这个启动的容器呢？是否可以和镜像一样，直接`rm`呢？
```
docker rm myjenkins
```
从图中我们可以看到,如果直接删除运行中的容器会报错，需要`先stop然后删除`
```
docker stop myjenkins
docker rm myjenkins
```
![image.png](https://cdn.nlark.com/yuque/0/2020/png/125389/1587726050250-b7bb8b37-85fb-49ff-a863-5305f223860e.png#align=left&display=inline&height=170&margin=%5Bobject%20Object%5D&name=image.png&originHeight=340&originWidth=1318&size=124034&status=done&style=none&width=659)<br />或者直接
```
docker rm -f myjenkins
```
我们从图片中可以看出，虽然这个容器是启动的状态，但是使用`docker rm -f`依然可以直接删除<br />[![](https://cdn.nlark.com/yuque/0/2020/png/125389/1587726061907-f0c1d498-990f-48c8-aa05-8302dca2c47c.png#align=left&display=inline&height=96&margin=%5Bobject%20Object%5D&originHeight=96&originWidth=955&size=0&status=done&style=none&width=955)](https://testerhome.com/uploads/photo/2019/ae9fe41a-4cd6-4b9f-a060-89d19b8f5f44.png!large)<br />在docker ps 的时候我们可以看到，`PORTS`字段下面显示了两个端口号，这两个端口号是做什么的呢？<br />其实呀，这两个端口号，是容器故意对外暴露的端口号，我们可以通过`端口映射`的方式，使容器内部的端口号与宿主机的某个端口号产生链接。这样我们就可以通过端口号，去访问或者操作容器啦<br />[![](https://cdn.nlark.com/yuque/0/2020/png/125389/1587726077088-7f0be84a-0bbc-4b44-a529-5f6ced2d0662.png#align=left&display=inline&height=106&margin=%5Bobject%20Object%5D&originHeight=106&originWidth=702&size=0&status=done&style=none&width=702)](https://testerhome.com/uploads/photo/2019/e2db9f54-04e7-4971-ad26-a6f4d74bb118.png!large)<br />如何指定端口号呢？就是使用 `-p` 参数
```
docker run -d --name=myjenkins -p 8080:8080 jenkins/jenkins
```
将宿主机的8080端口指向容器的8080端口，这样我们在宿主机的8080端口就可以访问到Jenkins啦<br />[![](https://cdn.nlark.com/yuque/0/2020/png/125389/1587726107051-e4cff7da-7164-4951-82e7-3496f26c9560.png#align=left&display=inline&height=395&margin=%5Bobject%20Object%5D&originHeight=395&originWidth=1121&size=0&status=done&style=none&width=1121)](https://testerhome.com/uploads/photo/2019/b2fb6749-112a-445c-b50a-247a733a2c1e.png!large)<br />在启动的过程中，我们可能会碰到各种各样的问题，我们如何定位问题呢？<br />当然是使用`查看log大法`
```
docker log -f myjenkins
```
[![](https://cdn.nlark.com/yuque/0/2020/png/125389/1587726106848-6930c581-5d36-4cfc-82e6-acf8363ce824.png#align=left&display=inline&height=329&margin=%5Bobject%20Object%5D&originHeight=329&originWidth=999&size=0&status=done&style=none&width=999)](https://testerhome.com/uploads/photo/2019/ccacc216-4269-4bd0-81c7-bd9aa57057db.png!large)
<a name="ClBx3"></a>
## Docker的数据持久化
可能有同学会有疑虑啦，如果docker挂掉，在docker内产生的数据应该怎么办呢，`这些数据应该如何保存呢`<br />接下来，我们要了解的，docker是如何进行数据持久化的呢？<br />当我们启动容器时，添加了数据挂载的参数`-v 宿主机_path:container_path`,docker就可以通过数据挂载的方式，使容器和宿主机的数据进行`同步`保存<br />[原文链接](https://testerhome.com/topics/21806)
