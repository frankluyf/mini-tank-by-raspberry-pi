from gpiozero import OutputDevice
from time import sleep
from rpi5_ws2812.ws2812 import Color, WS2812SpiDriver

# 初始化 WS2812 灯带
led_count = 8
strip = WS2812SpiDriver(spi_bus=0, spi_device=0, led_count=led_count).get_strip()
strip.set_brightness(0.1)

def set_all_leds(color: Color):
    for i in range(led_count):
        strip.set_pixel_color(i, color)
    strip.show()

# 初始状态设为绿色（就绪）
set_all_leds(Color(0, 255, 0))

# 发射控制引脚
fire_pin = OutputDevice(22)

def fire():
    set_all_leds(Color(255, 0, 0))  # 发射前变红
    fire_pin.on()
    sleep(0.1)  # 保持 100ms
    fire_pin.off()
    set_all_leds(Color(0, 255, 0))  # 发射后变绿

# 定义电机引脚
motors = {
    "M1": (OutputDevice(27), OutputDevice(17)),  # 右前轮
    "M2": (OutputDevice(23), OutputDevice(24)),  # 左前轮
    "M3": (OutputDevice(5), OutputDevice(6)),    # 左后轮
    "M4": (OutputDevice(26), OutputDevice(16)),  # 右后轮
}

def stop():
    for motor_pins in motors.values():
        motor_pins[0].off()
        motor_pins[1].off()

def forward():
    motors["M1"][0].off(); motors["M1"][1].on()
    motors["M2"][0].on(); motors["M2"][1].off()
    motors["M3"][0].off(); motors["M3"][1].on()
    motors["M4"][0].on(); motors["M4"][1].off()

def backward():
    motors["M1"][0].on(); motors["M1"][1].off()
    motors["M2"][0].off(); motors["M2"][1].on()
    motors["M3"][0].on(); motors["M3"][1].off()
    motors["M4"][0].off(); motors["M4"][1].on()

def strafe_left():
    motors["M1"][0].off(); motors["M1"][1].on()
    motors["M2"][0].off(); motors["M2"][1].on()
    motors["M3"][0].off(); motors["M3"][1].on()
    motors["M4"][0].off(); motors["M4"][1].on()

def strafe_right():
    motors["M1"][0].on(); motors["M1"][1].off()
    motors["M2"][0].on(); motors["M2"][1].off()
    motors["M3"][0].on(); motors["M3"][1].off()
    motors["M4"][0].on(); motors["M4"][1].off()

def rotate_left():
    motors["M1"][0].on();  motors["M1"][1].off()
    motors["M2"][0].off(); motors["M2"][1].on()
    motors["M3"][0].off(); motors["M3"][1].on()
    motors["M4"][0].on();  motors["M4"][1].off()

def rotate_right():
    motors["M1"][0].off(); motors["M1"][1].on()
    motors["M2"][0].on();  motors["M2"][1].off()
    motors["M3"][0].on();  motors["M3"][1].off()
    motors["M4"][0].off(); motors["M4"][1].on()
