import tkinter as tk
import matplotlib
import datetime as dt
import json
import os


class TaskManager():


	def __init__(self):
		self.root_path = os.path.dirname(os.path.abspath(__file__))
		if not os.path.exists(self.root_path+"/data"):
			os.mkdir(self.root_path+"/data")
		self.themes = ["arrays", "strings", "geometry", "stacks", "greedy","database","math","probability and statistics","prefix sum","segment tree"]
		for theme in self.themes:
			if not os.path.exists(self.root_path+"/data/"+theme):
				os.mkdir(self.root_path+"/data/"+theme)


	def save_task(self, theme, task_name, difficulty):
		if not os.path.exists(self.root_path+"/data/"+theme+"/"+task_name):
			os.mkdir(self.root_path+"/data/"+theme+"/"+task_name)
		else:
			print("Такая задача уже существует. ")



a = TaskManager()
a.save_task("arrays", "error", "hard")