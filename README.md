# PicoUSB
Repository for PicoUSB - RP2040 based, affordable, easy to use and easy to program - Bad USB

![PicoUSB-3](https://github.com/TomBrlek/PicoUSB/assets/137766608/e64d61c2-e8db-4887-aa5e-6456fb3bd157)

You just got an empty PicoUSB? How to program it:

**Setup:**
1. Download the latest [CircuitPython for Rasperry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/).
2. Insert PicoUSB into your USB drive while holding the "Boot" button. (Opens it in a bootloader mode)
3. Copy the CircuitPython .uf2 file to the USB and wait for a minute or two for it to finish setting up. (will close and reopen the explorer, be patient)
4. Download/Clone the contents of this repository.
5. Remove the PicoUSB and insert it again (Holding "Mode" does not do anything yet. Dont hold "Boot").
6. Open the folder in explorer and copy/paste this repo into it.
7. Finished! That is it. Modify pico_usb.txt to change the functionality.

**Operation:**
 - If you insert the PicoUSB while not holding any buttons, it will not show as a USB drive and it will execute the "bad usb" code found in the pico_usb.txt.
 - If you insert it while holding the "Mode" button, it will not execute the "bad usb" code and it will show as a USB drive so you can freely edit the code.
 - If you insert it while holding the "Boot" button, it will open in bootloader mode. This is usually only used the first time the device is set up and never again.

**Important Files:**
 - pico_usb.txt - here is where your executable code is located
 - layout.txt - here is where you select your keyboard layout
 - code.py - interpreter that executes your pesudo code. Free to modifly. (1)
 - boot.py - this code. Free to modify. (1)

**pico_usb.txt API:**
- delay()   - delays the execution for the number of seconds that is in between brackets, example: delay(0.8)
- press()   - presses once, all together, one or more buttons. for example, to press enter, use press(enter), to "select all", use press(control + a).
- write()   - writes down anything that is written between the brackets. example: write(https://www.youtube.com/)
- hold()    - holds down one or more buttons
- release() - releases all held keys (all)
- move(x, y) - moves the mouse on the main display to the given location, from the current location as a reference. negative x = left, possitive x = right, negative y = down, possitive y = up.
- click(btn)- btn is the mouse button, options are left, right, middle
- scroll(x) - negative number scrolls down, possitive scrolls up
- volume(x) - negative number is volume down by x, possitive volume up by x. min volume = 0. max = 100. volume(mute) mutes the speakers.

**(1)** There are ways you can brick your PicoUSB never to be used again if you disable the USB communication in code. Please do not do that unless you want to make a special code that bricks it. I dont recommend it. Modify at your own discretion. I am not responible if you brick it.
