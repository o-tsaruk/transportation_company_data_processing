import tkinter as tk
import sqlite3
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import cbook
import pandas as pd
from pywaffle import Waffle
import warnings
import squarify


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('trucks.sql')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS trucks (id integer primary key, number text, brand text, 
               model text, date text, color text, tgroup text)'''
        )
        self.conn.commit()

    def insert(self, columns):
        self.c.execute(
            '''INSERT INTO trucks (number, brand, model, date, color, tgroup) VALUES (?,?,?,?,?,?)''', (columns))
        self.conn.commit()


class Trucks(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.database = DB()

        self.icon = tk.PhotoImage(file="resources\\icon.png")
        self.iconphoto(False, self.icon)
        self.title("База даних транспортних засобів")
        self.geometry("705x492+500+250")
        self.resizable(False, False)

        self.toolbar = tk.Frame(self, bg='#C4FFF3', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="resources\\add_trucks.png")
        self.edit_img = tk.PhotoImage(file="resources\\edit_emp.gif")
        self.delete_img = tk.PhotoImage(file="resources\\delete_emp.gif")
        button_add = tk.Button(self.toolbar, text='Додати запис', command=self.open,
                               bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.add_img)
        button_add.pack(side=tk.LEFT)
        button_edit = tk.Button(self.toolbar, text='Редагувати запис', command=self.edit,
                                bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.edit_img)
        button_edit.pack(side=tk.LEFT)
        button_delete = tk.Button(self.toolbar, text='Видалити запис', command=self.delete_records,
                                  bg='#C4FFF3', bd=0, compound=tk.TOP, image=self.delete_img)
        button_delete.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('id', 'number', 'brand', 'model', 'date', 'color', 'group'),
                                 height=17, show='headings')
        self.tree.column('id', width=40, anchor=tk.CENTER)
        self.tree.column('number', width=110, anchor=tk.CENTER)
        self.tree.column('brand', width=110, anchor=tk.CENTER)
        self.tree.column('model', width=110, anchor=tk.CENTER)
        self.tree.column('date', width=110, anchor=tk.CENTER)
        self.tree.column('color', width=110, anchor=tk.CENTER)
        self.tree.column('group', width=110, anchor=tk.CENTER)
        self.tree.heading('id', text='ID')
        self.tree.heading('number', text='Держ. номер')
        self.tree.heading('brand', text='Марка')
        self.tree.heading('model', text='Модель')
        self.tree.heading('date', text='Дата випуску')
        self.tree.heading('color', text='Колір')
        self.tree.heading('group', text='Група')
        self.tree.pack()

        button_waffle = tk.Button(self, text='Композиція груп автопарку', command=self.plot_waf,
                                  bd=0.5, bg='white', height=2, compound=tk.BOTTOM)
        button_waffle.pack(side=tk.LEFT)
        button_treemap = tk.Button(self, text='Композиція автопарку фур', command=self.plot_map,
                                   bd=0.5, bg='white', height=2, compound=tk.BOTTOM)
        button_treemap.pack(side=tk.LEFT)
        self.view_records()
        self.focus_set()

    def add_records(self, columns):
        self.database.insert(columns)
        self.view_records()

    def edit_records(self, columns):
        self.database.c.execute(
            '''UPDATE trucks SET number=?, brand=?, model=?, date=?, color=?, tgroup=? WHERE id=?''',
            (columns[0], columns[1], columns[2], columns[3], columns[4], columns[5],
            self.tree.set(self.tree.selection()[0], '#1')))
        self.database.conn.commit()
        self.view_records()

    def delete_records(self):
        for item in self.tree.selection():
            self.database.c.execute('''DELETE FROM trucks WHERE id=?''', (self.tree.set(item,'#1'),))
        self.database.conn.commit()
        self.view_records()

    def view_records(self):
        self.database.c.execute('''SELECT * FROM trucks''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in self.database.c.fetchall()]

    def open(self):
        Add(self)

    def edit(self):
        Edit(self)

    def plot_waf(self):
        df_raw = pd.read_sql("SELECT * FROM trucks", self.database.conn)
        df = df_raw.groupby('tgroup').size().reset_index(name='counts')
        n_categories = df.shape[0]
        color = cm.get_cmap('inferno_r')
        colors = [color(i / float(n_categories)) for i in range(n_categories)]
        warnings.filterwarnings("ignore", category=cbook.mplDeprecation)
        fig = plt.figure(
            FigureClass=Waffle,
            plots={
                '111': {
                    'values': df['counts'],
                    'labels': ["{0} ({1})".format(n[0], n[1]) for n in df[['tgroup', 'counts']].itertuples()],
                    'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1), 'fontsize': 9},
                    'title': {'label': 'Композиція груп транспорту автопарку компанії', 'loc': 'center', 'fontsize': 12}
                },
            },
            rows=3,
            colors=colors,
            figsize=(7,2.5)
        )
        fig.show()

    def plot_map(self):
        df_raw = pd.read_sql("SELECT brand FROM trucks WHERE tgroup='Фура'", self.database.conn)
        df = df_raw.groupby('brand').size().reset_index(name='counts')
        labels = df.apply(lambda x: str(x[0]) + "\n (" + str(x[1]) + ")", axis=1)
        sizes = df['counts'].values.tolist()
        color = cm.get_cmap('Spectral')
        colors = [color(i / float(len(labels))) for i in range(len(labels))]
        plt.figure(figsize=(5,5))
        squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8)
        plt.title('Композиція брендів автопарку компанії (фури)')
        plt.axis('off')
        plt.show()


