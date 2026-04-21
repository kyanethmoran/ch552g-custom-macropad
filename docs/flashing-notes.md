# Flashing Notes

## Purpose

These notes document the process used to successfully reflash the CH552G 6-key macropad used in this project.

The board started as a cheap prebuilt keypad with limited stock functionality. The goal of reflashing it was to turn it into a dedicated macro device that sends custom function keys (`F13` through `F21`) for use with a Python desktop-side listener.

---

## Board Information

### Board type

- CH552G-based 6-key macropad with rotary encoder
- ANXIN-K6-VT1-LED-V01 style PCB

### Relevant hardware details

- USB-C connection
- 6 buttons
- 1 rotary encoder with press
- bootloader access through pads labeled `SW2`

---

## Firmware Base

The firmware used for this project is based on:

- `Pakleni/ch552g-keypad-software`

That repo is based on:

- `hexesdesu/CH552X_HidKeyboard`

---

## Firmware Changes Before Flashing

The firmware was modified so the board sends dedicated function keys instead of normal keyboard keys or media controls.

### Final key mapping

- Button 1 → `F13`
- Button 2 → `F14`
- Button 3 → `F15`
- Button 4 → `F16`
- Button 5 → `F17`
- Button 6 → `F18`
- Encoder press → `F19`
- Encoder clockwise → `F20`
- Encoder counterclockwise → `F21`

This avoids conflicts with a standard full-size keyboard and makes the keypad easier to use as a dedicated macro device.

---

## Software Used

### Arduino IDE

The firmware was successfully compiled and uploaded using:

- **Arduino IDE 1.8.19**

### Why Arduino IDE 1.8.19 was used

Arduino IDE 2.x produced path/toolchain issues with CH55xDuino on Windows because the Windows username contained a space. Even after fixing temp folder issues, the CH55x toolchain still failed due to build/output paths under the user profile.

Using Arduino IDE 1.8.19 in portable mode avoided those path problems.

### Board package

- **CH55xDuino**

### Required board manager URL

```text
https://raw.githubusercontent.com/DeqingSun/ch55xduino/ch55xduino/package_ch55xduino_mcs51_index.json

## Bootloader Entry Method

The board did not automatically enter bootloader mode during upload, so it had to be placed into bootloader mode manually.

### Working method on this board revision

The most reliable method I found was to use **jumper wires** to short the pads labeled `SW2` while also holding the **4th key**, which is the key farthest from the USB-C port.

### Working sequence

1. click **Upload** in Arduino IDE
2. let the sketch finish compiling completely
3. wait until Arduino moves from compilation to the actual upload stage
4. while the board is unplugged, use jumper wires to short the `SW2` pads
5. hold down **key 4** (the key farthest from the USB-C port)
6. plug the board in while still shorting `SW2` and holding key 4
7. keep that state briefly so the board enters bootloader mode
8. release once the uploader detects the device and the upload begins

### Why this mattered

Normal upload attempts without the `SW2` short and key hold were not detected by the CH55x uploader.

Using jumper wires made the process easier for one person working alone and more repeatable than trying to short the pads manually with a metal tool.
```
