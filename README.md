# EyeTrackerArduino
This project (top 15 at YorkU Hacks 2018) represents the MVP of a
device that steers wheelchairs (and potentially any actuator) with
only head/eye movement. It uses the Python OpenCV library to track
the user's eyes, while communicating over serial with an Arduino
that controls a servomotor (that represents the steering mechanism
for a wheelchair) and some indicator LEDs.

## The Problem
Individuals lacking upper body control as a result of diseases and
disablities such as:
* Parkinson’s disease
* Multiple sclerosis

The current technology is inadequate.
  * Sip-and-Puff controllers
    * One sips to turn one direction, puffs to turn the other way
  * Issues:
    * High cost sensors (~$300)
    * Injury-prone
    * Break easily, require repairs often
    * Require constant cleaning

![Current tech: sip-and-puff wheelchair controllers](/Assets/sip-and-puff.png)

## The Idea
Our idea was to enable the use of simple, intuitive gestures to control
wheelchairs. To this end, we decided to use computer vision to track
the movement of eyes about an imaginary "center-line", where looking
to the left makes the device turn left, while looking right makes it
turn right.

Eventually we would like to have the frontend be mounted on the user's
smartphone, making it lower cost and more accessible. It would use wireless
communications to "speak" to the steering mechanism of the wheelchair.

## Benefits
* Affordability
* Only uses existing tech
* Less injury-prone
* Less physical effort required to use

## Technologies Used

* Arduino
  * Servo
  * LEDs (for indicators)
* Python
  * OpenCV
  * PySerial
