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
		result = []
		if not os.path.exists(self.root_path+"/data/"+theme+"/"+task_name):
			os.mkdir(self.root_path+"/data/"+theme+"/"+task_name)
			meta_data = \
			{
				"name": task_name,
				"topic": theme,
				"difficulty": difficulty,
				"status": "unsolved",
				"add_date": str(dt.datetime.now()),
				"solved_date": None
			}

			data_path = self.root_path.replace("\\", "/") + "/data/" + theme + "/" + task_name
			file_path = os.path.join(data_path, "meta.json")

			if condition_path.split(".")[-1] == "pdf":
				shutil.copy(condition_path, data_path + '/condition.pdf')
				result.append("condition.pdf успешно создан")
			else:
				result.append("condition.pdf не был создан")

			if solution_path:
				if solution_path.split(".")[-1] == "py":
					shutil.copy(solution_path, data_path + '/solution.py')
					meta_data["status"] = "solved"
					meta_data["solved_date"] = str(dt.datetime.now())
					result.append("Решение было добавлено")
				else:
					result.append("Решение не было добавлено")
			else:
				result.append("Решение не задано")

			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(meta_data, f, ensure_ascii=False, indent=4)

		else:
			result.append("Такая задача уже существует")

		return result

	def update(self, theme, task_name, difficulty = None, condition_path = None, new_theme = None, new_task_name = None, solution_path = None):
		result = []


a = TaskManager()
print(a.save_task("arrays", "error", "hard", "C:/Users/densa/OneDrive/Desktop/lesson_34-36/test.pdf", r"C:\Users\densa\OneDrive\Desktop\lesson_34-36\asdt.py"))
