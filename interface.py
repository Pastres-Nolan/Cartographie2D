import tkinter as tk
import tkinter.messagebox as tkm
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageGrab
from pilotage import Pilotage
from math import sin,cos,pi
import traitement as Tr
import numpy as np
import threading
import os


class Interface:
    def __init__(self):
        self.tr = Tr.Traitement()
        
        self.window = tk.Tk()
        self.window.title("zone detector 3000")

        width_screen = self.window.winfo_screenwidth()
        height_screen = self.window.winfo_screenheight()

        self.width_window = width_screen 
        self.height_window = height_screen - 90

        self.canvas = tk.Canvas(self.window, bg='black', width=self.width_window , height=self.height_window)
        self.canvas.grid()

        self.canvas.bind("<Button-1>", self.on_click)
        
        self.ball1 = self.canvas.create_oval(10, 10, 35, 35, fill='white')
        
        img = Image.open("detector3000.png")
        img = img.resize((self.width_window, self.height_window), Image.LANCZOS)

        self.im = ImageTk.PhotoImage(img)
        self.image = self.canvas.create_image(
            self.width_window // 2,
            self.height_window // 2,
            image=self.im)
        self.canvas.image = self.im

        menubar = tk.Menu(self.window)

        self.menu1 = tk.Menu(menubar, tearoff=0)
        self.boutonstart = self.menu1.add_command(label="Start", command=self.start)
        self.menu1.add_command(label="Stop", command=self.stop)
        self.menu1.add_separator()
        self.menu1.add_command(label="EXIT", command=self.pop)
        menubar.add_cascade(label="Mouvement", menu=self.menu1)

        menu2 = tk.Menu(menubar, tearoff=0)
        menu2.add_command(label="DOWNLOAD", command=self.download_canva)
        menubar.add_cascade(label="Sauvegarder", menu=menu2)

        self.window.config(menu=menubar)
        self.position = [(0, 0), (0, 0)]
        self.lines_canva = []

        # Initialisation du pilotage en thread
        self.pilotage = None
        threading.Thread(target=self.init_pilotage, daemon=True).start()


    def init_pilotage(self):
        try:
            self.pilotage = Pilotage()
            self.update_position()
        except Exception as e:
            tkm.showwarning("Erreur Bluetooth", f"Connexion au robot échouée :\n{e}")
    
    
    def update_position(self):
        try:
            self.position.append(self.pilotage.position())
            self.update_canvas()
            self.window.after(200, self.update_position) 
        except Exception as e:
            print(f"Error updating position: {e}")


    def update_canvas(self):
        aggrandissement = 2
        decalage_x = 600
        decalage_y = 400
        
        x1, y1 = self.position[-2]   
        x2, y2 = self.position[-1]
       
        x1p = x1 * aggrandissement + decalage_x
        x2p = x2 * aggrandissement + decalage_x
        y1p = y1 * aggrandissement + decalage_y
        y2p = y2 * aggrandissement + decalage_y
        self.line = self.canvas.create_line(x1p, y1p, x2p, y2p,
            fill="ivory", tags="line", width= 2)
        self.lines_canva.append(self.line)

    
    def move_bot(self):
        self.canvas.itemconfig(self.ball1, fill="green")
        if self.pilotage:
            self.pilotage.start_moving()

    
    def start(self):
        if not self.pilotage:
            tkm.showerror("Erreur", "Connexion au robot non terminée.")
            return
        self.canvas.itemconfig(self.ball1, fill="green")
        threading.Thread(target=self.pilotage.start, daemon=True).start()
        self.menu1.entryconfig("Start", command = self.move_bot)


    def stop(self):
        self.canvas.itemconfig(self.ball1, fill="red")
        if self.pilotage:
            self.pilotage.running.set()
            self.pilotage.stop_moving()


