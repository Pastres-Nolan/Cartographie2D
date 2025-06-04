import tkinter as tk
import tkinter.messagebox as tkm
from PIL import Image, ImageTk, ImageGrab
from pilotage import Pilotage
import threading
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
        
        self.ball1 = self.canvas.create_oval(10, 10, 25, 25, fill='white')
        self.carre = None
        self.boutons = []
        img = Image.open("detector3000.png")
        img = img.resize((800, 600), Image.LANCZOS)
        self.im = ImageTk.PhotoImage(img)
        self.image = self.canvas.create_image(self.width_window // 2, self.height_window // 2, image=self.im)
        self.b = ["Contour"]

        menubar = tk.Menu(self.window)
        menu0 = tk.Menu(menubar, tearoff=0)
        menu0.add_command(label="Suprimer", command=self.supzone)
        menubar.add_cascade(label="Zone", menu=menu0)

        self.menu1 = tk.Menu(menubar, tearoff=0)
        self.boutonstart = self.menu1.add_command(label="Start", command=self.start)
        self.menu1.add_command(label="Stop", command=self.stop)
        self.menu1.add_separator()
        self.menu1.add_command(label="EXIT", command=self.pop)
        menubar.add_cascade(label="Analyse", menu=self.menu1)

        menu2 = tk.Menu(menubar, tearoff=0)
        menu2.add_command(label="DOWNLOAD", command=self.download)
        menubar.add_cascade(label="Sauvegarder", menu=menu2)

        self.position = []
        self.window.config(menu=menubar)

        # Initialisation du pilotage en thread
        self.pilotage = Pilotage()
        threading.Thread(target=self.init_pilotage, daemon=True).start()

    def init_pilotage(self):
        try:
            self.pilotage = Pilotage()
            while True:
                self.position.append(self.pilotage.pos_all[-1]) 
                self.update_canvas()
                time.sleep(0.1)

        except Exception as e:
            tkm.showerror("Erreur Bluetooth", f"Connexion au robot échouée :\n{e}")


    def update_canvas(self):
        aggrandissement = 3
        decalage = 400

        for i in range(1, len(self.position)):
            x1, y1 = self.position[i - 1]   
            x2, y2 = self.position[i]
        
            x1p = x1 * aggrandissement + decalage
            x2p = x2 * aggrandissement + decalage
            y1p = y1 * aggrandissement + decalage
            y2p = y2 * aggrandissement + decalage
            self.canvas.create_line(x1p, y1p, x2p, y2p, fill="ivory")
        

    def start(self):
        if not self.pilotage:
            tkm.showerror("Erreur", "Connexion au robot non terminée.")
            return
        self.canvas.itemconfig(self.ball1, fill="green")
        threading.Thread(target=self.pilotage.start, daemon=True).start()
        self.menu1.entryconfig("Start", command = self.move_bot)

    def move_bot(self):
        if self.pilotage:
            self.pilotage.start_moving()

    def stop(self):
        self.canvas.itemconfig(self.ball1, fill="red")
        if self.pilotage:
            self.pilotage.stop_moving()

    def create_zone(self):
        self.canvas.delete(self.image)
        self.Ok = True
        zone1 = self.canvas.create_rectangle(
            self.width_window - self.width_window * 0.94,
            self.height_window - self.height_window * 0.90,
            self.width_window,self.height_window - 60, outline="ivory", width=2)
        self.carre = zone1
        for i in range(len(self.b)):
            button = tk.Button(self.window, text=self.b[i], command=None, width=13)
            self.boutons.append(button)
            button.place(x=self.width_window - self.width_window * 0.96 + i * 110, y=10)

    def supzone(self):
        self.Ok = False
        self.canvas.delete(self.carre)
        for btn in self.boutons:
            btn.destroy()
        self.boutons.clear()

    def pop(self):
        if tkm.askyesno('EXIT', 'Voulez-vous quitter?'):
            self.window.destroy()
        else:
            tkm.showerror("Go", "OK")

    def on_click(self, event):
        if 0 <= event.x <= self.width_window and 0 <= event.y <= self.height_window:
            self.start()
            self.create_zone()

    def download(self):
        self.window.update() 

        x = self.window.winfo_rootx()
        y = self.window.winfo_rooty()
        w = x + self.window.winfo_width()
        h = y + self.window.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, w, h))
        img.save("interface.png")
        print("Image sauvegardée sous 'interface.png'")
        print("Image sauvegardée dans :", os.path.abspath("interface.png"))


    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.run()
