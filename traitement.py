from math import sqrt
#tableau = Pilotage.pos_colisions



class Traitement :
    
    rayon = 5
    distance_min = 3 
    aggrandissement = 23
    decalage_x = 450
    decalage_y = 250
    
    
    def afficher_point(self, tableau_pts, canvas):
        
        for pt1 in range(len(tableau_pts)):
            x1 = tableau_pts[pt1][0]
            y1 = tableau_pts[pt1][1]
            x1p_affichage = self.decalage_x + x1*self.aggrandissement - self.rayon
            x2p_affichage = self.decalage_x + x1*self.aggrandissement + self.rayon
            y1p_affichage = self.decalage_y + y1*self.aggrandissement - self.rayon
            y2p_affichage = self.decalage_y + y1*self.aggrandissement + self.rayon
            point = canvas.create_oval(x1p_affichage, y1p_affichage, x2p_affichage, y2p_affichage, fill='purple')
    
    
    def relierpoint(self, tableau_pts,canvas):
    
        for pt1 in range(len(tableau_pts)):
            x1 = tableau_pts[pt1][0]
            y1 = tableau_pts[pt1][1]
           
            for pt2 in range(pt1 + 1, len(tableau_pts)):
                x2 = tableau_pts[pt2][0]
                y2 = tableau_pts[pt2][1]
                distance = sqrt((x2-x1)**2 + (y2-y1)**2)
    
                if distance <= self.distance_min and distance != self.distance_min :
                    x1_affichage = self.decalage_x + x1*self.aggrandissement
                    x2_affichage = self.decalage_x + x2*self.aggrandissement
                    y1_affichage = self.decalage_y + y1*self.aggrandissement
                    y2_affichage = self.decalage_y + y2*self.aggrandissement
                    line = canvas.create_line(x1_affichage ,y1_affichage ,x2_affichage ,y2_affichage ,fill = "black")
    
       
    
        
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
            

if __name__ == "__main__" :
    t = Traitement()
    tableau_corrige = Traitement.corriger_point(tableau) 
    t.afficher_point(tableau_corrige)