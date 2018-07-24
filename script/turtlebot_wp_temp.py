#!/usr/bin/env python
"""
Example of using PyDDL to solve an eight-puzzle. Each number is a tile that
can slide vertically or horizontally to fill in the blank space. This "hard"
instance (requiring the maximum of 31 steps) is taken from the following paper:

Reinefeld, Alexander. "Complete Solution of the Eight-Puzzle and the Benefit of
  Node Ordering in IDA*." International Joint Conference on Artificial
  Intelligence. 1993.

Initial State:
+---+---+---+
| 8   7   6 |
|     4   1 |
| 2   5   3 |
+---+---+---+

Goal State:
+---+---+---+
|     1   2 |
| 3   4   5 |
| 6   7   8 |
+---+---+---+

"""


from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner
from rocon_std_msgs.msg import StringArray
import rospy

class Listner_Action_states:
    def __init__(self):
        self.sub = rospy.Subscriber("/action_states", StringArray, self.callback)
        self.action_state = StringArray()

    def callback(self,data):
        self.action_state.strings = data.strings

def problem(verbose):
    domain = Domain((
        Action(
            'move',
            parameters=(
                ('position', 'wp_prec'),
                ('position', 'wp_effe'),
            ),
            preconditions=(
                ('connect', 'wp_prec', 'wp_effe'),
                ('base', 'wp_prec'),
                ('arm','unreach'),
            ),
            effects=(
                neg(('base', 'wp_prec')),
                ('base', 'wp_effe'),
            ),
        ),

        Action(
            'reach',
            parameters=(
                ('position', 'wp'),
                ('location','loc'),
            ),
            preconditions=(
                ('reachable','wp','loc'),
                ('base', 'wp'),
                ('arm','unreach'),
            ),
            effects=(
                neg(('arm','unreach')),
                ('arm','reach'),
            ),
        ),

        Action(
            'grip',
            parameters=(
                ('position', 'wp'),
                ('object', 'obj'),
                ('location','loc'),
            ),
            preconditions=(
                ('locate','obj','loc'),
                ('ungripped','obj'),
                ('reachable','wp','loc'),
                ('base', 'wp'),
                ('arm','reach'),
            ),
            effects=(
                neg(('ungripped','obj')),
                ('gripped','obj'),
            ),
        ),




        Action(
            'unreach',
            parameters=(
            ),
            preconditions=(
                ('arm','reach'),
            ),
            effects=(
                ('arm','unreach'),
                neg(('arm','reach')),
            ),
        ),


        Action(
            'reach-when-gripping',
            parameters=(
                ('position', 'wp'),
                ('location','loc'),
                ('object', 'obj'),
            ),
            preconditions=(
                ('reachable','wp','loc'),
                ('base', 'wp'),
                ('gripped','obj'),
                ('arm','unreach'),
           ),
            effects=(
                neg(('arm','unreach')),
                ('arm','reach'),
                ('locate','obj','loc'),
            ),
        ),

        Action(
            'ungrip',
            parameters=(
                ('object', 'obj'),
            ),
            preconditions=(
                ('gripped','obj'),
           ),
            effects=(
                neg(('gripped','obj')),
                ('ungripped','obj'),

            ),
        ),


    ))
    problem = Problem(
        domain,
        {
            'position': ('wp1', 'wp2', 'wp3'),
            'location':('loc1','loc2'),
            'object':('obj1','obj2'),
        },
        init=(
            ('connect', 'wp3', 'wp2'),
            ('connect', 'wp2', 'wp1'),
            ('connect', 'wp1', 'wp2'),
            ('reachable','wp1','loc1'),
            ('reachable','wp2','loc2'),
            ('base', 'wp3'),
            ('locate','obj1','loc1'),
            ('ungripped','obj1'),
            ('arm','unreach'),
            #('locate','obj2','loc2'),
            #('ungripped','obj2'),
        ),
        goal=(
            #('base','wp1'),
            #('gripped','obj1'),
            ('locate','obj1','loc2'),
            ('ungripped','obj1'),
        )
    )


    plan = planner(problem, verbose=verbose)
    #action_string = []
    if plan is None:
        print('No Plan!')
    else: 
        for action in plan:
            str_arr = StringArray()
            i=1
            for arg in action.sig:
                str_arr.strings.append(str(arg))
            print(str_arr)

            flag = 'unfinish'
            while(flag != 'finish'): #status_listener.string != 'finish'):
                pub.publish(str_arr)
                #print(str_arr,i) 
                i=i+1

                #print(listening.action_state.strings)
                if listening.action_state.strings:#empty check
                    flag = listening.action_state.strings[1]
                    while listening.action_state.strings[1] == 'finish':{} #may get previous 'finish', wait for a new unfinish
                if rospy.is_shutdown() :
                    return 0

                #r.sleep()
            print('finish',i)
                #print(status_listener.string)
    #for i in action_string:
    #    print(i)
    return 0
    #print(action_string)
    #return action_string

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    rospy.init_node('action_talker', anonymous=True)
    #r = rospy.Rate(20)
    pub = rospy.Publisher('/action_strarr', StringArray, queue_size=10)

    listening = Listner_Action_states()
    #rospy.Subscriber("status_listener", String, callback)
    
    #Status_Listener status_listener
    # Parse arguments
    opts, args = parser.parse_args()
    problem(opts.verbose)

    rospy.spin()
    #r.sleep()
    #rospy.signal_shutdown(str_arr)
