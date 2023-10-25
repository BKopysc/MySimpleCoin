from seed_node import SeedNode
import signal
import sys
import time

# try to stop node by interrupting with CTRL+C
def signal_handler(sig, frame):
    print('Stopping node...')
    seed_n.stop()
    sys.exit(0)

# try to exit node by interrupting with CTRL+C
signal.signal(signal.SIGINT, signal_handler)

seed_n = SeedNode("127.0.0.1", 6000)
time.sleep(1)

seed_n.start()

while True:
    quit_com = input("Press 'q' to quit: ")
    if(quit_com == "q"):
        print("exiting....")
        break
    else:
        print("Wrong command!")
        continue

seed_n.stop()