#Fonctions liées aux boutons
    def contour(self):
        tableau_de_collisions = self.pilotage.pos_collisions
        self.tr.afficher_points(tableau_de_collisions , canvas= self.canvas)
        self.tr.afficher_contour(tableau_de_collisions , canvas = self.canvas)


    def rotate_canva(self):
        self.delete_canva()
        s_xb = 0
        s_yb = 0
        nb = len(self.pilotage.pos_collisions)

        for i in range(nb):
            if self.pilotage.pos_collisions:
                xb, yb = self.pilotage.pos_collisions[i]
                s_xb += xb
                s_yb += yb

        if nb > 0:
            g_xb, g_yb = s_xb / nb, s_yb / nb
        
        ANGLE = simpledialog.askstring("Rotate canva", "Quel est votre angle de rotation ? (en degré)")
        ANGLE = float(ANGLE) * pi / 180
        ca = cos(ANGLE)
        sa = sin(ANGLE)
        rot_mat = np.array([[ca, -sa], 
                            [sa, ca]])

        for i in range(nb):
            if self.pilotage.pos_collisions:
                xb, yb = self.pilotage.pos_collisions[i]
                xb -= g_xb
                yb -= g_yb

                rotated = np.array([xb, yb]) @ rot_mat

                x1b = rotated[0] + g_xb
                y1b = rotated[1] + g_yb

                self.pilotage.pos_collisions[i] = (x1b, y1b)
        self.canvas.delete("boules")
        self.canvas.delete("contour")
        tableau_de_collisions = self.pilotage.pos_collisions
        self.tr.afficher_points(tableau_de_collisions, canvas=self.canvas)
        self.tr.afficher_contour(tableau_de_collisions, canvas=self.canvas)



    def translate_canva(self):
        self.delete_canva()
        input_str = simpledialog.askstring("Translation", "Entrez dx et dy séparés par une virgule (ex: 10, 20) :")
        dx_str, dy_str = input_str.split(",")
        TRANSLATION_x = float(dx_str.strip())
        TRANSLATION_y = float(dy_str.strip())

        for i in range(len(self.pilotage.pos_collisions)):
            if self.pilotage.pos_collisions:
                x, y = self.pilotage.pos_collisions[i]
                x_new = x + float(TRANSLATION_x)
                y_new = y + float(TRANSLATION_y)
                self.pilotage.pos_collisions[i] = (x_new, y_new)
        self.canvas.delete("boules")
        self.canvas.delete("contour")
        tableau_de_collisions = self.pilotage.pos_collisions
        self.tr.afficher_points(tableau_de_collisions , canvas= self.canvas)
        self.tr.afficher_contour(tableau_de_collisions , canvas = self.canvas)

    
    def delete_canva(self):
        self.canvas.delete("line")


#Fonction liée au click de départ
    def create_zone(self):
        self.canvas.itemconfigure(self.image, state='hidden')
        self.Ok = True

        self.x1_z = self.width_window - self.width_window * 0.94
        self.y1_z = self.height_window - self.height_window * 0.90
        self.x2_z = self.width_window -  self.width_window * 0.06
        self.y2_z = self.height_window - self.height_window * 0.10

        self.carre = self.canvas.create_rectangle(self.x1_z, self.y1_z, self.x2_z, self.y2_z, outline="ivory", width=2)

        self.button1 = tk.Button(self.window, text="Contour", command=self.contour, width=13)
        self.button1.place(x=self.width_window - self.width_window * 0.96, y=10)

        self.button2 = tk.Button(self.window, text="Rotation", command=self.rotate_canva, width=13)
        self.button2.place(x=self.width_window - self.width_window * 0.96 + 110, y=10)

        self.button3 = tk.Button(self.window, text="Translate", command=self.translate_canva, width=13)
        self.button3.place(x=self.width_window - self.width_window * 0.96 + 220, y=10)

        self.button4 = tk.Button(self.window, text="Delete", command = self.delete_canva, width=13)
        self.button4.place(x = self.width_window - self.width_window * 0.96 + 330, y=10)


#Fonctions liées aux menus
    def download_canva(self):
        self.window.update() 
     
        x = self.x1_z + 20
        y = self.y1_z + 70
        w = self.x2_z + 365
        h = self.y2_z + 230
        
        img = ImageGrab.grab(bbox=(x, y, w, h))
        img.save("interface.png")
        
        print("Image sauvegardée sous 'interface.png'")
        print("Image sauvegardée dans :", os.path.abspath("interface.png"))


    def pop(self):
        if tkm.askyesno('EXIT', 'Voulez-vous quitter?'):
            self.window.destroy()
        else:
            tkm.showerror("Go", "OK")


    def on_click(self, event):
        self.window.unbind("Button-1")
        if 0 <= event.x <= self.width_window and 0 <= event.y <= self.height_window:
            self.start()
            self.create_zone()
            


    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.run()
