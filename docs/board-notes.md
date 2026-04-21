# Board Notes

## Board Identification

This project is based on a cheap 6-key macropad with a rotary encoder built around the **CH552G** microcontroller.

The PCB and board layout match the **ANXIN-K6-VT1-LED-V01** style board.

### Physical features

- 6 button positions
- 1 rotary encoder with press
- USB-C connection
- CH552G microcontroller
- empty LED footprints on the PCB
- bootloader access through pads labeled `SW2`

---

## Original Behavior

When I first tested the keypad in its original state, every input produced the same visible output:

- all 6 buttons output `c`
- rotary encoder press output `c`
- rotary encoder clockwise output `c`
- rotary encoder counterclockwise output `c`

That made the stock keypad effectively unusable for any real macro workflow, since the PC could not distinguish one input from another.

The stock keypad also had very limited built-in customization options and did not provide the level of remapping I wanted.

---

## Why I Reworked It

I wanted the keypad to act as a dedicated control device that could work alongside my normal 100% keyboard without conflicting with it.

Instead of throwing away a cheap keypad that cost only a few dollars, I decided to turn it into something more useful.

This project also has a second purpose: I want to set up another one as a gift for a friend who is interested in getting into streaming.

---

## Fork / Firmware Base

The firmware used for this project is based on:

- `Pakleni/ch552g-keypad-software`

That repo itself is based on:

- `hexesdesu/CH552X_HidKeyboard`

The forked firmware already improved the board by mapping the 6 keypad buttons to normal keys:

- `Alt`
- `w`
- `f`
- `a`
- `s`
- `d`

However, I did not want the keypad to overlap with my normal keyboard, so I changed the mappings again to use dedicated function keys instead.

---

## Current Firmware Mapping

### Buttons

- Button 1 → `F13`
- Button 2 → `F14`
- Button 3 → `F15`
- Button 4 → `F16`
- Button 5 → `F17`
- Button 6 → `F18`

### Rotary encoder

- Encoder press → `F19`
- Encoder clockwise → `F20`
- Encoder counterclockwise → `F21`

These mappings make the board behave more like a dedicated macro pad and avoid conflicts with a standard full-size keyboard.

---

## Why F13-F21 Were Chosen

I originally used `1` through `9` during testing because they were easy to verify in Notepad.

After confirming the reflashed firmware worked, I changed the keypad outputs to `F13` through `F21` because:

- they do not type visible characters into text fields
- they are less likely to interfere with normal typing
- they avoid overlapping with number-row shortcuts and game controls
- they make the keypad behave as a separate macro device

---

## Windows Detection Behavior

### Normal mode

When plugged in normally, the board enumerates as a keyboard/media-style HID device.

### Bootloader mode

When put into bootloader mode by shorting `SW2`, Windows detects it as a different USB device.

Before the correct driver was installed, it appeared as:

- `Unknown device`

After installing the correct driver, it appeared as:

- `USB Module`

### Bootloader USB ID

- `VID_4348`
- `PID_55E0`

---

## Flashing Notes

Flashing required:

1. compiling the firmware successfully with **Arduino IDE 1.8.19**
2. putting the board into bootloader mode by shorting `SW2`
3. installing the correct Windows driver
4. reconnecting the board in bootloader mode during upload

The correct driver package I installed was:

- **CH372DRV**

Once installed, Windows recognized the bootloader device correctly and the board could be flashed successfully.

---

## Upload Result

The firmware upload completed successfully with:

- device found as `CH552`
- write complete
- verify complete
- reset OK

That confirmed the reflashed firmware was written successfully to the board.

---

## LED Notes

The PCB includes LED support footprints, but LEDs were not populated on this hardware variant.

This means the board appears to share a PCB design with another version that includes lighting hardware.

I may add LEDs in the future to make the board more polished and feature-complete, but that is currently a stretch goal.

---

## PCB / Hardware Notes

### Confirmed from inspection

- MCU is marked **CH552G**
- board uses a USB-C connector
- PCB has `SW2` marking used during bootloader entry
- board has empty LED footprints
- board uses 6 key switch positions and 1 rotary encoder

### Important practical takeaway

The board is cheap, but the hardware is usable once reflashed.  
The biggest limitations were the stock firmware behavior and the need to manually enter bootloader mode for reflashing.

---

## Current Project Role of the Board

At this stage, the board is no longer treated as a normal keyboard.

Instead, it functions as a dedicated input device whose job is to send:

- `F13`
- `F14`
- `F15`
- `F16`
- `F17`
- `F18`
- `F19`
- `F20`
- `F21`

Those inputs are then interpreted by the Python desktop-side scripts to perform actual actions such as:

- launching applications
- muting/unmuting
- changing app volume
- triggering future macros

---

## Future Ideas

Possible future improvements for the board include:

- adding LEDs if the hardware is later populated
- refining or removing leftover brightness logic if it is no longer needed
- making the board easier to reflash without manual boot shorting
- building a full Python UI for changing what each key does
