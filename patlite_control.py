###############################################################################
# Name    : PATLITE PHE-3B2 serial controller
# Author  : mokunine
# Date    : 2022/08/19
# Version : 0.0.2
###############################################################################

import sys
import argparse
import configparser
import serial

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

parser = argparse.ArgumentParser(description='Serial control.')
parser.add_argument('-c','--command', type = str, default = '0', choices = ['0', '1'], 
    help = 'Select a command. 0 = Put off LEDs and stop buzzer. 1 = Put on LEDs and start buzzer.')
parser.add_argument('-r','--red', type = int, default = 0, choices=[0, 1, 2], 
    help = 'Select red LED pattern. 0 = none, 1 = on/off, 2 = blink')
parser.add_argument('-y','--yellow', type = int, default = 0, choices=[0, 1, 2], 
    help = 'Select yellow LED pattern. 0 = none, 1 = on/off, 2 = blink')
parser.add_argument('-g','--green', type = int, default = 0, choices=[0, 1, 2], 
    help = 'Select green led pattern. 0 = none, 1 = on/off, 2 = blink')
parser.add_argument('-b','--buzzer', type = int, default = 0, choices=[0, 1, 2], 
    help = 'Select buzzer pattern. 0 = none, 1 = alert, 2 = ringing')

args = parser.parse_args()

# Arguments from ini
com = "COM" + config['SERIAL']['ComPort']
baud = config['SERIAL']['Baudrate']
retry = int(config['SERIAL']['Retry'])


def clean():
    ser.close()

try:
    ser = serial.Serial(com)
    ser.baudrate = config['SERIAL']['Baudrate']
    ser.timeout = int(config['SERIAL']['Timeout'])
    print(ser)
except Exception as e:
    print(e)
    sys.exit(1) 

headder = ord(config['PHE3FB']['Headder'])
encode = ord(config['PHE3FB']['Encode'])
id = [ ord(config['PHE3FB']['Id_high']), ord(config['PHE3FB']['Id_low']) ]
# All off by default
data = [ 0x30, 0x30 ] 
print(args)

command = ord(args.command)

if args.red == 1:
    data[0] |= 1 << 0
elif args.red == 2:
    data[1] |= 1 << 1

if args.yellow == 1:
    data[0] |= 1 << 1
elif args.yellow == 2:
    data[1] |= 1 << 2

if args.green == 1:
    data[0] |= 1 << 2 
elif args.green == 2:
    data[1] |= 1 << 3 

if args.buzzer == 1:
    data[0] |= 1 << 3
elif args.buzzer == 2:
    data[1] |= 1 << 0

# Serial transfer format ( command 0 or 1 )
tx_data = [ headder, id[1], id[0], command, data[1], data[0], encode ]
print("Tx data =", tx_data)


ser.write( tx_data )

for count in range(retry):
    result = ser.read_all()
    if result == b'\x06':
        print("Transmit success.") 
        break
    elif result == b'\x15':
            print("ERROR - NACK is recieved.") 
            clean()
            sys.exit(1)
    else:
        if (count + 1) == retry:
            print("ERROR - ACK wait timeout")
            clean()
            sys.exit(1)
        else:
            print("retry : " + str(count + 1))
   
clean()

sys.exit(0)
