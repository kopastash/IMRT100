# Custom code for IMRT100 robot project
# Author: Gruppe 4; Henrik J. Larsson, Carsten Emil Ruud Walaas, Mathilde Sofie Ødegaard Gaustad, Olav Asp, Storm Malme Vierskjær

# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
from math import sqrt,copysign


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

# Litt custom kode her

MÅLFART = 250           # v
AKSELBREDDE = 0.335     # L
ROTASJONSFART = 0       # w

VENSTRE = -1
HØYRE = 1
FREM = 1
BAK = -1
STOPPAVSTAND = 25

'''
vl = v - w*L/2
vr = v + w*L/2
'''

def roter(retning, varighet):
    speed = MÅLFART/3 * retning
    iterations = int(varighet * execution_frequency)

    for i in range(iterations):
        motor_serial.send_command(int(speed * -retning), int(speed * retning))
        time.sleep(0.10)

def kjør_frem(hastighet, rotasjon):
    motor_serial.send_command(hastighet + (rotasjon * AKSELBREDDE)/2, hastighet - (rotasjon * AKSELBREDDE)/2)


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


    # Get the current time
    iteration_start_time = time.time()


    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_4()      # Venstre
    dist_2 = motor_serial.get_dist_5()      # Venstre C
    dist_3 = motor_serial.get_dist_1()      # Front
    dist_4 = motor_serial.get_dist_3()      # Høyre C
    dist_5 = motor_serial.get_dist_2()      # Høyre


    # Calculate commands for each motor using sensor readings
    # In this simple example we will multiply each sensor reading
    # with a constant to obtain our commands

    distansemod = 1
    frontsensor = min(dist_2, dist_3, dist_4)

    if frontsensor < 50:
        distansemod = 1 - 10/(max(frontsensor, 15))

    MODFART = int(MÅLFART * distansemod)

    normalized = (2 * (min(dist_5, 20) - 0) / (20 - 0) - 1)

    svingfart = 1

    if frontsensor < 15 and (dist_5 or dist_1) < 30 and ((dist_5 - dist_1 > 10) or (dist_1 - dist_5 > 10)):
        retning = int(copysign(1, dist_1-dist_5)) # Gir 1 eller -1
        roter(retning, 0.5)
        print("Roterer")
    else:
        motor_serial.send_command(int(MODFART + (MODFART * normalized * 0.8)), int(MODFART - (MODFART * normalized * 0.7)))



    print("1 V:", dist_1, "    2 VC:", dist_2, "   3 F:", dist_3, "   4 HC:", dist_4, "   5 H:", dist_5, "   FS:", frontsensor)

    '''
    gain = 20


    if dist_2 <= 10:
        speed_motor_1, speed_motor_2 = int(10 * -1/(max(dist_2, 1)) * gain), int(10 * -1/dist_2 * gain)

    if dist_2 > 10:
        speed_motor_1 = int(sqrt(max((dist_3 - 5) * 1, 0) * (dist_2 * 2)/3)) * gain
        speed_motor_2 = int(sqrt(max((dist_1 - 5) * 1, 0) * (dist_2 * 2)/3)) * gain
    '''


    # Send commands to motor
    # Max speed is 400.
    # E.g.a command of 500 will result in the same speed as if the command was 400
    # motor_serial.send_command(speed_motor_1, speed_motor_2)



    # Here we pause the execution of the program for the apropriate amout of time
    # so that our loop executes at the frequency specified by the variable execution_frequency
    iteration_end_time = time.time() # current time
    iteration_duration = iteration_end_time - iteration_start_time # time spent executing code
    if (iteration_duration < execution_period):
        time.sleep(execution_period - iteration_duration)



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
