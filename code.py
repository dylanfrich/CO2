import time

import board
import digitalio
import adafruit_scd4x


i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

# initialize the LED
led = digitalio.DigitalInOut(board.led)
led.direction = digitalio.Direction.OUTPUT

#initialize the button
button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

while True:
    if scd4x.data_ready:
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()

# Push the boot button to turn off and on the self calibration mode. It will reset to on after reboot.
    if button.value:
        if not led.value:
            scd4x.self_calibration_enabled = True
            led.value = True
            time.sleep(1)
        else:
            scd4x.self_calibration_enabled = False
            led.value = False
            time.sleep(1)

    time.sleep(1)
