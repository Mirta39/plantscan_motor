#!/usr/bin/env python3

import sys
import rospy
import time
from std_msgs.msg import Bool
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
        #if self.offset < 10:
            #print('pozicije su dobre   ' + str(self.offset)+ '   ' + str(self.id))
        #else:
            #print('pozicije ne odgovaraju   ' + str(self.offset) + '  ' +str(self.id))
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
        self.move_motor(self.command, self.id, self.addr_name, value)
        while self.offset > 10 :
            time.sleep(0.001)
        time.sleep(1)
        print(self.actual_position, self.goal_position)


    def calc_h(self, max_h, num_of_h):  #max_h u cm, num_of_h broj visina za slikanje
        return int(((max_h/7.54)*4096)/(num_of_h-1))

    def calc_a(self, num_of_photo):    #broj slika po rotaciji
        return int((6.5*4096)/num_of_photo)




if __name__ == '__main__':
    try:
        rospy.init_node('motor_position')
        m1 = Move_motors('command', 1, 'Goal_Position', 0)
        m2 = Move_motors('command', 2, 'Goal_Position', 0)
        pub = rospy.Publisher('/ready', Bool, queue_size = 1)
        num_of_h = 3        # broj visina na kojima ce se slikati
        num_of_photo = 5       # broj slika po jednoj rotaciji
        max_h = 60
        time.sleep(2)
        for height in range (num_of_h):  #ova varijabla ce se mozda trebat mijenjat
            m2.move(m2.calc_h(max_h, num_of_h) * (height))
            for angle in range (5):  #i ovo prilagoditi
                value = m1.calc_a(num_of_photo) * (angle)
                m1.move(value)
                pub.publish(True)
                time.sleep(1)
                print('nesto' + str(angle))
                
            m1.move(0) #mozda neg vrijednost
            time.sleep(2)
            #time.sleep(2)
    except rospy.ROSInterruptException:
        pass

