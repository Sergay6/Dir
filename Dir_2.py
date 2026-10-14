import os
import tkinter as tk
from tkinter import filedialog, messagebox
import filecmp
from pathlib import Path
import shutil
from tkinter import scrolledtext

path_from = ''
path_before = ''
dark_mode = False


themes = {
    "light": {
        "bg": "#f0f0f0", "fg": "#000000", "select": "#ffffff",
        "border": "#bcbcbc", "btn_start_bg": "#2e7d32"
    },
    "dark": {
        "bg": "#2d2d2d", "fg": "#ffffff", "select": "#404040",
        "border": "#555555", "btn_start_bg": "#1b5e20"
    }
}




def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    theme = themes["dark"] if dark_mode else themes["light"]

    root.config(bg=theme["bg"])
    main_frame.config(bg=theme["bg"])

    for widget in main_frame.winfo_children():
        w_class = widget.winfo_class()
        if w_class in ("Label", "Radiobutton", "Button"):
            widget.config(bg=theme["bg"], fg=theme["fg"], activebackground=theme["bg"], activeforeground=theme["fg"])

        if w_class == "Radiobutton":
            widget.config(selectcolor=theme["select"])


        if w_class == "Button" and widget != start_btn and widget != theme_btn:
            widget.config(highlightbackground=theme["border"])

        start_btn.config(fg="white", bg=theme["btn_start_bg"],
                         activebackground=theme["btn_start_bg"], activeforeground="white",
                         highlightbackground=theme["border"], highlightcolor=theme["border"])

        if w_class == "Label":
            text = widget.cget("text")
            if "Откуда:" in text or "Куда:" in text:
                widget.config(fg="green")
            elif text == "Папка не выбрана":
                widget.config(fg="gray")

    theme_btn.config(text="🌙 Темная тема" if not dark_mode else "☀️ Светлая тема")


def choose_folder():
    global path_from
    folder = filedialog.askdirectory(title="Выберите папку-источник")
    if folder:
        path_from = folder
        folder_label.config(text=f"Откуда: {os.path.basename(folder)}", fg="#4CAF50" if not dark_mode else "#81c784")


def choose_folder_2():
    global path_before
    folder = filedialog.askdirectory(title="Выберите папку назначения")
    if folder:
        path_before = folder
        folder_label_2.config(text=f"Куда: {os.path.basename(folder)}", fg="#4CAF50" if not dark_mode else "#81c784")



def file_work():
    global path_from
    global path_before
    global folder_info_option
    global copy_move_info_option
    global file_examination_info_option

    if path_from == '' or path_before == '':
        messagebox.showinfo("Ошибка", "Нужно выбрать обе папки для работы программы!!")
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
                        if file_examination_info_option.get() == "Option 1":
                            x = filecmp.cmp(path_i, path_j, shallow=False)
                        else:
                            x = filecmp.cmp(path_i, path_j)
                        if x == True:
                            file_list.pop(i)
                            break
                        else:
                            j += 1
                else:
                    j += 1
        else:
            if folder_info_option.get() == "Option 1":
                while j <= len(file_list) - 1:
                    path_j = path_from + '/' + file_list[j]
                    if Path(path_j).is_dir():
                        if j == i:
                            j += 1
                        else:
                            x = filecmp.dircmp(path_i, path_j)
                            if not (x.left_only) and not (x.right_only):
                                file_list.pop(i)
                                break
                            else:
                                j += 1
                    else:
                        j += 1
            else:
                file_list.pop(i)

        if length == len(file_list):
            i += 1

    path_before += '/'
    for p in file_list:
        path_from_file = path_from + '/' + p
        if Path(path_from_file).is_file():
            if copy_move_info_option.get() == "Option 1":
                shutil.copy(path_from_file, path_before)
            else:
                shutil.move(path_from_file, path_before)
        else:
            if folder_info_option.get() == "Option 1":
                y = path_before + p
                if copy_move_info_option.get() == "Option 1":
                    shutil.copytree(path_from_file, y)
                else:
                    shutil.move(path_from_file, y)

    messagebox.showinfo("Успех", "Операция выполнена успешно!")





root = tk.Tk()
root.title("File Cleaner & Mover")
root.geometry("450x650")
root.config(bg=themes["light"]["bg"])

main_frame = tk.Frame(root, bg=themes["light"]["bg"], padx=25, pady=10)
main_frame.pack(expand=True, fill="both")

theme_btn = tk.Button(main_frame, text="🌙 Темная тема", command=toggle_theme,
                      relief="flat", font=("Arial", 9), bd=0, highlightthickness=0)
theme_btn.pack(anchor="ne")

tk.Label(main_frame, text="Синхронизация папок", font=("Arial", 14, "bold")).pack(pady=5)


folder_btn_params = {
    "relief": "flat",
    "pady": 7,
    "width": 28,
    "highlightthickness": 2,
    "highlightbackground": themes["light"]["border"]
}

