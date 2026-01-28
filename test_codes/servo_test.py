#!/usr/bin/env python3
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

SERVO_CH = 1  # サーボのチャンネル
CENTER_US = 1500  # 中央位置（マイクロ秒）
MIN_US = 1000     # 最小値（目安）
MAX_US = 2000     # 最大値（目安）

def set_position(pca, us: int) -> None:
    """サーボの位置をマイクロ秒で設定"""
    duty = int(us / 20000 * 65535)
    duty = max(0, min(65535, duty))
    pca.channels[SERVO_CH].duty_cycle = duty

def move_to(pca, us: int, wait: float = 0.5) -> None:
    """サーボを指定位置に移動"""
    print(f"Move to {us}us")
    set_position(pca, us)
    time.sleep(wait)  # サーボが移動する時間を確保

def center(pca) -> None:
    """サーボを中央位置に戻す"""
    print("Returning to center...")
    move_to(pca, CENTER_US, 1.0)

def sweep_range(pca, start_us: int, end_us: int, step: int = 50, delay: float = 0.3) -> None:
    """指定範囲をスイープして動作を確認"""
    print(f"\nSweeping from {start_us}us to {end_us}us (step: {step}us)")
    if start_us < end_us:
        range_us = range(start_us, end_us + 1, step)
    else:
        range_us = range(start_us, end_us - 1, -step)
    
    for us in range_us:
        print(f"  {us}us", end="", flush=True)
        set_position(pca, us)
        time.sleep(delay)
    print()

def find_limits(pca) -> tuple[int, int, int]:
    """インタラクティブにサーボの限界位置を探索"""
    print("\n=== Finding servo limits ===")
    print("Watch the servo movement and press Enter to continue, 'n' to stop")
    
    # 左方向（小さい値）を探索
    print("\n--- Testing RIGHT direction (smaller values) ---")
    right_limit = MIN_US
    for us in range(CENTER_US, MIN_US - 50, -50):
        move_to(pca, us, 1.0)
        response = input(f"  At {us}us - Continue? (Enter/n): ").strip().lower()
        if response == 'n':
            right_limit = us
            break
    else:
        right_limit = MIN_US
    
    center(pca)
    
    # 右方向（大きい値）を探索
    print("\n--- Testing LEFT direction (larger values) ---")
    left_limit = MAX_US
    for us in range(CENTER_US, MAX_US + 50, 50):
        move_to(pca, us, 1.0)
        response = input(f"  At {us}us - Continue? (Enter/n): ").strip().lower()
        if response == 'n':
            left_limit = us
            break
    else:
        left_limit = MAX_US
    
    # 中央位置を確認
    print("\n--- Finding neutral/center position ---")
    center_us = CENTER_US
    move_to(pca, CENTER_US, 1.0)
    response = input(f"  Is {CENTER_US}us the center? (Enter to confirm, or enter value): ").strip()
    if response:
        try:
            center_us = int(response)
            move_to(pca, center_us, 1.0)
        except ValueError:
            pass
    
    return right_limit, center_us, left_limit

def test_found_values(pca, left: int, center: int, right: int) -> None:
    """見つけた値をテスト"""
    print(f"\n=== Testing found values ===")
    print(f"LEFT: {left}us, CENTER: {center}us, RIGHT: {right}us")
    
    move_to(pca, center, 2.0)
    move_to(pca, left, 2.0)
    move_to(pca, center, 2.0)
    move_to(pca, right, 2.0)
    move_to(pca, center, 2.0)
    
    print("\nSmooth sweep test:")
    sweep_range(pca, left, right, step=20, delay=0.1)
    center(pca)

def main() -> None:
    print("=== Servo Motor Test ===")
    print("Finding neutral position and operating range.")
    print("Ctrl+C to stop anytime.\n")

    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50  # 50Hz for servos

    try:
        # 初期化：中央位置に移動
        print("Initializing to center position...")
        center(pca)
        time.sleep(1.0)

        # 範囲を探索
        left, center_val, right = find_limits(pca)
        
        # 見つけた値をテスト
        test_found_values(pca, left, center_val, right)

        # 結果を表示
        print("\n" + "="*50)
        print("FINAL VALUES:")
        print(f"  LEFT (full left):   {left}us")
        print(f"  CENTER (neutral):   {center_val}us")
        print(f"  RIGHT (full right): {right}us")
        print(f"  RANGE: {right - left}us ({left - center_val}us left, {right - center_val}us right)")
        print("="*50)

    except KeyboardInterrupt:
        print("\n[Interrupted by user]")
    finally:
        try:
            center(pca)
        except Exception:
            pass
        pca.deinit()
        print("\nServo returned to center. Deinitialized.")

if __name__ == "__main__":
    main()