import psutil
import time
import os
from classifier import classify_process


class ProcessMonitor:
    def __init__(self):
        self.previous_io = {}
        self.previous_time = time.time()

        # Initialize CPU measurement for all processes
        for process in psutil.process_iter():
            try:
                process.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def get_process_type(self, process):
        try:
            username = process.username()

            # Windows system processes usually run under these accounts
            system_accounts = [
                "NT AUTHORITY\\SYSTEM",
                "NT AUTHORITY\\LOCAL SERVICE",
                "NT AUTHORITY\\NETWORK SERVICE",
                "SYSTEM",
                "LOCAL SERVICE",
                "NETWORK SERVICE"
            ]

            if username.upper() in [account.upper()
                                    for account in system_accounts]:
                return "System"
            else:
                return "User"

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return "Unknown"

    def get_processes(self):
        current_time = time.time()
        elapsed = max(current_time - self.previous_time, 0.1)

        processes = []

        for process in psutil.process_iter(
            ['pid', 'name', 'username', 'memory_info']
        ):
            try:
                pid = process.info['pid']
                name = process.info['name'] or "Unknown"

                cpu = process.cpu_percent(interval=None)

                memory_info = process.info['memory_info']
                memory_mb = (
                    memory_info.rss / (1024 * 1024)
                    if memory_info else 0
                )

                io_read_rate = 0
                io_write_rate = 0

                try:
                    io = process.io_counters()
                    current_read = io.read_bytes
                    current_write = io.write_bytes

                    if pid in self.previous_io:
                        old_read, old_write = self.previous_io[pid]

                        io_read_rate = max(
                            0, current_read - old_read
                        ) / elapsed

                        io_write_rate = max(
                            0, current_write - old_write
                        ) / elapsed

                    self.previous_io[pid] = (
                        current_read, current_write
                    )

                except (psutil.AccessDenied, AttributeError):
                    pass

                process_type = self.get_process_type(process)

                classification = classify_process(
                    cpu,
                    io_read_rate + io_write_rate
                )

                processes.append({
                    'pid': pid,
                    'name': name,
                    'type': process_type,
                    'cpu': cpu,
                    'memory': memory_mb,
                    'read_rate': io_read_rate,
                    'write_rate': io_write_rate,
                    'io_rate': io_read_rate + io_write_rate,
                    'classification': classification
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        self.previous_time = current_time

        # Sort by CPU usage, highest first
        processes.sort(
            key=lambda p: p['cpu'],
            reverse=True
        )

        return processes
