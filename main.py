# ficihier qui fait tourner l'ensemble



from interface import Interface
from traitement import *

if __name__ == "__main__":
    fenetre = Interface()

    # la faut faire faire une boucle ou on fait rouler le robot et choper le tableau au fur et a mesure
    


    # TRAITEMENT
    tableau_arrondie = arrondire_point(tableau_réaliste ,aggrandissement,decalage_x,decalage_y)
    tableau_corrige = corriger_point(tableau_arrondie) 
    test1 = relierpoint(tableau_corrige, distance_min,aggrandissement,decalage_x,decalage_y,rayon,fenetre)
    #test2 = afficher_point(tableau_réaliste,distance_min,aggrandissement,decalage_x,decalage_y,'purple')
    #test3 = afficher_point(tableau_corrige,distance_min,aggrandissement,decalage_x,decalage_y,'green')
    test4 = afficher_point(tableau_arrondie,distance_min,aggrandissement,decalage_x,decalage_y,'blue', fenetre)
    #meme_point = point_egaux(tableau_corrige)
    #print(f"Il y a {meme_point} point égaux")
    fenetre.run()