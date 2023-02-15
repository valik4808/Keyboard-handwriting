import json
from tkinter import *
from typing import NoReturn
import hashlib
import os
import keyboard
import time



def input_text() -> list:

    def func(e):
        sleep_time(e.event_type, e.name, e.time)

    def sleep_time(type_event: str, name: str, time_event: int) -> NoReturn:
        nonlocal flag, lst_keystroke
        try:

            if name == '+':  # при нажатии клавиши "+" удаляем последнюю неполную записть
                lst_keystroke.pop()
                return
            if type_event == 'up':  # при отпускании клавиши записываем ее имя и время нажатия
                lst_keystroke.append([name, time_event])
                flag += 1
            else:
                if flag != 0:  # если флаг равен 0, то это первое нажатие, его игнорируем.
                    # находим разницу между временем отпуска предыдущей клавиши и новой и записываем в список
                    lst_keystroke[flag - 1][1] = time_event - lst_keystroke[flag - 1][1]
                    lst_keystroke[flag - 1].append(name)
        except:
            pass
    try:
        lst_keystroke = []
        flag = 0
        keyboard.hook(func) #fresh meat
        keyboard.wait('+')
        keyboard.unhook(func)
        time.sleep(0.005)
        print()
        lst_keystroke_2 = [lst for lst in lst_keystroke if len(lst) == 10]
        return lst_keystroke_2
    except:
        pass


def main_2(db_info):
    db_user: dict = {}

    name_user: str = in_users.get()
    db_user = db_info
    rez = []
    for i in range(len(db_user[0])):
        time_lst = []
        try:
            for j in db_user:
                a = j[i][0] + j[i][2]
                time_lst.append(j[i][1])
        except:
            pass
        mn = min(time_lst)
        mx = max(time_lst)
        sr = round((mx - mn) / 10 + 0.00005, 5)
        t = []
        for i in range(10):
            mn_2 = round(mn + sr, 5)
            t.append([mn, mn_2])
            mn = mn_2
        chastota = [0] * 10
        for i in time_lst:
            for count, values in enumerate(t):
                if values[0] <= i < values[1]:
                    chastota[count] += 1
                    break
        mato = 0
        for i, values in enumerate(chastota):
            mato += values / len(time_lst) * (t[i][1] - t[i][0]) / 2
        disp = 0
        for i, values in enumerate(chastota):
            disp += values / len(time_lst) * ((t[i][1] - t[i][0]) / 2) ** 2 - mato
        rez.append((a, mato, disp, (abs(disp) ** 0.5)/2))

    #f = open('rez_1.txt', 'r')
    #z = f.readlines()
    flag = 0
    print(rez)
    rez_2 = []
    for i in range(len(z)):
        print(z[i].rstrip(), name_user)
        if z[i].rstrip() == name_user:
            for j in range(i + 1, len(z)):
                if '.' not in z[j]:
                    break
                strok = z[j].split()
                del strok[0]
                strok = list(map(float, strok))
                rez_2.append(strok)
            break
   # print(rez_2)
   # for i in range(len(rez_2)):
        print("rez2")
        print(rez_2[i])
        print("rez")
        print(rez[0])
        if rez_2[i][0] - rez_2[i][2] <= rez[i][1] or rez_2[i][0] + rez_2[i][2] >= rez[i][1]:
        # if abs(rez_2[i][0] - rez[i][1]) > rez_2[i][0] * 0.7:7
            flag = 1
            break
    if flag:
        label_title = Label(text='Авторизация успешна!', font=('Arial', 14))
        label_title.place(width=300, height=50, x=200, y=340)
    else:
        label_title = Label(text='Отказано в доступе!', font=('Arial', 14))
        label_title.place(width=300, height=50, x=200, y=340)

    f.close()


def main(db_info):
    db_user: dict = {}

    name_user: str = in_users.get()
    db_user = db_info
    rez = []
    for i in range(len(db_user[0])):
        time_lst = []
        try:
            for j in db_user:
                a = j[i][0] + j[i][2]
                time_lst.append(j[i][1])
        except:
            pass
        mn = min(time_lst)
        mx = max(time_lst)
        sr = round((mx - mn) / 10 + 0.00005, 5)
        t = []
        for i in range(10):
            mn_2 = round(mn + sr, 5)
            t.append([mn, mn_2])
            mn = mn_2
        chastota = [0] * 10
        for i in time_lst:
            for count, values in enumerate(t):
                if values[0] <= i < values[1]:
                    chastota[count] += 1
                    break
        mato = 0
        for i, values in enumerate(chastota):
            mato += values / len(time_lst) * (t[i][1] - t[i][0]) / 2
        disp = 0
        for i, values in enumerate(chastota):
            disp += values / len(time_lst) * ((t[i][1] - t[i][0]) / 2) ** 2 - mato
        rez.append((a, mato, disp, abs(disp) ** 0.5))

    f = open('rez_1.txt', 'w')
    f.write(f'{name_user}\n')
    for i in rez:
        for j in i:
            f.write(f'{j} ')
        f.write('\n')
    f.close()
    f = open('rez_2.txt', 'w')
    f.write(f'{name_user}\n')
    for i in rez:
        st = ''
        for j in i:
            st += str(j)
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', st.encode('utf-8'), salt, 100000)
        f.write(f'{key}\n')
    f.write('-'*100)
    f.close()

