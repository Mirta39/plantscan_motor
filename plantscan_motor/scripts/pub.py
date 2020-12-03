#!/usr/bin/env python3

import sys
import rospy
import time
from dynamixel_workbench_msgs.srv import DynamixelCommand
from dynamixel_workbench_msgs.msg import DynamixelState


#ocitat polozaj, pretplaceni smo na topic joint_states, u callbacku spremamo taj position i usporedujemo ga s tim kakav treba biti
#unutar klase cu imat varijablu tipa neki goal koja cuva podatak di bi fkt motori trebali biti nakon pomaka
#ucallbacku cu ih usporedivati, pomocu recimo boola i onda je true ili fase, zatim jos run i 


class Moving_motors():
    
    def pose_callback(self, data):
        self.position = data.present_position
        print('u callbacku smo')
        if self.position == a:
            print('pozicije su dobre')
        else:
            print('pozicije ne odgovaraju')
    #moram usporediti trenutni polozaj samotora koji je ocitan/preuzet s topica joint_states sa očekivanim položajem motora
    #očekivani položaj motora je zasnovan na tome koje smo srgumente poslali, tj koji broj za pomak motora
    #usporedujem ih pomocu boola
    
    def __init__(self, command, id, addr_name, value):
    #nisam kompletno ziher kaj bi tu trebalo ici
        rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
        #print("Tu sam")
        self.command = command
        self.id = id
        self.addr_name = addr_name
        self.value = value
        
        self.position = DynamixelState()
        rospy.Subscriber('/dynamixel_workbench/dynamixel_state', DynamixelState, self.pose_callback)
        
        try:
            self.move_motor = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            motor = self.move_motor(command, id, addr_name, value)
        except rospy.ServiceException as e:
            print("There was a problem with initializing motors: %s" %e)

    def run(self):
        a = 0
        while not rospy.is_shutdown() and a < 8000:
            a = a + 300
            self.move_motor(self.command, self.id, self.addr_name, a)
            print(self.position.present_position, a)
            time.sleep(1)
              
        self.move_motor(self.command, self.id, self.addr_name, 200)




if __name__ == '__main__':
    try:
        rospy.init_node('motor_position')
        m = Moving_motors('command', 2, 'Goal_Position', 0)
        m.run()
    except rospy.ROSInterruptException:
        pass
    #dynamixel_command_('command', 2, 'Goal_Position', 2000)
    #print("Uspijeli smo pokrenuti motore", dynamixel_command_('command', 2, 'Goal_position', 2048))
