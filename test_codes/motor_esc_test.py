#!/usr/bin/env python3
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

ESC_CH = 0
STOP = 1500
FWD  = 1370   # 前進（1400しきい値より余裕）
REV  = 1610   # 後退（1580しきい値より余裕）

def set_us(pca, us: int) -> None:
    duty = int(us / 20000 * 65535)
    duty = max(0, min(65535, duty))
    pca.channels[ESC_CH].duty_cycle = duty

def hold(pca, us: int, sec: float) -> None:
    print(f"HOLD {us}us for {sec:.1f}s")
    set_us(pca, us)
    time.sleep(sec)

def safe_stop(pca) -> None:
    set_us(pca, STOP)
    time.sleep(5.0)

def main() -> None:
    print("=== Confirm FINAL (STOP/FWD/REV) ===")
    print("Wheels off ground. ESC ON (beep side). Ctrl+C anytime.\n")

    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50

    try:
        hold(pca, STOP, 5.0)

        print("\nForward (should go forward)")
        hold(pca, FWD, 1.0)
        safe_stop(pca)

        print("\nReverse (should go backward)")
        hold(pca, REV, 1.0)
        safe_stop(pca)

        print("\nDone.")
        safe_stop(pca)

    except KeyboardInterrupt:
        print("\n[Stopped]")
    finally:
        try:
            safe_stop(pca)
        except Exception:
            pass
        pca.deinit()
        print("Back to STOP and deinit done.")

if __name__ == "__main__":
    main()
