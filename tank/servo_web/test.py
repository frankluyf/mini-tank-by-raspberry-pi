#!/usr/bin/env python3
import time
from pathlib import Path

# ====== Pi 5 上 GPIO18/19 映射到 pwmchip2 的 pwm2/pwm3 ======
PWMCHIP   = 2
PWM_YAW   = 2   # GPIO18
PWM_PITCH = 3   # GPIO19

# ====== 舵机 PWM 参数 ======
PERIOD_NS = 20_000_000   # 20ms -> 50Hz
PULSE_MIN = 1_000_000    # 1.0ms
PULSE_MAX = 2_000_000    # 2.0ms

# ====== 角度限制（你的 SERVO_LIMIT）=====
YAW_MIN,   YAW_MAX   = 10, 131
PITCH_MIN, PITCH_MAX = 20, 160

STEP_DEG   = 2
STEP_DELAY = 0.02

BASE = Path(f"/sys/class/pwm/pwmchip{PWMCHIP}")

def sysfs_write(path: Path, value):
    with open(path, "w") as f:
        f.write(f"{value}\n")

def export_channel(idx: int) -> Path:
    pwm_path = BASE / f"pwm{idx}"
    if not pwm_path.exists():
        sysfs_write(BASE / "export", idx)
        for _ in range(100):
            if pwm_path.exists():
                break
            time.sleep(0.01)
        else:
            raise RuntimeError(f"{pwm_path} didn't appear")
    return pwm_path

def setup_pwm(pwm_path: Path):
    # 顺序必须：disable -> period -> duty_cycle -> enable
    sysfs_write(pwm_path / "enable", 0)
    sysfs_write(pwm_path / "period", PERIOD_NS)
    sysfs_write(pwm_path / "duty_cycle", PULSE_MIN)  # duty 必须 < period
    sysfs_write(pwm_path / "enable", 1)

def angle_to_pulse_ns(angle: float) -> int:
    angle = max(0, min(180, angle))
    return int(PULSE_MIN + (angle / 180.0) * (PULSE_MAX - PULSE_MIN))

def set_angle(pwm_path: Path, angle: float):
    sysfs_write(pwm_path / "duty_cycle", angle_to_pulse_ns(angle))

def sweep_one(pwm_path: Path, a_min: int, a_max: int, step: int, delay: float):
    for a in range(a_min, a_max + 1, step):
        set_angle(pwm_path, a)
        time.sleep(delay)
    for a in range(a_max, a_min - 1, -step):
        set_angle(pwm_path, a)
        time.sleep(delay)

def cleanup(*pwm_paths):
    for p in pwm_paths:
        try:
            sysfs_write(p / "enable", 0)
        except Exception:
            pass

def main():
    yaw_pwm   = export_channel(PWM_YAW)
    pitch_pwm = export_channel(PWM_PITCH)

    print(f"YAW   -> {yaw_pwm} (GPIO18) sweep {YAW_MIN}~{YAW_MAX}°")
    print(f"PITCH -> {pitch_pwm} (GPIO19) sweep {PITCH_MIN}~{PITCH_MAX}°")

    setup_pwm(yaw_pwm)
    setup_pwm(pitch_pwm)

    try:
        yaw_mid   = (YAW_MIN + YAW_MAX) // 2
        pitch_mid = (PITCH_MIN + PITCH_MAX) // 2

        # 回中
        set_angle(yaw_pwm, yaw_mid)
        set_angle(pitch_pwm, pitch_mid)
        time.sleep(0.5)

        print("Sweeping yaw ...")
        sweep_one(yaw_pwm, YAW_MIN, YAW_MAX, STEP_DEG, STEP_DELAY)

        print("Sweeping pitch ...")
        sweep_one(pitch_pwm, PITCH_MIN, PITCH_MAX, STEP_DEG, STEP_DELAY)

        # 回中
        set_angle(yaw_pwm, yaw_mid)
        set_angle(pitch_pwm, pitch_mid)
        time.sleep(0.5)

    finally:
        cleanup(yaw_pwm, pitch_pwm)

if __name__ == "__main__":
    main()
