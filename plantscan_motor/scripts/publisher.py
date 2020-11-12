#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool

#publisher for sending information that motors moved
def talker():
    pub = rospy.Publisher('finish', Bool, queue_size=1)
    rospy.init_node('publisher_motor', anonymous = True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        move()
        pub.publish(True)
        rospy.sleep(2.)

#func that will keep track of whether or not camera did finish circle around plant
def talker2():
    pub2 = rospy.Publisher('done', Bool, queue_size=1)
    #here comes condition
        pub2.Publish(True)

#function that will move motors
def move():
    #after each movement talker2 is called

if __name__ = '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
