

# AndroidAppLaunchTest

## 测试工具介绍

### /MokeyTest/ApplunchTest.py

应用启动时间自动化测试工具

用法：

1. 打开py工具，修改 'test env property' 为你本次测试的信息
   
   ``` python
   # test env property
   # 安装包地址
   apkfiledir = 'your apk file dir'
   # 应用包名
   packagename = 'com.iflytek.sample'
   # 默认入口activity 名称
   defaultactivity = '.MainActivity'
   #卸载安装首次启动时间测试次数
   reinstall_launch_time = 2
   #进程关闭首次启动时间测试次数
   stopapp_launch_time = 2
   ```
   
2. 通过monkeyrunner 运行该工具进行测试
   
   ``` 
   $ monkeyrunner [yourgitclonedir]//MokeyTest/ApplunchTest.py
   ```
   
   ​