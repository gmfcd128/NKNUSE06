import tkinter as tk                   
from tkinter import ttk
from tkinter import messagebox
import TkTreectrl as treectrl
from tkinter import *
import dataset
import sys

db = dataset.connect('sqlite:///users.db')
user_id = 0

#功能區塊
def cmd_select(selected):
    print('Selected items :', selected)


window3 = tk.Tk() #必須
user_id = int(sys.argv[1])        
current_user = db['Employer'].find_one(ID=user_id)             
window3.title("E04求職網-公司方視角" + "(目前使用者: " + current_user['userName'] + ")")#必須
window3.resizable(width=False, height=False)#必須
window3.geometry('800x600')#必須
tabControl = ttk.Notebook(window3)

#標籤
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text = "收到的履歷")
tabControl.add(tab2, text = "提供職缺")
tabControl.add(tab3, text = "公司資訊")
tabControl.pack(expand = 1 , fill = "both")



#履歷列表
listbox = treectrl.MultiListbox(tab1)
listbox.pack(expand = 1 , fill = "both")
listbox.focus_set()
listbox.configure(selectcmd = cmd_select, selectmode = 'extended')
listbox.config(columns=('年齡','性別','姓名','學歷'))

#提供職缺

#公司資訊編輯
#功能 : 更新資訊(可以改變sql)
def company_update():
    db.query('UPDATE Employees SET coName = "' + coName_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employer SET workName = "' + workname_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET companyIntro = "' + intro_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET works = "' + works_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET welfare = "' + welfare_entry.get() +'" WHERE ID=' + str(user_id) +';')
    db.query('UPDATE Employees SET jobVac = "' + jobVac_entry.get() +'" WHERE ID=' + str(user_id) +';')
#公司資料排版
Grid.columnconfigure(tab3 , 1 , weight = 1)
#公司名稱
coName_prompt = Label(tab3 , text = "公司名稱").grid(row = 0, column = 0, sticky = N+W)
coName_entry = Entry(tab3)
coName_entry.grid(row = 0 , column = 1 , sticky = E+W)
coName_entry.insert(0, current_user['companyName'])
#職稱
workname_prompt = Label(tab3, text= "職稱").grid(row = 1, column = 0, sticky= N+W)
workname_entry = Entry(tab3)
workname_entry.grid(row=1, column = 1, sticky = E+W)
workname_entry.insert(0, current_user['workName'])
#公司介紹
intro_prompt = Label(tab3, text = "公司介紹").grid(row = 3, column = 0, sticky = N+W)
intro_entry = Entry(tab3)
intro_entry.grid(row = 3, column = 1, sticky = E+W)
intro_entry.insert(0,current_user['companyIntro'])
#工作內容
works_prompt = Label(tab3, text = "工作內容").grid(row = 4, column = 0, sticky = N+W)
works_entry = Entry(tab3)
works_entry.grid(row= 4, column = 1, sticky = E+W)
works_entry.insert(0,current_user['Works'])
#公司福利
welfare_prompt = Label(tab3, text = "公司福利").grid(row = 5 , column = 0 , sticky = N+W)
welfare_entry = Entry(tab3)
welfare_entry.grid(row = 5, column = 1, sticky = E+W)
welfare_entry.insert(0, current_user['Welfare'])
#職位空缺
jobVac_prompt = Label(tab3, text = "職位空缺").grid(row = 6, column = 0 , sticky = N+W)
jobVac_entry = Entry(tab3)
jobVac_entry.grid(row = 6 , column = 1, sticky = E+W)
jobVac_entry.insert(0 , current_user['jobVacancy'])
Grid.rowconfigure(tab3, 7 , weight =1 )
#更多空間
extra_prompt = Label (tab3, text = "公司介紹/福利/制度").grid(row=7, column = 0, sticky = N+W)
extra_entry = Entry(tab3)
extra_entry.grid(row = 7, column = 1 , sticky = N+W+E+S)
extra_entry.insert(0, current_user['companyIntro'])
save_button = Button(tab3, text = "更新內容", command = company_update)
save_button.grid(row = 8, column = 1)




#迴圈實作window3
window3.mainloop()