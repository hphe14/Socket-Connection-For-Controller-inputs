import pygame
import socket
import time
import pickle
import sys
pygame.init()

def initialise():
    if pygame.joystick.get_count() == 0:
        print("Please connect a controller")
        return None
    else:
        print("Ready for connection")


def main():
    controller = initialise()
    conn, addr = s.accept()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                controller = pygame.joystick.Joystick(event.device_index)
                controller.init()
                print(f"Connected: {controller.get_name()}")
                time.sleep(2) 
                
            if event.type == pygame.JOYDEVICEREMOVED:
                print("Controller Disconnected")
                controller = None
                        
        if controller:
            #Only using these  inputs
            #Raw trigger values when unpressed start at -1 so may need to be adjusted as preference      
            L_stick_X = round(controller.get_axis(0),3)
            L_trigger = round(controller.get_axis(4),3)
            R_trigger = round(controller.get_axis(5),3)
            
            #Button_A = controller.get_button(0)
            #Button_B = controller.get_button(1)
            
            #Other Xbox controller inputs include:   (Can just use for loop instead tbh)           
            # L_stick_Y = controller.get_axis(1)
            # R_stick_X = controller.get_axis(2)
            # R_stick_Y = controller.get_axis(3)
            # Button_X = controller.get_button(2)
            # Button_Y = controller.get_button(3)
            # L_bumper = controller.get_button(4)
            # R_bumper = controller.get_button(5)
            # LSB  = controller.get_button(8)
            # RSB  = controller.get_button(9)
            #DPAD = controller.get_hat(0)
                   
            #Depending on stick alignment value may not default to 0 so a threshold is used.
            if abs(L_stick_X) <= 0.05:
                L_stick_X = 0
            
            controller_inputs = [
                L_stick_X,
                L_trigger,
                R_trigger,
            ]            
            #print("\033c", end="") 
            controller_inputs = [float(i) for i in controller_inputs]
            print(controller_inputs)
            send_inputs(conn,controller_inputs)

            
def send_inputs(sock,inputs):
        #pickle to send as a list of floats
        try:
            inputs = pickle.dumps(inputs)
            sock.sendall(inputs)
        except ConnectionResetError:
            print("Connection closed on client side")
            sock.close()         
        except OSError:
            print("Stopping")
            sys.exit(0)
            

if __name__ == "__main__":
    
    #Setting up socket connection using host computer ip
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 8080
    ADDRESS = (HOST,PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDRESS)
    s.listen()
    
    main()

    print("Connection Established")
    pygame.quit()


   