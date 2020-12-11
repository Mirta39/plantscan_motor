#!/usr/bin/env python3

import sys
import rospy
import time
from dynamixel_workbench_msgs.srv import DynamixelCommand
from dynamixel_workbench_msgs.msg import DynamixelStateList


#ocitat polozaj, pretplaceni smo na topic joint_states, u callbacku spremamo taj position i usporedujemo ga s tim kakav treba biti
#unutar klase cu imat varijablu tipa neki goal koja cuva podatak di bi fkt motori trebali biti nakon pomaka
#ucallbacku cu ih usporedivati, pomocu recimo boola i onda je true ili fase, zatim jos run i 


class Move_motors():
    
    def pose_callback(self, data):
        if self.id == 1 :
            self.actual_position = data.dynamixel_state[0].present_position
        elif self.id == 2 :
            self.actual_position = data.dynamixel_state[1].present_position
        self.offset = abs(self.actual_position - self.goal_position)
        if self.offset < 10:
            print('pozicije su dobre   ' + str(self.offset)+ '   ' + str(self.id))
        else:
            print('pozicije ne odgovaraju   ' + str(self.offset) + '  ' +str(self.id))
    #moram usporediti trenutni polozaj samotora koji je ocitan/preuzet s topica joint_states sa očekivanim položajem motora
    #očekivani položaj motora je zasnovan na tome koje smo srgumente poslali, tj koji broj za pomak motora
    #usporedujem ih pomocu boola

    
    def __init__(self, command, id, addr_name, value):
        rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
        self.command = command
        self.id = id
        self.addr_name = addr_name
        self.value = value
        self.goal_position = 0
        self.offset = 0

        self.actual_position = DynamixelStateList()
        rospy.Subscriber('/dynamixel_workbench/dynamixel_state', DynamixelStateList, self.pose_callback)
        
        try:
            self.move_motor = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            motor = self.move_motor(command, id, addr_name, value)
        except rospy.ServiceException as e:
            print("There was a problem with initializing motors: %s" %e)


    def move(self, value):
        self.goal_position = value
        while self.offset > 10 :
            self.move_motor(self.command, self.id, self.addr_name, value)
        time.sleep(2)
        print(self.actual_position, self.goal_position)


if __name__ == '__main__':
    try:
        rospy.init_node('motor_position')
        m1 = Move_motors('command', 1, 'Goal_Position', 0)
        m2 = Move_motors('command', 2, 'Goal_Position', 0)
        pub = rospy.Publisher('/ready', Bool, queue_size = 1)
        time.sleep(2)
        for height in range (3):  #ova varijabla ce se mozda trebat mijenjat
            for angle in range (10):  #i ovo prilagoditi
                m1.move(600 * (angle + 1))
                pub.publish(True)
            m1.move(0) #mozda neg vrijednost
            #time.sleep(2)
            m2.move(300 * (height + 1))
            #time.sleep(2)
    except rospy.ROSInterruptException:
        pass

