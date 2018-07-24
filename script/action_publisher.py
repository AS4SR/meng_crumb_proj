#!/usr/bin/env python
import rospy
from rocon_std_msgs.msg import StringArray
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
import tf
from math import pi,sqrt,pow,fabs
from geometry_msgs.msg import Pose
import numpy as np
from kobuki_msgs.msg import MotorPower
from std_msgs.msg import Float64
from control_msgs.msg import JointControllerState

class Listener_Joint_grip:
    def __init__(self):
        self.sub = rospy.Subscriber("/gripper_1_joint/state", JointControllerState, self.callback)
        self.joint = JointControllerState()
    def callback(self,data):

        self.joint= data


class Listener_Joint_2:
    def __init__(self):
        self.sub = rospy.Subscriber("/arm_2_joint/state", JointControllerState, self.callback)
        self.joint = JointControllerState()
    def callback(self,data):

        self.joint= data

class Listener_Joint_4:
    def __init__(self):
        self.sub = rospy.Subscriber("/arm_4_joint/state", JointControllerState, self.callback)
        self.joint = JointControllerState()
    def callback(self,data):

        self.joint= data

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
                'wp1':[1,0],
                'wp2':[1,1],
                'wp3':[0,0]
               }
    return switcher.get(waypoint,[0,0])


class Listener_object:

    def __init__(self):
        self.sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback)
        self.pose = Pose()

    def callback(self,data):
        i = 0
        for name in data.name:
            if name == "object":
                break
            i=i+1
        self.pose = data.pose[i]



def orientation(listen_object,listenToModelstate):
    obj_x = listen_object.pose.position.x
    obj_y = listen_object.pose.position.y
    sel_x = listenToModelstate.pose.position.x
    sel_y = listenToModelstate.pose.position.y
    psidmpsi = 1
    kp_g = 0.75
    while psidmpsi > 0.001 and fabs(listen_object.pose.orientation.w - listenToModelstate.pose.orientation.w) > 0.005:
        psid   = np.arctan2(obj_y-sel_y, obj_x-sel_x)
        eular = tf.transformations.euler_from_quaternion(quaternion)
        psi = eular[2] # in radians
        psidmpsi = psid-psi
        psidot = kp_g * (psidmpsi)
        cmd = Twist()
        cmd.angular.z = psidot
        pub_base.publish(cmd)

