import numpy as np
import os 
from pprint import pprint
import psutil
import matplotlib.pyplot as plt
from collections import Counter
import tkinter as tk
from tkinter import ttk
import threading
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dict_to_csv(dict, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dict.keys())
        writer.writerow(dict.values())

def get_file_type(file_location):
    _, file_extension = os.path.splitext(file_location)
    return file_extension

def iterate_files_in_all_roots():
    file_types = {}
    for partition in psutil.disk_partitions():
        for root, dirs, files in os.walk(partition.mountpoint):
            for file in files:
                type = get_file_type(os.path.join(root, file))
                if type in file_types:
                    file_types[type] += 1
                else:
                    file_types[type] = 1
    return file_types

def start_counting():
    button.config(state='disabled')

    threading.Thread(target=count_files).start()

def count_files():
    file_types_dict = iterate_files_in_all_roots()

    most_common_types = Counter(file_types_dict).most_common(10)

    file_types, counts = zip(*most_common_types)

    fig = plt.Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(file_types, counts)
    ax.set_xlabel('File Type')
    ax.set_ylabel('Count')
    ax.set_title('10 Most Common File Types')
    ax.set_xticks(file_types)
    ax.set_xticklabels(file_types, rotation=90)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    button.config(state='normal')

def download_csv():
    file_types_dict = iterate_files_in_all_roots()
    dict_to_csv(file_types_dict, 'file_types.csv')

root = tk.Tk(baseName='File Type Counter', screenName='File Type Counter')
root.geometry('800x800')

explanation = tk.Text(root, height=10, width=50 , font=("Helvetica", 12))
explanation.insert(tk.END, "This app counts the file types in all root directories\n and displays the 10 most common types in a bar plot.\n You can also download the counts as a CSV file.\nDon't press the button multiple times, it will freeze the app.\nAlso first press the 'Start counting' button.\nand download the csv after the plot is displayed.")
explanation.pack()

button = ttk.Button(root, text="Start counting", command=start_counting)
button.pack()

download_button = ttk.Button(root, text="Download CSV", command=download_csv)
download_button.pack()

root.mainloop()