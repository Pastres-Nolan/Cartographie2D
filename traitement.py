# fichier pour traiter les données récupérées


import tkinter as tk
from math import sqrt
import random as rd
import numpy as np

window = tk.Tk()
canvas = tk.Canvas(window, bg = 'white', width=900, height=500)
canvas.pack()
distance_min = 3
aggrandissement = 23
decalage_x = 450
decalage_y = 250
rayon = 5
def position_tracking():
    data = np.load("positions.npy", allow_pickle=True)
    return data.tolist()

tableau_réaliste=position_tracking()





'''
def afficher_point(tableau_pts,distance_min,aggrandissement,decalage_x,decalage_y,couleur):
    for pt1 in range(len(tableau_pts)):
        x1 = tableau_pts[pt1][0]
        y1 = tableau_pts[pt1][1]
        x1p_affichage = decalage_x + x1*aggrandissement -rayon
        x2p_affichage = decalage_x + x1*aggrandissement + rayon
        y1p_affichage = decalage_y + y1*aggrandissement -rayon
        y2p_affichage = decalage_y + y1*aggrandissement + rayon
        point = canvas.create_oval(x1p_affichage, y1p_affichage, x2p_affichage, y2p_affichage, fill=couleur)
'''

def relierpoint(tableau_pts,distance_min,aggrandissement,decalage_x,decalage_y,rayon,fenetre):
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
                line = fenetre.create_line(x1_affichage ,y1_affichage ,x2_affichage ,y2_affichage ,fill = "black")

   

    
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

def afficher_point(tableau_pts,distance_min,aggrandissement,decalage_x,decalage_y,couleur,fenetre):
    for pt1 in range(len(tableau_pts)):
        x1 = tableau_pts[pt1][0]
        y1 = tableau_pts[pt1][1]
        x1p_affichage = x1 - rayon
        x2p_affichage = x1 + rayon
        y1p_affichage = y1 - rayon
        y2p_affichage = y1 + rayon
        point = fenetre.create_oval(x1p_affichage, y1p_affichage, x2p_affichage, y2p_affichage, fill=couleur)