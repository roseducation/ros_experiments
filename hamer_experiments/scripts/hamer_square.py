#! /usr/bin/env python 
import rospy
import math
import sys
import time
import tf
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry

			
def callback(msg):
    t_move=time.time()+5
    t_turn=time.time()+13
    t_move2=time.time()+18
    t_turn2=time.time()+27
    t_move3=time.time()+32
    t_turn3=time.time()+40
    t_move4=time.time()+45

    while True:
        move.linear.x=0.0
        move.angular.z=0.0
        if time.time()<t_move:
            move.linear.x=0.4
        elif time.time()>t_move and time.time()<t_turn:
            move.linear.x=0.0
            move.angular.z=0.23
        elif time.time()>t_turn and time.time()<t_move2:
            move.angular.z=0.0
            move.linear.x=0.3
        elif time.time()>t_move2 and time.time()<t_turn2:
            move.linear.x=0.0
            move.angular.z=0.23
        elif time.time()>t_turn2 and time.time()<t_move3:
            move.linear.x=0.4
            move.angular.z=0.0
        elif time.time()>t_move3 and time.time()<t_turn3:
            move.linear.x=0.0
            move.angular.z=0.23
        elif time.time()>t_turn3 and time.time()<t_move4:
            move.angular.z=0.0
            move.linear.x=0.4
        
        
	pub.publish(move)
rospy.init_node('square')
sub=rospy.Subscriber('/hamer/odom',Odometry, callback)
pub=rospy.Publisher('/hamer/cmd_vel',Twist,queue_size=5)
p=Odometry()
move=Twist()
rospy.spin()
