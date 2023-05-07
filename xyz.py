import serial
import pymysql

# Configure the serial port
arduino_port = 'COM13'  # Replace with the correct port for your Arduino
baud_rate = 115200

# Configure the MySQL database connection
db_host = '35.154.104.139'
db_user = 'root'
db_password = ''
db_name = 'food'

# Establish the database connection
db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
cursor = db.cursor()

# Open the serial port
ser = serial.Serial(arduino_port, baud_rate)

try:
    while True:
        # Read data from Arduino
        data = ser.readline().decode().strip()  # Decode the bytes and remove whitespace

        # Insert the data into the database
        sql = "INSERT INTO sensor_data (value) VALUES (%s)"
        cursor.execute(sql, (data,))
        db.commit()

        print(f"Data received and stored: {data}")

except KeyboardInterrupt:
    print("Program stopped by the user.")

# Close the serial port and database connection
ser.close()
cursor.close()
db.close()