# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:23:25 2020

@author: Dustin Tengdyantono
"""

#this code is meant to use the servo.py code
from pymemcache.client import base
from servomaincode import servo_
import math
import time
servo= servo_()
cache_dat= base.Client(('localhost',11211))
angleout= 90
anglenow= 90
anglenowp = 90


#initializing
print("Initializing Servo") 
servo.reset_()
print("Initializing complete")
time.sleep (0.5)
while True: 
    try:
        #initial conditions needed
        try:
            dist= cache_dat.get('distance')
            distance= float(dist.decode('utf-8'))
        except:
            distance = 100
        if distance <=85 and distance>=1:
            time.sleep(0.2)
            try:
                done= cache_dat.get('end_cycle')
                finished = str(done.decode('utf-8'))
                ovrlp = cache_dat.get('y_overlap')
                overlap = str(ovrlp.decode('utf-8'))
                dist= cache_dat.get('distance')  #to update the current distance inside this while loop
                distance= float(dist.decode('utf-8'))
                yfhd= cache_dat.get('y_forehead')
                yforehead= float(yfhd.decode('utf-8'))
                #dy_fhd= cache_dat.get('y_est_temp_points')
                #dynamicfhd= float(dy_fhd.decode('utf-8'))
                dynamicfhd=295 #no longer following the dynamic point since we are using thermal imaging
            except:
                distance = 100
                overlap = 'False'
                finished = 'False'
                yforehead = float(295)
                dynamicfhd = float(295)

            if finished == 'True':
                #cache_dat.set('servo_running','True')
                time.sleep(0.5)
                print('process is completed, returning back to initial state')
                print ('anglenow is '+ str(anglenow) + ' degree')
                servo.return_to_ninety(anglenow,anglenowp)
                print('initial state achieved')
                anglenow= 90
                time.sleep(1)
                break

            if yforehead == float(99999):
                time.sleep(0.5)
                print ('subject gone missing')
                print ('anglenow is '+ str(anglenow) + ' degree')
                servo.return_to_ninety(anglenow,anglenowp)
                print('initial state achieved')
                anglenow = 90
                anglenowp = 90
                time.sleep(1)
                break

            if distance >85:
                print('subject is out of range (subject >85)')
                break
            elif distance<1:
                print('subject is out of range (subject <1)')
                break

            if overlap == 'True':
                while finished == 'False' and yforehead != float(99999) and distance < 85:
                    print('overlap udah True tapi finished masi false, waiting for the iteration to be completed')
                    time.sleep(0.5)
                    done= cache_dat.get('end_cycle')
                    finished = str(done.decode('utf-8'))
                    yfhd= cache_dat.get('y_forehead')
                    yforehead= float(yfhd.decode('utf-8'))
                    dist= cache_dat.get('distance')  #to update the current distance inside this while loop
                    distance= float(dist.decode('utf-8'))
                    print('finish state'+finished)
                    print('y forehead state'+ str(y_forehead))
                    print('current distance' + str(distance))


                while finished == 'True' or yforehead == float(99999) or distance >85:
                    break
                else:
                    break

            if finished == 'False' and overlap == 'False':
                #setting up cache to be used by others
                cache_dat.set('servo_running','False')
                #math to find the value of the angle that's going to be put in
                angle = float(math.degrees(math.atan((dynamicfhd-yforehead)/800*130.8/distance))) #still pixel/centimeter
                angleout = angle *1.3 #bisa kasih magic number
                total = anglenow+angleout 
                try:
                    total >180 and total <0
                except:
                    if anglenow >90:
                        print ('you are out of the maximum tilting range')
                    elif anglenow <90:
                        print('you are out of the minimum tilting range')
                    else:
                        print('stay')
                    angle = 0
                    angleout = 0
                print ("(1) delta dynamic forehead y is " + str(dynamicfhd)+ ' pixels')
                print ("(2) real forehead y is " + str(yforehead)+ ' pixels')
                print ("(3) distance is " +str (distance)+ ' cm')
                print ("(4) change in angle is at " + str(angle))
                print ("(5) change in angle output to servo is at " + str(angleout))
                anglenow,anglenowp= servo.converter(angleout)   

                time.sleep(0.01)

        if distance >85:
           # cache_dat.set('servo_running','False')
            time.sleep(0.5)
            print ('(01) distance is greater than 85, which is at '+ str(distance))
            servo.return_to_ninety(anglenow,anglenowp)
            anglenow= 90
            anglenowp= 90
            time.sleep(0.5)

        if distance <1:
            #cache_dat.set('servo_running','False')
            time.sleep(0.5)
            print ('(02) distance is smaller than 1, which is at '+ str(distance))
            servo.return_to_ninety(anglenow,anglenowp)
            anglenow= 90
            anglenowp= 90
            time.sleep(0.5) 

        else:
            #cache_dat.set('servo_running','False')
            print ('pass from main script')

    except KeyboardInterrupt:
        print('ada gangguan dari keyboard')
        servo.return_to_ninety(anglenow,anglenowp)
    
    '''except ValueError:
        print('you are out of range')
        if anglenow>90:
            print('atas')
        else:
            print('bawah')
        servo.return_to_ninety(anglenow,anglenowp)
    '''
        

