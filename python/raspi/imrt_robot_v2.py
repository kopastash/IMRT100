# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 150
TURNING_SPEED = 150
STOP_DISTANCE = 20
TURN_DISTANCE = 20

def stop_robot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)



def drive_robot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.10)



def turn_right():
    for i in range(10):
        motor_serial.send_command(TURNING_SPEED * RIGHT, -TURNING_SPEED * RIGHT)
        time.sleep(0.10)



def turn_left():
    for i in range(10):
        motor_serial.send_command(TURNING_SPEED * LEFT, -TURNING_SPEED * LEFT)
        time.sleep(0.10)



# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 10 #Hz
execution_period = 1. / execution_frequency #seconds


# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ###############################################################
    # This is the start of our loop. Your code goes below.        #
    #                                                             #
    # An example is provided to give you a starting point         #
    # In this example we get the distance readings from each of   #
    # the two distance sensors. Then we multiply each reading     #
    # with a constant gain and use the two resulting numbers      #
    # as commands for each of the two motors.                     #
    #  ________________________________________________________   #
    # |                                                        |  #
    # V                                                           #
    # V                                                           #
    ###############################################################






    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()
    dist_5 = motor_serial.get_dist_5()
    print("FRONT:", dist_1, "RIGHT:", dist_2, "RIGHT_45:", dist_3, "LEFT:", dist_4, "LEFT_45:", dist_5)

    LEFT = dist_4
    LEFT_45 = dist_5
    FRONT = dist_1
    RIGHT_45 = dist_3
    RIGHT = dist_2
    
    # Check if there is an obstacle in the way
    if dist_1 < STOP_DISTANCE:
        # There is an obstacle in front of the robot
        # First let's stop the robot for 1 second
        print("Obstacle!")
        stop_robot(0.5)

        # Reverse for 0.25 second
        drive_robot(BACKWARDS, 0.25)

        # Turn set angle
        if dist_2 and dist_4 < TURN_DISTANCE:
            turn_right()
            turn_right()
        
        elif dist_2 < dist_4:
            turn_left()
        
        elif dist_2 > dist_4:
            turn_right()

    elif dist_3 < TURN_DISTANCE:
        motor_serial.send_command(DRIVING_SPEED + 10, DRIVING_SPEED - 10)
        time.sleep(0.10) 

    elif dist_5 < TURN_DISTANCE:
        motor_serial.send_command(DRIVING_SPEED - 10, DRIVING_SPEED + 10)
        time.sleep(0.10) 

    else:
        # If there is nothing in front of the robot it continus driving forwards

        error = 20 - dist_4

        pid = 2 * error
        if error > 10:
          pid = 50
        if error < -10:
          pid = -50

        motor_serial.send_command(DRIVING_SPEED + pid, DRIVING_SPEED - pid)
        time.sleep(0.10) 


  
                



    ###############################################################
    #                                                           A #
    #                                                           A #
    # |_________________________________________________________| #
    #                                                             #
    # This is the end of our loop,                                #
    # execution continus at the start of our loop                 #
    ###############################################################
    ###############################################################





# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("Goodbye")
