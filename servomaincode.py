# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:35:06 2020

@author: Dustin Tengdyantono

for servo using bus 0 (pins 28 and 27 for scl and sda)
"""
import time
from adafruit_servokit import ServoKit
from pymemcache.client import base
import busio
import board
cache_dat= base.Client(('localhost',11211))

class servo_:
    
    def __init__(self):
        self.dpixels= 0
        self.angle= 90
        self.angle0= 90
        self.angle0p= 90
        self.i2c_bus0=(busio.I2C(board.SCL, board.SDA))
        self.kit= ServoKit(channels=16, reference_clock_speed=25000000, i2c=self.i2c_bus0)
        self.kit.servo[15].angle = self.angle
        self.kit.servo[14].angle = self.angle
        self.ts= 0.01 #time sleep yang diperuntukkan untuk forloop kecepatan daripada servo itu sendiri
        self.norm = 15
        self.n=0
        self.m= 0
        self.t=90

    def converter(self,pix_in):
        self.dpixels= int(pix_in)*-1
        if -1.5<self.dpixels<1.5:
            time.sleep(0.01)
            print("currently it's at "+ str(float(self.angle0p))+"degree, nothing changed")
            pass
        else:
            self.angle = self.angle + self.dpixels
            self.angle0p =  self.angle0p - self.dpixels
            self.deltaangle = self.angle-self.angle0
           
            #run the servo with changing instantaneous speed
            self.servo_mover(self.angle0,self.angle,self.deltaangle,self.norm)
            print("currently it's at "+ str(float(self.angle0p))+" degree") #if it gets break in the middle of the iteration, self will make sure that angle0p is using the last value from servo_mover
        return self.angle0,self.angle0p

    def reset_(self):
        self.kit.servo[15].angle = 90
        print('reset')
            
    def return_to_ninety(self,angle0,angle0p):
        if self.angle0 >= 89.5 and self.angle0<=90.5:
            print('let it pass')
            time.sleep(0.5)
            pass

        elif self.angle0 < 89.5:  
        #self.angle = self.angle0 + self.angle
        
            for t in range (int(self.angle0*self.norm),90*self.norm,4):
                self.kit.servo[15].angle = t/self.norm
                time.sleep (self.ts)
            print('return to 90 naik from the angle '+ str(self.angle0))
            self.angle0= 90
            self.angle0p= 90
            return(self.angle0)
        elif self.angle0 > 90.5:
            for t in range (int(self.angle0*self.norm),90*self.norm,-4):
                self.kit.servo[15].angle = t/self.norm
                time.sleep (self.ts)
            print('return to 90 turun from the angle '+ str(self.angle0))
            self.angle0 = 90
            self.angle0p= 90
            return(self.angle0)
    
    def servo_mover(self,angle0, angle, deltaangle, norm ):
        ovrlp = cache_dat.get('y_overlap')
        overlap = str(ovrlp.decode('utf-8'))

        if overlap == 'False':

            if self.angle0 < self.angle:
                while self.n<15:
                    while self.n <5:
                        self.m+=1
                        for t in range (int((self.angle0+self.deltaangle*self.n/15)*self.norm),int((self.angle0+self.deltaangle*(self.n+2)/15)*self.norm),self.m):
                            self.kit.servo[15].angle = t/self.norm
                            try:
                                ovrlp = cache_dat.get('y_overlap')
                                overlap = str(ovrlp.decode('utf-8'))
                            except:
                                overlap == 'False'

                            if overlap == 'True':
                                time.sleep(0.01)
                                print('break overlap inside servo.py1')
                                time.sleep(0.5)
                                break
                            else:
                                time.sleep (self.ts)
                        self.n+=1
                        
                    while self.n>=5 and self.n<10:
                        for t in range (int((self.angle0+self.deltaangle*self.n/15)*self.norm),int((self.angle0+self.deltaangle*(self.n+1)/15)*self.norm),self.m):
                            try:
                                ovrlp = cache_dat.get('y_overlap')
                                overlap = str(ovrlp.decode('utf-8'))
                            except:
                                overlap == 'False'
                            
                            self.kit.servo[15].angle = t/self.norm
    
                            if overlap == 'True':
                                time.sleep(0.01)
                                print('break overlap inside servo.py2')
                                time.sleep(0.5)
                                break
                            else:
                                time.sleep (self.ts)
                        self.n+=1
                        self.m-=1

                    while self.n>=10 and self.n<15:
                        self.m=1
                        for t in range (int((self.angle0+self.deltaangle*self.n/15)*self.norm),int((self.angle0+self.deltaangle*(self.n+1)/15)*self.norm),self.m):
                            try:
                                ovrlp = cache_dat.get('y_overlap')
                                overlap = str(ovrlp.decode('utf-8'))
                            except:
                                overlap == 'False'
                            
                            self.kit.servo[15].angle = t/self.norm
    
                            if overlap == 'True':
                                time.sleep(0.01)
                                print('break overlap inside servo.py3')
                                time.sleep(0.5)
                                break
                            else:
                                time.sleep (self.ts)
                        self.n+=1

            elif self.angle0 > self.angle:  
                while self.n<15:
                    while self.n <5:
                        self.m+=1
                        for t in range (int((self.angle0+self.deltaangle*self.n/15)*self.norm),int((self.angle0+self.deltaangle*(self.n+1)/15)*self.norm),-self.m):
                            self.kit.servo[15].angle = t/self.norm
                            try:
                                ovrlp = cache_dat.get('y_overlap')
                                overlap = str(ovrlp.decode('utf-8'))
                            except:
                                overlap == 'False'

                            if overlap == 'True':
                                time.sleep(0.01)
                                print('break overlap inside servo.py4')
                                time.sleep(0.5)
                                break
                            else:
                                time.sleep (self.ts)
                        self.n+=1
            
                    while self.n>=5 and self.n<10:
                        for t in range (int((self.angle0+self.deltaangle*self.n/15)*self.norm),int((self.angle0+self.deltaangle*(self.n+1)/15)*self.norm),-self.m):
                            self.kit.servo[15].angle = t/self.norm
                            try:
                                ovrlp = cache_dat.get('y_overlap')
                                overlap = str(ovrlp.decode('utf-8'))
                            except:
                                overlap == 'False'

                            if overlap == 'True':
                                time.sleep(0.01)
                                print('break overlap inside servo.py5')
                                time.sleep(0.5)
                                break
                            else:
                                time.sleep (self.ts)
                        self.n+=1
                        self.m-=1
                
                    while self.n>=10 and self.n<15:
                        self.m=1
                        for t in range (int((self.angle0+self.deltaangle*self.n/15)*self.norm),int((self.angle0+self.deltaangle*(self.n+1)/15)*self.norm),-self.m):
                            try:
                                ovrlp = cache_dat.get('y_overlap')
                                overlap = str(ovrlp.decode('utf-8'))
                            except:
                                overlap == 'False'
                            
                            self.kit.servo[15].angle = t/self.norm
    
                            if overlap == 'True':
                                time.sleep(0.01)
                                print('break overlap inside servo.py6')
                                time.sleep(0.5)
                                break
                            else:
                                time.sleep (self.ts)
                        self.n+=1
                    

            print('apa aja boleh')
            self.n=0
            self.m=0
            self.angle0 = (t/self.norm)
            self.angle0p = (180 - t/self.norm)
            print('udah keluar dari loop pergantian kecepatan')
            time.sleep(0.01)
            self.t= t

        elif overlap == 'True':
            self.n=0
            self.m=0
            self.angle0 = (self.t/self.norm)
            self.angle0p = (180 - self.t/self.norm)
            print ('is currently overlapping, therefore servo isnt moving anymore')
            time.sleep(0.5)
            print('time sleep 0.5 second because its true')
        


