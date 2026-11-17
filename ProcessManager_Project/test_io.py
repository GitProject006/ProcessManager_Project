import os
import time

filename = "io_test_file.bin"
data = os.urandom(1024 * 1024)

with open(filename, "wb", buffering=0) as file:
    for i in range(200):
        file.write(data)
        time.sleep(0.1)

print("I/O test completed")
