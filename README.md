# MPC Physics PhysRacer

LEGO race timing infrastructure

## About the Project

This project was created for Family STEM Day at Monterey Peninsula College. Designed as a fun activity for LEGO and racing fans of all ages to participate in, it features microsecond timing accuracy and a video-game like interface for logging and displaying race timing results.

The track itself is an [Aluminum Dynamics Track](https://www.pasco.com/products/lab-apparatus/mechanics/carts-and-tracks/aluminum-dynamics-track-2-2-m) (approx 2m long), inclined at roughly 25 degrees from horizontal. Starting and finish lines are implemented with [IR Beambreak Sensors](https://www.adafruit.com/product/2168) sensed by a [Teensy 4.1 microcontroller](https://www.pjrc.com/store/teensy41.html) (600 MHz Cortex-M7). The Teensy is dedicated almost entirely to timing the race start and stop conditions, allowing for a high degree of timing precision. Program execution has been instrumented and tested to loop in under 200 ns, so the resulting timings are reliable to microsecond accuracy.

Race results are reported to a Raspberry Pi minicomputer over a USB connection. Race times are then logged, along with user-entered nicknames, in the file highscores.txt. After recording a timing, the fastest times in race history are then displayed.
