import pydobot, serial  # Import pydobot and serial libraries for Dobot control

device = pydobot.Dobot(port='COM7')  # Connect to Dobot Magician, replace 'COM18' with the correct port (easily found in DobotStudio)

# Define target position
x, y, z, r = 100, 0, -30, 0  # Initialize variables x, y, z, and r for coordinates and rotation

start_z = 0  # Initial Z-position value
delta_z = 67  # Z-position change for calibration

speed = 300  # Initialize speed
acceleration = 500  # Initialize acceleration
device.speed(speed, acceleration)  # Set movement speed and acceleration

def vacuum_on():  # Function to turn on the vacuum pump
    device.suck(True)  # Activates the vacuum pump

def vacuum_off():  # Function to turn off the vacuum pump
    device.suck(False)  # Deactivates the vacuum pump

def wait(ms):  # Function for waiting
    device.wait(ms)  # Waits for the specified time in milliseconds

def center():  # Moves Dobot to the center position
    wait = True  # Set wait to True
    device.move_to(219, 0, start_z, r, wait=wait)  # Moves Dobot to the center position

def left45():  # Moves Dobot 45 degrees to the left
    wait = True  # Set wait to True
    device.move_to(150, 147, start_z, r, wait=wait)  # Moves Dobot to the left

def right45():  # Moves Dobot 45 degrees to the right
    wait = True  # Set wait to True
    device.move_to(144, -153, start_z, r, wait=wait)  # Moves Dobot to the right

def down():  # Moves Dobot to the down position
    wait = True  # Set wait to True
    (x1, y1, z1, r, j1, j2, j3, j4) = device.pose()  # Retrieves Dobot's current position
    device.move_to(x1, y1, start_z - delta_z, r, wait=wait)  # Moves Dobot down

def almost_down():  # Moves Dobot to almost the down position
    delta = 10  # Value to subtract from Z-position
    wait = True  # Set wait to True
    (x1, y1, z1, r, j1, j2, j3, j4) = device.pose()  # Retrieves Dobot's current position
    device.move_to(x1, y1, start_z - delta_z + delta, r, wait=wait)  # Moves Dobot almost down

def up():  # Moves Dobot to the up position
    wait = True  # Set wait to True
    (x1, y1, z1, r, j1, j2, j3, j4) = device.pose()  # Retrieves Dobot's current position
    device.move_to(x1, y1, start_z, r, wait=wait)  # Moves Dobot up

def main():  # Main function to execute a sequence of movements
    left45()  # Performs a left turn
    right45()  # Performs a right turn
    center()  # Moves Dobot to the center
    almost_down()  # Moves Dobot almost down
    vacuum_on()  # Turns on the vacuum pump
    down()  # Moves Dobot down
    wait(500)  # Waits for 500 milliseconds
    up()  # Moves Dobot up
    vacuum_off()  # Turns off the vacuum pump

if __name__ == "__main__":  # If the script is run directly, execute the main function
    main()  # Run the main function