import RPi.GPIO as GPIO

# define pins
in1_pin = 12
in2_pin = 13
in3_pin = 18
in4_pin = 19
#enLA_pin = 36
#enLB_pin = 38
#enRA_pin = 35
#enRB_pin = 37

# Set the GPIO mode to use physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Set pins output
GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)

# Set up PWM
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

try:
    while True: 
        left_velocity = float(input("Enter left wheel velocity [-1,1]"))
        if( -1 <= left_velocity <= 0): # backwards
            pwm_IN1.ChangeDutyCycle(0)
            pwm_IN2.ChangeDutyCycle(abs(left_velocity))
        elif(left_velocity <= 1):
            pwm_IN1.ChangeDutyCycle(left_velocity)
            pwm_IN2.ChangeDutyCycle(0)
        else : 
            print("Invalid input \n")
            

        right_velocity = float(input("Enter right velocity velocity [-1,1]"))
        if( -1 <= right_velocity <= 0): # backwards
            pwm_IN3.ChangeDutyCycle(0)
            pwm_IN4.ChangeDutyCycle(abs(right_velocity))
        elif(right_velocity <= 1):
            pwm_IN3.ChangeDutyCycle(right_velocity)
            pwm_IN4.ChangeDutyCycle(0)
        else : 
            print("Invalid input \n")

except KeyboardInterrupt:
    print("hello\n")

finally:
    # Stop PWM and clean up GPIO settings
    pwm_IN1.stop()
    pwm_IN2.stop()
    pwm_IN3.stop()
    pwm_IN4.stop()
    GPIO.cleanup()
