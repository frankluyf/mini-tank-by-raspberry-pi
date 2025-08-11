from gpiozero import OutputDevice
import time

# 定义电机引脚
# 和您提供的一样，如果方向不对，请调整下面的函数
motors = {
    "M1": (OutputDevice(17), OutputDevice(27)),  # 右前轮
    "M2": (OutputDevice(23), OutputDevice(24)),  # 左前轮
    "M3": (OutputDevice(5), OutputDevice(6)),    # 左后轮
    "M4": (OutputDevice(26), OutputDevice(16)),  # 右后轮
}

# --- 电机控制函数 ---

def stop():
    """停止所有电机"""
    for motor_pins in motors.values():
        motor_pins[0].off()
        motor_pins[1].off()

def forward():
    """所有轮子向前转，小车前进"""
    motors["M1"][0].on()
    motors["M1"][1].off()
    motors["M2"][0].on()
    motors["M2"][1].off()
    motors["M3"][0].on()
    motors["M3"][1].off()
    motors["M4"][0].on()
    motors["M4"][1].off()

def backward():
    """所有轮子向后转，小车后退"""
    motors["M1"][0].off()
    motors["M1"][1].on()
    motors["M2"][0].off()
    motors["M2"][1].on()
    motors["M3"][0].off()
    motors["M3"][1].on()
    motors["M4"][0].off()
    motors["M4"][1].on()

def strafe_left():
    """左平移"""
    motors["M1"][0].on()   # 右前轮向前
    motors["M1"][1].off()
    motors["M2"][0].off()  # 左前轮向后
    motors["M2"][1].on()
    motors["M3"][0].on()   # 左后轮向前
    motors["M3"][1].off()
    motors["M4"][0].off()  # 右后轮向后
    motors["M4"][1].on()

def strafe_right():
    """右平移"""
    motors["M1"][0].off()  # 右前轮向后
    motors["M1"][1].on()
    motors["M2"][0].on()   # 左前轮向前
    motors["M2"][1].off()
    motors["M3"][0].off()  # 左后轮向后
    motors["M3"][1].on()
    motors["M4"][0].on()   # 右后轮向前
    motors["M4"][1].off()


# --- 主程序 ---
if __name__ == "__main__":
    print("自动控制程序启动...")
    # 使用 try...finally 来确保无论程序如何退出，电机都会停止
    try:
        # 动作序列
        print("步骤 1: 向前移动 5 秒...")
        forward()
        time.sleep(5)

        print("步骤 2: 停止 5 秒...")
        stop()
        time.sleep(5)

        print("步骤 3: 向后移动 5 秒...")
        backward()
        time.sleep(5)

        print("步骤 4: 停止 5 秒...")
        stop()
        time.sleep(5)

        print("步骤 5: 向左平移 5 秒...")
        strafe_left()
        time.sleep(5)

        print("步骤 6: 停止 5 秒...")
        stop()
        time.sleep(5)

        print("步骤 7: 向右平移 5 秒...")
        strafe_right()
        time.sleep(5)

        print("\n所有动作执行完毕，程序结束。")

    except KeyboardInterrupt:
        # 如果用户按 Ctrl+C 中断程序，也会执行 finally
        print("\n程序被用户中断。")
    except Exception as e:
        # 捕获其他可能的错误
        print(f"发生错误: {e}")
    finally:
        # 最后的安全保障：确保所有电机都已停止
        print("执行最终清理：停止所有电机。")
        stop()