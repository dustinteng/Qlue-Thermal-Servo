# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:35:06 2020

@author: Dustin Tengdyantono

for servo using bus 0 (pins 28 and 27 for scl and sda)
"""
import time
from adafruit_servokit import ServoKit
import busio
import board

class shervo:
    
    def __init__(self):
        self.dpixels= 0
        self.angle= 90
        self.angle0= 90
        self.angle0p= 90
        self.i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))
        self.kit= ServoKit(channels=16, reference_clock_speed=25000000, i2c=self.i2c_bus0)
        self.kit.servo[15].angle = self.angle
        self.kit.servo[14].angle = self.angle

    def converter(self,pix_in):
        self.dpixels= int(pix_in)*-1
        if -1<self.dpixels<1:
            time.sleep(1)
            print("currently it's at "+ str(self.angle)+"degree, nothing changed")
            pass
        else:
            time.sleep(1)
            self.angle = self.dpixels + self.angle
            self.angle0p =  self.angle0p - (self.dpixels)
            deltaangle = self.angle-self.angle0
            if deltaangle >=-5 and deltaangle <=5:
                if self.angle0 < self.angle:
                    for t in range (self.angle0*10,self.angle*10,1):
                        self.kit.servo[15].angle = t/10
                        self.kit.servo[14].angle = t/10
                        time.sleep (0.01)
                elif self.angle0 > self.angle:
                    for t in range (self.angle0*10,self.angle*10,-1):
                        self.kit.servo[15].angle = t/10
                        self.kit.servo[14].angle = t/10
                        time.sleep (0.01)
                self.angle0 = self.angle
            else:
                if self.angle0 < self.angle:
                    for t in range (self.angle0*10,self.angle*10,1):
                        self.kit.servo[15].angle = t/10
                        self.kit.servo[14].angle = t/10
                        time.sleep (0.001)
                elif self.angle0 > self.angle:
                    for t in range (self.angle0*10,self.angle*10,-1):
                        self.kit.servo[15].angle = t/10
                        self.kit.servo[14].angle = t/10
                        time.sleep (0.001)
                self.angle0 = self.angle

            print("currently it's at "+ str(self.angle0p)+" degree")
            return self.angle0p

    def reset_(self):
        self.kit.servo[15].angle = 90
        self.kit.servo[14].angle = 90
        print('reset')
            
    def return_to_ninety(self,angle0):
        if self.angle0 >= 89.5 and self.angle0<=90.5:
            print('let it pass')
            time.sleep(0.5)
            pass

        elif self.angle0 < 89.5:  
        #self.angle = self.angle0 + self.angle
            for t in range (self.angle0*10,90*10,1):
                self.kit.servo[15].angle = t/10
                self.kit.servo[14].angle = t/10
                time.sleep (0.005)
            print('return to 90 naik from the angle '+ str(self.angle0))
            self.angle0= 90
            return(self.angle0)
        elif self.angle0 > 90.5:
            for t in range (self.angle0*10,90*10,-1):
                self.kit.servo[15].angle = t/10
                self.kit.servo[14].angle = t/10
                time.sleep (0.005)
            print('return to 90 turun from the angle '+ str(self.angle0))
            self.angle0 = 90
            return(self.angle0)