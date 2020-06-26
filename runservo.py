# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:23:25 2020

@author: Dustin Tengdyantono
"""

#this code is meant to use the servo.py code
from pymemcache.client import base
from servo import shervo
#from pixstabilizer import pixelstabilizer
import math
import time
seervo= shervo()
cache_dat= base.Client(('localhost',11211))
#stabilize = pixelstabilizer()
div = 5 #total numbers that we summed up
angleout=90
anglenow =90
#initializing
print("Initializing Servo") 
seervo.reset_()
print("Initializing complete")

while True: 
    #initial conditions needed

    done= cache_dat.get('end_cycle')
    finished = str(done.decode('utf-8'))
    dist= cache_dat.get('distance')
    distance= float(dist.decode('utf-8'))
    if distance <=85 and distance>=1:
        time.sleep(0.5)
        while finished == 'False':
            ''' 
            n=0      #setting up the counter
            listdfhd = list()
            listrealfhd = list()
            listdis = list()
            '''
            cache_dat.set('servo_running','False')
            print ('coba sekali jos')
            
            #getting data from pymemcache
            dy_fhd= cache_dat.get('y_est_temp_points')
            dynamicfhd= float(dy_fhd.decode('utf-8'))
            yfhd= cache_dat.get('y_forehead')
            yforehead= float(yfhd.decode('utf-8'))
            dist= cache_dat.get('distance')
            distance= float(dist.decode('utf-8'))


            '''
            listdfhd.append(dynamicfhd)
            listrealfhd.append(yforehead)
            listdis.append(distance)
            n+=1

            #printing out lists
            print('list fhd = '+ str(listdfhd))
            print('list realfhd = '+ str(listrealfhd))
            print('list distance = '+ str(listdis))

            #doing calculation
            totaldfhd= sum(listdfhd[n-5:n]) 
            totalrealfhd = sum(listrealfhd[n-5:n])  
            totaldis= sum(listdis[n-5:n])          
            avgdfhd = totaldfhd/div
            avgrealfhd = totalrealfhd/div
            avgdis = totaldis/div
            '''

            print ("(1) delta dynamic forehead y is " + str(dynamicfhd)+ ' pixels')
            print ("(2) real forehead y is " + str(yforehead)+ ' pixels')
            print ("(3) distance is " +str (distance)+ ' cm')
            
            '''            
            #making the lists empty again and counter to 0
            listdfhd = list()
            listdis = list()
            listrealfhd = list()
            n=0
            '''
            cache_dat.set('servo_running','True')
            #math to find the value of the angle that's going to be put in
            angle = float(math.degrees(math.atan((dynamicfhd-yforehead)/800*60.5/distance))) #still pixel/centimeter
            angleout = angle *0.8 #bisa kasih magic number
            print ("(4) change in angle is at " + str(angle))
            print ("(5) change in angle output to servo is at " + str(angleout))
            anglenow= seervo.converter(angleout)   
            time.sleep(0.001)
            break

        
        while finished == 'True':
            cache_dat.set('servo_running','True ')
            time.sleep(0.5)
            print('process is completed, returning back to initial state')
            seervo.return_to_ninety(anglenow)
            print('initial state achieved')
            anglenow= 90
            time.sleep(1)
            break
        
    elif distance >85:
        cache_dat.set('servo_running','False')
        time.sleep(1)
        print ('(01)distance is greater than 85, which is at '+ str(distance))
        seervo.return_to_ninety(anglenow)
        anglenow= 90
        time.sleep(0.5)
    elif distance <1:
        cache_dat.set('servo_running','False')
        time.sleep(1)
        print ('(02)distance is smaller than 1, which is at '+ str(distance))
        seervo.return_to_ninety(anglenow)
        anglenow= 90
        time.sleep(0.5)       
    else:
        cache_dat.set('servo_running','False')
        print ('pass from main script')
        pass