# Implements a differential drive robot class

# Libraries
import numpy as np

class DiffDriveRobot:
    def __init__(self, wheel_radius = 0.05, wheel_sep = 0.15):
        self.x = 0.0        # Initial x coordinate
        self.y = 0.0        # Initial y coordinate
        self.theta = 0.0    # Orientation

        self.wl = 0.0 #rotational velocity left wheel
        self.wr = 0.0 #rotational velocity right wheel
        
        # self.I = inertia
        # self.d = drag
        # self.dt = dt
        
        self.r = wheel_radius
        self.l = wheel_sep

    def base_velocity(self):
        pass

    def update_pose(self):
        pass


# Implement a PI controller 
class Controller:
    
    ## Play around with gain values
    def __init__(self, Kp = 0.1, Ki = 0.01, wheel_radius = 0.05, wheel_sep = 0.15):
        self.Kp = Kp
        self.Ki = Ki


        self.r = wheel_radius
        self.l = wheel_sep

        # Initialise error term for integral control
        self.e_l = 0.0      # Left wheel
        self.e_r = 0.0      # Right wheel


    def generate_control(self):
        pass
