from tkinter import *
from tkinter import messagebox
import tkinter
import dataset
import os

# 將登入器接上員工的資料庫    
db = dataset.connect('sqlite:///users.db')    



def test():
    messagebox.showinfo("Info", "We're FUCKED.")

    
def verify(username, password):
    for user in db['Employees']:
        if user['Username'] == username and user['Pw'] == password:
            messagebox.showinfo("登入成功", "即將進入求職者視角")
            window.destroy()
            os.system("python find_job.py %d" % (user['ID']))
            return
    messagebox.showerror("登入失敗", "系統查無此使用者")


    
window = tkinter.Tk()
frame_form = Frame(window)
frame_buttons = Frame(window)
window.title("E04求職登入器")
window.resizable(width=False, height=False)
window.geometry('300x110')
username_prompt = Label(frame_form , text="使用者名稱").grid(row=0, column=0, sticky=E)
password_prompt = Label(frame_form , text="密碼").grid(row=1, column=0, sticky=E)
username_entry = Entry(frame_form)
username_entry.grid(row=0, column=1, sticky=W)
password_entry = Entry(frame_form)
password_entry['show'] = '*'
password_entry.grid(row=1, column=1, sticky=W)
button_login = Button(frame_buttons, text="登入", command=lambda:verify(username_entry.get(), password_entry.get()))
button_register = Button(frame_buttons, text="註冊", command=test)
button_login.pack(side=LEFT)
button_register.pack(side=LEFT)
frame_form.pack(pady=10)
frame_buttons.pack()



window.mainloop()


