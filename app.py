from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
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
def motorControl(motorInput):
    left_velocity = motorInput[0]
    right_velocity = motorInput[1]
    if -1 <= left_velocity <= 0:  # Backward
        pwm_IN1.ChangeDutyCycle(0)
        pwm_IN2.ChangeDutyCycle(abs(left_velocity) * 100)
    elif 0 < left_velocity <= 1:  # Forward
        pwm_IN1.ChangeDutyCycle(left_velocity * 100)
        pwm_IN2.ChangeDutyCycle(0)
    else:
        print("Invalid left wheel velocity. Please enter a value between -1 and 1.")
        return

    if -1 <= right_velocity <= 0:  # Backward
        pwm_IN3.ChangeDutyCycle(0)
        pwm_IN4.ChangeDutyCycle(abs(right_velocity) * 100)
    elif 0 < right_velocity <= 1:  # Forward
        pwm_IN3.ChangeDutyCycle(right_velocity * 100)
        pwm_IN4.ChangeDutyCycle(0)
    else:
        print("Invalid right wheel velocity. Please enter a value between -1 and 1.")
        return

# Function to handle encoder measurement
def measure_encoders():
    distL, distR = 0, 0

    def encoder_callback(channel):
        nonlocal distL, distR
        if channel == enLB_pin:
            distL += 1
        elif channel == enRB_pin:
            distR += 1

    GPIO.add_event_detect(enLB_pin, GPIO.RISING, callback=encoder_callback)
    GPIO.add_event_detect(enRB_pin, GPIO.RISING, callback=encoder_callback)

    try:
        while True:
            # Output encoder readings
            print(f"Left Wheel Count: {distL}")
            print(f"Right Wheel Count: {distR}\n")
            distL, distR = 0, 0
            threading.Event().wait(1)  # Sleep for 1 second
    finally:
        GPIO.remove_event_detect(enLB_pin)
        GPIO.remove_event_detect(enRB_pin)

###############
## FLASK APP ##
###############

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/clientData', methods=['POST'])
def receive_data():
    data = request.json
    motorControlDataRecieved = data.get('motorControlData')
    if motorControlDataRecieved is not None:
        motorControl(motorControlDataRecieved)
    return jsonify({"message": "Data received successfully"})

if __name__ == '__main__':
    # Start the encoder measurement thread
    #encoder_thread = threading.Thread(target=measure_encoders)
    #encoder_thread.daemon = True  # Daemonize thread to exit when the main program exits
    #encoder_thread.start()

    try:
        app.run(host='0.0.0.0', port=6969, debug=False)  # Use debug=False for production
    except KeyboardInterrupt:
        pass
    finally:
        # Stop PWM and clean up GPIO settings
        pwm_IN1.stop()
        pwm_IN2.stop()
        pwm_IN3.stop()
        pwm_IN4.stop()
        GPIO.cleanup()
