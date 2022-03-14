'''
Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
http://www.electronicwings.com

blink an LED with the LGPIO library
Uses lgpio library, compatible with kernel 5.11
Author: William 'jawn-smith' Wilson
'''            

import smbus2            #import SMBus module of I2C
import time                #import
import csv
import lgpio

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

pin_read = 1
switch_pin = 23

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, switch_pin,lgpio.SET_BIAS_PULL_UP)

#setup csv
f= open('./data_'+str(int(time.time()))+'.csv', 'w')

writer = csv.writer(f)

header = ['time', 'Gx', 'Gy', 'Gz', 'Ax', 'Ay', 'Az']

writer.writerow(header)

def MPU_Init():
#write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
                
#Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
                            
#Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
                                        
#Write to Gyro configuration register
#    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
                                                    
#Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
#Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
#concatenate higher and lower value
    value = ((high << 8) | low)
#to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value

bus = smbus2.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()
print(" Reading Data of Gyroscope and Accelerometer")
try:
    while pin_read:
        #Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0
        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
        writer.writerow([time.time(),Gx,Gy,Gz,Ax,Ay,Az])
        pin_read = lgpio.gpio_read(h, switch_pin)
        print(pin_read)
    f.close()
    lgpio.gpiochip_close(h)
except KeyboardInterrupt:
    f.close()
    lgpio.gpiochip_close(h)
    
