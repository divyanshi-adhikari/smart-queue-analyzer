# Smart Queue Analyzer with GUI

import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt


# Functions

def timestamps(timestamp_list):
    """Convert list of HH:MM:SS strings to datetime objects and sort them."""
    times = []
    for t in timestamp_list:
        try:
            dt = datetime.datetime.strptime(t, "%H:%M:%S")
            times.append(dt)
        except ValueError:
            messagebox.showerror("Error", f"Invalid time format: {t}")
            return None
    times.sort()
    return times



def calculate_avg_service_time(times, max_interval=300, recent_orders=5):
    """Calculate realistic average service time in seconds."""
    differences = []
    for i in range(1, len(times)):
        diff = (times[i] - times[i-1]).total_seconds()
        if diff <= max_interval:
            differences.append(diff)
    if differences:
        recent = differences[-recent_orders:]
        return sum(recent)/len(recent)
    else:
        return None



def estimate_wait_time(queue_length, avg_service_time):
    """Estimate total wait time in seconds."""
    return queue_length * avg_service_time



def analyze_queue():
    """Main analysis function called by GUI."""
    timestamp_text = timestamp_input.get("1.0", tk.END).strip()
    if not timestamp_text:
        messagebox.showwarning("Warning", "Please enter timestamps first!")
        return
    timestamp_list = timestamp_text.splitlines()
    
    times = timestamps(timestamp_list)
    if times is None:
        return
    
    avg_service_time = calculate_avg_service_time(times)
    if avg_service_time is None:
        messagebox.showinfo("Info", "Not enough realistic data to calculate service time (huge gaps ignored).")
        return
    
    
    
    try:
        queue_length_val = int(queue_length_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Queue length must be an integer!")
        return
    
    
    
    wait_time = estimate_wait_time(queue_length_val, avg_service_time)
    minutes = int(wait_time // 60)
    seconds = int(wait_time % 60)
    
    
    
    # Load Level
    if queue_length_val <= 7:
        level = "LOW "
    elif queue_length_val < 15:
        level = "MEDIUM "
    else:
        level = "HIGH "
    
    
    
    # Customer Flow
    duration_seconds = (times[-1] - times[0]).total_seconds() if len(times) > 1 else avg_service_time
    orders_per_minute = len(times)/(duration_seconds/60) if duration_seconds>0 else 1
    if orders_per_minute >= 2:
        flow = " Very Fast Service"
    elif orders_per_minute >= 1:
        flow = " Normal Service Speed"
    else:
        flow = "Slow Service"
    
    
    
    # Display results
    result_text = f"Average service time: {avg_service_time:.2f} sec\n"
    result_text += f"Estimated wait time: {minutes} min {seconds} sec\n"
    result_text += f"Queue Load Level: {level}\n"
    result_text += f"Customer Flow Rating: {flow}"
    result_label.config(text=result_text)
    
    
    
    # Plot graphs
    service_times = [min((times[i]-times[i-1]).total_seconds(),300) for i in range(1,len(times))]
    plt.figure(figsize=(8,5))
    plt.plot(service_times, marker='o')
    plt.title("Service Time Trend (Seconds Between Orders, capped at 5 min)")
    plt.xlabel("Order Number")
    plt.ylabel("Service Time (seconds)")
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(6,4))
    plt.bar(["Estimated Wait"], [wait_time], color='orange')
    plt.title("Estimated Total Waiting Time")
    plt.ylabel("Seconds")
    plt.show()




# GUI Setup

root = tk.Tk()
root.title("Smart Queue Analyzer")

tk.Label(root, text="Enter timestamps of orders (HH:MM:SS), one per line:").pack()
timestamp_input = tk.Text(root, height=10, width=30)
timestamp_input.pack()

tk.Label(root, text="Enter current queue length:").pack()
queue_length_entry = tk.Entry(root)
queue_length_entry.pack()

analyze_btn = tk.Button(root, text="Analyze Queue", command=analyze_queue)
analyze_btn.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()
