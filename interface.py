# fichier qui gère l'interface



import tkinter as tk
import tkinter.messagebox as tkm

class Interface :
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title( "zone detector 3000" )

        self.canvas = tk.Canvas(self.window, bg = 'light gray', width=1500, height=700)
        self.canvas.pack()

        self.ball1 = self.canvas.create_oval(10, 10, 25, 25, fill = 'white') 
        self.Ok = False 
        self.carre = None 
        self.bouton = []
        self.b = ["Point", "Contour", "Point Corrigé"]

        self.menubar = tk.Menu(self.window)

        menu0 = tk.Menu(self.menubar, tearoff=0)
        menu0.add_command(label="Nouveau", command= self.zone)
        self.menubar.add_cascade(label = "Zone", menu = menu0) #creation des options du menu

        menu1 = tk.Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Start", command= self.start)
        menu1.add_command(label="Stop", command= self.stop)
        menu1.add_separator()
        menu1.add_command(label="EXIT", command=self.pop)
        self.menubar.add_cascade(label="Analyse", menu=menu1)
    
    def start(self):
        if self.Ok:
            self.canvas.itemconfig(self.ball1, fill = "green") 
        else:
            tkm.showerror("No zone", "Créer une nouvelle zone dans Zone") 

    def stop(self):
        self.canvas.itemconfig(self.ball1, fill = "red") 
    
    def pop (self): 
            if tkm.askyesno('EXIT', 'Voulez vous quitter?'):
                self.window.destroy()
            else:
                tkm.showerror("Go", "OK")

    def zone(self):
        zone1 = self.canvas.create_rectangle(50, 50, 1050, 850, outline = "ivory", width = 2) 
        self.Ok = True
        self.carre = zone1 
        for i in range (len(self.b)):
            button = tk.Button(self.window, text = self.b[i], command = None)
            self.bouton.append(button)
            button.pack(side = "left", padx = 5+i)
    
    def draw(self):
        self.window.config(menu=self.menubar) 
        self.window.mainloop()
