#!/usr/bin/env python3
import speech_recognition as sr
import rospy
from geometry_msgs.msg import Twist
r = sr.Recognizer()
rospy.init_node('ses_kontrol')
pub=rospy.Publisher('/hamer/cmd_vel',Twist,queue_size=5)
move=Twist()
while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        data = r.record(source, duration=5)
        print('Awaiting command...',end=' ')
        text = r.recognize_google(data,language='tr',show_all= True)
        text_str=str(text)
        print(text_str)
        if 'ilerle' in text_str:
            print("Moving Forward...")
            move.linear.x=0.5
            move.angular.z=0
            pub.publish(move)
        elif 'sağa dön' in text_str:
            print("Turning Right...")
            move.angular.z=-0.3
            move.linear.x=0
            pub.publish(move)
        elif 'sola dön' in text_str:
            print('Turning Left...')
            move.angular.z=0.3
            move.linear.x=0
            pub.publish(move)
        elif 'dur' in text_str:
            print('Stopped...')
            move.linear.x=0
            move.angular.z=0
            pub.publish(move)
        elif 'geri' in text_str:
            print("Moving back...")
            move.linear.x=-0.5
            move.angular.z=0
            pub.publish(move)
                

        
        

