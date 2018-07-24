#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from math import pow,atan2,sqrt,fabs,pi
from gazebo_msgs.msg import ModelStates
import tf
import numpy as np
from kobuki_msgs.msg import MotorPower

#global xw, xi, yw, yi, psidot
xi = 0
yi = 0
psidot = 0
xw = 1
yw = 2
kp = 0.5


def callback(data):
    global xi, yi, psidot
    #global xw, yw, kp
    #xi = data.x
    #yi = data.y
    #psi = data.theta
    
    #data.name = [..., crumb, ...]
    i = 0
    for name in data.name:
        if name == "mobile_base": #why no crumb anymore
            break
        i=i+1
    piece = data.pose[i]
    xi = piece.position.x
    yi = piece.position.y
    quaternion = (piece.orientation.x,piece.orientation.y,piece.orientation.z,piece.orientation.w)
    eular = tf.transformations.euler_from_quaternion(quaternion)
    psi = eular[2] # in radians
    #psid   = atan2(yd-yn, xd-xn) # psid is the desired heading to move to the waypoint
    #psi = data.theta
    psid   = np.arctan2(yw-yi, xw-xi) # psid is the desired heading to move to the waypoint # radians
    #psidot = kp*(psid - psi) # turn rate
    
    psidmpsi = psid-psi
    #print("CALLBACK1: psidmpsi= %f" % (psidmpsi,))
    while (psidmpsi > pi) or (psidmpsi < -pi*2): # want range to be between -pi and pi
        if psidmpsi > pi:
            psidmpsi = psidmpsi - pi*2
        #if psidmpsi < pi:
        #    psidmpsi = psidmpsi
        if psidmpsi < -pi*2:
            psidmpsi = psidmpsi + pi*2
        #print("CALLBACK3: psidmpsi = %f" % (psidmpsi,))
    #print("CALLBACK2: psidmpsi = %f" % (psidmpsi,))
    psidot = kp*(psidmpsi) # turn rate

    #print("CALLBACK: xw = %f, xi = %f" % (xw,xi))
    #print("CALLBACK: yw = %f, yi = %f" % (yw,yi))
    #print("CALLBACK: psidot = %f" % (psidot,))
    #print("CALLBACK: theta= %f" % (psi,))

    
if __name__ == '__main__': # this is main function
   
    rospy.init_node('wp_control', anonymous=True) # initialize node here
    #r = rospy.Rate(20)
    r = rospy.Rate(50)
    
    ## setup the publisher
    pub2 = rospy.Publisher('/mobile_base/commands/motor_power', MotorPower, queue_size = 10)
    turn_on_motors = MotorPower()
    turn_on_motors.state = 1 # or "ON"
    pub2.publish(turn_on_motors)
    #pub1 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size = 10)#/mobile_base/commands/velocity # NOT THIS ONE, because you end up fighting the cmd_vel_mux'er that was set up to talk on this same channel/topic!!!
    pub1 = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size = 10)#/mobile_base/commands/velocity
   
    #global xw, xi, yw, yi, psidot
    
    ## setup the subscriber
    #sub = rospy.Subscriber("/gazebo/get_model_state", Pose, callback) #motion model
    #sub = rospy.Subscriber("/gazebo/set_model_state", Pose, callback)
    sub = rospy.Subscriber("/gazebo/model_states", ModelStates, callback)

    while not rospy.is_shutdown():
        cmd = Twist()
        cmd.linear.x = 0.25 #0.5
        cmd.linear.y = 0.0
        cmd.linear.z = 0.0
        cmd.angular.x = 0.0
        cmd.angular.y = 0.0
        # note, need to do "positive" of angle because z frame is same, not opposite?
        if fabs(psidot) > 1.0: # cutoff max turn rate
            #cmd.angular.z = -0.25*np.sign(psidot)
            cmd.angular.z = 1.0*np.sign(psidot)
        else:
            #cmd.angular.z = -psidot
            cmd.angular.z = psidot
        #cmd.angular.z = 1.0

        if (sqrt(pow((xw - xi), 2) + pow((yw - yi), 2)) <= 0.05):
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            pub1.publish(cmd)
            print("DONE!!!")
            rospy.loginfo(" Waypoint reached ")
           # rospy.signal_shutdown(0)
        
        print("linear.x = %f, angular.z = %f" % (cmd.linear.x,cmd.angular.z))
        print("xw = %f, xi = %f" % (xw,xi))
        print("yw = %f, yi = %f" % (yw,yi))
        print("psidot = %f" % (psidot,))

        ## publish to the topics
        pub1.publish(cmd)
        

        r.sleep()
    rospy.loginfo("Controller Node Has Shutdown.")
    rospy.signal_shutdown(0)
