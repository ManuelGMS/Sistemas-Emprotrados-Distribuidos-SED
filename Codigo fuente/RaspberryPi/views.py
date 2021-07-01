from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from controller import Controller
from tkinter.scrolledtext import ScrolledText

# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************

class Window(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)

        self.title('Mastermind')
        self.geometry('800x480')
        self.configure(bg='white')
        self.resizable(width=False, height=False)

        self.frames = {}
        self.mainContainer = Frame(self)
        self.mainContainer.grid_rowconfigure(0, weight=1)
        self.mainContainer.grid_columnconfigure(0, weight=1)
        self.mainContainer.pack(side="top", fill="both", expand = True)

        for frameClass in (MainMenu, ConfigurationMenu, MatchMenu, InformationMenu):

            frameInstance = frameClass(self.mainContainer, self.changeWindowFrameTo, self.closeWindow)

            frameInstance.grid(row=0, column=0, sticky="nsew")

            self.frames[frameClass] = frameInstance

        self.changeWindowFrameTo(MainMenu)

    def changeWindowFrameTo(self, frame):

        if frame is MainMenu:

            Controller.getInstance().action({ "event": "ACTIVATE_DEACTIVATE_RESTABLISH_MATCH_BUTTON", "object": { 'frame': self.frames[frame] } })

        elif frame is ConfigurationMenu:

            Controller.getInstance().action({ "event": "LOAD_USER_CONFIGURATION", "object": { 'frame': self.frames[frame] } })

        elif frame is MatchMenu:

            Controller.getInstance().action({ "event": "CLEAN_FRAME_ENTRIES", "object": { 'frame': self.frames[frame] } })

        self.frames[frame].tkraise()

    def closeWindow(self):

        self.destroy()

# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************

class MainMenu(Frame):
   
    def __init__(self, parent, changeWindowFrameTo, closeWindow):
    
        Frame.__init__(self, parent)

        self.btnIniciar = Button(self, text="JUGAR PARTIDA", font=("Arial Bold", 40), command=lambda : changeWindowFrameTo(MatchMenu))
        self.btnIniciar.pack(side=TOP, fill=X, padx=10, pady=10)

        self.btnRestablecer = Button(self, text="RESTABLECER PARTIDA", font=("Arial Bold", 40), command=lambda : Controller.getInstance().action({ "event": "RESTABLISH_MATCH", "object": { 'frame' : self } }))
        self.btnRestablecer.pack(side=TOP, fill=X, padx=10, pady=10)

        self.btnAjustes = Button(self, text="CONFIGURACIÓN", font=("Arial Bold", 40), command=lambda : changeWindowFrameTo(ConfigurationMenu))
        self.btnAjustes.pack(side=TOP, fill=X, padx=10, pady=10)

        self.btnInfo = Button(self, text="INFORMACIÓN", font=("Arial Bold", 40), command=lambda : changeWindowFrameTo(InformationMenu))
        self.btnInfo.pack(side=TOP, fill=X, padx=10, pady=10)

        self.btnSalir = Button(self, text="SALIR", font=("Arial Bold", 40), command=lambda : closeWindow())
        self.btnSalir.pack(side=TOP, fill=X, padx=10, pady=10)

        self.changeWindowFrameTo = changeWindowFrameTo

    def updateFrame(self, context):

        if context["event"] == "ACTIVATE_DEACTIVATE_RESTABLISH_MATCH_BUTTON":

            self.btnRestablecer.configure(state = 'active' if context["object"]["exists"] else 'disabled')

        elif context["event"] == "SHOW_OLD_MATCH_RESULTS":

            text = "Restaurando partida.\n\nTus resultados fueron:\n\n"

            for selection, result in zip(context["object"]["match"]["selections"], context["object"]["match"]["results"]):
                text += "(" + selection + "," + result + ")\n"

            messagebox.showinfo("INFO", text)

        elif context["event"] == "BAD_MATCH_CONFIGURATION":
            
            messagebox.showwarning("AVISO", "No se pudo iniciar.\n\nCompruebe lo siguiente:\n\n1º) Los nombres deben tener entre 1 y 12 caracteres.\n\n2º) El código debe estar formado por 4 numeros [0-9].\n\n3º) Los jugadores deben tener nombres diferentes.")

        elif context["event"] == "UNABLE_TO_CONNECT":
            
            messagebox.showerror("ERROR", "No se puede conectar\ncon el dispositivo.")
            self.changeWindowFrameTo(MainMenu)

        elif context["event"] == "CONNECTION_MISSED":
            
            messagebox.showerror("ERROR", "Perdida la comunicación\ncon el dispositivo.")
            self.changeWindowFrameTo(MainMenu)

        elif context["event"] == "GAME_ENDED_CORRECTLY":

            self.changeWindowFrameTo(MainMenu)
            messagebox.showinfo("INFO", "La partia finalizó.")

# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************

class MatchMenu(Frame):
   
    def __init__(self, parent, changeWindowFrameTo, closeWindow):
    
        Frame.__init__(self, parent)

        self.lblCodificador = Label(self, text='CODIFICADOR', font=("Arial Bold", 20), justify='center')
        self.lblCodificador.pack(side=TOP, fill=X, padx=10, pady=10)

        self.etrCodificador = Entry(self, font=("Arial Bold", 20), justify='center')
        self.etrCodificador.pack(side=TOP, fill=X, padx=10, pady=10)

        self.lblCodigo = Label(self, text='CÓDIGO', font=("Arial Bold", 20), justify='center')
        self.lblCodigo.pack(side=TOP, fill=X, padx=10, pady=10)

        self.etrCodigo = Entry(self, font=("Arial Bold", 20), justify='center')
        self.etrCodigo.pack(side=TOP, fill=X, padx=10, pady=10)

        self.lblDecodificador = Label(self, text='DECODIFICADOR', font=("Arial Bold", 20), justify='center')
        self.lblDecodificador.pack(side=TOP, fill=X, padx=10, pady=10)

        self.etrDecodificador = Entry(self, font=("Arial Bold", 20), justify='center')
        self.etrDecodificador.pack(side=TOP, fill=X, padx=10, pady=10)

        self.btnIniciar = Button(self, text="INICIAR", font=("Arial Bold", 20), justify='center', command=lambda : Controller.getInstance().action({ "event": "PLAY_GAME", "object": { 'frame' : self, 'encoder' : self.etrCodificador.get() , 'code' : self.etrCodigo.get() , 'decoder' : self.etrDecodificador.get() } }))
        self.btnIniciar.pack(side=TOP, fill=X, padx=10, pady=10)

        self.btnVolver = Button(self, text="VOLVER AL MENÚ PRINCIPAL", font=("Arial Bold", 20), command=lambda : changeWindowFrameTo(MainMenu))
        self.btnVolver.pack(side=TOP, fill=X, padx=10, pady=10)

        self.changeWindowFrameTo = changeWindowFrameTo

    def updateFrame(self, context):

        if context["event"] == "CLEAN_FRAME_ENTRIES":

            self.etrCodigo.delete(0, END)
            self.etrCodificador.delete(0, END)
            self.etrDecodificador.delete(0, END)

        elif context["event"] == "BAD_MATCH_CONFIGURATION":
            
            messagebox.showwarning("AVISO", "No se pudo iniciar.\n\nCompruebe lo siguiente:\n\n1º) Los nombres deben tener entre 1 y 16 caracteres.\n\n2º) El código debe estar formado por 4 numeros [0-9].\n\n3º) Los jugadores deben tener nombres diferentes.")

        elif context["event"] == "UNABLE_TO_CONNECT":
            
            messagebox.showerror("ERROR", "No se puede conectar\ncon el dispositivo.")
            self.changeWindowFrameTo(MainMenu)

        elif context["event"] == "CONNECTION_MISSED":

            messagebox.showerror("ERROR", "Perdida la comunicación\ncon el dispositivo.")
            self.changeWindowFrameTo(MainMenu)

        elif context["event"] == "GAME_ENDED_CORRECTLY":

            messagebox.showinfo("INFO", "La partia finalizó.")
            self.changeWindowFrameTo(MainMenu)
            
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************

