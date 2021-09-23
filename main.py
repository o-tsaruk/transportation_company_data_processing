import tkinter as tk
import employees as emp
import trucks
import tasks


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init()
        self.focus_set()

    def init(self):
        toolbar1 = tk.Frame(bg='#000000', bd=0)
        toolbar1.pack(side=tk.TOP, fill=tk.BOTH)
        toolbar2 = tk.Frame(bg='#FFFFFF', bd=0)
        toolbar2.pack(side=tk.BOTTOM, fill=tk.X)
        self.add_img = tk.PhotoImage(file="resources\\logo.png")
        icon = tk.Label(toolbar1, image=self.add_img, bd=0)
        icon.place(x=10,y=5)
        icon.pack()

        self.add_img1 = tk.PhotoImage(file="resources\\main_employees.png")
        self.add_img2 = tk.PhotoImage(file="resources\\main_trucks.png")
        self.add_img3 = tk.PhotoImage(file="resources\\main_tasks.png")

        button_add1 = tk.Button(toolbar2, text='Співробітники', command=self.open_add, bg='#FFFFFF',
                                width=160, bd=0, compound=tk.TOP, image=self.add_img1)
        button_add1.pack(side=tk.LEFT)
        button_add2 = tk.Button(toolbar2, text='Транспортні засоби', command=self.open_trucks, bg='#FFFFFF',
                                width=160, bd=0, compound=tk.TOP, image=self.add_img2)
        button_add2.pack(side=tk.LEFT)
        button_add3 = tk.Button(toolbar2, text='Завдання', command=self.open_tasks, bg='#FFFFFF',
                                width=160, bd=0, compound=tk.TOP, image=self.add_img3)
        button_add3.pack(side=tk.LEFT)

    def open_add(self):
        emp.Employees()

    def open_trucks(self):
        trucks.Trucks()

    def open_tasks(self):
        tasks.Tasks()


if __name__ == "__main__":
    root = tk.Tk()
    wind = Main(root)
    wind.pack()

    icon = tk.PhotoImage(file="resources\\icon.png")
    root.iconphoto(False, icon)
    root.title("Data processing program")
    root.geometry("480x370+600+300")
    root.resizable(False, False)
    root.mainloop()
