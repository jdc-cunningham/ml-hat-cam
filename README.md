### About

An auto-zoom hat-mounted camera using an Arducam IMX477 with 8-50mm lens and ML for rc plane detection

<img src="./devlog/images/ml-hat-cam.JPG"/>

### The vision

<img src="./devlog/images/layout.jpg"/>

Actually I decide the camera will just dangle to reduce moment arm/closer to hat. I'll just rotate the video 90 deg before saving.

### Note

Try to avoid using `GPIO 1` this affects the camera (not detected).

It can be avoided if you don't have a shared ground connected but requires a switch until after boot.

### Progress
- [ ] physical body
  - [x] usable lens focus/tele assembly (01/27/2023)
  - [ ] display and dpad
  - [ ] full design (attachable to hat)
- [ ] functionality code
  - [x] steppers and position tracking (02/09/2023)
    - [x] motion (01/28/2023)
    - [x] track in db for boot resume (02/09/2023)
  - [ ] menu design
  - [ ] dpad bindings
- [x] auto focus (02/12/2023)
  - [x] some method like comparing frames, more blurry go other way
    - used laplace variance
- [ ] auto zoom
  - use ML to find target, then zoom
- [ ] machine learning
  - train small shots of plane sillhouette against wall
  - record actual flying footage, label samples, train model
