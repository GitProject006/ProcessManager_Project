## Process Manager – Process Monitoring and Classification System

## About the Project

Process Manager is a Python-based desktop application developed to monitor system and user processes. It provides information about CPU utilization, memory usage, and I/O activity and classifies processes into CPU-bound, I/O-bound, and Balanced/Other categories.

## Project Objectives

- Identify system and user processes.
- Monitor CPU utilization of running processes.
- Track memory consumption.
- Measure input/output activity.
- Classify processes based on CPU and I/O usage.
- Store process monitoring history in an SQLite database.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Tkinter | Graphical user interface |
| Psutil | Process monitoring |
| Matplotlib | Graphs and visualization |
| SQLite | Database storage |

## Main Features

1. **Process Monitoring:** Displays running processes with PID and process name.
2. **CPU Monitoring:** Shows CPU utilization.
3. **Memory Monitoring:** Displays memory usage.
4. **I/O Monitoring:** Tracks process input/output activity.
5. **Process Classification:** Identifies CPU-bound, I/O-bound, and Balanced/Other processes.
6. **Database Logging:** Saves process monitoring information in SQLite.
7. **Dashboard:** Presents process information and resource usage through a graphical interface.

## Process Classification

- **CPU-bound:** Processes that primarily depend on CPU processing.
- **I/O-bound:** Processes that primarily depend on input/output operations.
- **Balanced/Other:** Processes that do not meet the defined CPU-bound or I/O-bound conditions.

## Project Structure

```text
ProcessManager_Project/
├── main.py
├── monitor.py
├── classifier.py
├── database.py
├── requirements.txt
├── test_cpu.py
├── test_io.py
├── check_database.py
├── process_manager.db
└── screenshots/
```

## Installation and Execution

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Project Output Screenshots

Screenshots of the Process Manager dashboard, process classification tests, and database output are included in this repository.

## Database

SQLite is used to maintain process history, including timestamps, process IDs, process names, CPU utilization, memory usage, I/O rate, and classification.

## Conclusion

The Process Manager provides an effective way to monitor running processes, analyze resource utilization, classify processes, and maintain process history using a graphical interface and SQLite database.
<img width="953" height="556" alt="dashboard" src="https://github.com/user-attachments/assets/b6cd4256-a872-490a-b1a9-946bc616eaba" />

