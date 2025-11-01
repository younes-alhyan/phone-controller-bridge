### 🎮 Controller Mapping Table

| PS4 Input         | Event Type | Event Code | Event Value                      | vJoy Mapping  | Notes                                           |
|-------------------|------------|------------|----------------------------------|---------------|-------------------------------------------------|
| Cross             | 0x01       | 0x130      | 1 = press, 0 = release           | Button 1      |                                                 |
| Circle            | 0x01       | 0x131      | 1 / 0                            | Button 2      |                                                 |
| Triangle          | 0x01       | 0x133      | 1 / 0                            | Button 3      |                                                 |
| Square            | 0x01       | 0x134      | 1 / 0                            | Button 4      |                                                 |
| L1                | 0x01       | 0x136      | 1 / 0                            | Button 5      |                                                 |
| R1                | 0x01       | 0x137      | 1 / 0                            | Button 6      |                                                 |
| L2 (Analog)       | 0x03       | 0x02       | 0–255                            | Button 7      | Only triggers if value > `TRIGGER_THRESHOLD`    |
| R2 (Analog)       | 0x03       | 0x05       | 0–255                            | Button 8      | Only triggers if value > `TRIGGER_THRESHOLD`    |
| Share             | 0x01       | 0x13A      | 1 / 0                            | Button 9      |                                                 |
| Options           | 0x01       | 0x13B      | 1 / 0                            | Button 10     |                                                 |
| PS                | 0x01       | 0x13C      | 1 / 0                            | Button 11     |                                                 |
| L3                | 0x01       | 0x13D      | 1 / 0                            | Button 12     |                                                 |
| R3                | 0x01       | 0x13E      | 1 / 0                            | Button 13     |                                                 |
| Left Stick X      | 0x03       | 0x00       | 0–255                            | Axis X (48)   | Mapped to vJoy axis                             |
| Left Stick Y      | 0x03       | 0x01       | 0–255                            | Axis Y (49)   | Mapped to vJoy axis                             |
| Right Stick X     | 0x03       | 0x03       | 0–255                            | Axis X (51)   | Mapped to vJoy axis                             |
| Right Stick Y     | 0x03       | 0x04       | 0–255                            | Axis Y (52)   | Mapped to vJoy axis                             |
| D-Pad Left/Right  | 0x03       | 0x10       | 0 = released, 1 = right,         | Button 15 / 17| Parsed as buttons                               |
|                   |            |            | `0xffffffff` = left              |               |                                                 |
| D-Pad Up/Down     | 0x03       | 0x11       | 0 = released, 1 = down,          | Button 14 / 16| Parsed as buttons                               |
|                   |            |            | `0xffffffff` = up                |               |                                                 |

---

### ℹ️ Notes

- **L2 & R2 Axis Only**: The key events (`0x138` for L2 and `0x139` for R2) are ignored. Only the analog axis values (`0x02` and `0x05`) are used. The button is considered **pressed only if value > `TRIGGER_THRESHOLD`**.
- **D-Pad** values are analog-like and must be parsed:  
  - `0`: Released  
  - `1`: Right / Down  
  - `0xffffffff`: Left / Up
