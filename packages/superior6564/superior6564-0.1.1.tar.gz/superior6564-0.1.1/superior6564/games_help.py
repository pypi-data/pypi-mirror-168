"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""


from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import itertools
import requests


def gen_ru_words(check: int):
    russian_nouns_txt = requests.get('https://raw.githubusercontent.com/Superior-GitHub/Superior6564/main/superior6564/russian_nouns.txt')

    out_1 = open("russian_nouns.txt", "wb")
    out_1.write(russian_nouns_txt.content)
    out_1.close()
    if check == 1:
        print("Write all of letters which do you have")
        letters = input("Write in this line: ")
        print("Write length of words which do you need")
        length_of_words = int(input("Write in this line: "))
        with open('russian_nouns.txt', encoding='utf-8') as f:
            list_of_ru_words = []
            for i in range(51300):
                list_of_ru_words.append(f.readline()[0:-1])
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
        print(result)

    elif check == 0:
        def generator():
            letters = txt.get()
            length_of_words = int(combo.get())
            with open('russian_nouns.txt', encoding='utf-8') as f:
                list_of_ru_words = []
                for i in range(51300):
                    list_of_ru_words.append(f.readline()[0:-1])
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
