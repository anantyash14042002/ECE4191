import RPi.GPIO as GPIO

# Set the GPIO mode to use physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Set pin 12 as an output
GPIO.setup(12, GPIO.OUT)

# Set up PWM on pin 12 with a frequency of 1000 Hz (1 kHz)
pwm = GPIO.PWM(12, 1000)

# Start PWM with a duty cycle of 0% (off)
pwm.start(0)

try:
    while True:
        # Get user input for the brightness level (0 to 1)
        brightness = float(input("Enter brightness level (0 to 1): "))

        # Ensure the input is within the valid range
        if 0 <= brightness <= 1:
            # Convert the input to a duty cycle percentage (0 to 100)
            duty_cycle = brightness * 100

            # Set the PWM duty cycle to control the brightness
            pwm.ChangeDutyCycle(duty_cycle)
        else:
            print("Please enter a value between 0 and 1.")

except KeyboardInterrupt:
    pass

finally:
    # Stop PWM and clean up GPIO settings
    pwm.stop()
    GPIO.cleanup()
