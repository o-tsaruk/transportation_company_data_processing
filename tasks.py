import tkinter as tk
import sqlite3
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sbn
import pandas as pd
import datetime
import warnings
import numpy
from docxtpl import DocxTemplate


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.sql')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS tasks (id integer primary key, status text, start_date text, end_date text,
               start_city text, end_city text, start_country text, end_country text, company text, type_cargo text, 
               cargo text, note text, truck text, time real, driver text, spending real, profit real)'''
        )
        self.conn.commit()

    def insert(self, columns):
        self.c.execute(
            '''INSERT INTO tasks (status, start_date, end_date, start_city, end_city, start_country, end_country,
            company, type_cargo, cargo, note, truck, time, driver, spending, profit) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (columns))
        self.conn.commit()


class Tasks(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.database = DB()

        self.icon = tk.PhotoImage(file="resources\\icon.png")
        self.iconphoto(False, self.icon)
        self.title("База даних вантажоперевезень")
        self.geometry("1200x569+380+250")
        self.resizable(False, False)

        self.toolbar = tk.Frame(self, bg='#C4FFF3', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="resources\\add_tasks.png")
        self.edit_img = tk.PhotoImage(file="resources\\edit_emp.gif")
        self.delete_img = tk.PhotoImage(file="resources\\delete_emp.gif")
        self.search_img = tk.PhotoImage(file="resources\\search.png")
        self.update_img = tk.PhotoImage(file="resources\\update.png")
        self.doc_img = tk.PhotoImage(file="resources\\doc.png")

        button_add = tk.Button(self.toolbar, text='Додати запис', command=self.open,
                               bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.add_img)
        button_add.pack(side=tk.LEFT)
        button_edit = tk.Button(self.toolbar, text='Редагувати запис', command=self.edit,
                                bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.edit_img)
        button_edit.pack(side=tk.LEFT)
        button_delete = tk.Button(self.toolbar, text='Видалити запис', command=self.delete_records,
                                  bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.delete_img)
        button_delete.pack(side=tk.LEFT)
        button_doc = tk.Button(self.toolbar, text='Файл .docx', command=self.create_doc,
                                  bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.doc_img)
        button_doc.pack(side=tk.RIGHT)
        button_update = tk.Button(self.toolbar, text='Оновити', command=self.view_records,
                                  bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.update_img)
        button_update.pack(side=tk.RIGHT)
        button_search = tk.Button(self.toolbar, text='Пошук', command=self.search,
                                  bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.search_img)
        button_search.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('id', 'status', 'start_date', 'end_date', 'start_city', 'end_city',
                                                'start_country', 'end_country', 'company', 'type_cargo', 'cargo',
                                                'note', 'truck', 'time', 'driver', 'spending', 'profit'),
                                 height=20, show='headings')
        self.tree.column('id', width=55, anchor=tk.CENTER)
        self.tree.column('status', width=110, anchor=tk.CENTER)
        self.tree.column('start_date', width=110, anchor=tk.CENTER)
        self.tree.column('end_date', width=110, anchor=tk.CENTER)
        self.tree.column('start_city', width=110, anchor=tk.CENTER)
        self.tree.column('end_city', width=110, anchor=tk.CENTER)
        self.tree.column('start_country', width=110, anchor=tk.CENTER)
        self.tree.column('end_country', width=110, anchor=tk.CENTER)
        self.tree.column('company', width=110, anchor=tk.CENTER)
        self.tree.column('type_cargo', width=110, anchor=tk.CENTER)
        self.tree.column('cargo', width=110, anchor=tk.CENTER)
        self.tree.column('note', width=110, anchor=tk.CENTER)
        self.tree.column('truck', width=110, anchor=tk.CENTER)
        self.tree.column('time', width=110, anchor=tk.CENTER)
        self.tree.column('driver', width=110, anchor=tk.CENTER)
        self.tree.column('spending', width=110, anchor=tk.CENTER)
        self.tree.column('profit', width=110, anchor=tk.CENTER)
        self.tree.heading('id', text='ID')
        self.tree.heading('status', text='Статус')
        self.tree.heading('start_date', text='Дата відправ.')
        self.tree.heading('end_date', text='Дата прибуття')
        self.tree.heading('start_city', text='Місто відправ.')
        self.tree.heading('end_city', text='Місто прибуття')
        self.tree.heading('start_country', text='Країна відправ.')
        self.tree.heading('end_country', text='Країна прибуття')
        self.tree.heading('company', text='Компанія')
        self.tree.heading('type_cargo', text='Тип вантажу')
        self.tree.heading('cargo', text='Вантаж')
        self.tree.heading('note', text='Примітка')
        self.tree.heading('truck', text='Транспорт')
        self.tree.heading('time', text='Час маршруту')
        self.tree.heading('driver', text='Водій')
        self.tree.heading('spending', text='Витрати')
        self.tree.heading('profit', text='Прибутки')
        self.tree.pack()
        self.scroll = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.scroll.pack(fill = tk.X)
        self.tree.configure(xscrollcommand=self.scroll.set)
        self.now = datetime.datetime.now()

        button_plt1 = tk.Button(self, text='Графік прибутків', command=self.plot_profit, bd=0.5, compound=tk.BOTTOM,
                                bg='white', height=2)
        button_plt1.pack(side=tk.LEFT)
        button_plt2 = tk.Button(self, text='Графік витрат', command=self.plot_spending, bd=0.5, compound=tk.BOTTOM,
                                bg='white', height=2)
        button_plt2.pack(side=tk.LEFT)
        button_plt3 = tk.Button(self, text='Гістограма компаній', command=self.plot_company, bd=0.5, compound=tk.BOTTOM,
                                bg='white', height=2)
        button_plt3.pack(side=tk.LEFT)
        button_plt4 = tk.Button(self, text='Карта міст', command=self.plot_city, bd=0.5, compound=tk.BOTTOM,
                                bg='white', height=2)
        button_plt4.pack(side=tk.LEFT)
        button_plt5 = tk.Button(self, text='Графік тривалості', command=self.plot_time, bd=0.5, compound=tk.BOTTOM,
                                bg='white', height=2)
        button_plt5.pack(side=tk.LEFT)
        button_plt6 = tk.Button(self, text='Гістограма вантажів', command=self.plot_cargo, bd=0.5, compound=tk.BOTTOM,
                                bg='white', height=2)
        button_plt6.pack(side=tk.LEFT)
        button_plt7 = tk.Button(self, text='Графік розподілення витрат', command=self.plot_spending_time,
                                bd=0.5, compound=tk.BOTTOM, bg='white', height=2)
        button_plt7.pack(side=tk.LEFT)
        button_plt8 = tk.Button(self, text='Діаграма накопичення прибутків', command=self.plot_stack,
                                bd=0.5, compound=tk.BOTTOM, bg='white', height=2)
        button_plt8.pack(side=tk.LEFT)

        self.view_records()
        self.focus_set()

    def add_records(self, columns):
        self.database.insert(columns)
        self.view_records()

    def edit_records(self, columns):
        self.database.c.execute(
            '''UPDATE tasks SET status=?, start_date=?, end_date=?, start_city=?, end_city=?, start_country=?,
            end_country=?, company=?, type_cargo=?, cargo=?, note=?, truck=?, time=?, driver=?, spending=?, profit=? 
            WHERE id=?''', (columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6],
                            columns[7], columns[8], columns[9], columns[10], columns[11], columns[12], columns[13],
                            columns[14], columns[15], self.tree.set(self.tree.selection()[0], '#1')))
        self.database.conn.commit()
        self.view_records()

    def delete_records(self):
        for item in self.tree.selection():
            self.database.c.execute('''DELETE FROM tasks WHERE id=?''', (self.tree.set(item,'#1'),))
        self.database.conn.commit()
        self.view_records()

    def view_records(self):
        self.database.c.execute('''SELECT * FROM tasks''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in self.database.c.fetchall()]

    def search_records(self, key):
        key = ('%' + key + '%',)
        self.database.c.execute('SELECT * FROM tasks WHERE end_date LIKE ?', key)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.database.c.fetchall()]

    def open(self):
        Add(self)

    def edit(self):
        Edit(self)

    def search(self):
        Search(self)

    def create_doc(self):
        Docx(self)

    def plot_profit(self):
        now_time = '%' + str(self.now.month) + '.' + str(self.now.year)
        sql='SELECT end_date, profit FROM tasks WHERE end_date LIKE ?'
        args=[now_time]
        df = pd.DataFrame(self.database.c.execute(sql,args))
        date_list = df[0]
        profit_list = df[1]
        first_day = min([int(x[:2]) for x in date_list])
        last_day = max([int(x[:2]) for x in date_list])
        days = [x for x in range(first_day,last_day+1)]
        money = [0]*len(days)

        for day in days:
            for date,i in zip(date_list,range(len(date_list))):
                if day == int(date[:2]):
                    money[days.index(day)-1] += profit_list[i]

        plt.figure(figsize=(8.5,3))
        plt.plot(days,money,color='tab:red')
        xtick_labels = [str(x) for x in range(first_day,last_day+1)]
        plt.xticks(ticks=range(first_day,last_day+1), labels=xtick_labels, rotation=0, fontsize=9,
                   horizontalalignment='center', alpha=.7)
        plt.title("Прибутки за місяць ("+str(self.now.month)+'.'+str(self.now.year)+')', fontsize=13)
        plt.grid(axis='both', alpha=.3)
        plt.gca().spines["top"].set_alpha(0.0)
        plt.gca().spines["bottom"].set_alpha(0.3)
        plt.gca().spines["right"].set_alpha(0.0)
        plt.gca().spines["left"].set_alpha(0.3)
        plt.show()

    def plot_spending(self):
        now_time = '%' + str(self.now.month) + '.' + str(self.now.year)
        sql='SELECT end_date, spending FROM tasks WHERE end_date LIKE ?'
        args=[now_time]
        df = pd.DataFrame(self.database.c.execute(sql,args))
        date_list = df[0]
        spending_list = df[1]
        first_day = min([int(x[:2]) for x in date_list])
        last_day = max([int(x[:2]) for x in date_list])
        days = [x for x in range(first_day,last_day+1)]
        money = [0]*len(days)
        for day in days:
            for date,i in zip(date_list,range(len(date_list))):
                if day == int(date[:2]):
                    money[days.index(day)-1] += spending_list[i]

        plt.figure(figsize=(8.5,3))
        plt.plot(days,money,color='tab:blue')
        xtick_labels = [str(x) for x in range(first_day,last_day+1)]
        plt.xticks(ticks=range(first_day,last_day+1), labels=xtick_labels, rotation=0, fontsize=9,
                   horizontalalignment='center', alpha=.7)
        plt.title("Витрати за місяць ("+str(self.now.month)+'.'+str(self.now.year)+')', fontsize=13)
        plt.grid(axis='both', alpha=.3)
        plt.gca().spines["top"].set_alpha(0.0)
        plt.gca().spines["bottom"].set_alpha(0.3)
        plt.gca().spines["right"].set_alpha(0.0)
        plt.gca().spines["left"].set_alpha(0.3)
        plt.show()

    def plot_stack(self):
        now_time = '%' + str(self.now.month) + '.' + str(self.now.year)
        args = [now_time]

        sql = "SELECT end_date, profit FROM tasks WHERE start_country LIKE 'Україна' " \
              "AND end_country LIKE 'Україна' AND end_date LIKE ?"
        df = pd.DataFrame(self.database.c.execute(sql, args))
        date_list_ua = df[0]
        spending_list_ua = df[1]

        sql = "SELECT end_date, profit FROM tasks WHERE NOT start_country LIKE 'Україна' " \
              "AND end_country LIKE 'Україна' AND end_date LIKE ?"
        df = pd.DataFrame(self.database.c.execute(sql, args))
        date_list_imp = df[0]
        spending_list_imp = df[1]

        sql = "SELECT end_date, profit FROM tasks WHERE NOT end_country LIKE 'Україна' AND end_date LIKE ?"
        df = pd.DataFrame(self.database.c.execute(sql, args))
        date_list_exp = df[0]
        spending_list_exp = df[1]

        days = [x for x in range(32)]
        money_ua = [0] * len(days)
        money_imp = [0] * len(days)
        money_exp = [0] * len(days)

        for date, i in zip(date_list_ua, range(len(date_list_ua))):
            for day in days:
                if day == int(date[:2]):
                    money_ua[days.index(day)-1] += spending_list_ua[i]

        for date, i in zip(date_list_imp, range(len(date_list_imp))):
            for day in days:
                if day == int(date[:2]):
                    money_imp[days.index(day)-1] += spending_list_imp[i]

        for date, i in zip(date_list_exp, range(len(date_list_exp))):
            for day in days:
                if day == int(date[:2]):
                    money_exp[days.index(day)-1] += spending_list_exp[i]

        colors = ['tab:purple', 'tab:blue', 'tab:cyan']
        y = numpy.vstack([money_ua, money_imp, money_exp])
        fig, ax = plt.subplots(1, 1, figsize=(11, 6.5), dpi=80)
        ax = plt.gca()
        ax.stackplot(days, y/1000, labels=['в Україні','імпорт','експорт'], colors=colors, alpha=0.8)
        ax.set_title('Вклад імпорту та експорту в загальний прибуток', fontsize=16)
        plt.xticks(range(0,32,1))
        plt.ylabel('Тисяч гривень', fontsize=12)
        ax.legend(fontsize=13)
        plt.gca().spines["top"].set_alpha(0)
        plt.gca().spines["bottom"].set_alpha(.3)
        plt.gca().spines["right"].set_alpha(0)
        plt.gca().spines["left"].set_alpha(.3)
        plt.show()

    def plot_company(self):
        warnings.filterwarnings(action='ignore', category=UserWarning)
        df_raw = pd.read_sql('SELECT company FROM tasks', self.database.conn)
        df = df_raw.groupby('company').size().reset_index(name='counts')
        plt.figure(figsize=(10, 8), dpi=80)
        plt.bar(df['company'], df['counts'], color='blue', width=.5)
        for i, val in enumerate(df['counts'].values):
            plt.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom',
                     fontdict={'fontweight': 500, 'size': 14})
        plt.gca().set_xticklabels(df['company'], rotation=25, horizontalalignment='center', fontsize=10)
        plt.yticks([])
        plt.title("Кількість виконаних замовлень компаній", fontsize=15)
        plt.gca().spines["top"].set_alpha(0.0)
        plt.gca().spines["right"].set_alpha(0.0)
        plt.gca().spines["left"].set_alpha(0.0)
        plt.show()

    def plot_city(self):
        df_raw = pd.read_sql('SELECT end_city FROM tasks', self.database.conn)
        df = df_raw.groupby('end_city').size().reset_index(name='counts')
        city_list = ['Брест','Брно','Будапешт','Білосток','Варшава','Вроцлав','Кишинів','Київ','Кривий Ріг','Львів',
                     'Мінськ','Одеса','Чернівці']
        city_x = [489,32,189,456,317,63,824,929,1114,512,741,945,634]
        city_y = [601,297,134,703,607,490,99,426,174,361,788,39,208]

        count_list = [0]*len(city_list)
        for city in city_list:
            for i,row in df.iterrows():
                if row['end_city'] == city:
                    count_list[city_list.index(city)] = row['counts']

        img = plt.imread("resources\\map.png")
        plt.figure(figsize=(16, 14))
        plt.imshow(img, extent=[0, 1337, 0, 818])
        plt.scatter(city_x, city_y, s=230, alpha=.9, color='white', edgecolors='black')
        for x, y, tex in zip(city_x, city_y, count_list):
            t = plt.text(x, y, round(tex,1), horizontalalignment='center',
                         verticalalignment='center', fontdict={'color': 'black'})
        plt.xticks([])
        plt.yticks([])
        plt.title('Кількість перевезень в міста', fontsize=14)
        plt.show()

    def plot_time(self):
        current = str(self.now.month) + '.' + str(self.now.year)
        if self.now.month != 1:
            previous = str(self.now.month-1) + '.' + str(self.now.year)
        else:
            previous = '12' + '.' + str(self.now.year)
        df = pd.read_sql('SELECT * FROM tasks', self.database.conn)

        plt.figure(figsize=(6,5))
        sbn.kdeplot(df.loc[df['end_date'].str.contains(previous), 'time'], shade=True, color="blue",
                    label="Минулий місяць", alpha=.7)
        sbn.kdeplot(df.loc[df['end_date'].str.contains(current), 'time'], shade=True, color="orange",
                    label="Поточний місяць", alpha=.8)
        plt.title('Розподіл тривалостей перевезень', fontsize=14)
        plt.ylabel('')
        plt.xlabel('Час')
        plt.legend()
        plt.show()

    def plot_cargo(self):
        df_raw = pd.read_sql('SELECT type_cargo FROM tasks', self.database.conn)
        df = df_raw.groupby('type_cargo').size().reset_index(name='counts')
        df.sort_values('counts', inplace=True)
        df.reset_index(inplace=True)
        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor='white', dpi=80)
        ax.vlines(x=df.type_cargo, ymin=0, ymax=df.counts, color='firebrick', alpha=0.7, linewidth=30)

        for i, counts in enumerate(df.counts):
            ax.text(i, counts + 0.3, counts, horizontalalignment='center', fontsize=11)
        ax.set_title('Кількість перевезених вантажів різних типів', fontdict={'size': 16})
        ax.set(ylim=[0,max(df['counts']+1)])
        plt.yticks([])
        plt.gca().spines["top"].set_alpha(0.0)
        plt.gca().spines["right"].set_alpha(0.0)
        plt.gca().spines["left"].set_alpha(0.0)
        plt.show()

    def plot_spending_time(self):
        df = pd.read_sql('SELECT * FROM tasks', self.database.conn)
        fig = plt.figure(figsize=(10, 6))
        grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)

        ax_main = fig.add_subplot(grid[:-1, :-1])
        ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
        ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])

        # Scatterplot on main ax
        ax_main.scatter('spending', 'time', s=25, c='orange', alpha=.9,
                        data=df, cmap="tab10", edgecolors='black', linewidths=.5)

        # histogram on the right
        ax_bottom.hist(df.spending, 40, histtype='stepfilled', orientation='vertical', color='blue')
        ax_bottom.invert_yaxis()

        # histogram in the bottom
        ax_right.hist(df.time, 40, histtype='stepfilled', orientation='horizontal', color='blue')

        ax_main.set(title='Відношення витрат до часу перевезення', xlabel='Витрати', ylabel='Години')
        ax_main.title.set_fontsize(14)
        for item in (
                [ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
            item.set_fontsize(10)

        xlabels = ax_main.get_xticks().tolist()
        warnings.filterwarnings(action='ignore', category=UserWarning)
        ax_main.set_xticklabels(xlabels)
        plt.show()


class Add(tk.Toplevel):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.init()

    def init(self):
        #self.iconphoto(False, self.view.icon)
        self.title("Додати запис")
        self.geometry("400x700+600+170")
        self.resizable(False, False)
        self.configure(bg='#FFFFFF')
        self.icon = tk.Label(self, image=self.view.add_img)
        self.icon.place(x=290, y=20)

        style = ttk.Style()
        style.configure('label.TLabel', background="#FFFFFF", font=('Helvetica', 9))
        label_status = ttk.Label(self, text='Статус', style='label.TLabel')
        label_status.place(x=20,y=100)
        label_start_date = ttk.Label(self, text='Дата відправ.', style='label.TLabel')
        label_start_date.place(x=20,y=150)
        label_end_date = ttk.Label(self, text='Дата прибуття', style='label.TLabel')
        label_end_date.place(x=220,y=150)
        label_start_city = ttk.Label(self, text='Місто відправ.', style='label.TLabel')
        label_start_city.place(x=20,y=200)
        label_end_city = ttk.Label(self, text='Місто прибуття', style='label.TLabel')
        label_end_city.place(x=220,y=200)
        label_start_country = ttk.Label(self, text='Країна відправ.', style='label.TLabel')
        label_start_country.place(x=20,y=250)
        label_end_country = ttk.Label(self, text='Країна прибуття', style='label.TLabel')
        label_end_country.place(x=220,y=250)
        label_type_cargo = ttk.Label(self, text='Тип вантажу', style='label.TLabel')
        label_type_cargo.place(x=20,y=300)
        label_cargo = ttk.Label(self, text='Вантаж', style='label.TLabel')
        label_cargo.place(x=220,y=300)
        label_note = ttk.Label(self, text='Примітка', style='label.TLabel')
        label_note.place(x=20,y=350)
        label_truck = ttk.Label(self, text='Транспорт', style='label.TLabel')
        label_truck.place(x=20,y=400)
        label_time = ttk.Label(self, text='Час маршруту', style='label.TLabel')
        label_time.place(x=20,y=450)
        label_driver = ttk.Label(self, text='Водій', style='label.TLabel')
        label_driver.place(x=20,y=500)
        label_company = ttk.Label(self, text='Компанія', style='label.TLabel')
        label_company.place(x=20, y=550)
        label_spending = ttk.Label(self, text='Витрати', style='label.TLabel')
        label_spending.place(x=20,y=600)
        label_profit = ttk.Label(self, text='Прибутки', style='label.TLabel')
        label_profit.place(x=220,y=600)

        self.status_value = ['В процесі','Виконаний','Скасований']
        self.status = ttk.Combobox(self, value=self.status_value)
        self.status.current(0)
        self.status.place(x=20,y=120)
        self.start_date = ttk.Entry(self)
        self.start_date.place(x=20,y=170)
        self.end_date = ttk.Entry(self)
        self.end_date.place(x=220,y=170)
        self.start_city = ttk.Entry(self)
        self.start_city.place(x=20,y=220)
        self.end_city = ttk.Entry(self)
        self.end_city.place(x=220,y=220)
        self.start_country = ttk.Entry(self)
        self.start_country.place(x=20,y=270)
        self.end_country = ttk.Entry(self)
        self.end_country.place(x=220,y=270)
        self.cargo_value = ['Насипний', 'Порошкоподібний', 'Наливний', 'Газоподібний', 'Штучний',
                            'Швидкопсувний', 'Негабаритний']
        self.type_cargo = ttk.Combobox(self, value=self.cargo_value)
        self.type_cargo.current(0)
        self.type_cargo.place(x=20,y=320)
        self.cargo = ttk.Entry(self)
        self.cargo.place(x=220,y=320)
        self.note_value = ['', 'Вибухонебезпечний', 'Вогненебезпечна рідина', 'Вогненебезпечна речовина',
                           'Окисляюча речовина', 'Токсичний', 'Радіоактивний', 'Корозійна речовина',
                           'Небезпечний (інше)', 'Високоцінний груз', 'Довгомірний', 'Надважкий',
                           '(написати свій варіант)']
        self.note = ttk.Combobox(self, value=self.note_value)
        self.note.current(0)
        self.note.place(x=20,y=370)
        self.truck = ttk.Entry(self)
        self.truck.place(x=20,y=420)
        self.time = ttk.Entry(self)
        self.time.place(x=20,y=470)
        self.driver = ttk.Entry(self)
        self.driver.place(x=20,y=520)
        self.company = ttk.Entry(self)
        self.company.place(x=20,y=570)
        self.spending = ttk.Entry(self)
        self.spending.place(x=20,y=620)
        self.profit = ttk.Entry(self)
        self.profit.place(x=220,y=620)

        self.close = ttk.Button(self, text='Закрити', command=self.destroy)
        self.close.place(x=300,y=670)
        self.confirm = ttk.Button(self, text='Підтвердити', command=self.destroy)
        self.confirm.place(x=200,y=670)
        self.confirm.bind('<Button-1>', lambda event: self.view.add_records([self.status.get(), self.start_date.get(),
                                                                        self.end_date.get(), self.start_city.get(),
                                                                        self.end_city.get(), self.start_country.get(),
                                                                        self.end_country.get(), self.company.get(),
                                                                        self.type_cargo.get(), self.cargo.get(),
                                                                        self.note.get(), self.truck.get(),
                                                                        self.time.get(), self.driver.get(),
                                                                        self.spending.get(), self.profit.get()]))
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
        self.title("Редагувати дані про завдання")
        self.confirm.bind('<Button-1>', lambda event: self.view.edit_records([self.status.get(), self.start_date.get(),
                                                                        self.end_date.get(), self.start_city.get(),
                                                                        self.end_city.get(), self.start_country.get(),
                                                                        self.end_country.get(), self.company.get(),
                                                                        self.type_cargo.get(), self.cargo.get(),
                                                                        self.note.get(), self.truck.get(),
                                                                        self.time.get(), self.driver.get(),
                                                                        self.spending.get(), self.profit.get()]))

    def init_data(self):
        try:
            self.view.database.c.execute('''SELECT * FROM tasks WHERE id=?''',
                                         (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        except IndexError:
            self.destroy()
        else:
            item = self.view.database.c.fetchone()
            for v in range(len(self.status_value)):
                if self.status_value[v] == item[1]:
                    self.status.current(v)
            self.start_date.insert(0, item[2])
            self.end_date.insert(0, item[3])
            self.start_city.insert(0, item[4])
            self.end_city.insert(0, item[5])
            self.start_country.insert(0, item[6])
            self.end_country.insert(0, item[7])
            self.company.insert(0, item[8])
            for v in range(len(self.cargo_value)):
                if self.cargo_value[v] == item[9]:
                    self.type_cargo.current(v)
            self.cargo.insert(0, item[10])
            for v in range(len(self.note_value)):
                if self.note_value[v] == item[11]:
                    self.note.current(v)
            self.truck.insert(0, item[12])
            self.time.insert(0, item[13])
            self.driver.insert(0, item[14])
            self.spending.insert(0, item[15])
            self.profit.insert(0, item[16])


class Search(tk.Toplevel):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.init_search()
        self.focus_set()

    def init_search(self):
        #self.iconphoto(False, self.view.icon)
        self.title('Пошук записів по даті')
        self.geometry('330x60+400+300')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Введіть кінцеву дату')
        label_search.place(x=15, y=10)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=15, y=30)
        self.close = ttk.Button(self, text='Закрити', command=self.destroy)
        self.close.place(x=235, y=30)
        self.confirm = ttk.Button(self, text='Пошук', command=self.destroy)
        self.confirm.place(x=155, y=30)
        self.confirm.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))


class Docx(tk.Toplevel):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.init_docx()
        self.focus_set()

    def init_docx(self):
        self.title('Заповніть додаткові дані')
        self.geometry('420x360+400+300')
        self.resizable(False, False)
        self.configure(bg='#FFFFFF')
        self.icon = tk.Label(self, image=self.view.doc_img)
        self.icon.place(x=290, y=20)

        style = ttk.Style()
        style.configure('label.TLabel', background="#FFFFFF", font=('Helvetica', 9))
        label_meh = ttk.Label(self, text='Ім\'я механіка', style='label.TLabel')
        label_meh.place(x=20, y=100)
        label_num = ttk.Label(self, text='Номер причепу', style='label.TLabel')
        label_num.place(x=20, y=150)
        label_weight = ttk.Label(self, text='Вага вантажу, т', style='label.TLabel')
        label_weight.place(x=220, y=150)
        label_dist = ttk.Label(self, text='Пройдена відстань, км', style='label.TLabel')
        label_dist.place(x=20, y=200)
        label_fuel = ttk.Label(self, text='Кількість придбано пального, л', style='label.TLabel')
        label_fuel.place(x=220, y=200)
        label_down = ttk.Label(self, text='Час простою', style='label.TLabel')
        label_down.place(x=20, y=250)
        label_cause = ttk.Label(self, text='Причина простою', style='label.TLabel')
        label_cause.place(x=220, y=250)

        self.meh = ttk.Entry(self)
        self.meh.place(x=20, y=120)
        self.num = ttk.Entry(self)
        self.num.place(x=20, y=170)
        self.weight = ttk.Entry(self)
        self.weight.place(x=220, y=170)
        self.dist = ttk.Entry(self)
        self.dist.place(x=20, y=220)
        self.fuel = ttk.Entry(self)
        self.fuel.place(x=220, y=220)
        self.down = ttk.Entry(self)
        self.down.place(x=20, y=270)
        self.cause = ttk.Entry(self)
        self.cause.place(x=220, y=270)

        self.close = ttk.Button(self, text='Закрити', command=self.destroy)
        self.close.place(x=300, y=300)
        self.confirm = ttk.Button(self, text='Підтвердити', command=self.init_data)
        self.confirm.place(x=200, y=300)

    def init_data(self):
        try:
            self.view.database.c.execute('''SELECT * FROM tasks WHERE id=?''',
                                         (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        except IndexError:
            item = ['']*17
        else:
            item = self.view.database.c.fetchone()

        doc = DocxTemplate("resources\\перевезення.docx")
        context = {'id' : item[0], 'status' : item[1], 'start_date' : item[2], 'end_date' : item[3],
                   'start_city' : item[4], 'end_city' : item[5], 'start_country' : item[6],
                   'end_country' : item[7], 'company' : item[8], 'type_cargo' : item[9],
                   'cargo' : item[10], 'note' : item[11], 'truck' : item[12], 'time' : item[13],
                   'driver' : item[14], 'spending' : item[15], 'profit' : item[16], 'meh' : self.meh.get(),
                   'num' : self.num.get(), 'weight' : self.weight.get(), 'dist' : self.dist.get(),
                   'fuel' : self.fuel.get(), 'down' : self.down.get(), 'cause' : self.cause.get()}
        doc.render(context)
        doc.save("resources\\перевезення " + str(item[0]) + ".docx")
