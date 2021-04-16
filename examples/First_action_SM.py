#!/usr/bin/env python
# StateMachine for the ASV and UAV for teh CRAWLABs ASV and UAV. 

import rospy
import smach
import smach_ros

from smach_ros import SimpleActionState
from smach import Concurrence

## Defining the state finding navigation channel
class find_NavChan_start(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['found', 'not_found'])
        self.counter = 0

    def execute(self, userdata): #This is where all the code for finding the navigation channel goes
            rospy.loginfo('Executing state find Navigation Channel')
            if self.counter < 3:
                    self.counter += 1
                    rospy.loginfo('Navigation Channel not found')
                    return 'not_found'
            else:
                    return 'found'


class cannot_find_NavChan(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes= ['back_to_find_NavChan'])

    def execute(self, userdata):
            rospy.loginfo('Cannot find Navigation Channel')
            return 'back_to_find_NavChan'

## Defining state pass through the navigation channel
class passthrough(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes= ['passing'])

    def execute(self, userdata): #All code for passing through goes here
            rospy.loginfo('Passing through')
            return 'passing'


def main():
    rospy.init_node('roboboatStateMach')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['finished'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('find_NavChan', find_NavChan_start(),transitions= {'not_found':'cannot_find_NavChan', 'found':'passthrough'})
        smach.StateMachine.add('cannot_find_NavChan', cannot_find_NavChan(), transitions={'back_to_find_NavChan':'find_NavChan'})
        smach.StateMachine.add('passthrough', passthrough(), {'passing':'finished'})

    sis = smach_ros.IntrospectionServer('statemach_viewer', sm, '/finding_navchan')
    sis.start()

    # Execute SMACH plan
    outcome = sm.execute()
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()