#!/usr/bin/env python
import rospy
from rocon_std_msgs.msg import StringArray



class Listner_Action:
    def __init__(self):
        self.sub = rospy.Subscriber("/action_strarr", StringArray, self.callback)
        self.action = StringArray()

    def callback(self,data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.strings)
        self.action.strings = data.strings


def state_machine(action):

    switcher = {
                'move':'waypoint controller',
                'reach-when-gripping':'waypoint controller',
                'reach':'joint states publisher',
                'unreach':'joint states publisher #2',
                'grip':'end effecter states publisher',
                'ungrip':'end effecter states publisher #2',
               }
    print switcher.get(action,"invalid action type")


if __name__ == '__main__':

    rospy.init_node('listener', anonymous=True)
    #r = rospy.Rate(20)
    pub = rospy.Publisher('/action_states', StringArray, queue_size=10)

    listening = Listner_Action()

    i = 0

    while not rospy.is_shutdown() : # main program
        #print(listening.action,'while loop')


        if listening.action.strings: #empty check

            action_states = StringArray()
            action_states.strings.append(listening.action.strings[0]) 

            if(i<1000):
                action_states.strings.append('unfinish')
                
            else:
                action_states.strings.append('finish')
                print(action_states.strings)
                state_machine(listening.action.strings[0])
                print(i)
                i=0

            i = i+1
            pub.publish(action_states)


        #if rospy.is_shutdown():
            #return 0


        #r.sleep()

    rospy.spin()













