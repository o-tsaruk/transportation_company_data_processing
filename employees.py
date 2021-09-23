import tkinter as tk
import sqlite3
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn
import datetime


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('employees.sql')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS employees (id integer primary key, surname text, name text, patronymic text,
               birthday text, phone text, email text, enrolment text,
               experience integer, position text)'''
        )
        self.conn.commit()

    def insert(self, columns):
        self.c.execute(
            '''INSERT INTO employees (surname, name, patronymic, birthday, phone, email,
            enrolment, experience, position) VALUES (?,?,?,?,?,?,?,?,?)''', (columns[0], columns[1],
            columns[2], columns[3], columns[4], columns[5], columns[6], columns[7], columns[8]))
        self.conn.commit()


class Employees(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.database = DB()

        self.icon = tk.PhotoImage(file="resources\\icon.png")
        self.iconphoto(False, self.icon)
        self.title("База даних співробітників")
        self.geometry("1000x552+450+200")
        self.resizable(False, False)

        self.toolbar = tk.Frame(self, bg='#C4FFF3', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="resources\\add_emp.gif")
        self.edit_img = tk.PhotoImage(file="resources\\edit_emp.gif")
        self.delete_img = tk.PhotoImage(file="resources\\delete_emp.gif")
        self.search_img = tk.PhotoImage(file="resources\\search.png")
        self.update_img = tk.PhotoImage(file="resources\\update.png")
        button_add = tk.Button(self.toolbar, text='Додати співробітника', command=self.open,
                               bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.add_img)
        button_add.pack(side=tk.LEFT)
        button_edit = tk.Button(self.toolbar, text='Редагувати запис', command=self.edit,
                               bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.edit_img)
        button_edit.pack(side=tk.LEFT)
        button_delete = tk.Button(self.toolbar, text='Видалити запис', command=self.delete_records,
                                bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.delete_img)
        button_delete.pack(side=tk.LEFT)
        button_update = tk.Button(self.toolbar, text='Оновити', command=self.view_records,
                                  bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.update_img)
        button_update.pack(side=tk.RIGHT)
        button_search = tk.Button(self.toolbar, text='Пошук', command=self.search,
                                  bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.search_img)
        button_search.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('ID', 'surname', 'name', 'patronymic',
                                              'birthday', 'phone', 'email', 'enrolment',
                                              'experience', 'position'),
                               height=20, show='headings')
        self.tree.column('ID', width=55, anchor=tk.CENTER)
        self.tree.column('surname', width=110, anchor=tk.CENTER)
        self.tree.column('name', width=110, anchor=tk.CENTER)
        self.tree.column('patronymic', width=110, anchor=tk.CENTER)
        self.tree.column('birthday', width=110, anchor=tk.CENTER)
        self.tree.column('phone', width=110, anchor=tk.CENTER)
        self.tree.column('email', width=110, anchor=tk.CENTER)
        self.tree.column('enrolment', width=110, anchor=tk.CENTER)
        self.tree.column('experience', width=60, anchor=tk.CENTER)
        self.tree.column('position', width=110, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('surname', text='Прізвище')
        self.tree.heading('name', text='Ім\'я')
        self.tree.heading('patronymic', text='По-батькові')
        self.tree.heading('birthday', text='Дата народження')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Пошта')
        self.tree.heading('enrolment', text='Дата прийняття')
        self.tree.heading('experience', text='Стаж')
        self.tree.heading('position', text='Посада')
        self.tree.pack()

        button_plt1 = tk.Button(self, text='Графік стажу', command=self.plot_exp, bd=0.5,
                                bg='white', height=2, compound=tk.TOP)
        button_plt1.pack(side=tk.LEFT)
        button_plt2 = tk.Button(self, text='Графік набору', command=self.plot_enr, bd=0.5,
                                bg='white', height=2, compound=tk.TOP)
        button_plt2.pack(side=tk.LEFT)
        self.view_records()
        self.focus_set()

    def add_records(self, columns):
        self.database.insert(columns)
        self.view_records()

    def edit_records(self, columns):
        self.database.c.execute(
                                '''UPDATE employees SET surname=?, name=?, patronymic=?, birthday=?, phone=?, email=?,
                                enrolment=?, experience=?, position=? WHERE id=?''',
                                (columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6],
                                columns[7], columns[8], self.tree.set(self.tree.selection()[0], '#1')))
        self.database.conn.commit()
        self.view_records()

    def delete_records(self):
        for item in self.tree.selection():
            self.database.c.execute('''DELETE FROM employees WHERE id=?''', (self.tree.set(item,'#1'),))
        self.database.conn.commit()
        self.view_records()

    def view_records(self):
        self.database.c.execute('''SELECT * FROM employees''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in self.database.c.fetchall()]

    def search_records(self, key):
        key = ('%' + key + '%',)
        self.database.c.execute('SELECT * FROM employees WHERE surname LIKE ?', key)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.database.c.fetchall()]

    def open(self):
        Add(self)

    def edit(self):
        Edit(self)

    def search(self):
        Search(self)

    def plot_exp(self):
        df = pd.read_sql('SELECT * FROM employees', self.database.conn)
        plt.figure(figsize=(9,5))
        plt.style.use('seaborn-whitegrid')
        sbn.set_style("white")
        sbn.boxplot(x='position', y='experience', data=df, notch=False)
        medians_dict = {grp[0]:grp[1]['experience'].median() for grp in df.groupby('position')}
        xticklabels = [x.get_text() for x in plt.gca().get_xticklabels()]
        test = df['position'].value_counts(sort=False)
        n = [None]*len(xticklabels)
        for el in range(len(xticklabels)):
            n[el] = test[xticklabels[el]]
        for (x, xticklabel), n in zip(enumerate(xticklabels), n):
            plt.text(x, medians_dict[xticklabel]*1.03, "#rec : "+str(n),
                     horizontalalignment='center', fontdict={'size':9}, color='white')
        plt.gca().set_title('Розподіл груп робітників відносно стажу роботи', fontdict={'size':15})
        plt.gca().set_ylabel('Стаж')
        plt.gca().set_xlabel('Посада')
        plt.show()

    def plot_enr(self):
        now = datetime.datetime.now()
        year = []
        for m in range(now.month,13,1):
            year.append(str(m)+'.'+str(now.year-1))
        for m in range(1,now.month+1,1):
            year.append(str(m)+'.'+str(now.year))
        enr = [0]*len(year)
        df = pd.read_sql("SELECT enrolment FROM employees WHERE position='Водій'", self.database.conn)
        for el in df['enrolment']:
            for date in year:
                if date in el:
                    enr[year.index(date)] += 1

        fig, ax = plt.subplots(figsize=(10.5,5), dpi= 80)
        ax.vlines(x=year, ymin=0, ymax=enr, color='firebrick', alpha=0.7, linewidth=2)
        ax.scatter(x=year, y=enr, s=75, color='firebrick', alpha=1)
        ax.set_title('Кількість прийнятих водіїв', fontdict={'size':13})
        ax.set_yticks([x for x in range(0,max(enr)+1, 1)])
        ax.set_ylim(0, max(enr)+1, 1)
        plt.show()


