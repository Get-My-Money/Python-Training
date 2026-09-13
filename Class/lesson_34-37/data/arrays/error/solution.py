import keyboard
import threading
import time
import datetime as dt

info_log = {}

def hello():
    a = str(dt.datetime.now()).split()[1]
    print("Привет!")
    info_log[a] = "Hello" 
    time.sleep(1)
keyboard.add_hotkey("ctrl+1", hello)

def hello2():
    a = str(dt.datetime.now()).split()[1]
    print("Как дела?")
    info_log[a] = "How are you?" 
    time.sleep(1)
keyboard.add_hotkey("ctrl+2", hello2)


def hello3():
    a = str(dt.datetime.now()).split()[1]
    print(f"Текущее время: {a}")
    info_log[a] = "What's time now" 
    time.sleep(1)
keyboard.add_hotkey("ctrl+3", hello3)

def hello4():
    a = str(dt.datetime.now()).split()[1]
    keyboard.write("Hello")
    keyboard.press_and_release("enter")
    info_log[a] = "Enter+Text" 
    time.sleep(1)
    
keyboard.add_hotkey("ctrl+4", hello4)


print("Нажми ESC для выхода")
keyboard.wait("esc")
keyboard.unhook_all()
print("Программа завершена")
print(info_log)

time.sleep(15)






