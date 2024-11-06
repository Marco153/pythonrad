import tkinter as tk
from PIL import Image, ImageTk
import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

def validate_float_input(P):
	if P == "" or P.replace('.', '', 1).isdigit():
		return True
	else:
		return False
aluno_id_ver_notas = 0
aluno_notas_ver_notas = 0
aluno_label_str = 0

def ColocarMateriaDeAluno(parent, id, materia):
	res = cur.execute(f"select sm1, sm2, av, avs from {materia} where alun_id = {id};")
	res = res.fetchall()
	aprovado = "aprovado"
	sm1 = 0
	sm2 = 0
	av = 0
	avs = 0

	if res[0][0] != None:
		sm1 = float(res[0][0])
	if res[0][1] != None:
		sm2 = float(res[0][1])
	if res[0][2] != None:
		av = float(res[0][2])
	if res[0][3] != None:
		avs = float(res[0][3])

	if sm1 + sm2 + max(av, avs) < 6:
		aprovado = "reprovado"
	lab = tk.Label(parent, text=f"{materia}: sm1 {sm1}, sm2 {sm2}, av {av}, avs {avs}={aprovado}")
	lab.pack()

def OpenVerNotasWindow(parent, id):
	new_windew = tk.Toplevel(parent)
	ColocarMateriaDeAluno(new_windew, id, "rad")
	ColocarMateriaDeAluno(new_windew, id, "java")

class PageVerNotas(tk.Frame):
	def __init__(self, parent, controller):
		aluno_label_str = tk.StringVar()
		tk.Frame.__init__(self, parent)
		lab = tk.Label(self, textvariable=aluno_label_str)
		lab.pack()


		print(f"id {aluno_notas_ver_notas}")

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
		res = cur.execute(f"SELECT professor, alun_id from usuarios where nome=\"{nome}\" and senha=\"{senha}\"")
		res = res.fetchall()
		print(f"logar is {res[0]}")

		if len(res) > 0:
			if res[0][0] == 1:
				print("professor")
				controller.show_frame(PageTwo)
			else:
				#print(res.fetchall())
				aluno_id_ver_notas = res[0][1]
				OpenVerNotasWindow(self, res[0][1])
				#controller.show_frame(PageVerNotas)
			
def ButtonVoltar(frame, page, controller):
	button = tk.Button(frame, text="voltar", command=lambda: controller.show_frame(page))
	button.pack()
def PackCheckBox(parent, var, frame, func):
	print(f"check box val {var.get()}")
	c1 = tk.Checkbutton(frame, text='',variable=var, command=func)
	c1.pack()
def CadastrarAluno(id, b, materia):
	#if check_vals.
	print(f"cad is {b}")
	if b == True:
		print("cadastrando")
		res = cur.execute(f"insert or ignore into {materia} (alun_id) values({id + 1});")
	else:
		res = cur.execute(f"delete from {materia} where alun_id = {id + 1};")
	con.commit()

	
def PackFloatingInput(parent, frame, default, txt_var):

	vcmd = (parent.register(validate_float_input), '%P')
	entry = tk.Entry(frame, validate='key', validatecommand=vcmd, textvariable=txt_var)
	entry.pack()
	entry.insert(0, default)
	input_value = entry.get()

	if input_value.strip():  # Check if the input is not empty or just whitespace
		try:
			float_val = float(input_value)
		except ValueError:
			print("Please enter a valid number.")
	else:
		print("Input cannot be empty.")
	#print(res.fetchall())
	
def PackNewFrame(parent, name):
	frame = tk.Frame(parent)
	frame.pack(side="left")
	label = tk.Label(frame, text=name)
	label.pack(pady=2, side=tk.TOP)
	return frame

	

