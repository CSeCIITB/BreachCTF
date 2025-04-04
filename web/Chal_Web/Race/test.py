import threading
import time

def print_hello():
    while True:
        print("Hello")
        time.sleep(1)  # Sleep for 1 second

# Start the function in a separate thread
hello_thread = threading.Thread(target=print_hello, daemon=True)
hello_thread.start()

# Main thread continues working
for i in range(5):
    print(f"Main thread working {i}")
    time.sleep(2)  # Simulating some main thread work

print("Main thread finished")
