#!/usr/bin/env python3
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

SERVO_CH = 1        # サーボのチャンネル
CENTER_US = 1500    # テストするパルス幅（マイクロ秒）
HOLD_SEC = 15.0     # どれくらい保持するか（秒）


def set_position(pca, us: int) -> None:
    """サーボの位置をマイクロ秒で設定（20ms周期前提）"""
    duty = int(us / 20000 * 65535)
    duty = max(0, min(65535, duty))
    pca.channels[SERVO_CH].duty_cycle = duty


def hold_center(pca, sec: float) -> None:
    """1500us を指定秒数だけ出力し続ける"""
    print(f"Set CH{SERVO_CH} to {CENTER_US}us and hold for {sec:.1f}s")
    set_position(pca, CENTER_US)
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed >= sec:
            break
        print(f"  elapsed: {elapsed:4.1f}s / {sec:.1f}s", end="\r", flush=True)
        time.sleep(1.0)
    print()


def main() -> None:
    print("=== Servo 1500us HOLD Test ===")
    print(f"Channel: {SERVO_CH}, Pulse: {CENTER_US}us, Duration: {HOLD_SEC:.1f}s")
    print("Ctrl+C to stop anytime.\n")

    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50  # サーボ用 50Hz

    try:
        hold_center(pca, HOLD_SEC)
        print("Done. Keeping servo at 1500us for now.")
        time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n[Interrupted by user]")
    finally:
        try:
            set_position(pca, CENTER_US)
        except Exception:
            pass
        pca.deinit()
        print("Servo at 1500us. PCA9685 deinitialized.")


if __name__ == "__main__":
    main()