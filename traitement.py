# fichier pour traiter les données récupérées
"""

Code pour merge l'interface et le traitement des données
Code toujours en cours de modification
"""

import tkinter as tk
from math import sqrt
import tkinter.messagebox as tkm


class interface :
    
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




showtime_interface = interface()    


distance_min = 3
aggrandissement = 23
decalage_x = 450
decalage_y = 250
rayon = 5

# tableau pour les test à dégager après
tableau=[(0,0),(2,8),(4,8),(6,8),(8,8),(9,7),(11,-3),(9,3),(9,1),(9,-1),(9,-3),(9,5),(13,-3),(15,-3),(16,-4),(16,-6),(16,-8),(14,-8),(12,-8),(10,-8),(8,-8),(6,-8),(4,-8),(2,-8),(0,-8),(-2,-8),(-4,-8),(-6,-8),(-8,-8),(-8,-6),(-8,-4),(-8,-2),(-8,0),(-8,2),(-8,4),(-8,6),(-8,8),(-6,8),(-4,8),(-2,8),(0,8)]
tableau_réaliste=[(32.653990387916565, -70.37491798400879), (-42.493802309036255, 22.5876584649086), (-37.66455948352814, -60.05956530570984), (-31.90612494945526, 46.60826623439789), (7.774793356657028, -63.29124569892883), (-8.85116159915924, 46.8517541885376), (26.032811403274536, -59.11096930503845), (-28.433534502983093, 36.19241714477539), (44.0132737159729, -42.39335358142853), (-3.177701309323311, 56.35762810707092), (11.164865642786026, -52.56150960922241), (25.615930557250977, 16.710180044174194), (-38.48676681518555, -33.89624059200287), (30.01987338066101, -11.342930048704147), (-39.79261815547943, 38.09795081615448), (15.331165492534637, 19.681741297245026), (-58.203381299972534, 18.192391097545624), (27.189067006111145, 4.61454875767231), (-48.81076514720917, 24.394164979457855), (9.39517617225647, 52.67293453216553), (-44.59964334964752, 5.561868101358414), (-37.614306807518005, 17.80865341424942), (-52.47160792350769, -1.9790902733802795), (-49.274659156799316, 21.302612125873566), (-47.46662080287933, 0.4555132705718279), (-46.257343888282776, 22.789941728115082), (-13.551042973995209, -26.03687345981598), (-23.084300756454468, 62.28222846984863), (40.65965414047241, -33.549392223358154), (-35.235795378685, 51.60511136054993), (50.84819793701172, -24.517254531383514), (-29.05036211013794, -14.327116310596466), (62.521177530288696, 7.829726487398148), (19.067226350307465, -52.6955783367157), (59.09321904182434, 13.771551847457886), (24.728961288928986, -44.90949511528015), (59.51218008995056, -1.394825056195259), (-26.746109127998352, -27.93770730495453), (20.446717739105225, -52.21531391143799), (-11.088642477989197, -39.51830267906189), (31.286436319351196, -50.219106674194336), (-65.06592035293579, 3.5842839628458023), (-47.83654808998108, -34.42429602146149), (-66.57535433769226, 19.277173280715942), (-42.176562547683716, -33.12143087387085), (-82.81156420707703, 7.534122467041016), (-78.30973863601685, -12.543822824954987), (-78.74554395675659, 4.7332920134067535), (-77.50597596168518, -16.07194095849991), (-84.80573892593384, 2.015037089586258), (-85.61519384384155, -16.53687059879303), (-67.59197115898132, 52.9438853263855), (-71.04811668395996, -12.815701961517334), (-84.35047268867493, 4.864003136754036), (-78.39850783348083, -8.558432757854462), (-88.62941265106201, 7.65380784869194), (-38.24123740196228, -15.654848515987396), (-71.22387886047363, 53.6013662815094), (-84.28698778152466, -20.258361101150513), (-44.582611322402954, 39.85431790351868), (-141.1825656890869, 2.9847944155335426), (-72.36403822898865, 62.17878460884094), (-129.85222339630127, -5.535401031374931), (-106.62322044372559, 65.39576053619385), (-104.17730808258057, -26.732558012008667), (-105.35495281219482, 26.530751585960388), (-79.33878302574158, -59.72895622253418), (-98.60799908638, 7.362568378448486), (-107.58352279663086, -64.24442529678345), (-68.54076385498047, 5.177443474531174), (-108.29176902770996, -70.11246681213379), (-72.67352938652039, 2.504439279437065), (-168.72018575668335, -25.767934322357178), (-112.71758079528809, -6.660833954811096), (-122.11133241653442, -8.348029851913452), (-87.47493624687195, -71.83620929718018), (-67.60253310203552, -6.3546136021614075), (-73.74957799911499, -81.51620626449585), (-84.61489677429199, -4.849525913596153), (-52.258509397506714, -53.160762786865234)]
tableau_réaliste= []

