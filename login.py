#! python3.5
from tkinter import *
from tkinter import messagebox
import tkinter
import dataset
import os

# 將登入器接上員工的資料庫    
db = dataset.connect('sqlite:///users.db')    


def signup():
    signup_window = tkinter.Toplevel(window)
    signup_window.title("註冊新帳號")
    signup_window.resizable(width=False, height=False)
    signup_window.geometry('300x150')
    frame_form = Frame(signup_window)
    frame_radiobuttons = Frame(frame_form)
    username_prompt = Label(frame_form , text="使用者名稱").grid(row=0, column=0, sticky=E)
    password_prompt = Label(frame_form , text="密碼").grid(row=1, column=0, sticky=E)
    name_prompt = Label(frame_form , text="姓名").grid(row=2, column=0, sticky=E)
    username_entry = Entry(frame_form)
    username_entry.grid(row=0, column=1, sticky=W)
    password_entry = Entry(frame_form)
    password_entry.grid(row=1, column=1, sticky=W)
    name_entry = Entry(frame_form)
    name_entry.grid(row=2, column=1, sticky=W)
    usertype = tkinter.IntVar()
    usertype_prompt = Label(frame_form, text='帳戶類型').grid(row=3, column=0, sticky=E)
    option_employee = Radiobutton(frame_radiobuttons, text="求職者",variable=usertype, value=1).grid(row=0, column=0)
    option_employer = Radiobutton(frame_radiobuttons, text="企業主", variable=usertype, value=2).grid(row=0, column=1)
    frame_radiobuttons.grid(row=3, column=1)
    register_button = Button(signup_window, text="送出", command=lambda: add_user(username_entry.get(), password_entry.get(), name_entry.get()))
    frame_form.pack(pady=10)
    register_button.pack()

    

    def add_user(username, password, name):
        if username!="" and password!=""  and name!="" and usertype.get()!=0:
            for employee in db['Employees']:
                if employee['Username'] == username:
                    messagebox.showerror("註冊失敗", "此帳號已被註冊")
                    return
            for employer in db['Employers']:
                if employer['Username'] == username:
                    messagebox.showerror("註冊失敗", "此帳號已被註冊")
                    return
            if usertype.get() == 1:
                #務必檢查該搷的欄位是否都有在註冊時填到，不然進到主程式的時候讀到空值會錯誤。
                db['Employees'].insert(dict(Name=name, Username=username, Pw=password,
                                            Age=0, Gender=" ", Phone=" ",
                                            Address=" ", Education=" ",About=" "))
            elif usertype.get() == 2:    
                db['Employers'].insert(dict(userName=username,passWord=password, companyIntro=" ",
                                            companyName=" ", companyDes=" "))
            messagebox.showinfo("註冊成功", "您可以登入程式開始搷寫履歷!") 
            signup_window.destroy()   
        else:
            messagebox.showerror("註冊失敗","有欄位沒有填寫")
    
        
def verify(username, password):
    for user in db['Employees']:
        if user['Username'] == username and user['Pw'] == password:
            messagebox.showinfo("登入成功", "即將進入求職者視角")
            window.destroy()
            os.system("python find_job.py %d" % (user['ID']))
            return
    for company in db['Employer']:
        if company['userName'] == username and company['passWord'] == password:
            messagebox.showinfo("登入成功", "即將進入公司方視角")
            window.destroy()
            os.system("python employer.py %d" % (company['ID']))
            return
    messagebox.showerror("登入失敗", "帳號或密碼輸入錯誤")

    
window = tkinter.Tk()
frame_form = Frame(window)
frame_buttons = Frame(window)
window.title("E04求職登入器")
window.resizable(width=False, height=False)
window.geometry('450x250')

#插入圖片
window.canvas = tkinter.Canvas(height=160, width=400)
window.image_file = tkinter.PhotoImage(file='get_a_job.png')#匯入圖檔
window.image = window.canvas.create_image(0,0, anchor='nw', image=window.image_file)
window.canvas.pack(side='bottom')

username_prompt = Label(frame_form , text="使用者名稱").grid(row=0, column=0, sticky=E)
password_prompt = Label(frame_form , text="密碼").grid(row=1, column=0, sticky=E)
username_entry = Entry(frame_form)
username_entry.grid(row=0, column=1, sticky=W)
password_entry = Entry(frame_form)
password_entry['show'] = '*'
password_entry.grid(row=1, column=1, sticky=W)
button_login = Button(frame_buttons, text="登入", command=lambda:verify(username_entry.get(), password_entry.get()))
button_register = Button(frame_buttons, text="註冊", command=signup)
button_login.pack(side=LEFT)
button_register.pack(side=LEFT)
frame_form.pack(pady=10)
frame_buttons.pack()

window.mainloop()