class Add(tk.Toplevel):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.init()

    def init(self):
        #self.iconphoto(False, self.view.icon)
        self.title("Додати транспортний засіб")
        self.geometry("400x450+600+300")
        self.resizable(False, False)
        self.configure(bg='#FFFFFF')
        self.icon = tk.Label(self, image=self.view.add_img)
        self.icon.place(x=300, y=20)

        style = ttk.Style()
        style.configure('label.TLabel', background="#FFFFFF", font=('Helvetica', 9))
        label_number = ttk.Label(self, text='Державний номер', style='label.TLabel')
        label_number.place(x=20,y=130)
        label_brand = ttk.Label(self, text='Марка', style='label.TLabel')
        label_brand.place(x=20,y=180)
        label_model = ttk.Label(self, text='Модель', style='label.TLabel')
        label_model.place(x=220,y=180)
        label_date = ttk.Label(self, text='Дата випуску', style='label.TLabel')
        label_date.place(x=20,y=250)
        label_color = ttk.Label(self, text='Колір', style='label.TLabel')
        label_color.place(x=20,y=300)
        label_tgroup = ttk.Label(self, text='Тип транспорту', style='label.TLabel')
        label_tgroup.place(x=220,y=300)

        self.number = ttk.Entry(self)
        self.number.place(x=20,y=150)
        self.brand = ttk.Entry(self)
        self.brand.place(x=20,y=200)
        self.model = ttk.Entry(self)
        self.model.place(x=220, y=200)
        self.date = ttk.Entry(self)
        self.date.place(x=20,y=270)
        self.color = ttk.Entry(self)
        self.color.place(x=20, y=320)
        self.group_value = ['Фура', 'Вантажівка', 'Фургон', 'Легковий авт.', 'Спецтехніка', 'Автобус']
        self.tgroup = ttk.Combobox(self, value=self.group_value)
        self.tgroup.current(0)
        self.tgroup.place(x=220, y=320)

        close = ttk.Button(self, text='Закрити', command=self.destroy)
        close.place(x=300,y=410)
        self.confirm = ttk.Button(self, text='Підтвердити', command=self.destroy)
        self.confirm.place(x=200,y=410)
        self.confirm.bind('<Button-1>', lambda event: self.view.add_records([self.number.get(), self.brand.get(),
                                                                             self.model.get(), self.date.get(),
                                                                             self.color.get(), self.tgroup.get()]))
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
        self.confirm.bind('<Button-1>', lambda event: self.view.edit_records([self.number.get(), self.brand.get(),
                                                                              self.model.get(), self.date.get(),
                                                                              self.color.get(), self.tgroup.get()]))

    def init_data(self):
        try:
            self.view.database.c.execute('''SELECT * FROM trucks WHERE id=?''',
                                         (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        except IndexError:
            self.destroy()
        else:
            item = self.view.database.c.fetchone()
            self.number.insert(0, item[1])
            self.brand.insert(0, item[2])
            self.model.insert(0, item[3])
            self.date.insert(0, item[4])
            self.color.insert(0, item[5])
            self.tgroup.insert(0, item[6])
            for v in range(len(self.group_value)):
                if self.group_value[v] == item[6]:
                    self.tgroup.current(v)
