# pcb-drill

pcb-drill is a software that allows you to drill the holes in your pcb from underneath while aiming with a webcam.

# Setup

## The microcontroller part

In my setup the microcontroller is a Arduino Mega2560. It controls a stepper motor that uses an eccentric tappet to lift and lower the drill.
Whenever a byte is sent to the Arduino using the USB serial connection, one full turn will be done. The value of this byte doesn't matter.
If your setup is differnent to mine, you can easily modify the code. The only important thing is that when the byte is received, a full turn will be performed.

## The webcam GUI

The webcam GUI is written in Python and uses OpenCV for displaying the camera image and overlaying the crosshair.

# How to use

1. Connect the USB Webcam to your computer as well as the Arduino.

2. Turn the drill on.

3. Start drill-eye

4. Place a offcut of pcb under the camera and hold it.

5. Push the spacebar. Now the drill should lift and lower one time and drill a hole into the pcb.

6. Adjust the position, size and shape of the crosshair to fit your hole.

7. Drill your real pcb now.

# Keys

 - `Esc` quits the drill-eye software.

 - `Space` starts a drill cycle.

 - `Up-Arrow`, `Down-Arrow`, `Left-Arrow` and `Right-Arrow` move the crosshair.

 - `Shift` + `Up-Arrow` streches the circle more, `Shift` + `Down-Arrow` less. 

 - `Ctrl` + `Up-Arrow` increases, `Ctrl` + `Down-Arrow` decreases the line thickness.

 - `r` resets everything to default

# Problems & Questions

If you have questions don't hesitate to ask me: bouni@owee.de   




