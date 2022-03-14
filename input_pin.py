# nk an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio

switch_pin = 23

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, switch_pin,lgpio.SET_BIAS_PULL_UP)

try:
    while True:
        # Turn the GPIO pin on
        pin_read = lgpio.gpio_read(h, switch_pin)
        print(pin_read)
except KeyboardInterrupt:
    lgpio.gpiochip_close(h)