def ShowAlunos(self, parent, materia):
	res = cur.execute(f"select nome, sm1, sm2, av, avs, a.id from alunos a inner join {materia} on {materia}.alun_id = a.id;")
	res = res.fetchall()
	self.db = res
	self.notes = [(tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()) for _ in range(len(res))]


	print(f"res is {res}")
	#print(f"notes {self.notes}")

	if len(res) > 0:
		#print(res)
		names_frame = tk.Frame(self)
		names_frame.pack(side="left")
		label = tk.Label(names_frame, text="nome")
		label.pack(pady=2, side=tk.TOP)
		for al in res:
			label = tk.Label(names_frame, text=al[0])
			label.pack(pady=2, side=tk.TOP)
			#print(res.fetchall())
		#controller.show_frame(PageTwo)
		self.sim1 = PackNewFrame(self, "sim1")
		self.sim2 = PackNewFrame(self, "sim2")
		self.av = PackNewFrame(self, "av")
		self.avs = PackNewFrame(self, "avs")
		#self.nc = PackNewFrame(self, "nc")
		self.salvar = PackNewFrame(self, "salvar")
		self.aprovado = PackNewFrame(self, "aprovado")

		for i, al in enumerate(res):
			sm1_nota = 0.0
			sm2_nota = 0.0
			av_nota = 0.0
			avs_nota = 0.0
			nc_nota = 0.0

			sm1_str_var, sm2_str_var, av_str_var, avs_str_var, aprovado_str_var = self.notes[i]
			if al[1] != None:
				sm1_nota = al[1]
			if al[2] != None:
				sm2_nota = al[2]
			if al[3] != None:
				av_nota = al[3]
			if al[4] != None:
				avs_nota = al[4]
			PackFloatingInput(parent, self.sim1, sm1_nota, sm1_str_var)
			PackFloatingInput(parent, self.sim2, sm2_nota, sm2_str_var)
			PackFloatingInput(parent, self.av, av_nota, av_str_var)
			PackFloatingInput(parent, self.avs, avs_nota, avs_str_var)
			button = tk.Button(self.salvar, text="Salvar", command=lambda i = i, materia = materia, apr = aprovado_str_var: Salvar(self, i, materia, apr))
			button.pack()
			ent = tk.Entry(self.aprovado, textvariable=aprovado_str_var)
			ent.pack()
	
def Salvar(self, id, materia, aprovado):
	final_id = self.db[id][5]
	sm1 = float(self.notes[id][0].get())
	sm2 = float(self.notes[id][1].get())
	av = float(self.notes[id][2].get())
	avs = float(self.notes[id][3].get())

	if (sm1 + sm2) + max(av, avs) >= 6:
		aprovado.set("aprovado")
	else:
		aprovado.set("reprovado")

	res = cur.execute(f"update {materia} set sm1 = {sm1}, sm2 = {sm2}, av = {av}, avs={avs} where alun_id = {final_id};")
	con.commit()
	print(f"notes {res}")
class PageJava(tk.Frame):
		
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		ButtonVoltar(self, PageTwo, controller)
		ShowAlunos(self, parent, "java")

				#print(res.fetchall())

