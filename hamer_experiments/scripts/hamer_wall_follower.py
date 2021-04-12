#! /usr/bin/env python 
import rospy
import math
import sys
import time
import tf
from geometry_msgs.msg import Twist, Point
from sensor_msgs.msg import LaserScan

	
def rotate(relative_angle_degree, angular_velocity):
	
	global move
	move.linear.x = 0
	move.angular.z = angular_velocity
	t0 = rospy.Time.now().to_sec()
	while True:
		pub.publish(move)
		rate.sleep()
		t1 = rospy.Time.now().to_sec()
		rospy.loginfo("t0: {t}".format(t=t0))
		rospy.loginfo("t1: {t}".format(t=t1))
		current_angle_degree = (t1 - t0) * angular_velocity
		rospy.loginfo("current angle: {a}".format(a=current_angle_degree))
		rospy.loginfo("angle to reach: {a}".format(a=relative_angle_degree))
		if abs(current_angle_degree) >= math.radians(abs(relative_angle_degree)):
			break
	move.angular.z = 0.0
	pub.publish(move)
			
def callback(msg):
	print('Distance to the wall on the right side')
	print msg.ranges[270]
	print ('Distance to the wall on the front right side')
	print msg.ranges[315]
	print('Distance to the wall infront')
	print msg.ranges[0]
	print('Distance to the wall  on the left side')
	print msg.ranges[90]
	print('Distance to the wall on the front left side')
	print msg.ranges[45]
	d=0.25

	if msg.ranges[90]<d or msg.ranges[45]<2*d: # if there is a wall on the left side
		move.linear.x=0.2
		print("Moving forward")
		move.angular.z=0
		if msg.ranges[0]<2*d: # if there is a wall on the left and infront
			move.linear.x=0.0
			print("Stopped")
			if msg.ranges[90] > msg.ranges[270]:#if the wall on the right side is the nearest
				print("Rotating")
				rotate(45,0.05)
			elif msg.ranges[90]<msg.ranges[270]: #if the wall on the left side is the nearest
				print("Rotating")
				rotate(45,-0.05)
	elif msg.ranges[90]>d or msg.ranges[315]<2*d: #if there is no wall on the left side
		print("Rotating")
		rotate(45,0.05)
		if msg.ranges[270]<2*d: #if there is a wall on the right side
			move.linear.x=0.2
			print("Moving forward")
	elif msg.ranges[90]<2*d and msg.ranges[90]<2*d: #if there are walls on both sides
		if msg.ranges[0]<3*d: #if there are walls on both sides and infront
			rotate(180,-0.1)
			print("Rotating")
		else:		
			move.linear.x=0.1
			print("Moving forward")
			move.angular.z=0
			
		
			
	
	pub.publish(move)
rospy.init_node('wall_follower')
sub=rospy.Subscriber('/scan',LaserScan, callback)
pub=rospy.Publisher('/hamer/cmd_vel',Twist)
move=Twist()
rospy.spin()
