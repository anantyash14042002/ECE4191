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

    def base_velocity(self, wl, wr):
        v = (wl*self.r + wr*self.r)/2.0
        w = (wl - wr)/self.l
        
        return v, w

    def update_pose(self, duty_cycle_l, duty_cycle_r):

        # Get rotational velocity of each wheel from encoder
        # self.wl = None
        # self.wr = None
        
        v, w = self.base_velocity(self.wl,self.wr)
        
        self.x = self.x + self.dt*v*np.cos(self.th)
        self.y = self.y + self.dt*v*np.sin(self.th)
        self.th = self.th + w*self.dt
        
        return self.x, self.y, self.th


# Implement a PI controller 
class Controller:
    
    ## Play around with gain values
    def __init__(self, Kp = 0.1, Ki = 0.01, wheel_radius = 0.05, wheel_sep = 0.15):

        # Gains
        self.Kp = Kp
        self.Ki = Ki

        # Wheel radius and separation
        self.r = wheel_radius
        self.l = wheel_sep

        # Initialise error term for integral control
        self.e_left = 0.0      # Left wheel
        self.e_right = 0.0      # Right wheel


    def get_control(self, w_desired, w_measured, error):
        duty_cycle = np.clip(self.kp*(w_desired-w_measured) + self.Ki*error, -1.0, 1.0) # Clip value to between -1 and 1

        error_new = error + (w_desired-w_measured) # Update error term

        return duty_cycle, error_new
    
    # Generate drive signals for left and right wheel
    def drive(self, v_desired, w_desired, w_left, w_right):

        wl_desired = v_desired/self.r + self.l*w_desired/2 
        wr_desired = v_desired/self.r - self.l*w_desired/2
        
        duty_cycle_l, self.e_left = self.get_control(wl_desired,w_left, self.e_left)
        duty_cycle_r, self.e_right = self.get_control(wr_desired,w_right, self.e_right)

        return duty_cycle_l, duty_cycle_r
