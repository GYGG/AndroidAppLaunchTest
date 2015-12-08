#!/usr/bin/env python3
# coding=utf-8
from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
from com.android.monkeyrunner import MonkeyImage
import re

# test env property
# 安装包地址
apkfiledir = 'your apk file dir'
# 应用包名
packagename = 'com.iflytek.sample'
# 默认入口activity 名称
defaultactivity = '.MainActivity'
#卸载安装首次启动时间测试次数
reinstall_launch_time = 12
#进程关闭首次启动时间测试次数
stopapp_launch_time = 12
#非首次启动应用时间测试次数
relaunch_time = 12

print '测试参数:'
print 'apk file dir:    %s'%(apkfiledir)
print 'package name:    %s'%(packagename)
print 'activity:        %s'%(defaultactivity)

def reinstall(device, package, apk_dir):
    remove_result = device.removePackage(package)
    result =  device.installPackage(apk_dir)
    if not result :
        print 'error : 安装失败'
        return False
    return True


class AmStartResult(object):
    def __init__(self, status, thistime, totaltime):
        self.status = bool(status)
        self.thistime = int(thistime)
        self.totaltime = int(totaltime)
    def printself(self):
        print "[Status: %s | ThisTime: %s | TotalTime: %s]"%(self.status, self.thistime, self.totaltime)

def re_match(cmd_output):
    re_find_status = re.compile(r'Status:\s+([a-zA-Z]+)')
    re_find_thistime = re.compile(r'ThisTime:\s+([0-9]+)')
    re_find_totaltime = re.compile(r'TotalTime:\s+([0-9]+)')
    # 尝试用数据对象来返回解析结果
    status = re_find_status.findall(cmd_output)[0]
    thistime = re_find_thistime.findall(cmd_output)[0]
    totaltime = re_find_totaltime.findall(cmd_output)[0]
    result = AmStartResult(status, thistime, totaltime)
    return result

def test_am_start(package, activity, needstop):
    if needstop :
        # $ adb shell amkill
        device.shell('am kill %s'%(package))
    result = device.shell('am start -S -W -n %s/%s'%( package, activity))
    re_result = re_match(result)
    # re_result.printself()
    return re_result


def printresult(pcount, pmax, psum):
    if pcount != 0:
        mean = psum / pcount
    else :
        mean = 0
    print 'result: \n执行次数：%r\n峰值: %r\n均值: %r'%(pcount, pmax, mean)


def test_appstarttime(device, pkg, apk, activity, count, needreinstall, needkillP) :
    if 0 == count:
        return
    timelist = list()
    for i in range(count) :
        if i == 0 or needreinstall :
            if not reinstall(device, pkg, apk) :
                print "error : 安装失败，无法继续执行测试"
                return
        resultobj = test_am_start(pkg, activity, needkillP)

        if False == resultobj.status :
            print "error : am start 测试执行失败"
            return
        timelist.append(resultobj.thistime)
        resultobj.printself()
        MonkeyRunner.sleep(2)

    timelist.sort()
    if count <= 2 :
        printresult(count, timelist[-1], sum(timelist))
    else :
        print '超过2次。去掉一个最大值，去掉一个最小值'
        timelist = timelist[1:-1]
        printresult(count-2, timelist[-1], sum(timelist))




if __name__ == '__main__' :

    device = MonkeyRunner.waitForConnection()

    print 'start =====>'
    print '\n\nCASE 卸载安装重启启动时间.'
    test_appstarttime(device, packagename, apkfiledir, defaultactivity, reinstall_launch_time, True, True)
    print '\n\nCASE 进程关闭首次启动时间.'
    test_appstarttime(device, packagename, apkfiledir, defaultactivity, stopapp_launch_time, False, True)
    print '\n\nCASE 非首次启动时间测试次数.'
    test_appstarttime(device, packagename, apkfiledir, defaultactivity, relaunch_time, False, False)
