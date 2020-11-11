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

#function that will move motors
def move():


if __name__ = '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
