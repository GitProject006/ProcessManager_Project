def classify_process(cpu_percent, io_rate):
    if io_rate >= 10 * 1024:
        return "I/O-bound"
    elif cpu_percent >= 50:
        return "CPU-bound"
    else:
        return "Balanced / Other"