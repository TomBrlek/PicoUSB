import io
import os
import re
import time
import board
import storage
import usb_hid
import digitalio

from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from exceptions import PicoCommandException, PicoLayoutException, PicoKeyboardException

cc = ConsumerControl(usb_hid.devices)
kb = Keyboard(usb_hid.devices)
ms = Mouse(usb_hid.devices)

from adafruit_hid.keyboard_layout_us import KeyboardLayout
layout = KeyboardLayout(kb)

bt = digitalio.DigitalInOut(board.GP25)
bt.direction = digitalio.Direction.INPUT
bt.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.GP12)
led.direction = digitalio.Direction.OUTPUT
led.value = True

looping = False
loop_pos = 0

def change_layout(layout_id: str):
    global layout
    del KeyboardLayout
    if layout_id == "US":
        from adafruit_hid.keyboard_layout_us import KeyboardLayout
    elif layout_id in ("SI", "HR", "BA"):
        from keyboard_layouts.keyboard_layout_win_cr import KeyboardLayout
    elif layout_id == "GB":
        from keyboard_layouts.keyboard_layout_win_uk import KeyboardLayout
    elif layout_id == "FR":
        from keyboard_layouts.keyboard_layout_win_fr import KeyboardLayout
    elif layout_id == "CZ":
        from keyboard_layouts.keyboard_layout_win_cz import KeyboardLayout
    elif layout_id == "BR":
        from keyboard_layouts.keyboard_layout_win_br import KeyboardLayout
    elif layout_id == "DE":
        from keyboard_layouts.keyboard_layout_win_de import KeyboardLayout
    elif layout_id == "ES":
        from keyboard_layouts.keyboard_layout_win_es import KeyboardLayout
    elif layout_id == "HU":
        from keyboard_layouts.keyboard_layout_win_hu import KeyboardLayout
    elif layout_id == "IT":
        from keyboard_layouts.keyboard_layout_win_it import KeyboardLayout
    elif layout_id == "PO":
        from keyboard_layouts.keyboard_layout_win_po import KeyboardLayout
    elif layout_id == "SE":
        from keyboard_layouts.keyboard_layout_win_sw import KeyboardLayout
    elif layout_id == "TR":
        from keyboard_layouts.keyboard_layout_win_tr import KeyboardLayout
    elif layout_id == "BE":
        from keyboard_layouts.keyboard_layout_win_bene import KeyboardLayout
    else:
        raise PicoLayoutException("Unknown keyboard layout")
    layout = KeyboardLayout(kb)

def execute_command(function: str, command: str):
    if function in ("DELAY", "SLEEP"):
        time.sleep(float(command))
    elif function == "LAYOUT":
        change_layout(command)
    elif function == "PRESS":
        command: list[str] = [x.strip().upper() for x in command.split("+")]
        if len(command) > 6:
            raise PicoKeyboardException("Too many keys pressed at once!")
        keys = [0] * len(command)
        for idx in range(0, len(command), 1):
            keys[idx] = getattr(Keycode, command[idx])
        kb.send(*keys)
    elif function == "WRITE":
        layout.write(command)
    elif function == "HOLD":
        command = command.split(" + ")
        for c in range(0, len(command), 1):
            command[c] = command[c].upper()
        if len(command) <= 6:
            keys = [0] * len(command)
            for idx in range(0, len(command), 1):
                keys[idx] = getattr(Keycode, command[idx])
            kb.press(*keys)
    elif function == "RELEASE":
        kb.release_all()
    elif function == "MOVE":
        command = command.split(", ")
        pos = [0] * 2
        for i in range(0, len(command), 1):
            pos[i] = int(command[i])
        ms.move(x=pos[0], y=-1*pos[1], wheel=0)
    elif function == "SCROLL":
        ms.move(x=0, y=0, wheel=int(command))
    elif function == "CLICK":
        if command == "left":
            ms.click(Mouse.LEFT_BUTTON)
        elif command == "middle":
            ms.click(Mouse.MIDDLE_BUTTON)
        elif command == "right":
            ms.click(Mouse.RIGHT_BUTTON)
    elif function == "VOLUME":
        if command.isdigit():
            for vc in range(0, abs(int(command)), 1):
                if int(command) > 0:
                    cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                elif int(command) < 0:
                    cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        elif command == "mute":
            cc.send(ConsumerControlCode.MUTE)
    else:
        raise PicoCommandException("Unknown command")

def get_substr(string, start, end):
    command = ""
    for idx in range(start+1, end):
            command += string[idx]
    return command

try:
    file: io.FileIO = io.open("/pico_usb.txt", "r")
    line = file.readline()
    while line != "":
        function = line.split("(",1)[0].upper()
        command = get_substr(line, line.find("("), line.rfind(")"))
        if looping == False:
            loop_pos += len(line)
        if function == "LOOP":
            looping = True
        execute_command(function, command)
        line = file.readline()
    file.close()  
    file = io.open("/pico_usb.txt", "r")
    while looping == True:
        file.seek(loop_pos)
        line = file.readline()
        while line != "":
            function = line.split("(",1)[0].upper()
            command = get_substr(line, line.find("("), line.rfind(")"))
            execute_command(function, command)
            line = file.readline()

    file.close()

except OSError as e:
    print(e)
kb.release_all()
