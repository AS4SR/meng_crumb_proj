#!/usr/bin/env python
import rospy
from rocon_std_msgs.msg import StringArray
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
import tf
from math import pi,sqrt,pow
from geometry_msgs.msg import Pose
import numpy as np
from kobuki_msgs.msg import MotorPower

class Listener_Action:
    def __init__(self):
        self.sub = rospy.Subscriber("/action_strarr", StringArray, self.callback)
        self.action = StringArray()

    def callback(self,data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.strings)

        self.action.strings = data.strings



class Listener_state:

    def __init__(self):
        self.sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback)
        self.pose = Pose()

    def callback(self,data):
        i = 0
        for name in data.name:
            if name == "crumb":
                break
            i=i+1
        self.pose = data.pose[i]



def wp_machine(waypoint):

    switcher = {
                'wp1':[2,3],
                'wp2':[1,1],
                'wp3':[0,0]
               }
    return switcher.get(waypoint,"invalid wp")


if __name__ == '__main__':

    rospy.init_node('listener', anonymous=True)
    #r = rospy.Rate(20)
    pub = rospy.Publisher('/action_states', StringArray, queue_size=10)
    pub_base = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size = 10)



    pub2 = rospy.Publisher('/mobile_base/commands/motor_power', MotorPower, queue_size = 10)
    turn_on_motors = MotorPower()
    turn_on_motors.state = 1 # or "ON"
    pub2.publish(turn_on_motors)


    listening = Listener_Action()
    listenToModelstate = Listener_state()

    i = 0

    kp = 0.5
    kd = 2
    while not rospy.is_shutdown() : # main program
        #print(listening.action,'while loop')


        if listening.action.strings: #empty check

            action_states = StringArray()
            action_states.strings.append(listening.action.strings[0]) 
            flag = 1

            if flag == 1:
                if listening.action.strings[0] == 'move':
                    if not rospy.is_shutdown():
                        quaternion = (listenToModelstate.pose.orientation.x,
                                      listenToModelstate.pose.orientation.y,
                                      listenToModelstate.pose.orientation.z,
                                      listenToModelstate.pose.orientation.w)
                        eular = tf.transformations.euler_from_quaternion(quaternion)
                        psi = eular[2] # in radians
                        wp = wp_machine(listening.action.strings[2])
                        xi = listenToModelstate.pose.position.x
                        yi = listenToModelstate.pose.position.y
                        psid   = np.arctan2(wp[1]-yi, wp[0]-xi)
                        psidmpsi = psid-psi
                        psidot = kp*(psidmpsi)
                        cmd = Twist()
                        cmd.linear.x = 0.4
                        cmd.angular.z = psidot
                        distance = sqrt(pow((wp[0] - xi), 2) + pow((wp[1] - yi), 2))
                        #v = distance * kp # - listenToModelstate.twist.linear.x * kd
                        if psidmpsi > pi/12:
                            cmd.linear.x = 0.0
                        #cmd.linear.x = v
                        pub_base.publish(cmd)
                        print flag, distance,psidmpsi,i
                        if distance < 0.2 :
                            psidot = 0
                            cmd.linear.x = 0.0                            
                            flag = 0
                            pub_base.publish(cmd)

                elif listening.action.strings[0] == 'grip':
                    if i > 1000 :
                        flag = 0

                elif listening.action.strings[0] == 'unreach':
                    if i > 1000 :
                        flag = 0


                elif listening.action.strings[0] == 'reach-when-gripping':
                    if i > 1000 :
                        flag = 0

                elif listening.action.strings[0] == 'ungrip':
                    if i > 1000 :
                        flag = 0


            if flag == 0:
                action_states.strings.append('finish')
                print(action_states.strings)
                
                print(i)
                i=0
            else:
                
                action_states.strings.append('unfinish')

            i = i+1
            pub.publish(action_states)


        #if rospy.is_shutdown():
            #return 0


        #r.sleep()

    rospy.spin()













