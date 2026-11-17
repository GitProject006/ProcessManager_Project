
import tkinter as tk
from tkinter import ttk
import psutil

from monitor import ProcessMonitor
from database import initialize_database, save_processes

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ProcessManagerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Process Manager")
        self.root.geometry("1250x750")

        self.monitor = ProcessMonitor()
        self.all_processes = []

        initialize_database()

        self.create_widgets()
        self.update_processes()

    def create_widgets(self):

        # Main heading
        heading = tk.Label(
            self.root,
            text="PROCESS MANAGER",
            font=("Arial", 20, "bold")
        )
        heading.pack(pady=10)

        # Summary information
        summary_frame = tk.Frame(self.root)
        summary_frame.pack(fill="x", padx=10)

        self.cpu_label = tk.Label(
            summary_frame,
            text="System CPU: 0%",
            font=("Arial", 12, "bold")
        )
        self.cpu_label.pack(side="left", padx=20)

        self.memory_label = tk.Label(
            summary_frame,
            text="System Memory: 0%",
            font=("Arial", 12, "bold")
        )
        self.memory_label.pack(side="left", padx=20)

        self.process_label = tk.Label(
            summary_frame,
            text="Processes: 0",
            font=("Arial", 12, "bold")
        )
        self.process_label.pack(side="left", padx=20)

        # Search and filter
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=8)

        tk.Label(
            control_frame,
            text="Search:"
        ).pack(side="left")

        self.search_var = tk.StringVar()

        self.search_var.trace_add(
            "write",
            lambda *args: self.display_processes()
        )

        search_entry = tk.Entry(
            control_frame,
            textvariable=self.search_var,
            width=25
        )
        search_entry.pack(side="left", padx=5)

        tk.Label(
            control_frame,
            text="Process Type:"
        ).pack(side="left", padx=(15, 5))

        self.type_filter = tk.StringVar(value="All")

        filter_box = ttk.Combobox(
            control_frame,
            textvariable=self.type_filter,
            values=["All", "System", "User", "Unknown"],
            state="readonly",
            width=12
        )

        filter_box.pack(side="left")

        filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.display_processes()
        )

        # Process table
        table_frame = tk.Frame(self.root)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        columns = (
            "PID",
            "Name",
            "Type",
            "CPU %",
            "Memory MB",
            "Read KB/s",
            "Write KB/s",
            "Classification"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        widths = [70, 180, 90, 80, 100, 100, 100, 160]

        for column, width in zip(columns, widths):
            self.tree.heading(
                column,
                text=column,
                command=lambda c=column: self.sort_table(c)
            )

            self.tree.column(
                column,
                width=width,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Charts
        chart_frame = tk.Frame(self.root)
        chart_frame.pack(
            fill="x",
            padx=10,
            pady=2
        )

        self.figure = Figure(
            figsize=(10, 1.8),
            dpi=90
        )

        self.cpu_axis = self.figure.add_subplot(121)
        self.memory_axis = self.figure.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=chart_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # Bottom controls
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(
            fill="x",
            padx=10,
            pady=8
        )

        refresh_button = tk.Button(
            bottom_frame,
            text="Refresh Now",
            command=self.update_processes
        )

        refresh_button.pack(side="left")

        self.status_label = tk.Label(
            bottom_frame,
            text="Monitoring processes..."
        )

        self.status_label.pack(side="right")

    def update_processes(self):

        self.all_processes = self.monitor.get_processes()

        # Save monitoring history
        try:
            save_processes(self.all_processes)
        except Exception as error:
            print("Database error:", error)

        self.display_processes()
        self.update_summary()
        self.update_charts()

        self.status_label.config(
            text="Last updated: " +
            self.root.tk.call(
                "clock",
                "format",
                self.root.tk.call("clock", "seconds"),
                "-format",
                "%H:%M:%S"
            )
        )

        # Automatic refresh every 2 seconds
        self.root.after(
            2000,
            self.update_processes
        )

    def display_processes(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_var.get().strip().lower()
        selected_type = self.type_filter.get()

        for process in self.all_processes:

            # Apply process type filter
            if selected_type != "All":
                if process["type"] != selected_type:
                    continue

            # Search PID, name, type and classification
            if search_text:

                searchable_text = (
                    str(process["pid"]) + " " +
                    str(process["name"]) + " " +
                    str(process["type"]) + " " +
                    str(process["classification"])
                ).lower()

                if search_text not in searchable_text:
                    continue

            # Display matching process
            self.tree.insert(
                "",
                "end",
                values=(
                    process["pid"],
                    process["name"],
                    process["type"],
                    f'{process["cpu"]:.1f}',
                    f'{process["memory"]:.1f}',
                    f'{process["read_rate"] / 1024:.1f}',
                    f'{process["write_rate"] / 1024:.1f}',
                    process["classification"]
                )
            )

    def update_summary(self):

        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().percent

        self.cpu_label.config(
            text=f"System CPU: {cpu:.1f}%"
        )

        self.memory_label.config(
            text=f"System Memory: {memory:.1f}%"
        )

        self.process_label.config(
            text=f"Processes: {len(self.all_processes)}"
        )

    def update_charts(self):

        # Exclude Windows idle process from charts
        valid_processes = [
            process
            for process in self.all_processes
            if process["name"].lower()
            != "system idle process"
        ]

        # Select top 5 processes by CPU usage
        top_processes = valid_processes[:5]

        names = [
            process["name"][:12]
            for process in top_processes
        ]

        cpu_values = [
            process["cpu"]
            for process in top_processes
        ]

        memory_values = [
            process["memory"]
            for process in top_processes
        ]

        self.cpu_axis.clear()
        self.memory_axis.clear()

        # CPU chart
        self.cpu_axis.bar(
            names,
            cpu_values
        )

        self.cpu_axis.set_title(
            "Top Processes - CPU Usage"
        )

        self.cpu_axis.set_ylabel("CPU %")

        self.cpu_axis.tick_params(
            axis="x",
            labelrotation=25
        )

        # Memory chart
        self.memory_axis.bar(
            names,
            memory_values
        )

        self.memory_axis.set_title(
            "Top Processes - Memory Usage"
        )

        self.memory_axis.set_ylabel("Memory MB")

        self.memory_axis.tick_params(
            axis="x",
            labelrotation=25
        )

        self.figure.tight_layout()
        self.canvas.draw()

    def sort_table(self, column):

        items = [
            (
                self.tree.set(item, column),
                item
            )
            for item in self.tree.get_children("")
        ]

        try:
            items.sort(
                key=lambda x: float(x[0]),
                reverse=True
            )
        except ValueError:
            items.sort(
                key=lambda x: x[0].lower()
            )

        for index, (_, item) in enumerate(items):
            self.tree.move(
                item,
                "",
                index
            )


if __name__ == "__main__":

    root = tk.Tk()
    app = ProcessManagerApp(root)
    root.mainloop()
