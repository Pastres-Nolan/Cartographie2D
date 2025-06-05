import tkinter as tk
import tkinter.messagebox as tkm
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageGrab
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageGrab
from pilotage import Pilotage
from math import sin,cos
import threading
import os
import os
import time 

class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("zone detector 3000")

        widht_screen = self.window.winfo_screenwidth()
        height_screen = self.window.winfo_screenheight()

        self.width_window = widht_screen - 200
        self.height_window = height_screen - 200

        self.canvas = tk.Canvas(self.window, bg='black', width=self.width_window + 100, height=self.height_window)
        self.canvas.grid()

        self.canvas.bind("<Button-1>", self.on_click)
        
        self.ball1 = self.canvas.create_oval(10, 10, 35, 35, fill='white')

        self.canvas.bind("<Button-1>", self.on_click)
        
        self.ball1 = self.canvas.create_oval(10, 10, 35, 35, fill='white')
        self.carre = None
        self.boutons = []
        
        img = Image.open("detector3000.png")
        img = img.resize((self.width_window, self.height_window), Image.LANCZOS)

        self.im = ImageTk.PhotoImage(img)
        self.image = self.canvas.create_image(
            self.width_window // 2,
            self.height_window // 2,
            image=self.im
        )
        self.canvas.image = self.im

        menubar = tk.Menu(self.window)

        self.menu1 = tk.Menu(menubar, tearoff=0)
        self.boutonstart = self.menu1.add_command(label="Start", command=self.start)
        self.menu1.add_command(label="Stop", command=self.stop)
        self.menu1.add_separator()
        self.menu1.add_command(label="EXIT", command=self.pop)
        menubar.add_cascade(label="Mouvement", menu=self.menu1)
        menubar.add_cascade(label="Mouvement", menu=self.menu1)

        menu2 = tk.Menu(menubar, tearoff=0)
        menu2.add_command(label="DOWNLOAD", command=self.download_canva)
        menu2.add_command(label="DOWNLOAD", command=self.download_canva)
        menubar.add_cascade(label="Sauvegarder", menu=menu2)

        self.window.config(menu=menubar)
        self.position = [(0, 0), (0, 0)]


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
        aggrandissement = 3
        decalage = 400
        
        x1, y1 = self.position[-2]   
        x2, y2 = self.position[-1]
    
        x1p = x1 * aggrandissement + decalage
        x2p = x2 * aggrandissement + decalage
        y1p = y1 * aggrandissement + decalage
        y2p = y2 * aggrandissement + decalage
        self.line = self.canvas.create_line(x1p, y1p, x2p, y2p, fill="ivory")
        

    def start(self):
        if not self.pilotage:
            tkm.showerror("Erreur", "Connexion au robot non terminée.")
            return
        self.canvas.itemconfig(self.ball1, fill="green")
        threading.Thread(target=self.pilotage.start, daemon=True).start()
        self.menu1.entryconfig("Start", command = self.move_bot)


    def move_bot(self):
        self.canvas.itemconfig(self.ball1, fill="green")
        if self.pilotage:
            self.pilotage.start_moving()

    def stop(self):
        self.canvas.itemconfig(self.ball1, fill="red")
        if self.pilotage:
            self.pilotage.running.set()
            self.pilotage.stop_moving()


    def rotate_canva(self):  
        for line in self.lines_canva:
            x1, y1, x2, y2 = self.canvas.coords(line)

            #ANGLE = int(input("Quel est votre angle de rotation ? (ex : pi/3)"))
            ANGLE = simpledialog.askstring("rotate canva", "Quel est votre angle de rotation ? (ex : pi/3)")
            TRANSLATION = 100
            print("l'angle saisi est : ", ANGLE)

            x1p = (x1 * cos(ANGLE) - y1 * sin(ANGLE)) + TRANSLATION
            y1p = (x1 * sin(ANGLE) + y1 * cos(ANGLE)) + TRANSLATION
            x2p = (x2 * cos(ANGLE) - y2 * sin(ANGLE)) + TRANSLATION
            y2p = (x2 * sin(ANGLE) + y2 * cos(ANGLE)) + TRANSLATION

            self.canvas.delete(line)
            self.canvas.create_line(x1p, y1p, x2p, y2p, fill="light blue")


    def download_canva(self):
        self.window.update() 

        x = self.window.winfo_rootx()
        y = self.window.winfo_rooty()
        w = x + self.window.winfo_width()
        h = y + self.window.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, w, h))
        img.save("interface.png")
        
        print("Image sauvegardée sous 'interface.png'")
        print("Image sauvegardée dans :", os.path.abspath("interface.png"))


    def create_zone(self):
        self.canvas.itemconfigure(self.image, state='hidden')
        self.Ok = True
        zone1 = self.canvas.create_rectangle(
        self.width_window - self.width_window * 0.94,
        self.height_window - self.height_window * 0.90,
        self.width_window,self.height_window - 60, outline="ivory", width=2)

        self.carre = zone1

        self.button_name = ["Contour", "Rotation"]
        self.button1 = tk.Button(self.window, text="Contour", command=None, width=13)
        self.boutons.append(self.button1)
        self.button1.place(x=self.width_window - self.width_window * 0.96, y=10)

        self.button2 = tk.Button(self.window, text="Rotation", command=self.rotate_canva, width=13)
        self.boutons.append(self.button2)
        self.button2.place(x=self.width_window - self.width_window * 0.96 + 110, y=10)


    def pop(self):
        if tkm.askyesno('EXIT', 'Voulez-vous quitter?'):
            self.window.destroy()
        else:
            tkm.showerror("Go", "OK")


    def on_click(self, event):
        if 0 <= event.x <= self.width_window and 0 <= event.y <= self.height_window:
            self.start()
            self.create_zone()


    def run(self):
        self.window.mainloop()



if __name__ == "__main__":
    app = Interface()
    app.run()