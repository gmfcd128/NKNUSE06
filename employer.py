import tkinter as tk                   
from tkinter import ttk
from tkinter import messagebox
import TkTreectrl as treectrl
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import dataset
import sys


def gui(id):

    db = dataset.connect('sqlite:///users.db')
    job_db = dataset.connect('sqlite:///jobs.db')
    user_id = id
    selected_applicant = None
    
    window3 = tk.Tk()  # 必須     
    current_user = db['Employer'].find_one(ID=user_id)             
    window3.title("E04求職網-公司方視角" + "(目前使用者: " + current_user['companyName'] + ")")  # 必須
    window3.resizable(width=False, height=False)  # 必須
    window3.geometry('800x600')  # 必須
    tabControl = ttk.Notebook(window3)
    
    # 標籤
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tabControl.add(tab1, text="收到的履歷")
    tabControl.add(tab2, text="提供職缺")
    tabControl.add(tab3, text="公司資訊")
    tabControl.pack(expand=1 , fill="both")
    
    # 選履歷囉
    global selected_resume
    global selected_reply
    global job 
    
    def select_resume(selected):
        global selected_resume
        global selected_reply
        print(list_resume.get(list_resume.curselection()[0])[0][0])
        selected_reply = job_db['Replies'].find_one(ID=list_resume.get(list_resume.curselection()[0])[0][0])
        selected_resume = db['Employees'].find_one(ID=selected_reply['RecipientID'])
    
    def view_detail():
        detail_window = tk.Toplevel(window3)
        resume = ScrolledText(detail_window)
        resume.insert(END, selected_resume['About'])
        detail_window.title("求職者的自介")
        # detail_window.resizable(width=False, height=False)
        detail_window.geometry('500x500')
        frame_buttons = Frame(detail_window)
        yes_button = Button(frame_buttons, text="來應徵吧", command=lambda: yes())
        no_button = Button(frame_buttons, text="謝謝再聯絡", command=lambda: no())
        resume.pack(pady=5, padx=5, fill=BOTH, expand=1)
        yes_button.pack(side=LEFT, pady=5, padx=5)
        no_button.pack(side=LEFT, pady=5, padx=5)
        frame_buttons.pack()
        
        def yes():
            print(str(selected_resume['ID']))
            print(str(selected_reply['JobID']))
            job_db.query('UPDATE Replies SET Stat = 1 WHERE RecipientID=' + str(selected_resume['ID']) + ' AND JobID =' + str(selected_reply['JobID']) + ';')
            #job_db.query('UPDATE Jobs SET Vacancy = Vacancy - 1 WHERE ID=' + str(selected_resume['ID']) + ' AND ID =' + str(selected_reply['JobID']) + ';')
            messagebox.showinfo("資訊", "已發出面試通知")
            detail_window.destroy()
        
        def no():
            job_db.query('UPDATE Replies SET Stat = 2 WHERE RecipientID=' + str(selected_resume['ID']) + ' AND JobID =' + str(selected_reply['JobID']) + ';')  
            messagebox.showinfo("資訊", "已發出拒絕訊息")
            detail_window.destroy()
              
    # 履歷列
    list_resume = treectrl.MultiListbox(tab1)
    list_resume.pack(expand=1, fill="both")
    list_resume.focus_set()
    list_resume.configure(selectcmd=select_resume, selectmode='extended')
    list_resume.config(columns=("ID", "姓名", "性別", "電話", "地址", "教育程度", "應徵職位"))
    
    for reply in job_db['Replies']:
            global job
            job = job_db['Jobs'].find_one(ID=reply['JobID'])
            if job['CompanyID'] == current_user['ID'] and reply['Stat'] == 0:
                recipient = db['Employees'].find_one(ID=reply['RecipientID'])
                list_resume.insert(END, reply['ID'], recipient['Name'], recipient['Gender'], recipient['Phone'], recipient['Address'], recipient['Education'], job['Name'])
    

    apply_button = Button(tab1, text="查看自介", command=lambda:view_detail())
    apply_button.pack(pady=5)
    if list_resume.size()==0:
        apply_button.config(state=DISABLED)
        
    # 公司資料排版
    Grid.columnconfigure(tab2 , 1 , weight=1)
    
    # 工作名稱
    workName_prompt = Label(tab2 , text="工作名稱").grid(row=1, column=0, sticky=N + W)
    workName = Entry(tab2)
    workName.grid(row=1 , column=1 , sticky=E + W)
    # workName.insert(0, job_db['Name'])
    # 薪水
    salary = Label(tab2 , text="薪水").grid(row=2, column=0, sticky=N + W)
    salary = Entry(tab2)
    salary.grid(row=2 , column=1 , sticky=E + W)
    # salary.insert(0, job_db['Salary'])
    # 職缺
    vacancy = Label(tab2 , text="缺額").grid(row=3, column=0, sticky=N + W)
    vacancy = Entry(tab2)
    vacancy.grid(row=3 , column=1 , sticky=E + W)
    # vacancy.insert(0, job_db['Vacancy'])
    # 條件要求
    require_prompt = Label(tab2 , text="條件要求").grid(row=4, column=0, sticky=N + W)
    require = ScrolledText(tab2)
    require.grid(row=4 , column=1 , sticky=N + S + E + W)
    Grid.rowconfigure(tab2, 4, weight=1)
    # require.insert(0, job_db['require'])
    # 公司福利
    welfare = Label(tab2 , text="公司福利").grid(row=5, column=0, sticky=N + W)
    welfare = ScrolledText(tab2)
    welfare.grid(row=5 , column=1 , sticky=N + S + E + W)
    Grid.rowconfigure(tab2, 5, weight=1)
    # welfare.insert(0, job_db['welfare'])
    # 聯絡人
    contact = Label(tab2 , text="聯絡人").grid(row=6, column=0, sticky=N + W)
    contact = ScrolledText(tab2)
    contact.grid(row=6 , column=1 , sticky=N + S + E + W)
    Grid.rowconfigure(tab2, 6, weight=1)
    # contact.insert(0, job_db['Contact'])
    
    # 提供職缺
    def job_update():
        job_db['Jobs'].insert(dict(Name=workName.get(), Vacancy=vacancy.get(), Salary=salary.get(), Contact=contact.get('1.0', END)
                          , Company=companyName.get(), CompanyID=current_user['ID'], Requirement=require.get('1.0', END), Welfare=welfare.get('1.0', END)))
        
    # 更新按鈕
    post_button_frame = Frame(tab2)
    post_button = Button(post_button_frame, text="張貼職缺", command=job_update)
    post_button.pack(pady=5)
    post_button_frame.grid(row=7, column=0, columnspan=2)
    
    # 公司資訊編輯
    # 功能 : 更新資訊(可以改變sql)
    def company_update():
        db.query('UPDATE Employer SET companyName = "' + companyName.get() + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employer SET companyIntro = "' + intro_entry.get('1.0', END) + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employer SET companyDes = "' + rules_entry.get('1.0', END) + '" WHERE ID=' + str(user_id) + ';')
        
    # 公司資料排版
    Grid.columnconfigure(tab3 , 1 , weight=1)
    # 公司名稱
    companyName_prompt = Label(tab3 , text="公司名稱").grid(row=0, column=0, sticky=N + W)
    companyName = Entry(tab3)
    companyName.grid(row=0 , column=1 , sticky=E + W)
    companyName.insert(0, current_user['companyName'])
    
    # 公司介紹
    intro_prompt = Label(tab3, text="公司介紹").grid(row=1, column=0, sticky=N + W)
    intro_entry = ScrolledText(tab3)
    intro_entry.grid(row=1, column=1, sticky=N + W + E + S)
    intro_entry.insert(END, current_user['companyIntro'])
    Grid.rowconfigure(tab3, 1, weight=1)
    
    # 更多空間
    rules_prompt = Label (tab3, text="公司制度").grid(row=2, column=0, sticky=N + W)
    rules_entry = ScrolledText(tab3)
    rules_entry.grid(row=2, column=1 , sticky=N + W + E + S)
    rules_entry.insert(END, current_user['companyDes'])
    Grid.rowconfigure(tab3, 2, weight=1)
    
    frame_button = Frame(tab3)
    save_button = Button(frame_button, text="更新內容", command=lambda:company_update())
    save_button.pack(pady=5)
    frame_button.grid(row=3, column=0, columnspan=2)
    
    
    # 迴圈實作window3
    window3.mainloop()
