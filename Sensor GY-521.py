import smbus			#impor modul SMBus dari I2C
from time import sleep          #impor

#beberapa register MPU6050 dan alamatnya
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


def MPU_Init():
	#tulis ke contoh daftar
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#tulis ke daftar manajemen daya
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#tulis ke Register konfigurasi
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#tulis ke konfigurasi gyro
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#tulis untuk menginterupsi aktifkan daftar
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Nilai Accelero dan Gyro adalah 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #menggabungkan nilai yang lebih tinggi dan lebih rendah
        value = ((high << 8) | low)
        
        #untuk mendapatkan nilai yang diintrak dari mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# atau bus = smbus. SMBus(0) untuk papan versi yang lebih lama
Device_Address = 0x68   # Alamat perangkat MPU6050

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")

while True:
	
	#Baca Nilai baku akselerometer
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Baca nilai mentah Giroskop
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#Rentang skala penuh +/- 250 derajat/C sesuai faktor skala sensitivitas
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	
	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0
	

	print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
	sleep(1)