class Add(tk.Toplevel):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.init()

    def init(self):
        #self.iconphoto(False, self.view.icon)
        self.title("Додати співробітника")
        self.geometry("400x500+600+300")
        self.resizable(False, False)
        self.configure(bg='#FFFFFF')
        self.icon = tk.Label(self, image=self.view.add_img)
        self.icon.place(x=280,y=20)

        style = ttk.Style()
        style.configure('label.TLabel', background="#FFFFFF", font=('Helvetica', 9))
        label_surname = ttk.Label(self, text='Прізвище', style='label.TLabel')
        label_surname.place(x=20,y=80)
        label_name = ttk.Label(self, text='Ім\'я', style='label.TLabel')
        label_name.place(x=20,y=130)
        label_patronymic = ttk.Label(self, text='По-батькові', style='label.TLabel')
        label_patronymic.place(x=220,y=130)
        label_birthday = ttk.Label(self, text='Дата народження', style='label.TLabel')
        label_birthday.place(x=20,y=200)
        label_phone = ttk.Label(self, text='Телефон', style='label.TLabel')
        label_phone.place(x=20,y=250)
        label_email = ttk.Label(self, text='Пошта', style='label.TLabel')
        label_email.place(x=220,y=250)
        label_position = ttk.Label(self, text='Посада', style='label.TLabel')
        label_position.place(x=20,y=320)
        label_experience = ttk.Label(self, text='Стаж', style='label.TLabel')
        label_experience.place(x=220,y=320)
        label_enrolment = ttk.Label(self, text='Дата прийняття', style='label.TLabel')
        label_enrolment.place(x=20,y=380)

        self.surname = ttk.Entry(self)
        self.surname.place(x=20,y=100)
        self.name = ttk.Entry(self)
        self.name.place(x=20,y=150)
        self.patronymic = ttk.Entry(self)
        self.patronymic.place(x=220,y=150)
        self.birthday = ttk.Entry(self)
        self.birthday.place(x=20,y=220)
        self.phone = ttk.Entry(self)
        self.phone.place(x=20,y=270)
        self.email = ttk.Entry(self)
        self.email.place(x=220,y=270)
        self.pos_value = ['Водій', 'Механік', 'Вантажник', 'Диспетчер', 'Лікар', 'Охорона', 'Бухгалтер', 'Менеджер']
        self.position = ttk.Combobox(self, value=self.pos_value)
        self.position.current(0)
        self.position.place(x=20,y=340)
        self.experience = ttk.Entry(self)
        self.experience.place(x=220,y=340)
        self.enrolment = ttk.Entry(self)
        self.enrolment.place(x=20,y=400)

        close = ttk.Button(self, text='Закрити', command=self.destroy)
        close.place(x=300,y=460)
        self.confirm = ttk.Button(self, text='Підтвердити', command=self.destroy)
        self.confirm.place(x=200,y=460)
        self.confirm.bind('<Button-1>', lambda event: self.view.add_records([self.surname.get(), self.name.get(),
                                                                        self.patronymic.get(), self.birthday.get(),
                                                                        self.phone.get(), self.email.get(),
                                                                        self.enrolment.get(), self.experience.get(),
                                                                        self.position.get()]))
        self.grab_set()
        self.focus_set()


