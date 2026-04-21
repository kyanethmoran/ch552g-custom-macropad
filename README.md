# ch552g-keypad-software

Based on https://github.com/hexesdesu/CH552X_HidKeyboard

Made for **ANXIN-K6-VT1-LED-V01** Ali express keyboard

--------Additions made by kyanethmoran--------------

## Why I Started This Project

This keypad originally came with its own stock firmware and built-in behavior, so it was not completely unusable out of the box. However, after testing it, I found that the default functionality was too limited for what I wanted.

The original options were minimal, the customization was very restricted, and there was no real support for setting fully custom hotkeys in the way I needed. On top of that, I noticed the keypad was causing issues with my main full-size keyboard instead of behaving like a clean secondary macro device.

Rather than throw away a cheap six-dollar keypad, I decided to turn it into something far more useful. This project is my attempt to repurpose that hardware into a dedicated CH552G-based control pad that can function more like a mini Stream Deck for Windows.

I also want to set up a second one as a gift for a friend who is looking into getting into streaming. That made the project more worthwhile, because the end result is not just a fix for a cheap keypad, but a customizable tool that can launch apps, control audio, and trigger desktop actions in a much more flexible way than the stock firmware allowed.

# CH552G 6-Key Macropad to Python-Controlled Stream Deck

This project turns a cheap CH552G-based 6-key macropad with a rotary encoder into a custom, programmable control pad for Windows.

The original hardware is an **ANXIN-K6-VT1-LED-V01** style keypad built around the **CH552G** microcontroller. The original firmware and vendor behavior were too limited for my use case, so I reflashed the board and repurposed it as a dedicated macro controller that works alongside my normal keyboard.

## Project Goal

The goal of this project is to create a custom "Stream Deck"-style controller that can:

- launch specific desktop applications
- trigger custom actions from dedicated macropad buttons
- use the rotary encoder press to mute/unmute
- use the rotary encoder turn to adjust volume
- eventually provide a Python-based UI for remapping button behavior without needing to constantly rewrite desktop-side logic

The firmware side is kept simple and only sends unique key events.  
The Python side is where the actual application logic and UI will live.

---

## Hardware

This project is based on a CH552G keypad board with:

- 6 buttons
- 1 rotary encoder with press
- USB-C connection
- PCB labeled similarly to `ANXIN-K6-VT1-LED-V01`
- bootloader access through shorting the board pads labeled `SW2`

### Notes about the board

- The board uses a **CH552G** microcontroller.
- The board originally enumerated as a keyboard/media device.
- When placed into bootloader mode, Windows detected it as a different USB device.
- Driver installation was required before successful flashing. In my case, I installed the
  **CH372/CH375 Windows driver package (`CH372DRV`)**, which changed the bootloader-mode device
  from an unknown device into a recognized **USB Module** device so the uploader could
  communicate with it.
- The PCB includes LED support footprints, but LEDs were not populated on this hardware variant.
  I may add LEDs in the future to make the board more polished and feature-complete, but that is
  currently a stretch goal.

---

## Base Repository

This project is based on the original firmware repo:

- `Pakleni/ch552g-keypad-software`

That repo itself is based on:

- `hexesdesu/CH552X_HidKeyboard`

---

## What I Changed From the Original Repo

The original firmware was designed around normal keyboard and media-style behavior.

I modified the firmware so the keypad acts as a dedicated control surface for a future Python desktop app.

### Main firmware changes

#### 1. Reworked the keypad mappings into dedicated function keys

When I first tested the keypad in its original state, I noticed that **every input produced the same output: `c`**. It did not matter which of the 6 buttons I pressed, whether I clicked the rotary encoder, or whether I turned the encoder clockwise or counterclockwise. Everything was being interpreted as the same key.

The repo I forked improved that behavior by remapping the 6 keypad buttons to normal keyboard keys:

- `Alt`
- `w`
- `f`
- `a`
- `s`
- `d`

That was already better than the stock behavior, but I still did not want the macropad to conflict with my main 100% keyboard. Using normal keys like letters and modifier keys would create unnecessary overlap with standard typing, games, shortcuts, and other desktop use.

Because of that, I changed the keypad mappings again so the board now sends **dedicated function keys that do not exist on a standard 100% keyboard**:

- Button 1 → `F13`
- Button 2 → `F14`
- Button 3 → `F15`
- Button 4 → `F16`
- Button 5 → `F17`
- Button 6 → `F18`

Using `F13` through `F18` makes the keypad behave like a separate macro device instead of acting like a second normal keyboard.

#### 2. Changed rotary encoder mappings to dedicated function keys

The forked firmware originally used HID consumer/media codes for the rotary encoder:

- press → mute
- clockwise → volume up
- counterclockwise → volume down

I changed those so the encoder now sends normal keyboard function keys instead:

- Encoder press → `F19`
- Encoder clockwise → `F20`
- Encoder counterclockwise → `F21`

This keeps the rotary encoder consistent with the rest of the keypad and prevents conflicts with my normal keyboard. It also makes the encoder much easier to manage in Python, because the desktop app can interpret those keypresses however I want.

#### 3. Switched encoder handling from consumer HID events to keyboard events

The original repo used consumer/media HID calls for the rotary encoder actions.  
I changed that behavior so encoder actions are now emitted as keyboard events, keeping the entire device consistent as a macro-trigger input device.

#### 4. Preserved the general hardware scanning logic

The following original firmware behavior was kept:

- button scanning
- debouncing
- encoder reading logic
- USB initialization
- brightness logic
- LED-related code structure

#### 5. Added a PythonListener workspace area

I added a Python-side area to the project for:

- key testing scripts
- future Windows listener logic
- future app-launch/mute/volume features
- future remapping UI

---

## Why I Switched to F13-F21 Instead of 1-9

At one point I tested the board by sending `1` through `9`, which was useful for debugging in Notepad.

However, for actual daily use, `F13` through `F21` are much better because:

- they do not type visible characters into text fields
- they are less likely to conflict with normal typing
- they are less likely to interfere with games or applications using number keys
- they make the keypad behave more like a dedicated macro pad instead of a second normal keyboard

This allows the keypad to work **in addition to** my regular keyboard instead of overlapping with it.

---

## Current Project Structure