tk.Button(main_frame, text="📁 ВЫБРАТЬ ИСТОЧНИК", command=choose_folder, **folder_btn_params).pack(pady=(15, 5))
folder_label = tk.Label(main_frame, text="Папка не выбрана", font=("Arial", 8, "italic"), fg="gray")
folder_label.pack()

tk.Button(main_frame, text="📁 ВЫБРАТЬ НАЗНАЧЕНИЕ", command=choose_folder_2, **folder_btn_params).pack(pady=(15, 5))
folder_label_2 = tk.Label(main_frame, text="Папка не выбрана", font=("Arial", 8, "italic"), fg="gray")
folder_label_2.pack()


def create_section(text, var, options):
    tk.Label(main_frame, text=text, font=("Arial", 10, "bold")).pack(pady=(15, 5))
    for text_opt, val in options:
        rb = tk.Radiobutton(main_frame, text=text_opt, variable=var, value=val,
                            highlightthickness=0, bd=0)
        rb.pack(anchor="w", padx=60)


folder_info_option = tk.StringVar(value="Option 1")
create_section("Обработка папок:", folder_info_option,[("Проверять папки", "Option 1"), ("Игнорировать папки", "Option 2")])

copy_move_info_option = tk.StringVar(value="Option 1")
create_section("Действие:", copy_move_info_option,
               [("Копировать", "Option 1"), ("Вырезать", "Option 2")])

file_examination_info_option = tk.StringVar(value="Option 1")
create_section("Метод сравнения:", file_examination_info_option,[("Проверять содержимое", "Option 1"), ("Проверять метаданные", "Option 2")])


start_btn = tk.Button(main_frame, text="ЗАПУСТИТЬ", command=file_work,
                      bg="#2e7d32", fg="white", font=("Arial", 12, "bold"),
                      relief="flat", width=22, pady=10,
                      highlightthickness=3, highlightbackground="#1b5e20")
start_btn.pack(pady=(25, 10))

ReadMe = tk.Tk()
ReadMe.title("ReadMe")
ReadMe.geometry("450x650")

readme_text = scrolledtext.ScrolledText(ReadMe, wrap=tk.WORD, width=40, height=15)
readme_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

content = """
    Название программы: Dir
    Версия: 2.0

    Описание:
    Это приложение разработано на Python для поиска 
    уникальных файлов

    Инструкция:
    1. Кнопка 'ВЫБРАТЬ ИСТОЧНИК' - при нажатии на
     кнопку откроется окно в котором нужно выбрать
      папку. При запуске программы файлы из этой 
      папки проверит программа, а потом скопирует 
      или вырежет(см. пункт 4.).
    
    2. Кнопка 'ВЫБРАТЬ НАЗНАЧЕНИЕ' - при нажатии на
     кнопку откроется окно в котором нужно выбрать
      папку. При запуске программы все уникальные 
      файлы перенесутся в выбранную паку. 
    
    3. 'Обработка папок' - выбор из двух вариантов:
     'Проверять папки','Игнорировать папки'. 
     Выбрать можно только один вариант. 
    
    'Проверять папки' - при выборе этого варианта,
     программа будет проверять и переносить папки.
      !Важно: При проверки папок проверяются только
       названия файлов внутри папки.
    
    'Игнорировать папки' - при выборе этого
     варианта, программа не будет проверять и 
     переносить папки.
    
    4. 'Действие' - выбор из двух вариантов:
     'Копировать','Вырезать'. Выбрать можно только
      один вариант. 
    
    'Копировать' - при выборе этого варианта, в
     папке назначения появятся копии всех
      уникальных файлов и директорий, папка 
      источник не измениться.
    
    'Вырезать' - при выборе этого варианта,
     программа вырежет все уникальные файлы и
      директории из папки источника и переместит их 
      в папку назначения.
    
    5. 'Метод сравнения' - выбор из двух вариантов:
     'Проверять содержимое','Проверять метаданные'. 
     Выбрать можно только один вариант.
     
    Выбор изменяет метод сравнения файлов, но не
    как не влияет на сравнение директорий
    
    'Проверять содержимое' - при выборе этого
     варианта, произойдёт побитовая проверка 
     файлов. Этот способ более надёжный, но 
     менеее быстрый.
    
    'Проверять метаданные' - при выборе этого
     варианта, произойдёт сравнение метаданных 
     файлов(размер файла, время изменения и тд.). 
     Этот способ менее надёжный, но более быстрый.
    
    6. Кнопка 'ЗАПУСТИТЬ' - при нажатии кнопки, 
    запускаеться алгоритм проверки и переносса 
    данных
    
    !Важно: алгоритм не запистится, если хотябы 
    одна из папок не выброна(см. пункты 1, 2).
    
    
    Автор: Мамонов Сергей
    """

readme_text.insert(tk.INSERT, content)
readme_text.configure(state='disabled')

root.mainloop()