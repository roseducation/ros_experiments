#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import fabs

def patrol():

    rospy.init_node('patrol',anonymous=True)
    pub=rospy.Publisher('/hamer/cmd_vel',Twist,queue_size=10)
    move=Twist()
    vel=0.5
    dist=3
    cnt=0

    while cnt<10:
        t0=rospy.Time.now().to_sec()
        tr_dist=0.0
        if cnt %2==0:
            move.linear.x=vel
        else:
            move.linear.x=-vel
    	while tr_dist<dist:
        	pub.publish(move)
        	t1=rospy.Time.now().to_sec()
        	tr_dist=fabs(vel*t1-vel*t0)
	move.linear.x=0
	pub.publish(move)
	cnt+=1
    rospy.is_shutdown()
    
if __name__=='__main__':
    try:
        patrol()
    except rospy.ROSInterruptException:
        pass
