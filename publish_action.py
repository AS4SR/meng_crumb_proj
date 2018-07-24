#!/usr/bin/env python
import rospy
from math import pi
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import MotorPower

def action_dispatcher(x):
    rospy.init_node('action_listener', anonymous=True)
    if x == 'move':    
        if i == 1:
            pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size = 10)
            i += 1 
            while not rospy.is_shutdown():
                sub = rospy.Subscriber("/gazebo/model_states", ModelStates, callback)

                cmd = Twist()
                cmd.linear.x = 0.4
                cmd.linear.y = 0.0
                cmd.linear.z = 0.0
                cmd.angular.x = 0.0
                cmd.angular.y = 0.0
                cmd.angular.z = psidot
                
                if (fabs(yw - yn)<0.2 and fabs(xw - xn)):
                    cmd.linear.x = 0.0
                    cmd.angular.z = 0.0
                    rospy.loginfo(" Waypoint reached ")
                    rospy.signal_shutdown(0)
                    
                ## publish to the topics
                pub1.publish(cmd)
     
    elif x == 'grip':
        pub = rospy.Publisher('/gripper_1_joint/command', Float64, queue_size = 10)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            cmd = Float64()            
            cmd = 0
            pub.publish(cmd)
            rate.sleep()
  
    elif x == 'unreach':
        pub = rospy.Publisher('/arm_2_joint/command', Float64, queue_size=10)
        pub1 = rospy.Publisher('/arm_4_joint/command', Float64, queue_size=10)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            cmd = Float64()
            cmd = 0
            pub.publish(cmd)
            cmd1 = Float64()
            cmd1 = 0
            pub1.publish(cmd1)
            rate.sleep()

    elif x == 'ungrip':
        pub = rospy.Publisher('/gripper_1_joint/command', Float64, queue_size = 10)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            cmd = Float64()
            cmd = 0.1
            pub.publish(cmd)
            rate.sleep()
                    
    else:
        pub = rospy.Publisher('/arm_2_joint/command', Float64, queue_size=10)
        pub1 = rospy.Publisher('/arm_4_joint/command', Float64, queue_size=10)
        rate = rospy.Rate(10)
        if x == 'reach':
            while not rospy.is_shutdown():
                cmd = Float64()
                cmd = pi/6
                pub.publish(cmd)
                cmd1 = Float64()
                cmd1 = pi/6
                print cmd1
                pub1.publish(cmd1)
                rate.sleep()
        
        elif x == 'unreach':
            while not rospy.is_shutdown():
                cmd = Float64()
                cmd = 0
                pub.publish(cmd)
                cmd1 = Float64()
                cmd1 = 0
                pub1.publish(cmd1)
                rate.sleep()

        elif x == 'reach-when-gripping':
            while not rospy.is_shutdown():
                cmd = Float64()
                cmd = pi/6
                pub.publish(cmd)
                cmd1 = Float64()
                cmd1 = pi/6
                pub1.publish(cmd1)
                rate.sleep()
    
    rospy.spin()

if __name__ == '__main__':
    
#    rospy.Subscriber("/action_strarr", String, f)
#    listener()
    
    action_dispatcher('unreach')
#action = wp.problem(True)
#action_py = ast.literal_eval(action)
#print(action_py)
#for i in action:
#    print(i)
#    if i = "move":
        
