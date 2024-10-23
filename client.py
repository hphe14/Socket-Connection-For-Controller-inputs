import socket
import pickle
import sys

def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 8080
    ADDRESS = (HOST,PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDRESS)

    while True:
        try:
            message = s.recv(1024)
        except socket.error:
            print("Connection closed on server side")
            sys.exit(1)  
            
            
        try:
            inputs = pickle.loads(message)
        except pickle.UnpicklingError:
            print(f"Cannot Unpickle {inputs}")
            # raise

        print(f"Recieved:{inputs}")
            
if __name__ == "__main__":
    main()