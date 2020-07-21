#实验名称：物品检测
#翻译和注释：01Studio
#实验目的：使用class模型识别20种物体

import sensor,image,lcd,time
import KPU as kpu

#摄像头初始化
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
sensor.set_auto_gain(1)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)  #摄像头后置方式

lcd.init() #LCD初始化

clock = time.clock()

#模型分类，按照class顺序
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

#下面语句需要将模型（class.kfpkg）烧写到flash的 0x500000 位置
#task = kpu.load(0x400000)

#将模型放在SD卡中。
task = kpu.load("/sd/class.kmodel") #模型SD卡上

#网络参数
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

#初始化yolo2网络，识别可信概率为0.7（70%）
a = kpu.init_yolo2(task, 0.7, 0.3, 5, anchor)

while(True):

    clock.tick()

    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img) #运行yolo2网络


    if code:
        for i in code:
            a=img.draw_rectangle(i.rect())

            img.draw_string(i.x(), i.y(), classes[i.classid()], color=(230,125,0), scale=2, mono_space=0)
            img.draw_string(i.x(), i.y()+12, '%f1.3'%i.value(), color=(230,150,0), scale=2, mono_space=0)
            fps =clock.fps()
            #显示帧率
            img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0,128,0), scale=2)
            lcd.rotation(2)
            a = lcd.display(img)


    else:
        fps =clock.fps()
        #显示帧率
        img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0,128,0), scale=2)
        lcd.rotation(2)
        a = lcd.display(img)

    #print(clock.fps())#打印FPS