class InformationMenu(Frame):
   
    def __init__(self, parent, changeWindowFrameTo, closeWindow):
    
        Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)    
        
        self.txtInfo = ScrolledText(self, font=("Arial Bold", 14))
        self.txtInfo.grid(row=0, column=0, padx=10, pady=10)
        
        self.txtInfo.insert(INSERT, "¿Qué es Mastermind?\n\n")
        self.txtInfo.insert(INSERT, "Mastermind es un juego de dos jugadores que consiste en adivinar una clave de color, pero en este caso, será numérica.\n\n")

        self.txtInfo.insert(INSERT, "¿Cómo se juega al Mastermind?\n\n")
        self.txtInfo.insert(INSERT, "El jugador codificador escoge una clave numérica de 4 dígitos que el jugador decodificador debe descifrar, este último ")
        self.txtInfo.insert(INSERT, "dispone originalmente de 10 rondas para lograrlo. Una vez el decodificador introduce una posible clave, el sistema le ")
        self.txtInfo.insert(INSERT, "dará feedback de la siguiente manera. Un led verde se encenderá si el número se encuentra posicionado correctamente en ")
        self.txtInfo.insert(INSERT, "la clave numérica elegida por el jugador codificador, de lo contrario se encenderá un led rojo y, opcionalmente, si se ")
        self.txtInfo.insert(INSERT, "juega con pistas (como es habitual), un led azul para indicar que el número está en la clave escogida por el jugador ")
        self.txtInfo.insert(INSERT, "codificador, pero no se encuentra en la posición indicada. Este proceso se repite hasta acabar el número de rondas.\n\n")

        self.txtInfo.insert(INSERT, "¿Cómo se utiliza esta aplicación?\n\n")
        self.txtInfo.insert(INSERT, "La aplicación se divide en 4 opciones, estas son: JUGAR PARTIDA, RESTAURAR PARTIDA, CONFIGURACIÓN e INFORMACIÓN. Cuando se ")
        self.txtInfo.insert(INSERT, "selecciona JUGAR PARTIDA, la aplicación llevará a un menú en el que el jugador codificador deberá de registrar su nombre, la ")
        self.txtInfo.insert(INSERT, "clave numérica y el nombre del jugador decodificador, antes de iniciar la partida. La opción RESTAURAR PARTIDA no estará ")
        self.txtInfo.insert(INSERT, "disponible a menos que el sistema hardware en el que juega el decodificador haya detectado que una partida no se acabó ")
        self.txtInfo.insert(INSERT, "correctamente y nos ofrezca la opción de restaurarla para acabarla. Si el jugador selecciona la opción CONFIGURACIÓN accederá ")
        self.txtInfo.insert(INSERT, "a un menú donde podrá ajustar algunas opciones de juego, como la dificultad (si las pistas están activas, entonces se encenderán ")
        self.txtInfo.insert(INSERT, "leds azules para indicar si el código final contiene el número indicado, pero en otra posición, en caso contrario sólo se ")
        self.txtInfo.insert(INSERT, "encenderán leds verdes si el número está en su sitio en la clave final, rojo en cualquier otro caso), el uso de sonidos, el tiempo ")
        self.txtInfo.insert(INSERT, "para ver su jugada en los leds, el tiempo que tiene el decodificador tiene por ronda para elegir una clave numérica y, finalmente, ")
        self.txtInfo.insert(INSERT, "el número de rondas de que dispone el decodificador para acertar la clave numérica. La última opción sería seleccionar INFORMACIÓN ")
        self.txtInfo.insert(INSERT, ", que llevará a este menú, donde se mostrará un resumen de la aplicación.\n\n")
        
        self.txtInfo.configure(state='disabled')

        self.btnVolver = Button(self, text="VOLVER AL MENÚ PRINCIPAL", font=("Arial Bold", 40), command=lambda : changeWindowFrameTo(MainMenu))
        self.btnVolver.grid(row=1, column=0, padx=10, pady=10)
    
    def updateFrame(self, context):
        pass
        
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************

