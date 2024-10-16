from tkinter import *
from tkinter import messagebox
import json


class button:
    def __init__(self, but):
        self.but = but

top = Tk()
top.geometry("200x200")


def getDbJson():
    data = 0
    f = open('db.json')

    # returns JSON object as a dictionary
    data = json.load(f)
    f.close()
    return data

def reset():
    print("will reset")
    '''Reset the list of participants'''
    for child in app.winfo_children():
        child.destroy()

    putInfo()

app = Frame(top)
app.grid()

buttons = []


def removeStudent(root, jsonObject, i):
    del jsonObject['db'][i]
    print(f"removed json {jsonObject}")
    with open('db.json', 'w') as f:
        json.dump(jsonObject, f)    
    reset()
    putInfo()


def helloCallBack(root, name):
    child_w= Toplevel(root)
    label_child= Label(child_w, text= name, font=('Helvetica 15'))
    label_child.pack()

def matriculaWind(root, jsonObject):
    def novoAluno(nome, jsonObject):
        jsonObject = getDbJson()
        jsonObject['db'].append({"name": nome})
        print(f"adding nome: {nome} jsonafter {jsonObject}")
        with open('db.json', 'w') as f:
            json.dump(jsonObject, f)    
        
        reset()
        putInfo()
        aoeu = 0

    child = Toplevel(root)
    child.wm_title("matriculas")
    child.geometry("200x200")
    # TextBox Creation 
    inputtxt = Text(child, 
                       height = 1, 
                       width = 10) 
    inputtxt.pack()
    
    printButton = Button(child, 
                            text = "novo",  
                            command = lambda:novoAluno(inputtxt.get(1.0, 'end-1c'), jsonObject))
    printButton.pack() 
    

def putInfo():
    f = open('db.json')

    # returns JSON object as a dictionary
    data = json.load(f)


    for i in range(0, len(data['db'])):
        name = data['db'][i]['name']
        B = Button(app, text =name, command = lambda name=name: helloCallBack(top, name))
        B.grid(row=i, column=0)
        B = Button(app, text ="x", command = lambda i=i: removeStudent(top, data, i))
        B.grid(row=i, column=2)
        #B.place(x=50,y=i*30)

def mainPage():
	# Criar uma variável para a caixa de texto
	texto_var = tk.StringVar()
	senha_var = tk.StringVar()

	# Criar um rótulo
	rotulo = tk.Label(root, text="Usuario:")
	rotulo.pack(pady=10)

	# Criar uma caixa de texto
	texto = tk.Entry(root, textvariable=texto_var, width=30)
	texto.pack(pady=10)

	rotulo = tk.Label(root, text="Senha:")
	rotulo.pack(pady=10)

	texto = tk.Entry(root, textvariable=senha_var, show='*', width=30)
	texto.pack(pady=10)

	# Criar um botão
	botao = tk.Button(root, text="Clique aqui", command=verificar)
	botao.pack(pady=10)



putInfo()
data = getDbJson()

B = Button(top, text ="nova matricula", command = lambda :matriculaWind(top, data))
B.grid()
top.mainloop()
