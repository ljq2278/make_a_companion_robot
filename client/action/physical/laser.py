
import time
import board
import adafruit_vl53l1x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# OPTIONAL: can set non-default values
# vl53.distance_mode = 2
vl53.timing_budget = 100

print("VL53L1X Simple Test.")
print("--------------------")
model_id, module_type, mask_rev = vl53.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Mask Revision: 0x{:0X}".format(mask_rev))
print("Distance Mode: ", vl53.distance_mode)
print("Timing Budget: {}".format(vl53.timing_budget))
print("--------------------")

vl53.start_ranging()

def get_distance():
    return vl53.distance

if __name__ == '__main__':
    while True:
        if vl53.data_ready:
            # print("Distance: {} cm".format(vl53.distance))
            print("Distance: {} cm".format(get_distance()))
            vl53.clear_interrupt()
            time.sleep(1.0)
