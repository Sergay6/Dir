import os
import tkinter as tk
from tkinter import filedialog
import filecmp
from pathlib import Path
import shutil

path_from = ''
path_before = ''

def choose_folder():
    global  path_from
    folder_path = filedialog.askdirectory(title="Выберите папку")
    path_from = folder_path
    if folder_path:
        folder_label.config(text=folder_path)

def choose_folder_2():
    global path_before
    folder_path_2 = filedialog.askdirectory(title="Выберите папку")
    path_before = folder_path_2
    if folder_path_2:
        folder_label_2.config(text=folder_path_2)

def file_work():
    global path_from
    global path_before
    if path_from == '' or path_before == '':
        return
    file_list = os.listdir(path_from)
    i = 0
    while i <= len(file_list) - 1:
        length = len(file_list)
        path_i = path_from + '/' + file_list[i]
        j = 0
        if Path(path_i).is_file():
            while j <= len(file_list) - 1:
                path_j = path_from + '/' + file_list[j]
                if Path(path_j).is_file():
                    if j == i:
                        j += 1
                    else:


                        x = filecmp.cmp(path_i, path_j, shallow=False)

                        if x == True:
                            file_list.pop(i)
                            break
                        else:
                            j += 1
                else:
                    j += 1
        else:
            while j <= len(file_list) - 1:
                path_j = path_from + '/' + file_list[j]
                if Path(path_j).is_dir():
                    if j == i:
                        j += 1
                    else:
                        x = filecmp.dircmp(path_i, path_j)

                        if not(x.left_only) and not(x.right_only):
                            file_list.pop(i)
                            break
                        else:
                            j += 1
                else:
                    j += 1
        if length == len(file_list):
            i += 1

    path_before += '/'
    for p in file_list:
        path_from_file = path_from + '/' + p

        if Path(path_from_file).is_file():
            shutil.copy(path_from_file, path_before)
        else:
            y = path_before + p
            shutil.copytree(path_from_file, y)

root = tk.Tk()
root.title("Выбор папки")
root.geometry("400x280")

button = tk.Button(root, text="Выбрать папку, источник", command=choose_folder)
button.pack(pady=20)

folder_label = tk.Label(root, text="Папка не выбрана", wraplength=350)
folder_label.pack()



button_2 = tk.Button(root, text="Выбрать папку", command=choose_folder_2)
button_2.pack(pady=20)

folder_label_2 = tk.Label(root, text="Папка не выбрана", wraplength=350)
folder_label_2.pack()

button3 = tk.Button(root, text="Переместить", command=file_work)
button3.pack(pady=20)

root.mainloop()