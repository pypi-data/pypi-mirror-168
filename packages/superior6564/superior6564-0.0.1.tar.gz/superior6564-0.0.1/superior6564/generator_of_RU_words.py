from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import itertools


def generator():
    letters = txt.get()
    length_of_words = int(combo.get())
    name_of_file = 'russian_nouns.txt'
    file = open(name_of_file, 'r', encoding='utf-8')
    list_of_ru_words = []
    for i in range(51300):
        list_of_ru_words.append(file.readline()[0:-1])
    result = ""
    result += f"Слова из {length_of_words} букв:        \n"
    words = set(itertools.permutations(letters, r=length_of_words))
    count_2 = 1
    for word in words:
        count = 0
        generate_word = "".join(word)
        for j in range(len(list_of_ru_words)):
            if generate_word == list_of_ru_words[j] and count == 0:
                result += f"{count_2} слово: {generate_word}        \n"
                count += 1
                count_2 += 1
    messagebox.showinfo("Результаты", result)


if __name__ == '__main__':
    window = Tk()
    window.title("Линия слова")
    window.geometry('230x120')
    lbl_input = Label(window, text="Введите все буквы из круга")
    lbl_input.grid(column=2, row=0)
    txt = Entry(window, width=24)
    txt.grid(column=2, row=1)
    txt.focus()
    lbl = Label(window, text="Выберите из скольки букв нужно слово?")
    lbl.grid(column=2, row=3)
    combo = Combobox(window)
    combo['values'] = (3, 4, 5, 6, 7)
    combo.current(0)
    combo.grid(column=2, row=4)
    btn = Button(window, text="Отправить параметры для поиска слов", command=generator)
    btn.grid(column=2, row=5)
    window.mainloop()