class PageMAtricularAlunos(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		ButtonVoltar(self, PageTwo, controller)
		res = cur.execute(f"select nome from alunos;")
		res = res.fetchall()
		if len(res) > 0:
			names_frame = tk.Frame(self)
			names_frame.pack(side="left")

			label = tk.Label(names_frame, text="")
			label.pack()

			java = tk.Frame(self)
			java.pack(side="left")
			label = tk.Label(java, text="java")
			label.pack()

			rad = tk.Frame(self)
			rad.pack(side="left")
			label = tk.Label(rad, text="rad")
			label.pack()
			
			for al in res:

				label = tk.Label(names_frame, text=al[0])
				label.pack(pady=2, side=tk.TOP)

			for al in res:
				b =tk.Checkbutton(rad)
				b.pack()
				b = tk.Checkbutton(java)
				b.pack()

class PageNotas(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		ButtonVoltar(self, PageTwo, controller)

		res = cur.execute(f"select nome from alunos;")
		res = res.fetchall()
		if len(res) > 0:
			names_frame = tk.Frame(self)
			names_frame.pack(side="left")
			for al in res:
				label = tk.Label(names_frame, text=al[0][0])
				label.pack(pady=2, side=tk.TOP)
class PageCadastar(tk.Frame):
	def CadastrarNovoAluno(self, name):
		res = cur.execute(f"insert into alunos(nome) values('{name}');")
		con.commit()
		tk.Label(self.names_frame, text=name)
		
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		ButtonVoltar(self, PageTwo, controller)

		lab = tk.Label(self, text="Matricular novo aluno")
		lab.pack()
		nome_var = tk.StringVar()
		lab = tk.Label(self, text="Nome:")
		lab.pack()
		ent = tk.Entry(self, textvariable=nome_var)
		ent.pack()

		button = tk.Button(self, text="Cadastrar", command=lambda: self.CadastrarNovoAluno( nome_var.get()))
		button.pack()

		res = cur.execute(f"select nome, (select 1 from alunos join java j on j.alun_id = a.id), (select 1 from alunos join rad r on r.alun_id = a.id) from alunos a;")
		res = res.fetchall()
		check_boxes = [[(tk.BooleanVar(), tk.BooleanVar(), 0) for _ in range(len(res))] for _ in range(2)]

		if len(res) > 0:
			#print(f"res is {res}")
			self.names_frame = tk.Frame(self)
			self.names_frame.pack(side="left")
			label = tk.Label(self.names_frame, text="nome")
			label.pack(pady=2, side=tk.TOP)
			for al in res:
				label = tk.Label(self.names_frame, text=al[0])
				label.pack(pady=2, side=tk.TOP)
				#print(res.fetchall())
			#controller.show_frame(PageTwo)
			java = tk.Frame(self)
			java.pack(side="left")
			rad = tk.Frame(self)
			rad.pack(side="left")

			label = tk.Label(java, text="java")
			label.pack(pady=2, side=tk.TOP)
			label = tk.Label(rad, text="rad")
			label.pack(pady=2, side=tk.TOP)
			aux = False

			for i, al in enumerate(res):
				c_vals = check_boxes[0][i]
				c_vals = (c_vals[0], c_vals[1], i)
				java_cadastrado, rad_cadastrado, _ = c_vals
				if al[1] == 1:
					print(f"esta em java {i}")
					java_cadastrado.set(True)
				if al[2] == 1:
					rad_cadastrado.set(True)
					
				print(c_vals)
				PackCheckBox(parent, java_cadastrado, java, lambda c_vals=c_vals, java_cadastrado=java_cadastrado: CadastrarAluno(c_vals[2], java_cadastrado.get(), "java"))
				PackCheckBox(parent, rad_cadastrado, rad, lambda c_vals=c_vals, rad_cadastrado=rad_cadastrado : CadastrarAluno(c_vals[2], rad_cadastrado.get(), "rad"))
				#PackCheckBox(parent, check_boxes[1][i], rad, lambda c_vals = c_vals : print(f"Check{c_vals[1]}"))
				#print(res.fetchall())
class PageRad(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		ButtonVoltar(self, PageTwo, controller)
		ShowAlunos(self, parent, "rad")

class PageTwo(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		ButtonVoltar(self, PageOne, controller)

		button = tk.Button(self, text="java", command=lambda: controller.show_frame(PageJava))
		button.pack()
		button = tk.Button(self, text="rad", command=lambda: controller.show_frame(PageRad))
		button.pack()
		button = tk.Button(self, text="cadastrar", command=lambda: controller.show_frame(PageCadastar))
		button.pack()
		button = tk.Button(self, text="matricular", command=lambda: controller.show_frame(PageMAtricularAlunos))
		button.pack()
		button = tk.Button(self, text="notas", command=lambda: controller.show_frame(PageNotas))
		button.pack()



class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)

		# Container to stack frames on top of each other
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		self.frames = {}

		# Iterate through page classes and initialize them
		for F in (PageOne, PageTwo, PageJava, PageRad, PageCadastar, PageNotas, PageVerNotas):
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

