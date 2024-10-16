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
    if function[0] == '#':
        return
    if function in ("DELAY", "SLEEP"):
        time.sleep(float(command))
    elif function == "LAYOUT":
        change_layout(command)
    elif function == "PRESS":
        command: list[str] = [x.strip().upper() for x in command.split("+")]
        if len(command) > 6:
            raise PicoKeyboardException("Too many keys pressed at once!")
        kb.send(Keycode.__dict__[k] for k in command)
    elif function == "WRITE":
        layout.write(command.replace("\\n", "\n"))
    elif function == "HOLD":
        command = [x.strip().upper() for x in command.split("+")]
        if len(command) > 6:
            raise PicoKeyboardException("Too many keys held at once!")
        kb.press(Keycode.__dict__[k] for k in command)
    elif function == "RELEASE":
        kb.release_all()
    elif function == "MOVE":
        x, y = [int(a) for a in command.split(',')]
        ms.move(x=x, y=-1*y, wheel=0)
    elif function == "SCROLL":
        ms.move(x=0, y=0, wheel=int(command))
    elif function == "CLICK":
        command = command.lower()  # We love consistency!!
        if command == "left":
            ms.click(Mouse.LEFT_BUTTON)
        elif command == "middle":
            ms.click(Mouse.MIDDLE_BUTTON)
        elif command == "right":
            ms.click(Mouse.RIGHT_BUTTON)
    elif function == "VOLUME":
        if command.lower() == "mute":
            cc.send(ConsumerControlCode.MUTE)
        else:
            amount = int(command)
            to_send = ConsumerControlCode.VOLUME_INCREMENT
            if amount < 0:
                amount = -amount
                to_send = ConsumerControlCode.VOLUME_DECREMENT
            for _ in range(amount):
                cc.send(to_send)
    else:
        raise PicoCommandException("Unknown command")


try:
    loop_pos = 0
    loop_times = -1
    # It is a good idea to seek and constantly read instead
    # of storing the whole file in RAM, as the file could
    # potentially be bigger than our tiny RAM
    file: io.TextIOWrapper = io.open("/pico_usb.txt", "r")
    file.seek(0, 2)  # Move to the end of the file
    file_end = file.tell()
    file.seek(0)
    while line := file.readline():
        line = line.rstrip('\r\n').split(" ", 1)
        if len(line) == 2:
            function, command = line
        else:
            function = line[0]
            command = None
        function = function.strip().upper()
        if function.upper() == "LOOP":
            loop_pos = file.tell()
            if command:
                loop_times = int(command)
        execute_command(function, command)
        if loop_pos and file.tell() == file_end:
            if not loop_times:
                break
            file.seek(loop_pos)
            # Explicitly check if we set loop_times so we
            # don't end up decrementing it and creating
            # a huge number (could result in a crash)
            if loop_times != -1:
                loop_times -= 1
finally:
    kb.release_all()
    if file:
        file.close()
