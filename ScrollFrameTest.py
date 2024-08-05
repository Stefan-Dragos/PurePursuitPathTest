import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry("400x400")
frameContainer = ttk.Frame(master=window)

input = ttk.Entry(master=window, width=1)
input.place(x=40, y=300, anchor="nw")

canvas_container = tk.Canvas(master=frameContainer, height=100, width=150, bg="red")
frame2 = ttk.Frame(master=canvas_container)
scrollbar = ttk.Scrollbar(master=frameContainer, orient="vertical", command=canvas_container.yview)
canvas_container.create_window((0,0),window=frame2, anchor="nw")

for i in range(10):
    button = ttk.Button(master=frame2, text=f"Button{i}", width=20)
    color = tk.Canvas(master=frame2, bg="blue", width=65, height=20)
    button.pack()
    color.pack()


frame2.update()
canvas_container.configure(yscrollcommand=scrollbar.set, scrollregion=f"0 0 0 {frame2.winfo_height()}")

canvas_container.pack(side="left")
scrollbar.pack(side="right", fill = "y")

frameContainer.place(x=40, y=40, anchor="nw")

window.mainloop()