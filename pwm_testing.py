import RPi.GPIO as GPIO
import time
import threading

# Define motor control pins
in1_pin = 12
in2_pin = 13
in3_pin = 18
in4_pin = 19

# Define encoder pins
enLA_pin = 36  # hardware not working
enLB_pin = 38
enRA_pin = 35
enRB_pin = 37

# Set the GPIO mode to use physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Set pins as output for motor control
GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)

# Set pins as input for encoders
GPIO.setup(enLA_pin, GPIO.IN)
GPIO.setup(enLB_pin, GPIO.IN)
GPIO.setup(enRA_pin, GPIO.IN)
GPIO.setup(enRB_pin, GPIO.IN)

# Set up PWM for motor control
frequency = 15000
pwm_IN1 = GPIO.PWM(in1_pin, frequency)
pwm_IN2 = GPIO.PWM(in2_pin, frequency)
pwm_IN3 = GPIO.PWM(in3_pin, frequency)
pwm_IN4 = GPIO.PWM(in4_pin, frequency)

# Start PWM with a duty cycle of 0% (off) for all pins
pwm_IN1.start(0)
pwm_IN2.start(0)
pwm_IN3.start(0)
pwm_IN4.start(0)

# Function to handle motor speed changes
def change_speed():
    while True:
        user_input = input("Enter wheel velocities as 'left right' [-1, 1]: ")
        try:
            left_velocity, right_velocity = map(float, user_input.split())
            
            # Control left motor
            if -1 <= left_velocity <= 0:  # Backward
                pwm_IN1.ChangeDutyCycle(0)
                pwm_IN2.ChangeDutyCycle(abs(left_velocity) * 100)
            elif 0 < left_velocity <= 1:  # Forward
                pwm_IN1.ChangeDutyCycle(left_velocity * 100)
                pwm_IN2.ChangeDutyCycle(0)
            else:
                print("Invalid left wheel velocity. Please enter a value between -1 and 1.")
                continue
            
            # Control right motor
            if -1 <= right_velocity <= 0:  # Backward
                pwm_IN3.ChangeDutyCycle(0)
                pwm_IN4.ChangeDutyCycle(abs(right_velocity) * 100)
            elif 0 < right_velocity <= 1:  # Forward
                pwm_IN3.ChangeDutyCycle(right_velocity * 100)
                pwm_IN4.ChangeDutyCycle(0)
            else:
                print("Invalid right wheel velocity. Please enter a value between -1 and 1.")
                continue

        except ValueError:
            print("Invalid input format. Please enter two numeric values separated by a space.")
            continue

        # Sleep to reduce CPU usage
        time.sleep(2)

# Function to handle encoder measurement
def measure_encoders():
    while True:
        distL, distR = 0, 0
        prev_enLA = GPIO.input(enLA_pin)
        prev_enLB = GPIO.input(enLB_pin)
        prev_enRA = GPIO.input(enRA_pin)
        prev_enRB = GPIO.input(enRB_pin)
        initial_time = time.time()
        
        while (time.time() - initial_time) < 0.1:  # 100ms measurement interval
            enLA = GPIO.input(enLA_pin)
            enLB = GPIO.input(enLB_pin)
            enRA = GPIO.input(enRA_pin)
            enRB = GPIO.input(enRB_pin)
            
            # Count left encoder transitions
            if enLA != prev_enLA and enLA == GPIO.HIGH:
                # distL += 1
            prev_enLA = enLA
            
            if enLB != prev_enLB and enLB == GPIO.HIGH:
                distL += 1
            prev_enLB = enLB
            
            # Count right encoder transitions
            if enRA != prev_enRA and enRA == GPIO.HIGH:
                # distR += 1
            prev_enRA = enRA
            
            if enRB != prev_enRB and enRB == GPIO.HIGH:
                distR += 1
            prev_enRB = enRB
            
            # Small delay to avoid excessive CPU usage
            time.sleep(0.001)  # 1ms delay
        
        # Output encoder readings
        print(f"Left Wheel Count: {distL*2}")
        print(f"Right Wheel Count: {distR}\n")

# Start the speed-changing thread
speed_thread = threading.Thread(target=change_speed)
speed_thread.daemon = True  # Daemonize thread to exit when the main program exits
speed_thread.start()

# Start the encoder measurement thread
encoder_thread = threading.Thread(target=measure_encoders)
encoder_thread.daemon = True  # Daemonize thread to exit when the main program exits
encoder_thread.start()

try:
    while True:
        # Main thread can be used for other tasks or just sleep
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    # Stop PWM and clean up GPIO settings
    pwm_IN1.stop()
    pwm_IN2.stop()
    pwm_IN3.stop()
    pwm_IN4.stop()
    GPIO.cleanup()
