import os
import random as rand
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

them = ""


def open_input_window():
    them = ""
    # Считываем данные из файла
    if os.path.isfile("RQ.txt"):
        data = return_data("RQ.txt")
        themas = return_question(data)
    else:
        themas = {}

    input_window = Toplevel(root)
    input_window.title("Редактирование тем и вопросов")

    # Фрейм для кнопок тем
    themes_frame = Frame(input_window)
    themes_frame.pack(padx=10, pady=5)

    # Текстовое поле для отображения и редактирования вопросов
    question_text = Text(input_window, height=15, width=50)
    question_text.pack(padx=10, pady=5)

    # Поле для ввода количества вопросов
    Label(input_window, text="Количество вопросов:").pack(padx=10, pady=5)
    question_count_entry = Entry(input_window)
    question_count_entry.pack(padx=10, pady=5)

    def show_questions(theme):
        # Очистка текстового поля при переключении тем
        global them
        them = theme
        question_text.delete(1.0, END)
        questions = themas[theme]["questions"]
        for question in questions:
            question_text.insert(END, question + "\n")
        question_count_entry.delete(0, END)
        question_count_entry.insert(0, str(themas[theme]["len"]))

    # Создание кнопок для каждой темы
    def create_theme_buttons():
        for widget in themes_frame.winfo_children():
            widget.destroy()  # Удаляем старые кнопки
        for thema in themas.keys():
            button = Button(themes_frame, text=thema, command=lambda t=thema: show_questions(t))
            button.pack(side=TOP, padx=5, pady=2)

    create_theme_buttons()

    def save_questions():
        global them
        theme = them
        questions = question_text.get(1.0, END).split("\n")

        if theme in themas:
            themas[theme]["questions"] = questions
            themas[theme]["len"] = int(question_count_entry.get())  # Обновляем количество вопросов
            messagebox.showinfo("Успешно", "Вопросы сохранены успешно")
        else:
            messagebox.showerror("Ошибка", "Тема не найдена")
            return

        # Перезаписываем файл
        with open("RQ.txt", "w", encoding="utf-8") as file:
            file.write("**themas\n")
            for thema, info in themas.items():
                file.write(f"{thema} {info['len']}\n")
            file.write("**questions\n")
            for thema, info in themas.items():
                for question in info["questions"]:
                    if question.replace(" ", "") != "":
                        file.write(f"{thema} {question}\n")

    # Кнопка для сохранения изменений
    save_button = Button(input_window, text="Сохранить изменения", command=save_questions)
    save_button.pack(padx=10, pady=5)

    # Поле для ввода новой темы
    Label(input_window, text="Введите название новой темы:").pack(padx=10, pady=5)
    theme_entry = Entry(input_window)
    theme_entry.pack(padx=10, pady=5)

    def add_theme():
        new_theme = theme_entry.get()
        if new_theme and new_theme not in themas:
            themas[new_theme] = {"len": 0, "questions": []}
            theme_entry.delete(0, END)
            messagebox.showinfo("Успешно", "Новая тема добавлена")
            create_theme_buttons()  # Обновляем кнопки тем
        else:
            messagebox.showerror("Ошибка", "Тема уже существует или пустая")

    # Кнопка для добавления новой темы
    add_theme_button = Button(input_window, text="Добавить новую тему", command=add_theme)
    add_theme_button.pack(padx=10, pady=5)


def return_data(path):
    with open(path, encoding="utf-8") as file:
        data = file.readlines()
    return data


def return_question(datas: list):
    themas = {}
    themas_questions = None

    for data in datas:
        data = data.replace("\n", "")
        if data.find("#") != -1:
            data = data[:data.find("#")]
        if data != "":
            if data.startswith("**questions"):
                themas_questions = False
            elif data.startswith("**themas"):
                themas_questions = True

            else:
                if themas_questions:
                    thema, len_questions = data.split(" ", maxsplit=1)
                    themas.update({thema: {"len": int(len_questions), "questions": []}})
                else:
                    thema, question = data.split(" ", maxsplit=1)
                    themas[thema]["questions"] += [question]
    return themas


def return_random_question(themas: dict):
    random = {}
    for thema in themas:
        random.update({thema: []})
        for _ in range(themas[thema]["len"]):
            number = rand.randint(0, len(themas[thema]["questions"]) - 1)
            random[thema] += [themas[thema]["questions"][number]]
            del themas[thema]["questions"][number]

    return random


def format_questions(th_questions: dict) -> list:
    to_box = list()
    for thema, questions in th_questions.items():
        to_box.append(thema)
        a = 0
        for quest in questions:
            a += 1
            strings = [f"  {a}. {quest}"]
            while len(strings[-1]) > 50:
                strings.append(strings[-1][:50])
                strings.append("        " + strings[-2][60:])
                del strings[-3]
            to_box += strings

    return to_box


def refresh():
    global questions_listbox
    global root
    questions_listbox.destroy()

    data = return_data("RQ.txt")
    themas = return_question(data)
    themas = return_random_question(themas)
    themas = format_questions(themas)

    questions_var_refresh = Variable(value=themas)

    questions_listbox = Listbox(listvariable=questions_var_refresh, height=30, width=85)

    questions_listbox.pack(anchor=NW, fill="both", padx=5, pady=5)


if os.path.isfile("RQ.txt"):
    pass
else:
    with open("RQ.txt", "w", encoding="utf-8") as file:
        file.write("""
# **themas означает начало ввода тем. Пишется название темы, а потом через пробел количество вопросов по теме
**themas

# **questions означает начало ввода вопросов по темам. Пишется название темы и через пробел сам вопрос
**questions
""")
        os.chmod("RQ.txt", 0o777)

root = Tk()
root.title("RQ V0.1b")

input_button = ttk.Button(text="Добавить темы и вопросы", command=open_input_window)
input_button.pack(anchor=NW, fill=X, padx=5, pady=5)

questions_var = Variable(value=[])

questions_listbox = Listbox(listvariable=questions_var)

refresh_button = ttk.Button(text="Refresh", command=refresh)

refresh_button.pack(anchor=NW, fill=X, padx=5, pady=5)

questions_listbox.pack(anchor=NW, fill="both", padx=5, pady=5)

root.mainloop()
