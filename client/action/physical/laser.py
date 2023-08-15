import time
import board
import adafruit_vl53l1x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# OPTIONAL: can set non-default values
# vl53.distance_mode = 2
# vl53.timing_budget = 100

# model_id, module_type, mask_rev = vl53.model_info

vl53.start_ranging()


def get_dist():
    dist = vl53.distance
    return dist if dist is not None else 10000


if __name__ == '__main__':
    while True:
        if vl53.data_ready:
            # print("Distance: {} cm".format(vl53.distance))
            print("Distance: {} cm".format(get_dist()))
            vl53.clear_interrupt()
            time.sleep(1.0)
