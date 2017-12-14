import time

time.sleep(5)
try:
    q1 = driver.find_element_by_name("我的设备")
    print("登录成功")
    el = driver.find_element_by_name("com.ustcinfo.f.ch:id/iv_add")    #定位要按压的元素
    TouchAction(driver).press(el).release().perform    #执行按压操作
    try:
        q2 = driver.find_element_by_name("添加设备")
        print("进入添加设备页面")
