### 列出你安装的所有可用的设备
xcrun instruments -s

### 启动指定的模拟器
xcrun instruments -w "iPhone 8 (11.2)"

### 安装指定的app
xcrun simctl install booted <app路径>

### 运行指定的app
xcrun simctl launch booted <com.example.app>

### 卸载指定的应用
xcrun simctl uninstall booted <com.example.app>

### 安装卸载
ideviceinstaller -u [udid] -i [xxx.ipa]   # 给指定连接的设备安装应用
ideviceinstaller -u [udid] -U [bundleId]   # 给指定连接的设备卸载应用

### 查看连接设备
idevice_id -l               # 显示当前所连接的设备[udid]，包括 usb、WiFi 连接
instruments -s devices      # 列出设备包括模拟器、真机及 mac 电脑本身

### 查看设备已安装的应用
ideviceinstaller -u [udid] -l                   # 指定设备，查看安装的第三方应用
ideviceinstaller -u [udid] -l -o list_user      # 指定设备，查看安装的第三方应用
ideviceinstaller -u [udid] -l -o list_system    # 指定设备，查看安装的系统应用
ideviceinstaller -u [udid] -l -o list_all       # 指定设备，查看安装的系统应用和第三方应用

### 获取设备信息
ideviceinfo -u [udid]                       # 指定设备，获取设备信息
ideviceinfo -u [udid] -k DeviceName         # 指定设备，获取设备名称：iPhone6s
idevicename -u [udid]                       # 指定设备，获取设备名称：iPhone6s
ideviceinfo -u [udid] -k ProductVersion     # 指定设备，获取设备版本：10.3.1
ideviceinfo -u [udid] -k ProductType        # 指定设备，获取设备类型：iPhone8,1
ideviceinfo -u [udid] -k ProductName        # 指定设备，获取设备系统名称：iPhone OS

