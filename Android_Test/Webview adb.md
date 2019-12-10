# Webview adb 调试

App 进入对应的 webview 页面，且开启 setWebContentsDebuggingEnabled 调试

1. adb shell cat /proc/net/unix | grep @

    ![https://img.mubu.com/document_image/1fbadff9-1086-4e16-8e05-d1407ecb47a7-3949851.jpg](https://img.mubu.com/document_image/1fbadff9-1086-4e16-8e05-d1407ecb47a7-3949851.jpg)

2. ps | grep 3593 查看对应的进程

    ![https://img.mubu.com/document_image/6ea51737-4cd3-4485-bcaf-b4460d0732b4-3949851.jpg](https://img.mubu.com/document_image/6ea51737-4cd3-4485-bcaf-b4460d0732b4-3949851.jpg)

3. adb forward tcp:7777 localabstract:webview_devtools_remote_3593

    ![https://img.mubu.com/document_image/2b39a42c-25f8-4b75-b670-97575f73e46d-3949851.jpg](https://img.mubu.com/document_image/2b39a42c-25f8-4b75-b670-97575f73e46d-3949851.jpg)

4. curl localhost:7777/json/version

    ![https://img.mubu.com/document_image/f8ea00dc-5b5e-4fd5-87cd-c523ac983222-3949851.jpg](https://img.mubu.com/document_image/f8ea00dc-5b5e-4fd5-87cd-c523ac983222-3949851.jpg)

输出如上内容，表示 webview debug 已经可以使用