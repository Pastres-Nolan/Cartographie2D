from math import sqrt, degrees, atan2
import tkinter as tk

class Traitement:
    aggrandissement = 2
    decalage_x = 600
    decalage_y = 400
    distance_min= 12
    angle_min = 20
    rayon = 5


    def distance(self, p1, p2):
        distance = sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        return distance

    def angle_entre_2_pt(self, p1, p2, p3):
        angle = degrees(atan2(p3[1]-p2[1], p3[0]-p2[0]) - atan2(p1[1]-p2[1], p1[0]-p2[0]))
        if angle < 0:
            return angle + 360
        else :
            return angle


    def trouver_contour_pas_ouf(self, tableau_pts):
        tableau_pts = tableau_pts.copy()
        contour = [tableau_pts.pop(0)]
        while len(tableau_pts) != 0:
            dernier = contour[-1]
            plus_proche = tableau_pts[0]
            self.distance_min = self.distance(dernier, plus_proche)
            for point in tableau_pts[1:]:
                d = self.distance(dernier, point)
                if d < self.distance_min:
                    self.distance_min = d
                    plus_proche = point
            contour.append(plus_proche)
            tableau_pts.remove(plus_proche)
        return contour


    def detecter_segments(self, tableau_contour):
        segments = []
        segment_aligner = [tableau_contour[0], tableau_contour[1]]
        
        for i in range(2, len(tableau_contour)):
            angle = self.angle_entre_2_pt(segment_aligner[-2], segment_aligner[-1], tableau_contour[i])
            
            if abs(angle - 180) < self.angle_min:
                segment_aligner.append(tableau_contour[i])
            else:
                segments.append(segment_aligner)
                segment_aligner = [segment_aligner[-1], tableau_contour[i]]
        
        segments.append(segment_aligner)
        return segments


    def jolie_contour(self, segments):
        contour = []
        for segment in segments:
            if len(segment) > 2:
                contour.append(segment[0])
                contour.append(segment[-1])
            else:
                contour.extend(segment)
        contour.append(contour[0])
        return contour


    def afficher_points(self, tableau_pts, couleur= 'red', rayon= 4, canvas = None):
        for pt in range(len(tableau_pts)):
            x1 = tableau_pts[pt][0]
            y1 = tableau_pts[pt][1]
            x1p_affichage = self.decalage_x + x1*self.aggrandissement - self.rayon
            x2p_affichage = self.decalage_x + x1*self.aggrandissement + self.rayon
            y1p_affichage = self.decalage_y + y1*self.aggrandissement - self.rayon
            y2p_affichage = self.decalage_y + y1*self.aggrandissement + self.rayon
            canvas.create_oval(x1p_affichage, y1p_affichage, x2p_affichage, y2p_affichage, fill=couleur)


    def afficher_contour(self, tableau_pts, couleur='white', largeur=2, canvas = None):
        contour = self.trouver_contour_pas_ouf(tableau_pts)
        segments = self.detecter_segments(contour)
        contour_final = self.jolie_contour(segments)
        for i in range(len(contour_final)-1):
            x1 = self.decalage_x + contour_final[i][0]* self.aggrandissement
            y1 = self.decalage_y + contour_final[i][1]*self.aggrandissement
            x2 = self.decalage_x + contour_final[i+1][0]*self.aggrandissement
            y2 = self.decalage_y + contour_final[i+1][1]*self.aggrandissement
            canvas.create_line(x1, y1, x2, y2, fill=couleur, width=largeur)


if __name__ == "__main__":
    tableau_pts = [(8,-4),(-8,10),(-8,-2),(11,2),(10,10),(2,-8),(-2,-8),(12,6),(-10,4),(12,4),(0,10),(9,-2),(-2,10),(-4,-6),(-6,10),(-10,0),(8,10),(10,0),(4,-8),(6,10),(-10,2),(12,8),(0,-8),(2,10),(6,-8),(-4,10),(-10,6),(12,10),(-6,-4),(7,-6),(-8,10),(-10,10)]
    
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1200, height=800, bg="black")
    canvas.pack()
    t = Traitement()
    t.afficher_points(tableau_pts, canvas = canvas)
    t.afficher_contour(tableau_pts, canvas = canvas)
    

    
    root.mainloop()