if __name__ == '__main__':

    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(100)
    pub = rospy.Publisher('/action_states', StringArray, queue_size=10)
    pub_base = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size = 10)

    pub_grip = rospy.Publisher('/gripper_1_joint/command', Float64, queue_size=10)
    cmd_grip = Float64()
    cmd_grip = 0.0185


    pub_j = rospy.Publisher('/arm_2_joint/command', Float64, queue_size=10)
    pub_j1 = rospy.Publisher('/arm_4_joint/command', Float64, queue_size=10)
    i = 0

    while i < 20:

        pub_grip.publish(cmd_grip)
        pub_j.publish(0)
        pub_j1.publish(0)
        i = i +1
        rate.sleep()

    pub2 = rospy.Publisher('/mobile_base/commands/motor_power', MotorPower, queue_size = 10)
    turn_on_motors = MotorPower()
    turn_on_motors.state = 1 # or "ON"
    pub2.publish(turn_on_motors)


    listening = Listener_Action()
    listenToModelstate = Listener_state()
    listen_object = Listener_object()
    joint_2 = Listener_Joint_2()
    joint_4 = Listener_Joint_4()
    joint_grip = Listener_Joint_grip()


    sleep = 20
    i = 0
    kp = 5
    kd = 2
    while not rospy.is_shutdown() : # main program
        #print(listening.action,'while loop')


        if listening.action.strings: #empty check

            action_states = StringArray()
            action_states.strings.append(listening.action.strings[0])
            a = 1
            if (a == 1):
                #action_states.strings.append('unfinish')
                #print(a," before if")
                if listening.action.strings[1] == 'move' :
                    if not rospy.is_shutdown() :
                        quaternion = (listenToModelstate.pose.orientation.x,
                                      listenToModelstate.pose.orientation.y,
                                      listenToModelstate.pose.orientation.z,
                                      listenToModelstate.pose.orientation.w)
                        eular = tf.transformations.euler_from_quaternion(quaternion)
                        psi = eular[2] # in radians
                        wp = wp_machine(listening.action.strings[3])
                        xi = listenToModelstate.pose.position.x
                        yi = listenToModelstate.pose.position.y
                        psid   = np.arctan2(wp[1]-yi, wp[0]-xi)
                        psidmpsi = psid-psi
                        psidot = kp*(psidmpsi)
                        cmd = Twist()
                        cmd.linear.x = 0.6
                        cmd.angular.z = psidot
                        distance = sqrt(pow((wp[0] - xi), 2) + pow((wp[1] - yi), 2))

                        #print psidmpsi
                        #v = distance * kp # - listenToModelstate.twist.linear.x * kd
                        if fabs(psidmpsi) > pi/12:
                            cmd.linear.x = 0.0
                        #cmd.linear.x = v
                        pub_base.publish(cmd)
                        if distance < 0.05 :
                            cmd.angular.z = 0.0
                            cmd.linear.x = 0.0
                            pub_base.publish(cmd)
                            print(a,"in distance conditional")
                            action_states.strings.append('finish')  
                            pub.publish(action_states)   
                            while i < 5:
                                #pub.publish(action_states)    
                                print(action_states.strings)
                                i+=1
                            #rospy.spin()
                        else:
                            action_states.strings.append('unfinish')
                            pub.publish(action_states)  

                else:

                    rate = rospy.Rate(10)
                    if listening.action.strings[1] == 'reach' or listening.action.strings[1] == 'reach-when-gripping':
                        if not rospy.is_shutdown():
                            if listening.action.strings[1] == 'reach' :
                                orientation(listen_object,listenToModelstate)
                            cmd_j = Float64()
                            cmd_j = pi/6
                            cmd_j1 = Float64()
                            cmd_j1 = pi/6
                            while joint_2.joint.set_point != cmd_j or joint_4.joint.set_point != cmd_j1:
                                pub_j.publish(cmd_j)
                                pub_j1.publish(cmd_j1)
                                print 'reaching!', cmd_j, joint_2.joint.set_point
                            i = 0
                            while i < sleep:   # extend publish time
                                i = i+1
                                rate.sleep()
                            action_states.strings.append('finish')        
                            print(action_states.strings)
                            pub.publish(action_states)

                    elif listening.action.strings[1] == 'grip':
                        cmd_grip = Float64()
                        cmd_grip = 0
                        while joint_grip.joint.set_point != cmd_grip :
                            pub_grip.publish(cmd_grip)
                            print 'gripping!',cmd_grip,joint_grip.joint.set_point
                        i = 0
                        while i < sleep:
                            i = i+1
                            rate.sleep()
                        action_states.strings.append('finish')      
                        pub.publish(action_states)

                    elif listening.action.strings[1] == 'unreach':
                        if not rospy.is_shutdown():
                            cmd_j = Float64()
                            cmd_j = 0
                            cmd_j1 = Float64()
                            cmd_j1 = 0
                            while joint_2.joint.set_point != cmd_j or joint_4.joint.set_point != cmd_j1:
                                pub_j.publish(cmd_j)
                                pub_j1.publish(cmd_j1)
                                print 'unreach',cmd_j,joint_2.joint.set_point
                            i = 0
                            while i < sleep:
                                i = i+1
                                rate.sleep()
                            action_states.strings.append('finish')        
                            print(action_states.strings)
                            pub.publish(action_states)
                            #rospy.spin()
                    elif listening.action.strings[1] == 'ungrip':
                        cmd_grip = Float64()
                        cmd_grip = 0.0185
                        while joint_grip.joint.set_point != cmd_grip :
                            pub_grip.publish(cmd_grip)
                            print 'ungrip',cmd_grip,joint_grip.joint.set_point
                        i = 0
                        while i < sleep:
                            i = i+1
                            rate.sleep()
                        action_states.strings.append('finish')
                        pub.publish(action_states)

                    else :
                        action_states.strings.append('unfinish')   
                        pub.publish(action_states)

           # print(action_states.strings[-1])
           # else:
           #     action_states.strings.append('finish')        
           #     print(action_states.strings)
           #     pub.publish(action_states)
    
    rospy.spin()













