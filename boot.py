"""Pico USB boot.py file. If button is not pressed, execute code.py, not showing as mass storage; if pressed reset into SAFE MODE where code.py is not executed"""
import time
import board
import storage
import digitalio
import microcontroller

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "PicoUSB"
storage.remount("/", readonly=True)
storage.enable_usb_drive()

bt = digitalio.DigitalInOut(board.GP25)
bt.direction = digitalio.Direction.INPUT
bt.pull = digitalio.Pull.UP

time.sleep(0.1) #wait a bit so the button gets pulled up

if bt.value:
    storage.disable_usb_drive()
else:
    storage.enable_usb_drive()
    microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
    microcontroller.reset()
    

# in case you screw up and disable usb drive without the ability to enable it, to enter safe mode write in shell:
# import microcontroller
# microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
# microcontroller.reset()
