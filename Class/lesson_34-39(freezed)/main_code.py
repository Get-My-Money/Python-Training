import tkinter as tk
import matplotlib
import datetime as dt
import json
import os
import shutil
import stat
import time
import tkinter as tk

class TaskManager():

    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(self.root_path + "/data"):
            os.mkdir(self.root_path + "/data")
        self.themes = ["arrays", "strings", "geometry", "stacks", "greedy", "database", "math",
                       "probability and statistics", "prefix sum", "segment tree"]
        for theme in self.themes:
            if not os.path.exists(self.root_path + "/data/" + theme):
                os.mkdir(self.root_path + "/data/" + theme)

    def save_task(self, theme, task_name, difficulty, condition_path, solution_path=None):
        result = []
        if not os.path.exists(self.root_path + "/data/" + theme + "/" + task_name):
            os.mkdir(self.root_path + "/data/" + theme + "/" + task_name)
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

    def update(self, theme, task_name, difficulty=None, condition_path=None, new_theme=None, new_task_name=None,
               solution_path=None):
        result = []

        old_path = self.root_path + "/data/" + theme + "/" + task_name

        if new_theme is None:
            final_theme = theme
        else:
            final_theme = new_theme

        if new_task_name is None:
            final_task_name = task_name
        else:
            final_task_name = new_task_name

        final_path = self.root_path + "/data/" + final_theme + "/" + final_task_name

        if final_path != old_path:
            if os.path.exists(final_path):
                result.append("Задача по такому пути уже существует. ")
            else:
                shutil.move(old_path, final_path)
                result.append("Путь задачи был изменен")


        meta_path =  old_path+"/meta.json"

        if not os.path.exists(meta_path):
            result.append("meta.json не найден")
            meta_data = \
                {
                    "name": None,
                    "topic": None,
                    "difficulty": None,
                    "status": None,
                    "add_date": None,
                    "solved_date": None
                }
        else:
            with open(meta_path, "r", encoding="utf-8") as file:
                meta_data = json.load(file)

        if difficulty:
            meta_data["difficulty"] = difficulty
            result.append("Сложность была изменена")

        if condition_path:
            if condition_path.split(".")[-1].lower() == "pdf":
                shutil.copy(condition_path, final_path + '/condition.pdf')
                result.append("Условие задачи обновленно/добавлено. ")
            else:
                result.append("Условие задачи не было обновленно. ")

        if solution_path:
            if solution_path.split(".")[-1].lower() == "py":
                shutil.copy(solution_path, final_path + '/solution.py')
                meta_data["status"] = 'solved'
                meta_data["solved_date"] = str(dt.datetime.now())
                result.append("Решение было добавлено/обновленно. ")
                result.append("Дата решения была добавлена/обновленна. ")
            else:
                result.append("Решение не было добавлено. ")

        meta_data["name"] = final_task_name
        meta_data["topic"] = final_theme
        if os.path.exists(meta_path):
            with open(meta_path, "w", encoding="utf-8") as file:
                json.dump(meta_data, file)
                result.append("Метаданные были обновленны. ")
            return result
        else:
            result.append("Метаданные не были обновленны. ")
            return result

    def delete_task(self, theme, task_name):
        result = []
        task_path = os.path.join(self.root_path, "data", theme, task_name)

        if not os.path.exists(task_path):
            result.append("Такой задачи не существует! ")
            return result

        def onexc(func, path, exc):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception as e:
                print(f"Не удалось удалить {path}: {e}")

        try:
            shutil.rmtree(task_path, onexc=onexc)
        except Exception as e:
            result.append(f"Ошибка при удалении: {e}")
            return result

        if os.path.exists(task_path):
            result.append("Задача не была полностью удалена. ")
        else:
            result.append("Задача была удалена полностью. ")

        return result


#a = TaskManager()
#print(a.save_task("arrays", "error", "hard", "C:Users/densa/OneDrive/Desktop/lesson_34-36/test.pdf", "C:/Users/densa/OneDrive/Desktop/lesson_34-36/asdt.py"))
#time.sleep(2)
#print(a.update("arrays", "error", "hard", "C:/Users/densa/OneDrive/Desktop/lesson_34-36/test.pdf","arrays","new_error", "C:/Users/densa/OneDrive/Desktop/lesson_34-36/asdt.py"))
#time.sleep(2)
#print(a.delete_task("arrays", "error"))
