from math import sqrt, degrees, atan2
import tkinter as tk

class Traitement:
    aggrandissement = 2
    decalage_x = 600
    decalage_y = 400
    distance_min= 12
    angle_min = 20
    rayon = 5
    distance_fermeture = 5
    distance_connexion = 6
    point_min = 9

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

    def trouver_contours_multiple(self, tableau_pts, distance_fermeture=18, distance_connexion=50, point_min = 4):
        tableau_pts = tableau_pts.copy()
        non_utilises = set(tableau_pts)
        utilise = set()
        tous_contours = []

        while len(non_utilises) != 0:
            pt_depart = non_utilises.pop()
            contour = [pt_depart]
            utilise.add(pt_depart)
            pt_actuel = pt_depart

            while True:
                plus_proche = None
                d_min = 9999999999999999999999

                for pt in tableau_pts:
                    if pt in utilise:
                        continue
                    d = self.distance(pt_actuel, pt)
                    if d < d_min and d < distance_connexion:
                        d_min = d
                        plus_proche = pt

                if plus_proche is None:
                    break

                if len(contour) > point_min and self.distance(plus_proche, pt_depart) < distance_fermeture:
                    contour.append(pt_depart)
                    break

                contour.append(plus_proche)
                utilise.add(plus_proche)
                pt_actuel = plus_proche

            if len(contour) > point_min :
                tous_contours.append(contour)
                
            non_utilises = set(tableau_pts) - utilise
        return tous_contours


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
        contours = self.trouver_contours_multiple(tableau_pts)
        for contour in contours:
            segments = self.detecter_segments(contour)
            contour_final = self.jolie_contour(segments)
            for i in range(len(contour_final)-1):
                x1 = self.decalage_x + contour_final[i][0]* self.aggrandissement
                y1 = self.decalage_y + contour_final[i][1]*self.aggrandissement
                x2 = self.decalage_x + contour_final[i+1][0]*self.aggrandissement
                y2 = self.decalage_y + contour_final[i+1][1]*self.aggrandissement
                canvas.create_line(x1, y1, x2, y2, fill=couleur, width=largeur,tags='contour')


if __name__ == "__main__":

    tableau_pts =[(-116.91201030255147, 18.4184848459224), (-72.41144551988505, 14.570366808324628), (-85.29462723309673, 36.656668530909805), (-71.45670424113345, 9.659116729825616), (-56.03223133968331, 44.97559368290209), (-112.2332758388042, 26.258237115885482), (-65.67358635374991, 44.45141592775044), (-60.7584621585736, 24.255068591125482), (-52.01284674499741, 49.05000477264792), (-60.431884456652234, 23.806866375326095), (-68.74726838832208, 45.10558550918697), (-12.545376192777493, 32.7979101325227), (-74.98580249436354, 43.236149522627585), (-66.7436337059178, 47.20633728577047), (-68.00166582501174, 23.508661584018025), (-88.22573005898069, 41.05737819143405), (-64.66550505954005, 20.961662611984377), (-89.31145531013094, 40.496233527895555), (-83.73206746045499, -20.257464863211645), (-88.24755529940077, 38.40870752443766), (-67.11489112376557, 20.86375365524728), (-110.56393964458726, 14.938153382999655), (-69.96781327998143, 18.3478292274882), (-96.16977439184168, -17.708167979013616), (-110.78177563659364, 28.034383792948816), (-109.86381106414736, 24.864118191724476), (-111.63184915643944, 33.0268933563651), (-112.76694122538731, 26.24834269780739), (-112.62415156324792, 35.71143252637195), (-66.87879272060837, 12.716216655134296), (-107.03916825372696, 24.093855970243727), (-39.12396224975373, 63.152644403192035), (-43.296578331366945, 4.144127031425861), (-34.538602894210776, 66.34568190540644), (-102.31430718219966, 22.216080513139467), (-98.84153602561123, 51.8591744857322), (-111.51667255527549, 44.44144807758252), (-68.93320173283513, 29.597073217917092), (-82.54825515537455, 60.14541819489945), (-16.97737242408325, 25.147679333616562), (-50.104640210823035, 36.09290200449578), (-10.603793242102956, 56.69940739123424), (-18.20966858311312, 22.434791950206545), (-11.67926591891299, 60.718108441403615), (-5.659249813041192, 46.25351586678803), (-54.10132430373943, 47.134283338052946), (-36.247046135399955, 16.825176333481025), (-51.569104772527055, 34.13744936277541), (-36.12997401868257, 11.324385620527714), (-53.74532679601824, 30.968313334544757), (-59.43886992018293, 5.65508645326656), (-5.041765539612669, 40.72579697634529), (-60.72821588007016, 8.731557708786069), (-63.59423267751248, 3.664231337110366), (-98.50194577015628, 16.310111764777048), (-61.637849587297936, 30.57150174657228), (-70.07780431585682, -3.138474802900072), (-53.30677989135775, 65.70849529091326), (-105.41199242740369, 44.019019142277834), (-65.47844520973669, 30.316330932965798), (-78.93014824480707, 57.31348754895606), (-15.811134590069175, 26.63261084130376), (-37.72419354402597, 33.749682564450275), (2.7086559079710835, 20.329782768940788), (-30.299542091318976, 3.6414070200963833), (-34.286563557930165, -1.3697582390402003)]

    root = tk.Tk()
    canvas = tk.Canvas(root, width=1200, height=800, bg="black")
    canvas.pack()

    t = Traitement()
    t.afficher_points(tableau_pts, canvas = canvas)
    t.afficher_contour(tableau_pts, canvas = canvas)
    root.mainloop()