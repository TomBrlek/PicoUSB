# PicoUSB

Repository for PicoUSB - RP2040 based, affordable, easy to use and easy to program Bad USB

- [PicoUSB](#picousb)
  - [Setup](#setup)
  - [Operation](#operation)
  - [Important Files](#important-files)
  - [Development](#development)

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
> Changing any python can result in **permanently bricking your device**. Be very careful when modifying `boot.py` as disabling the USB drive without a failsafe could render the device useless!
> Be careful when writing your own micropython scripts! The developers are not responsible if you brick your own device this way!

- pico_usb.txt - here is where your executable pseudo-code is located.
- layout.txt - here is where you select your keyboard layout.
- code.py - interpreter that executes your pesudo code. Free to modify. (1)
- boot.py - this code executes before the USB is recognised. Free to modify. (1)

**pico_usb.txt API:**

- delay()   - waits for the specified amount of time before resuming execution. Example: delay(0.8)
- press()   - presses one or more buttons once. For example to press enter, use `press(enter)`. To "select all", use `press(control + a)`.
- write()   - sequentially presses many buttons in a row. example: `write(Hello world!)`
- hold()    - presses and holds down one or more buttons until `release()` is called
- release() - releases **all** held keys
- move(x, y) - moves the mouse on the main display to the given location, from the current location as a reference. negative x = left, possitive x = right, negative y = down, possitive y = up.
- click(btn)- clicks the mouse. `btn` is the mouse button, options are left, right, middle
- scroll(x) - scrolls the mouse. Negative number scrolls down, possitive scroll up
- volume(x) - Modifies the system volume. Negative numbers move the volume slider down by x, possitive move it up by x. min volume = 0. max = 100. `volume(mute)` mutes the speakers.
- loop() - loops everything before this command

## Development

1. Create a new venv: `python -m venv .venv`
2. Activate the venv: `.venv\Scripts\Activate.ps1` (Windows) or `source .venv\Scripts\activate` (Unix)
3. Install stubs: `pip install -r requirements-dev.txt`
