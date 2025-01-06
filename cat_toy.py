import sphero_mini
import sys
import time

state = 'NORMAL'	# 'NORMAL' or 'HIT'
hit_time = 0
num_collisions = 0

# Collision handling callback(s)
def collision_callback():
    global num_collisions
    global state
    global hit_time

    if state == 'NORMAL':
        num_collisions += 1
        print("COLLISION # " + str(num_collisions))

        r = num_collisions % 3
        if r == 0:
            sphero.setLEDColor(red = 255, green = 0, blue = 0)
        if r == 1:
            sphero.setLEDColor(red = 0, green = 255, blue = 0)
        if r == 2:
            sphero.setLEDColor(red = 0, green = 0, blue = 255)

        hit_time = time.time()
        state = 'Hit'

    if state == 'Hit':
        return

# regular functions
def move_circle():
    # Move around:
    angle = 0
    angle_increment = 25
    start = time.time()

    # Approximate a circle by moving forward in short bursts, then adjusting heading slightly
    while(time.time() - start < 30):
        sphero.roll(30, angle)  # roll forwards (heading = 0) at speed = 30
        sphero.wait(0.2)          # Keep rolling for 0.5 seconds

        angle += angle_increment
        if angle >= 360:
            angle = 0

    sphero.roll(0, 0)       # stop
    sphero.wait(1)          # Allow time to stop

def move_line():
    sphero.roll(100, 0)      # start
    sphero.wait(1.0)         # Keep rolling for 1s

    sphero.roll(0, 0)       # stop
    sphero.wait(1)

def hit_move():
    sphero.roll(80, 0)
    sphero.wait(0.1)
    sphero.roll(0, 110)
    sphero.wait(0.1)
    sphero.roll(129, 0)
    sphero.wait(0.2)
    sphero.roll(0, 180)
    sphero.wait(0.1)
    sphero.roll(100, 0)
    sphero.wait(0.3)
    sphero.roll(50, 30)
    sphero.wait(0.2)
    sphero.roll(60, 300)
    sphero.wait(0.2)

def check_battery():
    sphero.getBatteryVoltage()
    volt = sphero.v_batt
    if volt is not None:
        if volt < 3.65:
            print("## BATTERY LOW WARNING ##")
        if volt < 3.59:
            print("GRACEFUL SHUTDOWN DUE TO BATTERY (ALMOST) EMPTY")
            sphero.sleep()
            sphero.disconnect()
            sys.exit(1)

###

if len(sys.argv) < 2:
    print("Usage: 'python [this_file_name.py] [sphero MAC address]'")
    print("eg C9:B7:C4:39:E5:BC")
    print("On Linux, use 'sudo hcitool lescan' to find your Sphero Mini's MAC address")
    print("You can also store it in an environment variable..")
    exit(1)

MAC = sys.argv[1] # Get MAC address from command line argument
try:
    # Connect
    sphero = sphero_mini.sphero_mini(MAC, verbosity = 4)

    # battery voltage
    while sphero.v_batt == None:
        sphero.getBatteryVoltage()
    print(f"Battery voltage: {sphero.v_batt}v")

    # firmware version number
    while sphero.firmware_version == []:
        sphero.returnMainApplicationVersion()
    print(f"Firmware version: {'.'.join(str(x) for x in sphero.firmware_version)}")

    # set callback(s)
    sphero.configureCollisionDetection(callback=collision_callback)

    #
    starttime = time.time()

    battery_check_time = starttime

    # Main Loop
    while(1):
        if state == 'NORMAL':
            move_circle()
            move_line()

        if state == 'Hit':
            hit_move()
            if (time.time() - hit_time) > 1:		# set state back to normal after 1s
                state = 'NORMAL'

        if (time.time() - battery_check_time) > 300:	# Check every 5 min
            check_battery()
            battery_check_time = time.time()
except KeyboardInterrupt:
    sphero.sleep()
    sphero.disconnect()

