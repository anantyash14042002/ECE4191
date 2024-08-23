import time
import numpy as np
import cv2

# Import classes
from DiffDriveRobot import DiffDriveRobot, Controller

# Load parameters from callibration
wheel_radius = 0
wheel_sep = 0
camera_matrix = np.array()

# Initialize classes
bot = DiffDriveRobot(wheel_radius=wheel_radius, wheel_sep=wheel_sep,)


# Infinite loop
while True:
    # While number of balls on robot < capacity:
        # Detect balls and save locations
        # Plan path
        # Navigate to ball and collect
    # Drive to box
    # Deposit balls 
    pass


