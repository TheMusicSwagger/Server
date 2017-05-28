import threading
from communicator.communicator import Communicator

class DataCenter(threading.Thread):
    def __init__(self):
        super(DataCenter, self).__init__()

if __name__=="__main__":
    try:
        comm=Communicator(True)
        while True:continue
    except KeyboardInterrupt as e:
        print("<Ctrl-c> = user quit")
    finally:
        print("Exiting...")