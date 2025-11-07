from machine import Pin, PWM, ADC
import time
import math

# Pin setup
pr_l = ADC(26)  # Photoresistor on ADC0 (GPIO 26)
pr_r = ADC(27)  # Photoresistor on ADC1
pr_c = ADC(28)  # Photoresistor on ADC2

# Servo setup
servo = PWM(Pin(18))
servo.freq(50)  # 50Hz for servo control

# Servo duty cycle constants (adjust for your servo)
MIN_DUTY = 1802  # 0 degrees
MAX_DUTY = 7864  # 180 degrees

angle = 90


def map_value(value, from_min, from_max, to_min, to_max):
    """Map a value from one range to another"""
    return int((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)


while True:
    duty = map_value(angle, 0, 180, MIN_DUTY, MAX_DUTY)
    servo.duty_u16(duty)
    light_level_left = pr_l.read_u16() + 1700
    light_level_right = pr_r.read_u16()
    light_level_center = pr_c.read_u16()

    if light_level_right == light_level_left:
        pass
    elif light_level_right > light_level_left:
        if angle > 0:
            angle -= 1
    elif light_level_left > light_level_right:
        if angle < 180:
            angle += 1

    print("LIGHT VALUE: " + str(light_level_center))
    time.sleep(.025)
