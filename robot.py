import pypot.dynamixel
import serial
from math import cos, sin, radians, atan2
from decimal import *
import time
import pandas as pd
class Robot:
    def __init__(self, port1, port2):
        port1 = '/dev/tty'+port1
        port2 = '/dev/tty'+port2
        self.origin = None
        self.dxl_io = pypot.dynamixel.DxlIO(port1)
        self.set_origin()
        self.arduino_ser = serial.Serial(port2,9600)
        self.shape_name = 'square_mc'

    def set_origin(self):
        self.origin = self.get_current_pos()
    def go_to(self, pos):
        if(self.origin is None):
            print("Error: Origin is not yet set")
            return 0
        final_pos = (pos[0]+self.origin[0], pos[1] + self.origin[1])
        current_pos = self.get_current_pos()
        parallel_vec = (final_pos[0] - current_pos[0], final_pos[1] - current_pos[1])
        t = 0
        while(t < 1):
            temp = (current_pos[0] + t* parallel_vec[0], current_pos[1]+t*parallel_vec[1])
            values = self.inv_kin(temp)
            print(self.fwd_kin(values))
            # print(values)
            self.dxl_io.set_goal_position({6:values[0], 1:values[1]})
            t= t + 0.01
            time.sleep(0.01)
    def get_current_pos(self):
        present_angles = self.dxl_io.get_present_position((6,1))
        present_angles = (Decimal(present_angles[0]) , Decimal(present_angles[1]))
        current_pos = self.fwd_kin(present_angles)
        return current_pos
    def fwd_kin(self, angles):
        offset_x = lambda theta1 : 15*cos(radians(theta1[0])) + 15*cos(radians(theta1[1]+theta1[0]))
        offset_y = lambda theta1 : 15*sin(radians(theta1[0])) + 15*sin(radians(theta1[1])+radians(theta1[0]))
        angles = self.__convert_angles_motor_to_workspace__(angles)
        return (offset_x(angles), offset_y(angles))

    def inv_kin(self,goal, l1 = 15, l2 = 15):
        goaldis = (goal[0]**2) + (goal[1]**2)
        square_of_sum = (l1+l2)**2
        square_of_diff = (l1-l2)**2
        num_in_root = square_of_sum - goaldis
        den_in_root = goaldis - square_of_diff

        theta2_pos = 2*atan2(num_in_root**0.5,den_in_root**0.5)
        theta2_neg = -theta2_pos

        den2_in_theta1_pos = l1 + l2*cos(theta2_pos)
        den2_in_theta1_neg = l1 + l2*cos(theta2_neg)
        num2_in_theta1_pos = l2*sin(theta2_pos)
        num2_in_theta1_neg = l2*sin(theta2_neg)

        theta1_pos = atan2(goal[1],goal[0]) + atan2(num2_in_theta1_pos, den2_in_theta1_pos )
        theta1_neg = atan2(goal[1], goal[0]) + atan2(num2_in_theta1_neg, den2_in_theta1_neg)

        theta1_pos = (theta1_pos/3.14) * 180
        theta2_pos = -1*(theta2_pos/3.14) * 180
        theta = self.__convert_angles_workspace_to_motor__((theta1_pos, theta2_pos))
        return theta

    def __convert_angles_motor_to_workspace__(self,given, offset1 = 11, offset2 =9, dir1 = 1, dir2 = 1):
        ang1 = given[0] + 90 - offset1*dir1
        ang2 = given[1]*dir2 - offset2
        return (ang1, ang2)

    def __convert_angles_workspace_to_motor__(self, given, offset1 = 11, offset2 =9, dir1 = 1, dir2 = 1):
        ang1 = given[0] - (90 - offset1*dir1)
        ang2 = given[1]*dir2 + offset2
        return (ang1, ang2)
    # def check_within_bounds(posi):
    #     if(posi == (0,0))
    def send_to_arduino(self,text):
        self.arduino_ser.write(str.encode(text))
        time.sleep(0.5)

    def execute_file(self, file_name):
        df = pd.read_csv('Image_Planning/final/'+self.shape_name+'_final_solution.txt')
        for index,rows in df.iterrows():
            self.send_to_arduino(str(rows['draw']))
            self.go_to((rows['x2'],rows['y2']))

if(__name__ == "__main__"):
    r1 = Robot()
    print(r1.inv_kin((-21, 20)))
