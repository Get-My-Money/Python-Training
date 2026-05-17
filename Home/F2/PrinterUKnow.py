import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import json
import shutil
import hashlib
import keyboard
import threading
import time
import sys

class MacroManager:
    def __init__(self, parent, app):
        self.window = tk.Toplevel(parent)
        self.window.title("Управление макросами")
        self.window.geometry("700x600")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)
        
        self.app = app
        self.config_file = os.path.join(os.path.dirname(sys.argv[0]), "macros_config.json")
        self.current_macro = None
        self.active_macros = set()
        self.macro_states = {}
        self.hotkeys_registered = {}
        self.is_macro_executing = False
        self.last_execution_time = {}
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()
        self.load_macros()
        self.start_macro_listener()
    
    def on_close(self):
        for macro_name in list(self.hotkeys_registered.keys()):
            try:
                keyboard.remove_hotkey(self.hotkeys_registered[macro_name])
            except:
                pass
        self.hotkeys_registered.clear()
        self.window.destroy()
        if self.app.macro_manager_window == self.window:
            self.app.macro_manager_window = None
    
    def setup_ui(self):
        current_bg = self.app.get_current_background_image()
        
        canvas = tk.Canvas(self.window, width=700, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        if current_bg:
            canvas.create_image(0, 0, image=current_bg, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
        
        main_frame = tk.Frame(canvas, bg="#2c2c2c")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=680, height=580)
        
        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        title = tk.Label(main_frame, text="Управление макросами", 
                        font=("Arial", 14, "bold"), bg="#2c2c2c", fg="#9b59b6")
        title.pack(pady=10)
        
        left_frame = tk.Frame(main_frame, bg="#2c2c2c")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(main_frame, bg="#2c2c2c")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(left_frame, text="Сохранённые макросы:", 
                font=("Arial", 11), bg="#2c2c2c", fg="white").pack(anchor="w", pady=(0,5))
        
        self.macros_listbox = tk.Listbox(left_frame, bg="#1e1e1e", fg="white", 
                                         font=("Arial", 10), height=12)
        self.macros_listbox.pack(fill="both", expand=True)
        self.macros_listbox.bind("<Double-Button-1>", self.load_selected_macro)
        
        tk.Label(left_frame, text="Активные макросы:", 
                font=("Arial", 11), bg="#2c2c2c", fg="white").pack(anchor="w", pady=(10,5))
        
        self.active_listbox = tk.Listbox(left_frame, bg="#1e1e1e", fg="#4CAF50", 
                                         font=("Arial", 10), height=5)
        self.active_listbox.pack(fill="both", expand=True)
        
        btn_frame_left = tk.Frame(left_frame, bg="#2c2c2c")
        btn_frame_left.pack(fill="x", pady=5)
        
        activate_btn = tk.Button(btn_frame_left, text="Активировать", 
                                command=self.activate_macro,
                                bg="#4CAF50", fg="white", cursor="hand2", width=10)
        activate_btn.pack(side="left", padx=2)
        
        deactivate_btn = tk.Button(btn_frame_left, text="Деактивировать", 
                                  command=self.deactivate_macro,
                                  bg="#f44336", fg="white", cursor="hand2", width=12)
        deactivate_btn.pack(side="left", padx=2)
        
        tk.Label(right_frame, text="Создание нового макроса:", 
                font=("Arial", 11), bg="#2c2c2c", fg="white").pack(anchor="w", pady=(0,5))
        
        tk.Label(right_frame, text="Текст для печати:", 
                bg="#2c2c2c", fg="white").pack(anchor="w", pady=(5,0))
        self.combo_entry = tk.Entry(right_frame, bg="#3c3c3c", fg="#9b59b6", 
                                    font=("Arial", 10), insertbackground="white")
        self.combo_entry.pack(fill="x", pady=(0,5))
        
        tk.Label(right_frame, text="Задержка между буквами (мс):", 
                bg="#2c2c2c", fg="white").pack(anchor="w", pady=(5,0))
        self.delay_entry = tk.Entry(right_frame, bg="#3c3c3c", fg="#9b59b6", 
                                   font=("Arial", 10), insertbackground="white")
        self.delay_entry.pack(fill="x", pady=(0,5))
        
        tk.Label(right_frame, text="Клавиша для бинда (1 буква):", 
                bg="#2c2c2c", fg="white").pack(anchor="w", pady=(5,0))
        self.bind_entry = tk.Entry(right_frame, bg="#3c3c3c", fg="#9b59b6", 
                                  font=("Arial", 10), insertbackground="white", width=5)
        self.bind_entry.pack(fill="x", pady=(0,5))
        
        tk.Label(right_frame, text="Название макроса:", 
                bg="#2c2c2c", fg="white").pack(anchor="w", pady=(5,0))
        self.name_entry = tk.Entry(right_frame, bg="#3c3c3c", fg="#9b59b6", 
                                  font=("Arial", 10), insertbackground="white")
        self.name_entry.pack(fill="x", pady=(0,10))
        
        btn_frame = tk.Frame(right_frame, bg="#2c2c2c")
        btn_frame.pack(fill="x", pady=10)
        
        save_btn = tk.Button(btn_frame, text="Сохранить макрос", 
                            command=self.save_macro,
                            bg="#4CAF50", fg="white", cursor="hand2", width=12)
        save_btn.pack(side="left", padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Удалить макрос", 
                              command=self.delete_macro,
                              bg="#f44336", fg="white", cursor="hand2", width=12)
        delete_btn.pack(side="left", padx=5)
        
        close_btn = tk.Button(right_frame, text="Закрыть", 
                             command=self.on_close,
                             bg="#2196F3", fg="white", cursor="hand2")
        close_btn.pack(pady=10)
        
        self.update_edit_state()
    
    def update_edit_state(self):
        is_active = self.current_macro in self.active_macros if self.current_macro else False
        
        state = "disabled" if is_active else "normal"
        
        self.combo_entry.config(state=state)
        self.delay_entry.config(state=state)
        self.bind_entry.config(state=state)
        self.name_entry.config(state=state)
    
    def show_message_in_window(self, message):
        msg_label = tk.Label(self.window, text=message, font=("Arial", 10, "bold"),
                              bg="#ff9800", fg="white")
        msg_label.place(relx=0.5, rely=0.9, anchor="center")
        self.window.after(3000, msg_label.destroy)
    
    def load_macros(self):
        self.macros_listbox.delete(0, tk.END)
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    macros = json.load(f)
                    for macro_name in macros.keys():
                        self.macros_listbox.insert(tk.END, macro_name)
            except:
                pass
    
    def update_active_listbox(self):
        self.active_listbox.delete(0, tk.END)
        for macro_name in self.active_macros:
            self.active_listbox.insert(tk.END, macro_name)
    
    def activate_macro(self):
        selection = self.macros_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите макрос для активации!")
            return
        
        macro_name = self.macros_listbox.get(selection[0])
        
        with open(self.config_file, "r", encoding="utf-8") as f:
            macros = json.load(f)
            if macro_name in macros:
                self.active_macros.add(macro_name)
                self.update_active_listbox()
                self.register_hotkeys()
                messagebox.showinfo("Успех", f"Макрос '{macro_name}' активирован!")
                self.update_edit_state()
    
    def deactivate_macro(self):
        selection = self.active_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите макрос для деактивации!")
            return
        
        macro_name = self.active_listbox.get(selection[0])
        
        if macro_name in self.active_macros:
            self.active_macros.discard(macro_name)
        
        if macro_name in self.hotkeys_registered:
            try:
                keyboard.remove_hotkey(self.hotkeys_registered[macro_name])
                del self.hotkeys_registered[macro_name]
            except:
                pass
        
        if macro_name in self.last_execution_time:
            del self.last_execution_time[macro_name]
        
        self.update_active_listbox()
        messagebox.showinfo("Успех", f"Макрос '{macro_name}' деактивирован!")
        
        if self.current_macro == macro_name:
            self.update_edit_state()
    
    def register_hotkeys(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                all_macros = json.load(f)
            
            for macro_name in self.active_macros:
                if macro_name in all_macros and macro_name not in self.hotkeys_registered:
                    macro_data = all_macros[macro_name]
                    bind_key = macro_data["bind_key"]
                    try:
                        def make_callback(m_name, m_data):
                            return lambda: self.execute_macro_with_block(m_name, m_data)
                        
                        keyboard.add_hotkey(bind_key, make_callback(macro_name, macro_data), suppress=True)
                        self.hotkeys_registered[macro_name] = bind_key
                    except Exception as e:
                        print(f"Ошибка регистрации {bind_key}: {e}")
    
    def execute_macro_with_block(self, macro_name, macro_data):
        current_time = time.time()
        
        if macro_name in self.last_execution_time:
            if current_time - self.last_execution_time[macro_name] < 0.5:
                return
        
        if self.is_macro_executing:
            return
        
        self.is_macro_executing = True
        self.last_execution_time[macro_name] = current_time
        
        try:
            text = macro_data["combo"]
            delay = macro_data["delay"] / 1000.0
            
            self.app.show_temp_message(f"▶ Макрос '{macro_name}' запущен!")
            
            for char in text:
                if self.is_macro_executing:
                    time.sleep(delay)
                    keyboard.write(char)
            
            self.app.show_temp_message(f"✓ Макрос '{macro_name}' завершён!")
            
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            self.is_macro_executing = False
    
    def save_macro(self):
        if self.current_macro and self.current_macro in self.active_macros:
            messagebox.showwarning("Ошибка", "Нельзя редактировать активный макрос! Сначала деактивируйте его.")
            return
        
        name = self.name_entry.get().strip()
        combo = self.combo_entry.get().strip()
        delay = self.delay_entry.get().strip()
        bind_key = self.bind_entry.get().strip()
        
        if not all([name, combo, delay, bind_key]):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        
        if len(bind_key) > 1:
            messagebox.showwarning("Ошибка", "Клавиша для бинда должна быть длиной 1 символ!")
            return
        
        try:
            delay_int = int(delay)
            if delay_int < 0:
                raise ValueError
        except:
            messagebox.showwarning("Ошибка", "Задержка должна быть положительным числом!")
            return
        
        old_name = self.current_macro
        
        macros = {}
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                macros = json.load(f)
        
        if old_name and old_name in macros and old_name != name:
            del macros[old_name]
        
        macros[name] = {
            "combo": combo,
            "delay": delay_int,
            "bind_key": bind_key
        }
        
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(macros, f, ensure_ascii=False, indent=4)
        
        if old_name and old_name in self.active_macros:
            self.deactivate_macro_by_name(old_name)
        
        self.load_macros()
        
        self.combo_entry.delete(0, tk.END)
        self.delay_entry.delete(0, tk.END)
        self.bind_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.current_macro = None
        
        messagebox.showinfo("Успех", f"Макрос '{name}' сохранён!")
    
    def deactivate_macro_by_name(self, macro_name):
        if macro_name in self.active_macros:
            self.active_macros.discard(macro_name)
        
        if macro_name in self.hotkeys_registered:
            try:
                keyboard.remove_hotkey(self.hotkeys_registered[macro_name])
                del self.hotkeys_registered[macro_name]
            except:
                pass
        
        if macro_name in self.last_execution_time:
            del self.last_execution_time[macro_name]
        
        self.update_active_listbox()
    
    def load_selected_macro(self, event):
        selection = self.macros_listbox.curselection()
        if not selection:
            return
        
        macro_name = self.macros_listbox.get(selection[0])
        
        if macro_name in self.active_macros:
            messagebox.showwarning("Ошибка", "Нельзя редактировать активный макрос! Сначала деактивируйте его.")
            return
        
        with open(self.config_file, "r", encoding="utf-8") as f:
            macros = json.load(f)
            macro = macros.get(macro_name)
            
            if macro:
                self.combo_entry.delete(0, tk.END)
                self.combo_entry.insert(0, macro["combo"])
                
                self.delay_entry.delete(0, tk.END)
                self.delay_entry.insert(0, str(macro["delay"]))
                
                self.bind_entry.delete(0, tk.END)
                self.bind_entry.insert(0, macro["bind_key"])
                
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, macro_name)
                
                self.current_macro = macro_name
                
                self.update_edit_state()
    
    def delete_macro(self):
        if not self.current_macro:
            messagebox.showwarning("Ошибка", "Выберите макрос для удаления!")
            return
        
        if self.current_macro in self.active_macros:
            messagebox.showwarning("Ошибка", "Нельзя удалить активный макрос! Сначала деактивируйте его.")
            return
        
        if messagebox.askyesno("Подтверждение", f"Удалить макрос '{self.current_macro}'?"):
            with open(self.config_file, "r", encoding="utf-8") as f:
                macros = json.load(f)
            
            if self.current_macro in macros:
                del macros[self.current_macro]
                
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(macros, f, ensure_ascii=False, indent=4)
                
                self.load_macros()
                self.current_macro = None
                
                self.combo_entry.delete(0, tk.END)
                self.delay_entry.delete(0, tk.END)
                self.bind_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                
                messagebox.showinfo("Успех", "Макрос удалён!")
    
    def start_macro_listener(self):
        def listener_loop():
            while True:
                time.sleep(1)
        
        threading.Thread(target=listener_loop, daemon=True).start()


class BackgroundSelector:
    def __init__(self, parent, app):
        self.window = tk.Toplevel(parent)
        self.window.title("Выбор фона")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)
        
        self.app = app
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()
        self.load_backgrounds()
    
    def on_close(self):
        self.window.destroy()
        if self.app.background_selector_window == self.window:
            self.app.background_selector_window = None
    
    def setup_ui(self):
        current_bg = self.app.get_current_background_image()
        
        canvas = tk.Canvas(self.window, width=400, height=500, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        if current_bg:
            canvas.create_image(0, 0, image=current_bg, anchor="nw", tags="bg")
            canvas.tag_lower("bg")
        
        control_panel = tk.Frame(canvas, bg="#2c2c2c")
        control_panel.place(relx=0.5, rely=0.5, anchor="center", width=380, height=480)
        
        title = tk.Label(control_panel, text="Выбор фона", 
                        font=("Arial", 14, "bold"), bg="#2c2c2c", fg="#9b59b6")
        title.pack(pady=10)
        
        main_frame = tk.Frame(control_panel, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas_frame = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas_frame.yview)
        self.bg_frame = tk.Frame(canvas_frame, bg="#1e1e1e")
        
        canvas_frame.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas_frame.pack(side="left", fill="both", expand=True)
        
        canvas_frame.create_window((0, 0), window=self.bg_frame, anchor="nw")
        
        self.bg_frame.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
        
        canvas_frame.bind("<Enter>", lambda e: canvas_frame.bind_all("<MouseWheel>", lambda event: canvas_frame.yview_scroll(int(-1*(event.delta/120)), "units")))
        canvas_frame.bind("<Leave>", lambda e: canvas_frame.unbind_all("<MouseWheel>"))
        
        close_btn = tk.Button(control_panel, text="Закрыть", 
                             command=self.on_close,
                             bg="#f44336", fg="white", font=("Arial", 11), 
                             cursor="hand2", height=2)
        close_btn.pack(fill="x", padx=10, pady=10)
    
    def load_backgrounds(self):
        for widget in self.bg_frame.winfo_children():
            widget.destroy()
        
        bg_files = self.app.get_background_files()
        
        if not bg_files:
            empty_label = tk.Label(self.bg_frame, text="Нет фонов\nДобавь фоны через главное окно", 
                                   font=("Arial", 10), bg="#1e1e1e", fg="white")
            empty_label.pack(expand=True, fill="both", pady=50)
            return
        
        for name, path in bg_files:
            frame = tk.Frame(self.bg_frame, bg="#3c3c3c", bd=2, relief="groove")
            frame.pack(fill="x", padx=5, pady=5)
            
            name_label = tk.Label(frame, text=name, font=("Arial", 11), 
                                 bg="#3c3c3c", fg="white", anchor="w", cursor="hand2")
            name_label.pack(side="left", padx=10, pady=10, expand=True, fill="x")
            name_label.bind("<Button-1>", lambda e, n=name: self.set_background(n))
            
            use_btn = tk.Button(frame, text="Применить", 
                               command=lambda n=name: self.set_background(n),
                               bg="#4CAF50", fg="white", cursor="hand2", width=10)
            use_btn.pack(side="right", padx=5, pady=5)
    
    def set_background(self, name):
        self.app.set_background(name)
        messagebox.showinfo("Успех", f"Фон '{name}' применён!")
        self.window.destroy()


class AutoCasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dota 2 AutoCaster")
        self.root.geometry("1300x700")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        
        self.bg_folder = os.path.join(os.path.dirname(sys.argv[0]), "backgrounds")
        self.config_file = os.path.join(os.path.dirname(sys.argv[0]), "config.json")
        
        self.bg_images = {}
        self.file_hashes = {}
        self.current_background_name = None
        
        self.background_selector_window = None
        self.macro_manager_window = None
        
        self.canvas = tk.Canvas(self.root, width=1300, height=700, highlightthickness=0)
        self.canvas.place(x=0, y=0, width=1300, height=700)
        
        if not os.path.exists(self.bg_folder):
            os.makedirs(self.bg_folder)
        
        self.load_backgrounds()
        self.create_ui()
        self.load_saved_background()
    
    def show_temp_message(self, message):
        temp_label = tk.Label(self.root, text=message, font=("Arial", 14, "bold"),
                              bg="#2c2c2c", fg="#ff9800")
        temp_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.after(2000, temp_label.destroy)
    
    def get_current_background_image(self):
        if self.current_background_name and self.current_background_name in self.bg_images:
            return self.bg_images[self.current_background_name]
        return None
    
    def get_file_hash(self, file_path):
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def load_backgrounds(self):
        self.bg_images.clear()
        self.file_hashes.clear()
        
        for file in os.listdir(self.bg_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                try:
                    path = os.path.join(self.bg_folder, file)
                    
                    file_hash = self.get_file_hash(path)
                    
                    if file_hash in self.file_hashes.values():
                        continue
                    
                    img = Image.open(path)
                    img = img.resize((1300, 700), Image.Resampling.LANCZOS)
                    
                    name_without_ext = os.path.splitext(file)[0]
                    
                    if name_without_ext not in self.bg_images:
                        self.bg_images[name_without_ext] = ImageTk.PhotoImage(img)
                        self.file_hashes[name_without_ext] = file_hash
                        
                except Exception as e:
                    print(f"Ошибка загрузки {file}: {e}")
    
    def get_background_files(self):
        bg_list = []
        for file in os.listdir(self.bg_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                name = os.path.splitext(file)[0]
                path = os.path.join(self.bg_folder, file)
                bg_list.append((name, path))
        return bg_list
    
    def set_background(self, name):
        if name in self.bg_images:
            self.canvas.delete("bg")
            self.canvas.create_image(0, 0, image=self.bg_images[name], anchor="nw", tags="bg")
            self.canvas.tag_lower("bg")
            
            self.current_background_name = name
            
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump({"last_background": name}, f)
    
    def load_saved_background(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    last_bg = config.get("last_background")
                    if last_bg in self.bg_images:
                        self.set_background(last_bg)
                        return
            except:
                pass
        
        if self.bg_images:
            first_bg = list(self.bg_images.keys())[0]
            self.set_background(first_bg)
    
    def add_background(self):
        file_path = filedialog.askopenfilename(
            title="Выбери изображение для фона",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            try:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(self.bg_folder, filename)
                
                file_hash = self.get_file_hash(file_path)
                
                if file_hash in self.file_hashes.values():
                    messagebox.showwarning("Предупреждение", "Это изображение уже есть в фонах!")
                    return
                
                if os.path.exists(dest_path):
                    base_name = os.path.splitext(filename)[0]
                    ext = os.path.splitext(filename)[1]
                    counter = 1
                    while os.path.exists(dest_path):
                        new_name = f"{base_name}_{counter}{ext}"
                        dest_path = os.path.join(self.bg_folder, new_name)
                        counter += 1
                
                shutil.copy2(file_path, dest_path)
                
                self.load_backgrounds()
                
                messagebox.showinfo("Успех", f"Фон '{os.path.splitext(os.path.basename(dest_path))[0]}' добавлен!")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить фон: {e}")
    
    def open_background_selector(self):
        if self.background_selector_window is not None:
            try:
                if self.background_selector_window.window.winfo_exists():
                    self.show_temp_message("Нельзя открыть два интерфейса одновременно!")
                    self.background_selector_window.window.lift()
                    return
            except:
                pass
        
        self.background_selector_window = BackgroundSelector(self.root, self)
    
    def open_macro_manager(self):
        if self.macro_manager_window is not None:
            try:
                if self.macro_manager_window.window.winfo_exists():
                    self.show_temp_message("Нельзя открыть два интерфейса одновременно!")
                    self.macro_manager_window.window.lift()
                    return
            except:
                pass
        
        self.macro_manager_window = MacroManager(self.root, self)
    
    def create_ui(self):
        button_frame = tk.Frame(self.root, bg="#2c2c2c", bd=2, relief="raised")
        button_frame.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
        
        change_bg_btn = tk.Button(button_frame, text="Поменять фон", 
                                  command=self.open_background_selector,
                                  bg="#2196F3", fg="white", font=("Arial", 12), 
                                  cursor="hand2", height=1, width=18)
        change_bg_btn.pack(padx=15, pady=(15,8))
        
        add_bg_btn = tk.Button(button_frame, text="+ Добавить фон", 
                              command=self.add_background,
                              bg="#4CAF50", fg="white", font=("Arial", 12), 
                              cursor="hand2", height=1, width=18)
        add_bg_btn.pack(padx=15, pady=8)
        
        macro_btn = tk.Button(button_frame, text="Управление макросами", 
                             command=self.open_macro_manager,
                             bg="#9b59b6", fg="white", font=("Arial", 12), 
                             cursor="hand2", height=1, width=18)
        macro_btn.pack(padx=15, pady=(8,15))


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoCasterApp(root)
    root.mainloop()
