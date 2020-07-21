# Untitled - By: lzbqr - 周五 6月 12 2020

import video, sensor, image, lcd, time,os

lcd.init()
lcd.rotation(2)
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.set_vflip(1)
sensor.skip_frames(30)

vedio_flag=0
dir_name=os.listdir()
print(dir_name)
for i_name in dir_name:
    if i_name == 'vedio':
        vedio_flag=1
if vedio_flag==0:
    os.mkdir('vedio')
dir_name=os.listdir()
print(dir_name)

v_rec = video.open("/sd/vedio/capture1.avi", record=1, interval=66000, quality=50)
j_video=1
i_frame=0
tim = time.ticks_ms()

while True:
    tim = time.ticks_ms()
    img = sensor.snapshot()
    lcd.display(img)
    img_len = v_rec.record(img)
    print("record",j_video,time.ticks_ms() - tim)
    i_frame += 1
    if i_frame == 75:
        print("finish:",j_video)
        j_video+=1
        v_rec.record_finish()
        i_frame=0
        v_rec = video.open("/sd/vedio/capture"+str(j_video)+".avi", record=1, interval=66000, quality=50)
