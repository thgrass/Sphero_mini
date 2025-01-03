# Changes in this fork:
I rewrote the BLE packet handling stuff so it does no longer crash in unexpected cases and improved the overall asynchronous handling of BLE events. I also changed the logging slightly (at verbosity level 4) to better debug unknown packages. Collision detection now works flawlessly for me. I changed some of the examples slightly and added a new one to help me debugging the BLE communications.

# Remaining work / bugs:
Sometimes my Sphero sends unknown notification packages not related to collision detection I do not know details about and hence do not parse them - it could be battery level related stuff or something else.
Examples of these packages (in arrays of bytes):
[141, 8, 19, 6, 255, 5, 218, 216]
[141, 8, 19, 26, 255, 203, 216]

Also sometimes I get checksum errors on some other packages - this could be systemic or occasional transmission errors, but seem to be always packages whose second byte is decimal 9. Example packages are:
[141, 9, 26, 14, 65, 0, 171, 5, 216]
[141, 9, 22, 7, 46, 0, 171, 35, 216]
[141, 9, 26, 14, 35, 0, 171, 35, 216]
[141, 9, 22, 7, 76, 0, 171, 5, 216]


Below follows the original README:

# Sphero Mini
An unofficial Python library (work in progress) for controlling the [Sphero Mini](https://www.sphero.com/sphero-mini) robot. Note that, because the communications protocols are very different, this library will not work out-of-the-box for other types of Sphero robots (e.g. BB8, BB9, SPRK+, etc).

If you use this library for anything fun, please let me know - MProx.contact@gmail.com

## Dependencies:
This library is being tested with Python 3.6.5, but should work for other 3.x versions. This library also uses the Bluepy module for BLE communication, so make sure this is installed. On Debian-based Linux:

> $ sudo apt-get install libglib2.0-dev

> $ pip install bluepy --user

## Usage:
The class methods are well commented, so for usage of each, see sphero_mini.py. 

As examples demonstrating basic usage, see the three example files included in this repo. Make sure that both sphero_mini.py and sphero_constants.py are saved in the same folder as the example file. Then from linux command prompt, navigate to that folder and run the following command:

> $ python example_roll.py [sphero MAC address]

On Linux, use 'sudo hcitool lescan' to find your Sphero Mini's MAC address.

Note on usage: If you need to use delays, you can use time.sleep(), but this is a blocking function. Any asynchronous notifications that come in during the delay period can only be processed when it ends. If you need asynchronous commands (e.g. collision detection or sensor value updates) to be processed immediately, use the provided convenience function:

> sphero.wait(delay)

where delay is a value in seconds.

## Troubleshooting, known issues and work-arounds:
* Sometimes, the bluetooth module fails to connect. If this happens, try again. If it keeps failing, double-check your MAC address.
* If it still fails, try connecting the sphero to USB power briefly and then disconnecting. This resets the microcontroller.
* If it keeps failing after that, try re-booting your computer. I find that, expecially after terminating a script with a keyboard interrupt (ctrl+C), the bluetooth module may struggle to reconnect afterwards
* The notifications (messages returned from the sphero to the client) are a little experimental right now. Messages may not come through, or may not come through immediately. Do not rely on things like command acknowledgements, battery voltage reporting, etc. 
* Sometimes, bluetooth collisions seem to happen, possibly caused by unexpected asynchronous notifications (e.g. collision detection) coming in at a poor time. I have not found a way to prevent them. They cause the program to crash and it needs to be restarted, but they seem to be quite rare.
* When issuing the "roll" command, the device rolls in a given direction at a given speed, but automatically stops after a few seconds. Keep issuing the command to continue rolling.
* Some functions (sensors, collision detection, etc) may not function correctly on older firmware versions. This library is tested with version 0.0.12.0.45.0.0. Test your version with the sphero.getFirmwareVersion() function (see examples), and update with the official Sphero Mini app if necessary.

## Progress:
For now, this library can do the following:
* Come out of sleep mode
* Reset the heading (aiming)
* Query the battery voltage
* Change the LED's colour
* Set back LED intensity
* Roll in a specified direction at a given speed
* Go back to sleep (or deep sleep)
* Experimental: Detect collisions and produce partially-parsed collision detection information. Can also set a collision callback function to execute on collision (this is buggy - often crashes)
*  Experimental: Receive sensor data and save it as a class attribute. Currently available sensors: device orientation angles (IMU_pitch, IMU_roll, IMU_yaw), accelerometer values (IMU_acc_x, IMU_acc_y IMU_acc_z), and gyroscope values (IMU_gyro_x, IMU_gyro_y, IMU_gyro_z). Position and velocity are unavailable at this time, but should be added soon.
