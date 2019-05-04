import serial
import mysql.connector
import time
from tkinter import simpledialog
import tkinter

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database = "rs232"
)

window = tkinter.Tk()
window.title("GUI")
global x
x = 1
global ser

def open_port():
    PortInput = simpledialog.askstring("Port", "What is name of Your COM Port (Something like: COM7)")
    global ser
    ser = serial.Serial(port = PortInput, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=1)
    make_sure()
    read_serial_GUI()

def change_x_close():
    global x
    x = 3
    
def change_x_exit():
    global x
    x = 2

def close_port():
    ser.close()
    make_sure()

def make_sure():
    try:
        ser.isOpen()
        print("serial port is open")
    except:
        print("Error: Is not opened")
        exit()
     
def read_serial():
    if(ser.isOpen()):
        try:          
            raw_data = ser.readline()
            print(raw_data)
            mycursor = mydb.cursor()

            sql = "INSERT INTO raw_data  (data, created) VALUES (%s, %s)"
            val = (raw_data, time.strftime("%Y-%m-%d %H:%M:%S"))
            mycursor.execute(sql, val)
            mydb.commit()
            
        except Exception:
            print("Read does not work")
    else:
        print("Can not open serial port")

def exit_program():
    ser.close()
    window.withdraw()

def read_serial_GUI():
    global x
    while (x != 2 or x !=3):
        read_serial()


tkinter.Label(window, text = "Serial Port Therminal").grid(row = 0, column = 1)
tkinter.Button(window, text = "Open port", command = open_port).grid(row = 1, column = 0)
tkinter.Button(window, text = "Close port", command = change_x_close).grid(row = 1, column = 2)
tkinter.Button(window, text = "Exit", command = change_x_exit).grid(row = 1, column = 1)

window.mainloop()