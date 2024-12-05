# PicoUSB

Repository for PicoUSB - RP2040 based, affordable, easy to use and easy to program Bad USB

- [PicoUSB](#picousb)
  - [Setup](#setup)
  - [Operation](#operation)
  - [Important Files](#important-files)
  - [Editing `pico_usb.txt` to execute commands](#editing-pico-usb)
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
**Note that** After copying the files the stick might automatically "reinsert" and play the example script in `pico_usb.txt` &rarr;
It will:
* Minimize all open windows
* Open an editor instance
* Type *Hello from PicoUSB!!*

6. **Usage:** To modify the behaviour you will need to modify `pico_usb.txt` to change the functionality. See below to know what to do next.

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

<a id="editing-pico-usb"> </a>
### Editing *`pico_usb.txt`* to execute commands:


#### **General Commands**

- **delay(seconds)**  
  Waits for the specified amount of time before resuming execution.  
  Example: `delay(0.8)`

- **loop()**  
  Loops the execution of all commands after the `loop()` command indefinitely.  
  **Note**: Use the `loop()` command only once.

#### **Keyboard Commands**

- **press(key1, key2, ...)**  
  Presses one or more buttons once. For example, to press Enter, use `press(enter)`.  
  To "select all", use `press(control + a)`.

- **write(text)**  
  Sequentially presses many buttons in a row.  
  Example: `write(Hello world!)`

- **hold(key1, key2, ...)**  
  Presses and holds down one or more buttons until `release()` is called.

- **release()**  
  Releases **all** held keys.

#### **Mouse Commands**

- **move(x_min, x_max, y_min, y_max)**  
  Moves the mouse to a random location within the given `x` and `y` range, relative to the current position.  
  - `x_min` and `x_max` define the horizontal range (negative x = left, positive x = right).  
  - `y_min` and `y_max` define the vertical range (negative y = down, positive y = up).  
  Example: `move(100, 500, 200, 800)` will move the mouse to a random position where:
    - `x` is between 100 and 500
    - `y` is between 200 and 800

- **click(btn)**  
  Clicks the specified mouse button.  
  `btn` can be one of: `left`, `middle`, `right`.

- **scroll(amount)**  
  Scrolls the mouse wheel.  
  - A negative number scrolls down, a positive number scrolls up.

#### **Volume Control Commands**

- **volume(amount)**  
  Modifies the system volume.  
  - A negative number decreases the volume by `amount`, a positive number increases it by `amount`.  
  - `volume(mute)` mutes the speakers.  
  - Volume range: 0 (min) to 100 (max).

## Development

1. Create a new venv: `python -m venv .venv`
2. Activate the venv: `.venv\Scripts\Activate.ps1` (Windows) or `source .venv\Scripts\activate` (Unix)
3. Install stubs: `pip install -r requirements-dev.txt`