for i in range(len(tableau)):
    x, y = tableau[i]
    x += rd.uniform(-0.9, 0.9)
    y += rd.uniform(-0.9, 0.9)
    tableau_réaliste.append((x, y))



def relierpoint(tableau_pts,distance_min,aggrandissement,decalage_x,decalage_y,rayon):
    for pt1 in range(len(tableau_pts)):
        x1 = tableau_pts[pt1][0]
        y1 = tableau_pts[pt1][1]
       
        for pt2 in range(pt1 + 1, len(tableau_pts)):
            x2 = tableau_pts[pt2][0]
            y2 = tableau_pts[pt2][1]
            distance = sqrt((x2-x1)**2 + (y2-y1)**2)

            if distance <= distance_min and distance != distance_min :
                x1_affichage = decalage_x + x1*aggrandissement
                x2_affichage = decalage_x + x2*aggrandissement
                y1_affichage = decalage_y + y1*aggrandissement
                y2_affichage = decalage_y + y2*aggrandissement
                line = showtime_interface.canvas.create_line(x1_affichage ,y1_affichage ,x2_affichage ,y2_affichage ,fill = "black")

    
def corriger_point(tableau_colision):
    ecart = 20
    x = "à_corriger_x"
    y = "à_corriger_y"

    tableau_corrige = [[pt[0], pt[1]] for pt in tableau_colision]

    for pt1 in range(len(tableau_colision)):
        x1, y1 = tableau_colision[pt1]
        point_aligne_x = []
        point_aligne_y = []

        for pt2 in range(len(tableau_corrige)):
            x2, y2 = tableau_corrige[pt2]

            if abs(x1 - x2) < ecart and abs(y1 - y2)> ecart/4 :
                tableau_corrige[pt2][0] = x
                point_aligne_x.append(pt2)

            if abs(y1 - y2) < ecart and abs(x1 - x2)> ecart/4 :
                tableau_corrige[pt2][1] = y
                point_aligne_y.append(pt2)

        if len(point_aligne_x) != 0:
            Xmoy = 0
            for i in range(len(point_aligne_x)):
                pt_x = point_aligne_x[i]
                Xmoy += tableau_colision[pt_x][0]
            Xmoy = Xmoy / len(point_aligne_x)

            for i in range(len(tableau_corrige)):
                if tableau_corrige[i][0] == x:
                    tableau_corrige[i][0] = Xmoy

        if len(point_aligne_y) != 0:
            Ymoy = 0
            for i in range(len(point_aligne_y)):
                pt_y = point_aligne_y[i]
                Ymoy += tableau_colision[pt_y][1]
            Ymoy = Ymoy / len(point_aligne_y)

            for i in range(len(tableau_corrige)):
                if tableau_corrige[i][1] == y:
                    tableau_corrige[i][1] = Ymoy

    return tableau_corrige

def arrondire_point(tableau_pts, aggrandissement, decalage_x, decalage_y):
    for pt1 in range(len(tableau_pts)):
        x1 = tableau_pts[pt1][0]
        y1 = tableau_pts[pt1][1]
        x1_affichage = decalage_x + x1 * aggrandissement - rayon
        y1_affichage = decalage_y + y1 * aggrandissement - rayon
        x = round(x1_affichage, -1)
        y = round(y1_affichage, -1)
        print(x, y)
        tableau_pts[pt1] = (x, y)  # remplace entièrement le tuple
    return tableau_pts
        
def point_egaux(tableau):
    pt_egaux = 0
    for i in range (len(tableau)):
        for j in range(i+1,len(tableau)):
            if tableau[i][0] == tableau[j][0] and tableau[i][1] == tableau[j][1] :
                pt_egaux += 1
    
    return pt_egaux

def afficher_point(tableau_pts,distance_min,aggrandissement,decalage_x,decalage_y,couleur):
    for pt1 in range(len(tableau_pts)):
        x1 = tableau_pts[pt1][0]
        y1 = tableau_pts[pt1][1]
        x1p_affichage = x1 - rayon
        x2p_affichage = x1 + rayon
        y1p_affichage = y1 - rayon
        y2p_affichage = y1 + rayon
        point = showtime_interface.canvas.create_oval(x1p_affichage, y1p_affichage, x2p_affichage, y2p_affichage, fill=couleur)


tableau_arrondie = arrondire_point(tableau_réaliste ,aggrandissement,decalage_x,decalage_y)
tableau_corrige = corriger_point(tableau_arrondie) 
#print(tableau_corrige)
test1 = relierpoint(tableau_corrige, distance_min,aggrandissement,decalage_x,decalage_y,rayon)
#test2 = afficher_point(tableau_réaliste,distance_min,aggrandissement,decalage_x,decalage_y,'purple')
#test3 = afficher_point(tableau_corrige,distance_min,aggrandissement,decalage_x,decalage_y,'green')
test4 = afficher_point(tableau_arrondie,distance_min,aggrandissement,decalage_x,decalage_y,'blue')


#meme_point = point_egaux(tableau_corrige)
#print(f"Il y a {meme_point} point égaux")

showtime_interface.draw()