def register(info):
    count = len(info)
    array = []
    for i in range(len(info[0])):
        array.append(0)
    for i in range(len(info)):
        for j in range(len(info[i])):
            array[j] += info[i][j][1]
    for i in range(len(array)):
        array[i] /= count
    print(array)
    name = in_users.get()
    string = ' '.join(str(x) for x in array)
    with open("doc1.txt", "w") as file:
        file.write(f'{name}\n{password} {string}')
    with open("doc1SHA.txt", "w") as file:
        salt = os.urandom(32)
        hashPass = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        file.write(f'{name}\n{hashPass} {string}')

def compare(info):
    name_user = in_users.get()
    f = open('doc1.txt', 'r')
    z = f.readlines()
    rez_2 = []
    for i in range(len(z)):
        if z[i].rstrip() == name_user:
            for j in range(i + 1, len(z)):
                if '.' not in z[j]:
                    break
                strok = z[j].split()
                if strok[0] != password:
                    label_title = Label(text='Неверный пароль', font=('Arial', 14))
                    label_title.place(width=300, height=50, x=200, y=340)
                    return
                del strok[0]
                strok = list(map(float, strok))
                rez_2.append(strok)
            break
        else:
            label_title = Label(text='Неверное имя пользователя', font=('Arial', 14))
            label_title.place(width=300, height=50, x=200, y=340)
            return
    fileInputCount = len(info[0])
    count = 0
    for i in range(len(info[0])):
        input = info[0][i][1]
        fileInput = rez_2[0][i]
        print(input, fileInput)
        if input <= (fileInput + 0.15) and input >= (fileInput - 0.15):
            count += 1
        else: print(False)
    if count == fileInputCount:
        label_title = Label(text='Авторизация успешна!', font=('Arial', 14))
        label_title.place(width=300, height=50, x=200, y=340)
    else:
        label_title = Label(text='Отказано в доступе!', font=('Arial', 14))
        label_title.place(width=300, height=50, x=200, y=340)

    f.close()

def menu():
    clear()


    b_1 = Button(text='Регистрация', font=('Arial', 24), fg='black', command=input_text_1)
    b_1.place(x=25, y=500, width=300)
    b_2 = Button(text='Вход', font=('Arial', 24), fg='black', command=input_text_2)
    b_2.place(x=375, y=500, width=300)


def clear():
    all_widg = window.place_slaves()
    for widg in all_widg:
        widg.destroy()

def resetResult():
    global db_user
    global flag
    global keystroke_array
    global count
    db_user = []
    keystroke_array = []
    flag = 0
    in_pass.delete(0, END)
    in_users.delete(0, END)
    count = 10
    updateLabel()


def setupUI():
    global uiIsSetuped
    global countLabel
    if uiIsSetuped: return
    label_title = Label(text='Введите имя пользователя:', font=('Arial', 14))
    label_title.place(width=300, height=50, x=200, y=140)
    # in_users = Entry(width=39, justify=CENTER)
    in_users.place(x=232, y=190)

    label_title = Label(text='Введите пароль:', font=('Arial', 14))
    label_title.place(width=300, height=50, x=200, y=220)
    # in_users = Entry(width=39, justify=CENTER)
    in_pass.place(x=232, y=270)

    countLabel = Label(textvariable=countString, font=('Arial', 14))


def input_text_1():
    global uiIsSetuped
    global isCheckingType
    isCheckingType = False
    setupUI()
    resetResult()
    countLabel.place(x=50, y=350)

def input_text_2():
    countLabel.place_forget()
    global isCheckingType
    isCheckingType = True
    setupUI()
    resetResult()
    

window = Tk()
window.title('Keyboard-handwriting')
window.geometry('700x600')

def updateLabel():
    countString.set(str(count) + "раз")

def clearPass():
    global password
    password = in_pass.get()
    in_pass.delete(0, END)
    global count
    global countString
    global keystroke_array
    global flag
    global db_user
    count -= 1
    updateLabel()
    keystroke_array.pop()
    db_user.append(keystroke_array)
    flag = 0
    keystroke_array = []
    if isCheckingType:
        # main_2(db_info=db_user)
        compare(info=db_user)
        db_user = []
    if count <= 0:
        countString.set("Обучение закончено")
        # main(db_info=db_user)
        register(info=db_user)
        return

def textChanged(sv):
    global flag
    sttr = sv.get()

    if flag != 0 and len(sttr) != 0:
        keystroke_array[flag - 1][1] = time.time() - keystroke_array[flag - 1][1]
        keystroke_array[flag - 1].append(sttr[-1])

def keyRelease(event):
    global flag
    sttr = sv.get()
    if len(sttr) == 0: return
    keystroke_array.append([sttr[-1], time.time()])
    flag += 1

password = ''
uiIsSetuped = False
isCheckingType = False
keystroke_array = []
db_user = []
sv = StringVar()
flag = 0
countString = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: textChanged(sv))

in_users = Entry(width=39, justify=CENTER)
in_pass = Entry(width=39, textvariable=sv, justify=CENTER, show = '*')
in_pass.bind("<Return>", (lambda event: clearPass()))
in_pass.bind("<KeyRelease>", keyRelease)
menu()

window.mainloop()