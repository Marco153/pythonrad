﻿import tkinter as tk
from PIL import Image, ImageTk
import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

def validate_float_input(P):
    if P == "" or P.replace('.', '', 1).isdigit():
        return True
    else:
        return False

class PageOne(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        padx = 40
        pady = 20


        img = Image.open("logo.jpg")
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self, image=img)
        panel.img = img
        panel.pack(padx=padx)

        label = tk.Label(self, text=" ")
        label.pack(pady=pady)

        label = tk.Label(self, text="Matricula")
        label.pack(padx=padx)
		# Create a StringVar to hold the text
        usuario = tk.StringVar()
		# Create an Entry widget linked to the StringVar
        textbox = tk.Entry(self, textvariable=usuario)
        textbox.pack(padx=padx)

        label = tk.Label(self, text="Senha")
        label.pack(padx=padx)
		# Create a StringVar to hold the text
        pw = tk.StringVar()
		# Create an Entry widget linked to the StringVar
        textbox = tk.Entry(self, textvariable=pw, show='*')
        textbox.pack(padx=padx)

        button = tk.Button(self, text="Login", command=lambda: self.try_login(controller, usuario.get(), pw.get()))
        button.pack()

    def try_login(self, controller, nome, senha):
        res = cur.execute(f"SELECT * from usuarios where nome=\"{nome}\" and senha=\"{senha}\"")
        res = res.fetchall()
        if len(res) > 0:
            #print(res.fetchall())
            print(res[0][1])
            controller.show_frame(PageTwo)
            
class PageJava(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        res = cur.execute(f"select nome, nota from alunos inner join java on java.alun_id = alunos.id;")
        res = res.fetchall()
        vcmd = (parent.register(validate_float_input), '%P')

        if len(res) > 0:
            print(res)
            names_frame = tk.Frame(self)
            names_frame.pack(side="left")
            label = tk.Label(names_frame, text="nome")
            label.pack(pady=2, side=tk.TOP)
            for al in res:
                label = tk.Label(names_frame, text=al[0])
                label.pack(pady=2, side=tk.TOP)
				#print(res.fetchall())
            #controller.show_frame(PageTwo)
            names_frame = tk.Frame(self)
            names_frame.pack(side="left")
            label = tk.Label(names_frame, text="nota")
            label.pack(pady=2, side=tk.TOP)
            for al in res:
                entry = tk.Entry(names_frame, validate='key', validatecommand=vcmd)
                entry.pack()
                entry.insert(0, al[1])
                input_value = entry.get()

                if input_value.strip():  # Check if the input is not empty or just whitespace
                    try:
                        float_val = float(input_value)
                    except ValueError:
                        print("Please enter a valid number.")
                else:
                    print("Input cannot be empty.")
				#print(res.fetchall())

class PageCpp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button = tk.Button(self, text="java", command=lambda: controller.show_frame(PageJava))
        button.pack()
        button = tk.Button(self, text="c++", command=lambda: controller.show_frame(PageCpp))
        button.pack()

        '''
        names_frame = tk.Frame(self)
        names_frame.pack(side="left")
        label = tk.Label(names_frame, text="")
        label.pack(pady=2, side=tk.TOP)
        label = tk.Label(names_frame, text="joao")
        label.pack(pady=2, side=tk.TOP)
        label = tk.Label(names_frame, text="mario")
        label.pack(pady=2, side=tk.TOP)

        other = tk.Frame(self)
        other.pack(side="left")
        label = tk.Label(other, text="java")
        label.pack(pady=2, side=tk.TOP)
        entry = tk.Entry(other, width=20)
        entry.pack(side="top", padx=10)
        entry = tk.Entry(other, width=20)
        entry.pack(side="top", padx=10)

        other = tk.Frame(self)
        other.pack(side="left")
        label = tk.Label(other, text="c++")
        label.pack(pady=2, side=tk.TOP)
        entry = tk.Entry(other, width=20)
        entry.pack(side="top", padx=10)
        entry = tk.Entry(other, width=20)
        entry.pack(side="top", padx=10)
'''
        '''
        # Create two rows (frames) and pack them vertically
        for row in range(2):
            row_frame = tk.Frame(self)
            row_frame.pack(side="top", fill="x", pady=5)

            label = tk.Label(row_frame, text="aluno")
            label.pack(pady=10, padx=10, side="top")

            # In each row, add two Entry widgets and pack them horizontally
            for col in range(2):
                entry = tk.Entry(row_frame, width=20)
                entry.pack(side="left", padx=10)
		'''


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Container to stack frames on top of each other
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        # Iterate through page classes and initialize them
        for F in (PageOne, PageTwo, PageJava, PageCpp):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageOne)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()  # Bring the frame to the front

if __name__ == "__main__":
    app = App()
    app.mainloop()

