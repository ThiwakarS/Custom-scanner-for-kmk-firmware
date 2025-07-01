# 🧠 KMK Firmware with Multiplexer on Raspberry Pi Pico

This project implements a **custom KMK scanner** using a **16-channel multiplexer** (like the 74HC4067) to read 16 keys using minimal GPIOs on a Raspberry Pi Pico running **CircuitPython**.

The scanner integrates with [KMK Firmware](https://github.com/KMKfw/kmk_firmware) and supports dynamic key detection using a custom `scan_for_changes()` function and `KeypadEvent` objects.

---

## 🔧 Hardware Setup

### 🧱 Components

- **Raspberry Pi Pico** (or any CircuitPython-compatible board)
- **74HC4067 Multiplexer**
- 16 push buttons
- Pull-up resistors (or use internal pull-ups)
- Jumper wires and breadboard

### 📡 Pin Connections

| Function       | GPIO Pin     | Description                      |
|----------------|--------------|----------------------------------|
| `S0`           | `GP10`       | Multiplexer select line 0        |
| `S1`           | `GP11`       | Multiplexer select line 1        |
| `S2`           | `GP12`       | Multiplexer select line 2        |
| `S3`           | `GP13`       | Multiplexer select line 3        |
| `SIG`          | `GP28`       | Common output/input from MUX     |
| `EN` (active-low) | `GP14`    | MUX enable (pulled LOW to enable)|

📌 Make sure to:
- Pull `EN` pin LOW to enable the multiplexer.
- Use **external pull-up resistors** on switches if not using internal ones.

---

## 🧠 Features

- ✅ Scans 16 keys using 4 select lines + 1 signal line
- ✅ Compatible with KMK’s event loop and `KeypadEvent`
- ✅ Efficient key scanning via `scan_for_changes()`
- ✅ Simple coordinate mapping (`coord_mapping`)
- 🧪 External pull-ups for stable signal detection
- ⚡ Active-low logic (LOW = pressed)

---

## 🗃️ File Structure

project/
│
├── code.py # Main CircuitPython script
├── lib/
│ └── kmk/ # KMK firmware library
├── README.md # This file

---

## 🧪 Key Mapping

Keymap is laid out like this (4x4):

A B C D
E F G H
I J K L
M N O P


Each key corresponds to a multiplexer channel from 0 to 15.

---

## 🧠 How It Works

1. The scanner sets the multiplexer to each channel (0–15).
2. It reads the `SIG` pin to detect if the button is pressed (LOW).
3. If a state change is found (press or release), it returns a `KeypadEvent`.
4. KMK handles the event and triggers the assigned key action.

---

## 🧼 Debouncing

Basic state comparison is implemented (`_prev_state`) to filter repeated events.  
For additional software debouncing, consider modifying `time.sleep()` or integrating a debounce module.

---

## ▶️ How to Run

1. Copy `code.py` to your CircuitPython device.
2. Install [KMK Firmware](https://github.com/KMKfw/kmk_firmware) in the `/lib` folder.
3. Plug in the board — it should act as a USB HID keyboard.

---

## 🛠️ Customization

- 💡 Change `keymap` for different layouts or key functions.
- 🎛️ Expand to 32+ keys by adding another multiplexer with different select or enable pins.
- 🧰 Modify `scan_for_changes()` to add debounce timing or signal smoothing.

---

## 📜 License

MIT License.  
Feel free to fork, modify, and build on this!

---

## 🙌 Credits

Built with ❤️ using [KMK Firmware](https://github.com/KMKfw/kmk_firmware) and CircuitPython on Raspberry Pi Pico.
