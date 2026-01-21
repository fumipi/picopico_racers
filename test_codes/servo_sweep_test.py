import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

CH = 1  # ステアリングがch1なら1

def set_count(count):
    count = max(0, min(4095, int(count)))
    # duty_cycleは16bitなので 12bitを16bitに拡大
    pca.channels[CH].duty_cycle = count << 4

try:
    center = 307  # 1500us相当（サーボのセンター目安）
    set_count(center)
    time.sleep(1)

    # 右方向（countを減らす/増やすはサーボの向きで逆なので両方試す）
    for c in [300, 290, 280, 270, 260, 250, 240, 230]:
        print("try", c)
        set_count(c)
        time.sleep(1)

    set_count(center)
    time.sleep(1)

    for c in [320, 340, 360, 380, 400, 420, 440]:
        print("try", c)
        set_count(c)
        time.sleep(1)

finally:
    set_count(center)
    time.sleep(0.5)
    pca.deinit()
