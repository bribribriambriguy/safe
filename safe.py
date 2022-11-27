import RPi.GPIO as gpio
from gpiozero import Servo
from RPLCD import i2c
from time import sleep

servo = Servo(17)
lcd = i2c.CharLCD('PCF8574', 0x27, port=1,charmap='A00',cols=20,rows=4)

rows = [10,9,11,5]
collums = [6,13,19,26]
keypad=[[1,2,3,'A'],[4,5,6,'B'],[7,8,9,'C'],['*',0,'#','D']]
a = None
rowOn = None
password = []
correct_password = [1,2,3,4]

def setup():
    gpio.setmode(gpio.BCM)
    for row in rows:
        gpio.setup(row, gpio.OUT)
    for collum in collums:
        gpio.setup(collum, gpio.IN, pull_up_down=gpio.PUD_DOWN)


def getKeyPad():
    for row in rows:
        gpio.output(row, 1)
        for collum in collums:
            if gpio.input(collum) == 1:
                index=keypad[rows.index(row)]
                sleep(0.3)
                return index[collums.index(collum)]
        gpio.output(row, 0)    


setup()
while True:
    while True:
        lcd.close(clear=True)
        lcd.write_string("Password:")
        password.clear()
        while True:
            out = getKeyPad()
            if out != None:
                password.append(out)
                char = str(out)
                lcd.write_string(char)
                print(password)
                if len(password) >= 4:
                    break
        lcd.close(clear=True)    
        if password == correct_password:
            print("correct")
            lcd.write_string('correct')
            lcd.crlf()
            lcd.write_string('opening door')
            lcd.crlf()
            servo.max()
            sleep(3)
            break
        else:
            lcd.crlf()
            lcd.write_string('Wrong Password')
            sleep(3)
    lcd.close(clear=True)
    lcd.write_string("press any key to close")
    while True:
        out = getKeyPad()
        if out != None:
            servo.min()
            break


"""        
except:
    print("cleaning up...")
    gpio.cleanup()
"""   