import tkinter as tk
import matplotlib
import datetime as dt
import json
import os
import shutil

class TaskManager():


	def __init__(self):
		self.root_path = os.path.dirname(os.path.abspath(__file__))
		if not os.path.exists(self.root_path+"/data"):
			os.mkdir(self.root_path+"/data")
		self.themes = ["arrays", "strings", "geometry", "stacks", "greedy","database","math","probability and statistics","prefix sum","segment tree"]
		for theme in self.themes:
			if not os.path.exists(self.root_path+"/data/"+theme):
				os.mkdir(self.root_path+"/data/"+theme)


	def save_task(self, theme, task_name, difficulty, condition_path, solution_path = None):
		if not os.path.exists(self.root_path+"/data/"+theme+"/"+task_name):
			os.mkdir(self.root_path+"/data/"+theme+"/"+task_name)
		else:
			print("Такая задача уже существует. ")
			#return None

			
		meta_data = {
		"name": task_name,
		"topic": theme,
		"difficulty": difficulty,
		"status": "unsolved",
		"add_date": str(dt.datetime.now()),
		"solved_date": None
		}

		data_path = self.root_path.replace("\\","/")+"/data/"+theme+"/"+task_name
		file_path = os.path.join(data_path, "meta.json")

		if condition_path.split(".")[-1] == "txt":
			shutil.copy(condition_path, data_path+'/condition.txt')
			print("Успех! ")
		else:
			print("Не подходящий формат! ")

		if solution_path != None:
			if solution_path.split(".")[-1] == "py":
				shutil.copy(solution_path, data_path+'/solution.py')
				meta_data["status"] = "solved"
				meta_data["solved_date"] = str(dt.datetime.now())
				print("Успех! ")
			else:
				print("Не подходящий формат! ")

		with open(file_path, 'w', encoding='utf-8') as f:
			json.dump(meta_data, f, ensure_ascii=False, indent=4)


	def update(self, theme, task_name, difficulty, condition_path = None, solution_path = None):
		pass


a = TaskManager()
a.save_task("arrays", "error", "hard", "B:/Python projects/Python-Training/Files/l_14/example.txt", "B:/Python projects/Python-Training/Other/testing_board.py")