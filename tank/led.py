from rpi5_ws2812.ws2812 import Color, WS2812SpiDriver
import time, random

led_count = 8
strip = WS2812SpiDriver(spi_bus=0, spi_device=0, led_count=led_count).get_strip()

# 设置整体亮度为 50%
strip.set_brightness(0.1)

while True:
    for i in range(led_count):
        randomR = random.randint(0, 255)
        randomG = random.randint(0, 255)
        randomB = random.randint(0, 255)
        strip.set_pixel_color(i, Color(randomR, randomG, randomB))
    
    strip.show()
    time.sleep(0.5)
