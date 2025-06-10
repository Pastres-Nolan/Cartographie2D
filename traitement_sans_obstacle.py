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


    def supprimer_point(self, tableau_pts, distance_delete=10):
        resultat = []

        for pt in tableau_pts:
            trop_proche = False
            for autre_pt in resultat:
                if self.distance(pt, autre_pt) < distance_delete:
                    trop_proche = True
                    break
            if not trop_proche:
                resultat.append(pt)

        return resultat

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
        tableau_pts = self.supprimer_point(tableau_pts)
        for pt in range(len(tableau_pts)):
            x1 = tableau_pts[pt][0]
            y1 = tableau_pts[pt][1]
            x1p_affichage = self.decalage_x + x1*self.aggrandissement - self.rayon
            x2p_affichage = self.decalage_x + x1*self.aggrandissement + self.rayon
            y1p_affichage = self.decalage_y + y1*self.aggrandissement - self.rayon
            y2p_affichage = self.decalage_y + y1*self.aggrandissement + self.rayon
            canvas.create_oval(x1p_affichage, y1p_affichage, x2p_affichage, y2p_affichage, fill=couleur,tags='boules')


    def afficher_contour(self, tableau_pts, couleur='white', largeur=2, canvas = None):
        tableau_pts = self.supprimer_point(tableau_pts)
        contour = self.trouver_contour_pas_ouf(tableau_pts)
        segments = self.detecter_segments(contour)
        contour_final = self.jolie_contour(segments)
        for i in range(len(contour_final)-1):
            x1 = self.decalage_x + contour_final[i][0]* self.aggrandissement
            y1 = self.decalage_y + contour_final[i][1]*self.aggrandissement
            x2 = self.decalage_x + contour_final[i+1][0]*self.aggrandissement
            y2 = self.decalage_y + contour_final[i+1][1]*self.aggrandissement
            canvas.create_line(x1, y1, x2, y2, fill=couleur, width=largeur,tags='contour')


if __name__ == "__main__":

    tableau_pts = [(-109.35201711127756, -5.643451095106641), (-106.83283992392951, 43.097082884378615), (-127.95437036544874, 21.46684794007967), (-76.90753995435992, 61.93939591523299), (-103.09782657712542, 63.04196634577943), (-67.5909703279808, 53.658204465106806), (-81.34672577024446, 75.95400256097177), (-103.72370736455044, 3.2712683674236773), (-133.50732542774836, 53.87406326172903), (-106.07864779071953, 4.456479859342185), (-83.36265333125915, 75.77653602991853), (-97.13824149252555, 70.04898560426628), (-57.78105995084264, 43.89724573636862), (-119.53943255617928, 22.509750962921633), (-60.2411323336628, 44.510552335027356), (-116.6347434942293, 21.538732147415136), (-87.54553716002744, 5.249227330424602), (-115.68772025212976, 21.78544266481758), (-53.445514780540265, 38.56271523247425), (-62.892330031807234, 17.135039786951317), (-89.02313233665019, 73.81036067243326), (-63.71598394363329, 67.81349285801008), (-85.55111331751185, 54.31114981905522), (-83.05457140421326, 78.97108942938777), (-52.52940117928201, 50.1191412898783), (-92.08414403195492, 78.65447897101613), (-91.46825726865944, 72.15508509962565), (-69.20092531513639, 82.25212026933988), (-81.87773784838849, 84.24658831839292), (-66.73199609095843, 81.8023963510552), (-72.00709734492116, 87.37647215848712), (-64.75516054423399, 82.19588414673137), (-84.33307516053094, 82.48178147269512), (-66.76268613377661, 89.66467913866062), (-83.77051917557237, 68.31740973348059), (-53.10882720196062, 68.45302660159896), (-82.85965390889316, 70.52142955273995), (-54.53401567308783, 28.080909074147865), (-80.20472938563925, 66.3027054807995), (-93.10994567522148, 20.225522664451503), (-67.08584062861976, 92.42759561505459), (-85.14404575787627, 21.884123963866546), (-115.48910433971307, 73.8053634973011), (-88.5379182683853, 22.01416261771316), (-98.22431111655655, 26.426527986758433), (-47.45987557444388, 66.07001065224343), (-94.62343736158317, 23.077886510246437), (-45.00070674261465, 48.72882030363432), (-45.2367722670259, 41.065349862603725), (-88.98564537463734, 83.87685322800165), (-42.834734338872444, 45.72427751786489), (-42.35614505658502, 48.656062198501814), (-41.56872068082175, 41.848216386877304), (-83.1889840297451, 73.73848624243917)]
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1200, height=800, bg="black")
    canvas.pack()

    t = Traitement()
    t.afficher_points(tableau_pts, canvas = canvas)
    t.afficher_contour(tableau_pts, canvas = canvas)
    root.mainloop()