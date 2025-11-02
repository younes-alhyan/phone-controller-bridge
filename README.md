# 🎮 PS4 Controller Simulator

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PS4](https://img.shields.io/badge/PS4-003791?style=flat-square&logo=playstation&logoColor=white)](https://www.playstation.com/)
[![ADB](https://img.shields.io/badge/ADB-3DDC84?style=flat-square&logo=android&logoColor=white)](https://developer.android.com/studio#downloads)
[![vJoy](https://img.shields.io/badge/vJoy-000000?style=flat-square&logo=youtubegaming&logoColor=white)](https://vjoystick.sourceforge.io/)

**This script bridges the gap for PCs without Bluetooth or a USB connection. It connects to an Android phone via ADB, reads input from a PS4 controller connected to the phone, and simulates a virtual controller on Windows using vJoy and x360ce. Essentially, the phone forwards the PS4 controller’s inputs to a vJoy device, and x360ce converts them into an Xbox 360 controller that PC games can recognize.** 🚀

## 📑 Table of Contents

- [🔍 Overview](#🔍-overview)
- [⚙️ Requirements](#⚙️-requirements)
- [🛠️ Setup](#🛠️-setup)
- [🔗 Getting the `controller_device_path`](#🔗-getting-the-controller_device_path)
- [🎛️ vJoy Configuration](#🎛️-vjoy-configuration)
- [🚀 Running the Script](#🚀-running-the-script)
- [🕹️ Making It Work in Games Using x360ce](#🕹️-making-it-work-in-games-using-x360ce)
- [🗂️ File Descriptions](#🗂️-file-descriptions)
- [⚠️ Troubleshooting](#⚠️-troubleshooting)
- [🎮 Controller Mapping Table](#🎮-controller-mapping-table)

## 🔍 Overview

- **Main Components**:

  - `main.py`: The entry point of the application. It sets up signal handling for graceful shutdown and starts listening for controller input.

  - `controller.py`: Listens for input events from the Android phone using ADB, processes the events, and forwards them to `vJoy`.

  - `event_handler.py`: Handles specific events such as button presses, triggers, and stick movements, translating them into vJoy actions.

  - `utils.py`: Utility functions for scaling inputs and parsing D-pad values.

  - `config.py`: Configuration file with mappings for buttons, triggers, and axes.

## ⚙️ Requirements

1.  **Python 3.x**\
    Ensure you have Python 3 installed on your system.

2.  **Dependencies**:

    - `pyvjoy`: Python bindings for the vJoy API, which simulates the controller.

    - `subprocess`: Used to interact with ADB and read the input events from the Android device.

    - `concurrent.futures`: Used for handling controller events asynchronously with a thread pool.

    - `logging`: For logging and debugging purposes.

    You can install the necessary dependencies using `pip`:

    ```shell
        pip install pyvjoy
    ```

3.  **ADB Setup**:

    - Ensure [ADB](https://developer.android.com/studio#downloads) is installed and properly configured on your machine. You'll need to connect your Android device via USB and enable USB debugging on the device.

4.  **vJoy Setup**:

    - You need to install [vJoy](https://vjoystick.sourceforge.io/) on your Windows machine to simulate the virtual controller. Ensure that the vJoy device is properly set up.

## 🛠️ Setup

1.  **Clone the repository**:

    ```shell
        git clone https://github.com/itachi-555/ps4-controllers-imulator
        cd ps4-controllers-imulator
    ```

2.  **Android Device Configuration**:

    - Enable **USB Debugging** on your Android phone and connect it to your PC.

    - Install `adb` on your machine and ensure that your Android device is recognized by running:

      ```shell
          adb devices
      ```

3.  **vJoy Configuration**:

    - Install and configure vJoy on your Windows PC, ensuring that a virtual joystick is created and ready to be used by the script.

## 🔗 Getting the `controller_device_path`

To identify the correct device path for your Android controller, follow these steps:

1.  **Connect your Android device** via USB and ensure that **USB debugging** is enabled.

2.  **Run the following command in your terminal**:

    ```shell
        adb shell getevent -i
    ```

3.  **Look for the device entry** in the output, which will resemble the following:

    ```shell
    add device 1: /dev/input/event7
      bus:      0005
      vendor    054c
      product   09cc
      version   8000
      name:     "Wireless Controller"
      location: "70:28:04:61:45:ee"
      id:       "a4:53:85:5e:ec:b1"
      version:  1.0.1
      events:
        KEY (0001): 0130  0131  0133  0134  0136  0137  0138 0139
                    013a  013b  013c  013d  013e
        ABS (0003): 0000  : value 144, min 0, max 255, fuzz 0, flat 15, resolution 0
                    0001  : value 122, min 0, max 255, fuzz 0, flat 15, resolution 0
                    0002  : value 27, min 0, max 255, fuzz 0, flat 15, resolution 0
                    0003  : value 129, min 0, max 255, fuzz 0, flat 15, resolution 0
                    0004  : value 124, min 0, max 255, fuzz 0, flat 15, resolution 0
                    0005  : value 0, min 0, max 255, fuzz 0, flat 15, resolution 0
                    0010  : value 0, min -1, max 1, fuzz 0, flat 0, resolution 0
                    0011  : value 0, min -1, max 1, fuzz 0, flat 0, resolution 0
        MSC (0004): 0004
        FF  (0015): 0050  0051  0058  0059  005a  0060
      input props:
        <none>
    ```

4.  **Locate the path** of the device in the `add device` line (e.g., `/dev/input/event7`). This is the value you need for `controller_device_path` in the `config.py` file.

5.  **Update** `config.py`\*\* with the correct device path:

    ```python
        # In config.py
        controller_device_path = "/dev/input/event7" # Update this path
    ```

## 🎛️ vJoy Configuration

To simulate a PS4 controller with vJoy, make sure that the vJoy configuration includes all the necessary buttons and axes. Specifically, you should have `17` buttons defined to simulate all PS4 controller buttons.
open `vJoyCon.exe` and edit `Number of Buttons` :

<p align="center">
  <img src="./images/vJoyConf.png" alt="vJoyConf" />
</p>

## 🚀 Running the Script

To run the project, execute the `main.py` script:

```shell
    python main.py
```

This will:

- Start listening for controller input from the Android device via ADB.

- Map the input events (buttons, sticks, D-pad, etc.) to vJoy actions, simulating a PS4 controller on your Windows PC.

### Graceful Shutdown

The application will continue running, listening for inputs. To shut it down, use `Ctrl+C` or send a `SIGTERM` signal to stop the script gracefully.

## 🕹️ Making It Work in Games Using x360ce

To use the simulated PS4 controller in games that require an Xbox 360 controller, you'll need to map the vJoy inputs to Xbox 360 controller inputs using **x360ce**. Here's how to set it up:

1.  **Download and Install x360ce**:

    - Download the **x360ce** software from [x360ce official website](https://www.x360ce.com/).

    - Extract the contents to the folder of the game or to a separate directory where you want to manage the configuration.

2.  **Configure x360ce**:

    - Run the `x360ce.exe` application.

    - The software will scan your connected devices and automatically detect the virtual controller created by vJoy.

    - If it's not automatically detected, make sure the vJoy device is active and try refreshing or restarting x360ce.

3.  **Map vJoy to Xbox 360 Controller**:

    - Once your controller is detected, you'll need to map the buttons and axes correctly. You can do this manually or use the **Auto** feature in x360ce.

4.  **Use the Mapping Image**:

    - To make the mapping process easier, refer to the following screenshot which shows the x360ce controller mapping setup:

    ***

    <p align="center"> <img src="./images/x360ce_mapping.png" alt="x360ce Controller Mapping" /> </p>

    The image shows the mapping of buttons, triggers, and axes from the virtual PS4 controller (via vJoy) to Xbox 360 controller inputs. Follow the mapping in the image for a seamless experience in compatible games.

    ***

5.  **Save the Configuration**:

    - After mapping the buttons and axes, save the configuration file (`x360ce.ini`) in the game folder.

    - Make sure to launch the game with the `x360ce` executable or ensure it runs alongside the game as required.

6.  **Test the Controller**:

    - Launch the game and test the controller to verify that all buttons and axes are functioning correctly.

## 🎮 Controller Mapping Table

| PS4 Input        | Event Type | Event Code | Event Value                                 | vJoy Mapping   | Notes                                        |
| ---------------- | ---------- | ---------- | ------------------------------------------- | -------------- | -------------------------------------------- |
| Cross            | 0x01       | 0x130      | 1 = press, 0 = release                      | Button 1       |                                              |
| Circle           | 0x01       | 0x131      | 1 / 0                                       | Button 2       |                                              |
| Triangle         | 0x01       | 0x133      | 1 / 0                                       | Button 3       |                                              |
| Square           | 0x01       | 0x134      | 1 / 0                                       | Button 4       |                                              |
| L1               | 0x01       | 0x136      | 1 / 0                                       | Button 5       |                                              |
| R1               | 0x01       | 0x137      | 1 / 0                                       | Button 6       |                                              |
| L2 (Analog)      | 0x03       | 0x02       | 0–255                                       | Button 7       | Only triggers if value > `TRIGGER_THRESHOLD` |
| R2 (Analog)      | 0x03       | 0x05       | 0–255                                       | Button 8       | Only triggers if value > `TRIGGER_THRESHOLD` |
| Share            | 0x01       | 0x13A      | 1 / 0                                       | Button 9       |                                              |
| Options          | 0x01       | 0x13B      | 1 / 0                                       | Button 10      |                                              |
| PS               | 0x01       | 0x13C      | 1 / 0                                       | Button 11      |                                              |
| L3               | 0x01       | 0x13D      | 1 / 0                                       | Button 12      |                                              |
| R3               | 0x01       | 0x13E      | 1 / 0                                       | Button 13      |                                              |
| Left Stick X     | 0x03       | 0x00       | 0–255                                       | Axis X (48)    | Mapped to vJoy axis                          |
| Left Stick Y     | 0x03       | 0x01       | 0–255                                       | Axis Y (49)    | Mapped to vJoy axis                          |
| Right Stick X    | 0x03       | 0x03       | 0–255                                       | Axis X (51)    | Mapped to vJoy axis                          |
| Right Stick Y    | 0x03       | 0x04       | 0–255                                       | Axis Y (52)    | Mapped to vJoy axis                          |
| D-Pad Left/Right | 0x03       | 0x10       | 0 = released, 1 = right,`0xffffffff` = left | Button 15 / 17 | Parsed as buttons                            |
| D-Pad Up/Down    | 0x03       | 0x11       | 0 = released, 1 = down, `0xffffffff` = up   | Button 14 / 16 | Parsed as buttons                            |

### ℹ️ Notes

- **L2 & R2 Axis Only**: The key events (`0x138` for L2 and `0x139` for R2) are ignored. Only the analog axis values (`0x02` and `0x05`) are used. The button is considered **pressed only if value > `TRIGGER_THRESHOLD`**.
- **D-Pad** values are analog-like and must be parsed:
  - `0`: Released
  - `1`: Right / Down
  - `0xffffffff`: Left / Up

## 🗂️ File Descriptions

- `main.py`: Initializes the application and listens for controller input. Handles graceful shutdown on `SIGINT` or `SIGTERM`.

- `controller.py`: Captures and processes input events from the Android phone and sends them to vJoy.

- `event_handler.py`: Processes individual input events like button presses and stick movements.

- `utils.py`: Contains helper functions like scaling input values and parsing D-pad button states.

- `config.py`: Contains mappings for controller buttons, triggers, and axes.

## ⚠️ Troubleshooting

- **ADB not detecting device**: Ensure that USB debugging is enabled and the phone is properly connected via USB. Run `adb devices` to check if the device is listed.

- **vJoy device not recognized**: Ensure that vJoy is installed and the virtual joystick is set up correctly. Check the vJoy configuration in the vJoy Control Panel.

- **Permission issues**: Make sure you have the necessary permissions to interact with ADB and the vJoy device on your machine.
