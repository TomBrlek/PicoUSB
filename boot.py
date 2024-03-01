#   Copyright 2024 PicoUSB
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Pico USB boot.py file. If button is not pressed, execute code.py, not showing as mass storage; if pressed reset into SAFE MODE where code.py is not executed"""
import time
import board
import storage
import digitalio
import microcontroller

mode = digitalio.DigitalInOut(board.GP25)
mode.direction = digitalio.Direction.INPUT
mode.pull = digitalio.Pull.UP

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "PicoUSB"
storage.remount("/", readonly=True)
storage.enable_usb_drive()

time.sleep(0.1) #wait a bit so the button gets pulled up

if mode.value:
    storage.disable_usb_drive()
else:
    time.sleep(0.1) #check again after 100ms to see if the button is still pressed
    if mode.value:
        storage.disable_usb_drive()
    else:
        storage.enable_usb_drive()
        microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
        microcontroller.reset()
    

# in case you screw up and disable usb drive without the ability to enable it, to enter safe mode write in shell:
# import microcontroller
# microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
# microcontroller.reset()
