#! python3.5
import tkinter as tk                   
from tkinter import ttk
from tkinter import messagebox
import TkTreectrl as treectrl
from tkinter.scrolledtext import ScrolledText
from tkinter import *
import dataset
import sys


def gui(id):
    db = dataset.connect('sqlite:///users.db')
    jobs_db = dataset.connect('sqlite:///jobs.db') 
    user_id = id
    
    def test():
        messagebox.showinfo("Info", "We're FUCKED.")
    
    window2 = tk.Tk()         
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
    
    global selected_job
    
    def select_cmd(selected):
        print ('Selected item ID:', int(list_jobs.get(list_jobs.curselection()[0])[0][0]))
        global selected_job
        selected_job = jobs_db['Jobs'].find_one(ID=list_jobs.get(list_jobs.curselection()[0])[0][0])
        print(selected_job['ID'])
    
    def show_detail(job):
        company = db['Employer'].find_one(ID=job['CompanyID'])
        window_details = tk.Toplevel(window2)
        window_details.title("職缺詳細資料")
        window_details.geometry('300x500')
        window_details.resizable(width=False, height=False)
        Grid.columnconfigure(window_details, 1, weight=1)
        
        label_company = Label(window_details, text="發布公司").grid(row=0, column=0)
        text_company = Entry(window_details)
        text_company.insert(END, company['companyName'])
        text_company.config(state='readonly')
        text_company.grid(row=0, column=1, sticky=N + E + W)
        
        label_title = Label(window_details, text="工作名稱").grid(row=1, column=0)
        text_title = Entry(window_details)
        text_title.insert(END, job['Name'])
        text_title.config(state='readonly')
        text_title.grid(row=1, column=1, sticky=N + E + W)
        
        label_content = Label(window_details, text="工作內容").grid(row=2, column=0, sticky=N)
        text_content = ScrolledText(window_details)
        text_content.insert(END, job['Content'])
        text_content.config(state='disabled')
        text_content.grid(row=2, column=1, sticky=N + S + E + W)
        Grid.rowconfigure(window_details, 2, weight=1)
        
        label_requirement = Label(window_details, text="工作要求").grid(row=3, column=0, sticky=N)
        text_requirement = ScrolledText(window_details)
        text_requirement.insert(END, job['Requirement'])
        text_requirement.config(state='disabled')
        text_requirement.grid(row=3, column=1, sticky=N + S + E + W)
        Grid.rowconfigure(window_details, 3, weight=1)
        
        label_requirement = Label(window_details, text="聯絡方式").grid(row=4, column=0, sticky=N)
        text_requirement = ScrolledText(window_details)
        text_requirement.insert(END, job['Contact'])
        text_requirement.config(state='disabled')
        text_requirement.grid(row=4, column=1, sticky=N + S + E + W)
        Grid.rowconfigure(window_details, 4, weight=1)
        
        frame_button = Frame(window_details)
        button_confirm = Button(frame_button, text="送出履歷", command=lambda:send_resume(job))
        button_confirm.pack(pady=5)
        frame_button.grid(row=5, column=0, columnspan=2)
        
        def send_resume(job):
            MsgBox = tk.messagebox.askquestion ('即將送出資料', '你確定要應徵這份工作嗎?', icon='warning')
            if MsgBox == 'yes':
                print(selected_job['ID'])
                print(current_user['ID'])
                jobs_db['Replies'].insert(dict(RecipientID=current_user['ID'], JobID=selected_job['ID'], Stat=0))
                window_details.destroy()
            else:
                window_details.destroy()
    
    # 職缺列表
    list_jobs = treectrl.MultiListbox(tab1)
    list_jobs.pack(expand=1, fill="both")
    list_jobs.focus_set()   
    list_jobs.configure(selectcmd=select_cmd, selectmode='extended')
    list_jobs.config(columns=('ID', '名稱', '發布公司', "待遇", "缺額", '聯絡資訊'))
    
    for job in jobs_db['Jobs']:
        # 因應python預設不支援多行文字 在時間不足以重寫UI下對多行文字進行格式化
        contact = job['Contact'].splitlines()
        contact_display = "/".join(contact)
        company = db['Employer'].find_one(ID=job['CompanyID'])
        list_jobs.insert(END, job['ID'], job['Name'], company['companyName'], job['Salary'], job['Vacancy'], contact_display)
        print(job['Contact'])
    
    button_apply = Button(tab1, text='應徵', command=lambda:show_detail(selected_job))
    button_apply.pack()
    
    # 求職狀態
    list_replies = treectrl.MultiListbox(tab2)
    list_replies.pack(expand=1, fill="both")
    list_replies.focus_set()
    list_replies.configure(columns=('職位', '公司', '結果'))
    for result in jobs_db['Replies']:
        job = jobs_db['Jobs'].find_one(ID=result['JobID'])
        company = db['Employer'].find_one(ID=job['CompanyID'])
        result_display = ""
        if result['Stat'] == 0:
            result_display = "企業尚未看過"
        elif result['Stat'] == 1:
            result_display = "請依約定日期前往面試"
        elif result['Stat'] == 2:
            result_display = "謝謝再聯絡"
        list_replies.insert(END, company['companyName'], job['Name'], result_display)
    
    # 按下更新按鈕後執行以下sql命令更新資料庫
    def update_info():
        db.query('UPDATE Employees SET Name = "' + name_entry.get() + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employees SET Age = "' + age_entry.get() + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employees SET Gender = "' + gender_entry.get() + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employees SET Phone = "' + phone_entry.get() + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employees SET Address = "' + address_entry.get() + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employees SET Education = "' + education_entry.get() + '" WHERE ID=' + str(user_id) + ';')
        db.query('UPDATE Employees SET About = "' + extra_entry.get(1.0, END) + '" WHERE ID=' + str(user_id) + ';')
    
    # 資料編輯頁面
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
    extra_entry = ScrolledText(tab3)
    extra_entry.grid(row=6, column=1, sticky=N + W + E + S)
    extra_entry.insert(INSERT, current_user['About'])
    save_button = Button(tab3, text="更新內容", command=update_info)
    save_button.grid(row=7, column=1)
    
    # 畫面出現
    
    window2.mainloop() 
                                 
