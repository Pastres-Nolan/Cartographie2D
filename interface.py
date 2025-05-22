

""" 22/05/2025
Fichier pour l'interface """

import tkinter as tk
import tkinter.messagebox as tkm
from PIL import Image, ImageTk


class Interface :
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("zone detector 3000")

        widht_screen = self.window.winfo_screenwidth()
        height_screen = self.window.winfo_screenheight()

        self.width_window = widht_screen - 200
        self.height_window = height_screen - 200

        self.canvas = tk.Canvas(self.window, bg ='black', width = self.width_window + 100, height = self.height_window)
        self.canvas.grid()

        self.ball1 = self.canvas.create_oval(10, 10, 25, 25, fill = 'white') #balle qui represente le statut (start/stop)
        self.Ok = False #True si une zone est créee False sinon
        self.carre = None 
        self.boutons = []
        img = Image.open("detector3000.png")
        img = img.resize((800, 600), Image.LANCZOS)
        self.im = ImageTk.PhotoImage(img)
        self.image = self.canvas.create_image(self.width_window // 2, self.height_window // 2, image = self.im)
        self.b = ["Point", "Contour", "Point Corrigé"]

        #creation du menu
        menubar = tk.Menu(self.window)

        #creation des options du menu
        menu0 = tk.Menu(menubar, tearoff = 0)
        menu0.add_command(label = "Nouveau", command = self.zone)
        menu0.add_command(label ="Suprimer", command  = self.supzone)
        menubar.add_cascade(label = "Zone", menu = menu0) 

        menu1 = tk.Menu(menubar, tearoff=0)
        menu1.add_command(label ="Start", command = self.start)
        menu1.add_command(label ="Stop", command = self.stop)
        menu1.add_separator()
        menu1.add_command(label ="EXIT", command = self.pop)
        menubar.add_cascade(label ="Analyse", menu = menu1)

        menu2 = tk.Menu(menubar, tearoff = 0)
        menu2.add_command(label ="UPLOAD", command = self.upload)
        menubar.add_cascade(label = "Sauvegarder", menu = menu2) 

        #configuration du menu
        self.window.config(menu=menubar) 

        
    def start(self):
        if self.Ok:
            self.canvas.itemconfig(self.ball1, fill = "green")               #balle : vert , statut : start
        else:
            tkm.showerror("No zone", "Créer une nouvelle zone dans Zone")    #affiche l'erreur "pas de zone"
            
    def stop(self):
        self.canvas.itemconfig(self.ball1, fill = "red")                     #balle : rouge , statut : stop
    
    def zone(self):
        self.canvas.delete(self.image)
        self.Ok = True
        zone1 = self.canvas.create_rectangle(self.width_window - self.width_window*0.94, self.height_window - self.height_window*0.90,                #delimitation du terrain de jeu pour les analyses
                                              self.width_window, self.height_window - 60, outline = "ivory", width = 2)   
        self.carre = zone1 
        for i in range (len(self.b)):
            button = tk.Button(self.window, text = self.b[i], command = None,width = 13)
            self.boutons.append(button)
            button.place(x=self.width_window - self.width_window*0.96 + i * 110, y = 10)
            
    def supzone(self):
        self.Ok = False
        self.canvas.delete(self.carre)
        for btn in self.boutons:
            btn.destroy()       #vide les boutons dans la liste boutons
        self.boutons.clear()    #supprime les boutons dans l'interface

    def pop(self):                                         
        if tkm.askyesno('EXIT', 'Voulez vous quitter?'):    #double check si on veut quitter
            self.window.destroy()
        else:
            tkm.showerror("Go", "OK")

    def upload(self):
        pass

    def run(self):
        self.window.mainloop()
    
