### About

An auto-zoom hat-mounted camera using an Arducam IMX477 with 8-50mm lens and ML for rc plane detection

<img src="hat-cam.JPG"/>

<img src="mlhatcam-1.JPG"/>

### Note

Try to avoid using `GPIO 1` this affects the camera (not detected).

It can be avoided if you don't have a shared ground connected but requires a switch until after boot.

### Progress
- [x] physical body (02/19/2023)
  - [x] usable lens focus/tele assembly (01/27/2023)
  - [x] display and dpad (02/17/2023)
  - [x] full design (attachable to hat) (02/19/2023)
- [ ] functionality code
  - [x] steppers and position tracking (02/09/2023)
    - [x] motion (01/28/2023)
    - [x] track in db for boot resume (02/09/2023)
  - [ ] menu design
  - [x] dpad bindings (02/18/2023)
  - [ ] record to USB
- [x] auto focus (02/12/2023)
  - [x] some method like comparing frames, more blurry go other way
    - used laplace variance
- [ ] auto zoom
  - use ML to find target, then zoom
- [ ] machine learning
  - train small shots of plane sillhouette against wall
  - record actual flying footage, label samples, train model

### Raspberry Pi 4B GPIO pin usage

| Left        | Right       |
| ----------- | ----------- |
| 3.3V        | 5V          |
| GPIO 2      | 5V          |
| GPIO 3      | Ground      |
| GPIO 4      | GPIO 14     |
| Ground      | GPIO 15     |
| GPIO 17     | GPIO 18     |
| GPIO 27     | Ground      |
| GPIO 22     | GPIO 23     |
| 3.3V        | GPIO 24 [I] |
| GPIO 10 [D] | Ground      |
| GPIO 9 [D]  | GPIO 25 [D] |
| GPIO 11 [D] | GPIO 8  [D] |
| Ground      | GPIO 7  [I] |
| GPIO 0  [I] | GPIO 1  [I] |
| GPIO 5  [I] | Ground      |
| GPIO 6  [S] | GPIO 12 [S] |
| GPIO 13 [S] | Ground      |
| GPIO 19 [S] | GPIO 16 [S] |
| GPIO 26 [S] | GPIO 20 [S] |
| Ground      | GPIO 21 [S] |

Legend

- Steppers [S]
- Display [D] (uses 3.3V Linear Regulator for power)
- dpad [I] (input)

### Disclaimer

Most of the physical dimensions on part models are not 100% accurate. They are for modeling the major dimensions for mounting/fitting in terms of volume.

This project might be a fail just because of how heavy/cumbersome it is.

A different approach is to use a tripod, ground-based tracker. Whether it tracks on its own or you aim with your head. The self-tracking sounds more interesting.
