#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
from math import pow,atan2,sqrt
from gazebo_msgs.srv import GetModelState
import tf

xd = 5
yd = 2
v = 0
kp = 0.5

def get_state_call(model_name):
    try:
        return get_model_state(model_name = model_name)
    except rospy.ServiceException as e:
        print e




def publisher():
    global v, xd, yd, kp, psi, psidot

    while (1):

        modelstate = get_state_call("crumb")
        cmd = Twist()

        xn = modelstate.pose.position.x
        yn = modelstate.pose.position.y

        quaternion = (modelstate.pose.orientation.x,modelstate.pose.orientation.y,modelstate.pose.orientation.z,modelstate.pose.orientation.w)
        eular = tf.transformations.euler_from_quaternion(quaternion)
        psi = eular[2]
        psid   = atan2(yd-yn, xd-xn) # psid is the desired heading to move to the waypoint
        psidot = 0 # turn rate
        v = 0
        if (sqrt(pow((xd - xn), 2) + pow((yd - yn), 2)) >= 0.05):
            v = 0.5
            psidot = kp*(psid - psi)
        cmd.linear.x = v
        cmd.angular.z = psidot
        print modelstate
        pub.publish(cmd)

        rate.sleep()

if __name__ == '__main__':

    rospy.init_node('wp_pub', anonymous=True)
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size = 10)
    rate = rospy.Rate(10)
    get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

    publisher()
    #talker()


