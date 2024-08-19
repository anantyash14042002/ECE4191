import RPi.GPIO as GPIO

# define pins
in1_pin = 12
in2_pin = 13
in3_pin = 18
in4_pin = 19

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
        # Get user input for each pin's brightness level (0 to 1)
        brightness_in1 = float(input("Enter brightness level for IN1 (0 to 1): "))
        brightness_in2 = float(input("Enter brightness level for IN2 (0 to 1): "))
        brightness_in3 = float(input("Enter brightness level for IN3 (0 to 1): "))
        brightness_in4 = float(input("Enter brightness level for IN4 (0 to 1): "))

        # Ensure inputs are within the valid range
        if all(0 <= b <= 1 for b in [brightness_in1, brightness_in2, brightness_in3, brightness_in4]):
            # Convert inputs to duty cycle percentages (0 to 100)
            duty_cycle_in1 = brightness_in1 * 100
            duty_cycle_in2 = brightness_in2 * 100
            duty_cycle_in3 = brightness_in3 * 100
            duty_cycle_in4 = brightness_in4 * 100

            # Set the PWM duty cycle for each pin
            pwm_IN1.ChangeDutyCycle(duty_cycle_in1)
            pwm_IN2.ChangeDutyCycle(duty_cycle_in2)
            pwm_IN3.ChangeDutyCycle(duty_cycle_in3)
            pwm_IN4.ChangeDutyCycle(duty_cycle_in4)
        else:
            print("Please enter values between 0 and 1 for all inputs.")

except KeyboardInterrupt:
    pass

finally:
    # Stop PWM and clean up GPIO settings
    pwm_IN1.stop()
    pwm_IN2.stop()
    pwm_IN3.stop()
    pwm_IN4.stop()
    GPIO.cleanup()
