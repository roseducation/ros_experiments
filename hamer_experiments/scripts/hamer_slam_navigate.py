#!/usr/bin/env python
# coding=utf-8
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
class State:
    def _init_(self, route=[], distance=int==0):
        self.route = route
        self.distance = distance
    def _eq_(self,other):
        for i in range(len(self.rout)):
            if(self.route[i]!=other.route[i]):
                return False
        return True
    def _lt_(self,other):
        return self.distance<other.distance
    
    def _repr_(self):
        return ('({0},{1})\n'.format(self.route,self.distance))
    def copy(self):
        return State(self.route, self.distance)
    def deepcopy(self):
        return State(copy.deepcopy(self.route), copy.deepcopy(self.distance))
    def update_distance(self,matrix,home):
        self.distance=0
        from_index=home
        for i in range(len(self.route)):
            self.distance += matrix[from_index][self.route[i]]
            from_index=self.route[i]
        self.distance+=matrix[from_index][home]

def movebase_istemci():
    istemci = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    istemci.wait_for_server()
    hedef = MoveBaseGoal()
    hedef.target_pose.header.frame_id = "map"
    point1=[1.5,2.5]
    point2=[1.5,1.5]
    point3=[0,0]
    list1=[point1,point2,point3]
    for i in range(len(list1)):
        hedef.target_pose.pose.position.x = list1[i][0]
        hedef.target_pose.pose.position.y = list1[i][1]
        bekle = istemci.wait_for_result()
        hedef.target_pose.pose.orientation.w = 1.0
        istemci.send_goal(hedef)
        i=i+1
    
   
    
    if not bekle:
        rospy.signal_shutdown("Action Servisi mevcut değil!")
    else:
        return istemci.get_result()   
   
if __name__ == '__main__':
    try:
        rospy.init_node('move_base_hedef_gonder')
        result = movebase_istemci()
        if result:
            rospy.loginfo("Hedef noktaya varıldı!")
        else:
            rospy.loginfo("Hedefe gidiliyor...")
    except rospy.ROSInterruptException:
        pass