class ConfigurationMenu(Frame):
    
    def __init__(self, parent, changeWindowFrameTo, closeWindow):

        Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.lblPistas = Label(self, text='ACTIVAR PISTAS', font=("Arial Bold", 20))
        self.lblPistas.grid(row=0, column=0, padx=10, pady=10)
        self.cboPistas = Combobox(self, justify='center', values=["SI", "NO"], state='readonly')
        self.cboPistas.grid(row=0, column=1, padx=10, pady=10)
        self.btnPistas = Button(self, text="ACTUALIZAR", font=("Arial Bold", 20), command=lambda : Controller.getInstance().action({ "event": "UPDATE_USER_CONFIGURATION", "object": { 'frame': self, 'field': 'clues', 'value': True if self.cboPistas.get() == "SI" else False }}))
        self.btnPistas.grid(row=0, column=2, padx=10, pady=10)
        
        self.lblSonidos = Label(self, text='ACTIVAR SONIDOS', font=("Arial Bold", 20))
        self.lblSonidos.grid(row=1, column=0, padx=10, pady=10)
        self.cboSonidos = Combobox(self, justify='center', values=["SI", "NO"], state='readonly')
        self.cboSonidos.grid(row=1, column=1, padx=10, pady=10)
        self.btnSonidos = Button(self, text="ACTUALIZAR", font=("Arial Bold", 20), command=lambda : Controller.getInstance().action({ "event": "UPDATE_USER_CONFIGURATION", "object": { 'frame': self, 'field': 'sounds', 'value': True if self.cboSonidos.get() == "SI" else False }}))
        self.btnSonidos.grid(row=1, column=2, padx=10, pady=10)

        self.lblResponder = Label(self, text='TIEMPO PARA RESPONDER', font=("Arial Bold", 20))
        self.lblResponder.grid(row=2, column=0, padx=10, pady=10)
        self.etrResponder = Entry(self, justify='center')
        self.etrResponder.grid(row=2, column=1, padx=10, pady=10)
        self.btnResponder = Button(self, text="ACTUALIZAR", font=("Arial Bold", 20), command=lambda : Controller.getInstance().action({ "event": "UPDATE_USER_CONFIGURATION", "object": { 'frame': self, 'field': 'answer', 'value': (int(self.etrResponder.get()) if int(self.etrResponder.get()) >= 0 and int(self.etrResponder.get()) <= 60 else 0 if int(self.etrResponder.get()) <= 0 else 60) if self.etrResponder.get().isnumeric() else 0 }}))
        self.btnResponder.grid(row=2, column=2, padx=10, pady=10)

        self.lblMemorizar = Label(self, text='TIEMPO PARA MEMORIZAR', font=("Arial Bold", 20))
        self.lblMemorizar.grid(row=3, column=0, padx=10, pady=10)
        self.etrMemorizar = Entry(self, justify='center')
        self.etrMemorizar.grid(row=3, column=1, padx=10, pady=10)
        self.btnMemorizar = Button(self, text="ACTUALIZAR", font=("Arial Bold", 20), command=lambda : Controller.getInstance().action({ "event": "UPDATE_USER_CONFIGURATION", "object": { 'frame': self, 'field': 'memory', 'value': (int(self.etrMemorizar.get()) if int(self.etrMemorizar.get()) >= 4 and int(self.etrMemorizar.get()) <= 60 else 4 if int(self.etrMemorizar.get()) <= 4 else 60) if self.etrMemorizar.get().isnumeric() else 4 }}))
        self.btnMemorizar.grid(row=3, column=2, padx=10, pady=10)

        self.lblRondas = Label(self, text='NÚMERO DE RONDAS', font=("Arial Bold", 20))
        self.lblRondas.grid(row=4, column=0, padx=10, pady=10)
        self.etrRondas = Entry(self, justify='center')
        self.etrRondas.grid(row=4, column=1, padx=10, pady=10)
        self.btnRondas = Button(self, text="ACTUALIZAR", font=("Arial Bold", 20), command=lambda : Controller.getInstance().action({ "event": "UPDATE_USER_CONFIGURATION", "object": { 'frame': self, 'field': 'rounds', 'value': (int(self.etrRondas.get()) if int(self.etrRondas.get()) >= 10 and int(self.etrRondas.get()) <= 20 else 10 if int(self.etrRondas.get()) <= 10 else 20) if self.etrRondas.get().isnumeric() else 10 }}))
        self.btnRondas.grid(row=4, column=2, padx=10, pady=10)

        self.btnPorDefecto = Button(self, text="REESTABLECER CONFIGURACIÓN POR DEFECTO", font=("Arial Bold", 24), command=lambda : Controller.getInstance().action({ "event": "RESET_USER_CONFIGURATION", "object": { 'frame': self }}))
        self.btnPorDefecto.grid(row=5, padx=10, pady=10, columnspan=3)

        self.btnSalir = Button(self, text="VOLVER AL MENÚ PRINCIPAL", font=("Arial Bold", 24), command=lambda : changeWindowFrameTo(MainMenu))
        self.btnSalir.grid(row=6, padx=10, pady=10, columnspan=3)

    def __setValues(self, context):

        self.etrRondas.delete(0, END)
        self.etrMemorizar.delete(0, END)
        self.etrResponder.delete(0, END)
        self.etrRondas.insert(0, context["object"]["config"]["rounds"])
        self.etrMemorizar.insert(0, context["object"]["config"]["memory"])
        self.etrResponder.insert(0, context["object"]["config"]["answer"])
        self.cboPistas.set("SI" if context["object"]["config"]["clues"] else "NO")
        self.cboSonidos.set("SI" if context["object"]["config"]["sounds"] else "NO")

    def updateFrame(self, context):

        if context["event"] == "LOAD_USER_CONFIGURATION":

            self.__setValues(context)

        elif context["event"] == "UPDATE_USER_CONFIGURATION":

            self.__setValues(context)

            messagebox.showinfo("Aviso", "El valor ha sido actualizado")

        elif context["event"] == "RESET_USER_CONFIGURATION":

            self.__setValues(context)

            messagebox.showinfo("Aviso", "Se han reestrablecido los valores por defecto")
