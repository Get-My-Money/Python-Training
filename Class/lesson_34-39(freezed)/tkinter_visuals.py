import tkinter as tk
import time

from main_code import TaskManager
manager = TaskManager()

window = tk.Tk()
window.title("Task Manager")
window.geometry("1000x400")

title = tk.Label(window, text="Task Manager", font=("Arial",20))
start_button = tk.Button(window, text="Запустить программу", font=("Arial",15,), bg="green")
exit_button = tk.Button(window, text ="Выйти из программы", font=("Arial",15), bg="red")
title.pack(pady=100)
start_button.pack()
exit_button.pack()


window.mainloop()