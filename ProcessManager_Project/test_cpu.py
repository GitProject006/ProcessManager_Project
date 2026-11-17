
import time
import os

print("CPU-bound test started")
print("Process ID:", os.getpid())
print("Keep this running while checking Process Manager.")
print("Press Ctrl+C to stop.")

try:
    while True:
        # Perform continuous calculations to use CPU
        result = 0
        for i in range(1000000):
            result += i * i

except KeyboardInterrupt:
    print("CPU-bound test stopped.")
