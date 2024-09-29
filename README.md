# PicoUSB

Repository for PicoUSB - RP2040 based, affordable, easy to use and easy to program Bad USB

![PicoUSB-3](https://github.com/TomBrlek/PicoUSB/assets/137766608/e64d61c2-e8db-4887-aa5e-6456fb3bd157)

[Get your PicoUSB here!](https://www.elecrow.com/picousb-raspberry-pi-pico-rp2040-powered-bad-usb-rubber-ducky.html)

[Check out PicoUSB Website & Subscribe to our newsetter!](https://picousb.com/)

You just got an empty PicoUSB? Here's how to program it:

## Setup

1. Download the latest [CircuitPython for Rasperry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/).
2. Insert PicoUSB into your USB drive while holding the "Boot" button. (Opens it in a bootloader mode. The first time you do this you don't have to hold the "Boot" button)
3. Copy `CircuitPython.uf2` file to the USB and wait for few seconds or a minute for it to finish setting up. (will close and reopen the explorer, be patient)
4. Download/Clone the contents of this repository.
5. Open the USB device in explorer and copy/paste everything from `./src/` into it. (Replace all)

That is it! Modify `pico_usb.txt` to change the functionality. See below to know what to do next.

([Video Tutorial](https://youtu.be/jKH6WgFiaB0))

## Operation

- Inserting the PicoUSB while not holding any buttons will not show as a USB drive and will execute the "bad usb" code found in the pico_usb.txt.
- Inserting it while holding the "Mode" button will not execute any "bad usb" code and will show as a USB drive. This way you can freely edit the code.
- If you insert it while holding the "Boot" button, it will open in bootloader mode. This is usually only used the first time the device is set up and never again.

## Important Files

> [!CAUTION]
> There are ways you can brick your PicoUSB never to be used again if you disable the USB communication in code, without the ability to enable it again. This happens if you write your own micropython scripts (please be careful!). Please do not modify the micropython code unless you know what you are doing. Modify at your own discretion. I am not responible if you brick it. PicoUSB pseudo-code will never brick the device!

- pico_usb.txt - here is where your executable pseudo-code is located.
- layout.txt - here is where you select your keyboard layout.
- code.py - interpreter that executes your pesudo code. Free to modify. (1)
- boot.py - this code executes before the USB is recognised. Free to modify. (1)

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
- loop() - forever loops everything after the loop command. Use loop only once.

## Development

1. Create a new venv: `python -m venv .venv`
2. Activate the venv: `.venv\Scripts\Activate.ps1` (Windows) or `source .venv\Scripts\activate` (Unix)
3. Install stubs: `pip install -r requirements-dev.txt`