class Edit(Add):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.init_edit()
        self.init_data()

    def init_edit(self):
        #self.iconphoto(False, self.view.icon)
        self.title("Редагувати дані про співробітника")
        self.confirm.bind('<Button-1>', lambda event: self.view.edit_records([self.surname.get(), self.name.get(),
                                                                         self.patronymic.get(), self.birthday.get(),
                                                                         self.phone.get(), self.email.get(),
                                                                         self.enrolment.get(), self.experience.get(),
                                                                         self.position.get()]))

    def init_data(self):
        try:
            self.view.database.c.execute('''SELECT * FROM employees WHERE id=?''',
                                         (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        except IndexError:
            self.destroy()
        else:
            item = self.view.database.c.fetchone()
            self.surname.insert(0, item[1])
            self.name.insert(0, item[2])
            self.patronymic.insert(0, item[3])
            self.birthday.insert(0, item[4])
            self.phone.insert(0, item[5])
            self.email.insert(0, item[6])
            for v in range(len(self.pos_value)):
                if self.pos_value[v] == item[9]:
                    self.position.current(v)
            self.experience.insert(0, item[8])
            self.enrolment.insert(0, item[7])


class Search(tk.Toplevel):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.init_search()
        self.focus_set()

    def init_search(self):
        #self.iconphoto(False, self.view.icon)
        self.title('Пошук записів по прізвищу')
        self.geometry('330x60+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Введіть прізвище')
        label_search.place(x=15, y=10)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=15, y=30)
        self.close = ttk.Button(self, text='Закрити', command=self.destroy)
        self.close.place(x=235, y=30)
        self.confirm = ttk.Button(self, text='Пошук', command=self.destroy)
        self.confirm.place(x=155, y=30)
        self.confirm.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
