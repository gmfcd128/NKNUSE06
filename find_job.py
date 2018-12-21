import tkinter as tk                   
from tkinter import ttk
from tkinter import messagebox
import TkTreectrl as treectrl
from tkinter import *
import dataset
import sys

db = dataset.connect('sqlite:///users.db') 
user_id = 0


def test():
    messagebox.showinfo("Info", "We're FUCKED.")


def select_cmd(selected):
    print ('Selected items:', selected)


window2 = tk.Tk() 
user_id = int(sys.argv[1])        
current_user = db['Employees'].find_one(ID=user_id)             
window2.title("E04求職網-求職者視角" + "(目前使用者：" + current_user['Name'] + ")")
window2.resizable(width=False, height=False)
window2.geometry('800x600')        
tabControl = ttk.Notebook(window2)          

# 視窗標籤相關設定
tab1 = ttk.Frame(tabControl)  
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)           
tabControl.add(tab1, text="職缺搜尋") 
tabControl.add(tab2, text="回覆狀況") 
tabControl.add(tab3, text="履歷編輯")
tabControl.pack(expand=1, fill="both")

# 搜尋框與按鈕 
search = ttk.Frame(tab1)    
searchbox = Entry(search).grid(row=0, column=0, sticky=W + E)
search.grid_columnconfigure(0, weight=1)
search_button = Button(search, text="搜尋", command=test).grid(row=0, column=1, padx=5, pady=5)
search.pack(expand=0, fill=X)

# 職缺列表
listbox = treectrl.MultiListbox(tab1)
listbox.pack(expand=1, fill="both")
listbox.focus_set()   
listbox.configure(selectcmd=select_cmd, selectmode='extended')
listbox.config(columns=('職位名稱', '工作地點', "工作時間", "應徵人數"))

#按下更新按鈕後執行以下sql命令更新資料庫
def update_info():
    db.query('UPDATE Employees SET Name = "' + name_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET Age = "' + age_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET Gender = "' + gender_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET Phone = "' + phone_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET Address = "' + address_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET Education = "' + education_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET About = "' + extra_entry.get() +'" WHERE ID=' + str(user_id) +';')


Grid.columnconfigure(tab3, 1, weight=1)
name_prompt = Label(tab3, text="姓名").grid(row=0, column=0, sticky=N + W)

name_entry = Entry(tab3)
name_entry.grid(row=0, column=1, sticky=E + W)
name_entry.insert(0, current_user['Name'])

gender_prompt = Label(tab3, text="性別").grid(row=1, column=0, sticky=N + W)

gender_entry = Entry(tab3)
gender_entry.grid(row=1, column=1, sticky=E + W)
gender_entry.insert(0, current_user['Gender'])

age_prompt = Label(tab3, text="年齡").grid(row=2, column=0, sticky=N + W)

age_entry = Entry(tab3)
age_entry.grid(row=2, column=1, sticky=E + W)
age_entry.insert(0, current_user['Age'])

address_prompt = Label(tab3, text="地址").grid(row=3, column=0, sticky=N + W)

address_entry = Entry(tab3)
address_entry.grid(row=3, column=1, sticky=E + W)
address_entry.insert(0, current_user['Address'])

phone_prompt = Label(tab3, text="電話").grid(row=4, column=0, sticky=N + W)

phone_entry = Entry(tab3)
phone_entry.grid(row=4, column=1, sticky=E + W)
phone_entry.insert(0, current_user['Phone'])

education_prompt = Label(tab3, text="教育程度").grid(row=5, column=0, sticky=N + W)

education_entry = Entry(tab3)
education_entry.grid(row=5, column=1, sticky=E + W)
education_entry.insert(0, current_user['Education'])
Grid.rowconfigure(tab3, 6, weight=1)
extra_prompt = Label(tab3, text="自我介紹").grid(row=6, column=0, sticky=N + W)
extra_entry = Entry(tab3)
extra_entry.grid(row=6, column=1, sticky=N + W + E + S)
extra_entry.insert(0, current_user['About'])
save_button = Button(tab3, text="更新內容", command=update_info)
save_button.grid(row=7, column=1)

# 畫面出現

window2.mainloop() 
                             
