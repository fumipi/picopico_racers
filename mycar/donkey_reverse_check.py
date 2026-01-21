import time
import donkeycar as dk
from donkeycar.parts.actuator import PWMThrottle
from donkeycar.parts.pins import pwm_pin_by_id
from donkeycar.parts.actuator import PulseController

# あなたの配線（ESCはch0）
PIN = "PCA9685.1:40.0"

# あなたが確定させた 12bit値（0..4095換算ではなく、DonkeyのPCA9685 12bit(0..4095)想定の値）
# ※あなたがいま使っているのは「0..1000系」(例:307,324,287)なのでそのまま使います
STOP = 307   # 1500us
FWD  = 324   # 1580us（あなたの車ではこの向きに回る）
REV  = 287   # 1400us（反対向き）

# Donkeyのpinsは frequency_hz のデフォルトが60なので、ここで明示的に 50Hz にする
pwm_pin = pwm_pin_by_id(PIN, frequency_hz=50)
ctl = PulseController(pwm_pin, pwm_scale=1.0, pwm_inverted=False)

thr = PWMThrottle(controller=ctl, max_pulse=FWD, min_pulse=REV, zero_pulse=STOP)

def hold(label, val, sec=1.0):
    print(label, val)
    thr.run(val)
    time.sleep(sec)

print("Neutral")
hold("t=0.0", 0.0, 2.0)

print("Forward(+)")
hold("t=+0.5", +0.5, 1.0)
hold("t=0.0", 0.0, 1.0)

print("Reverse(-)")
hold("t=-0.5", -0.5, 1.0)
hold("t=0.0", 0.0, 2.0)

print("done")
