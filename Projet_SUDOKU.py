### Informations ###
'''
On se place dans le dossier désiré et on rentre le nom de la grille vers la ligne 590.

Recommandations :

Pas de 4 calligraphié avec une barre centrale verticale, pas de sudoku de taille inférieure à 300*300, pas de sudoku au format autre que RVB ou RVBA,  chaque chiffre doit être présent au moins une fois dans la grille (sinon il faut rajouter une image centrée pour chaque chiffre manquant  ayant une taille de l'ordre de grandeur des chiffres de la grille dans le dossier dans lequel on a placé l'image de la grille) et l'image de sudoku doit être centrée avec des bordures noires. Enfin la grille et les chiffres doivent être noirs et le fond blanc.

'''


## Import des bibliothèques nécessaires

import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import chdir,getcwd,mkdir 
from time import clock


## Déclaration de deux variables globales qui prennent les coordonnées des chiffres sur la grille

tableaudecoordonnéesx=[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
tableaudecoordonnéesy=[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
# On prendra les coordonnées du point le plus en haut à gauche de chaque chiffre

## Fonctions de fabrication du vecteur du chiffre reconnu 


def rapportfrontauxhautbas(imagecadrée,ligne):
    '''fonction qui calcul le rapport frontal haut ou bas '''
    rapport=np.mean(imagecadrée[ligne])   #np.mean fait la moyenne des pixels du bord haut ou bas de chiffre centré 
    return rapport


def rapportfrontalcentre(imagecadrée):
    '''fonction qui calcul le rapport frontal de la ligne du centre '''
    taille2=imagecadrée.shape
    lignecentre=taille2[0]//2
    rapport=np.mean(imagecadrée[lignecentre])   #np.mean fait la moyenne des pixels de la ligne du centre du chiffre centré
    return rapport
   
    
def rapportfrontauxdroitegauche(imagecadrée,colonne):
    '''fonction qui calcul le rapport frontal droite ou gauche '''
    rapport=np.mean(imagecadrée[:,colonne])     #np.mean fait la moyenne des pixels de la colonne droite et gauche  du chiffre centré
    return rapport
    
def pointcentre(imagecadrée):
    '''fonction qui prend la couleur du point central de l'image du chiffre centré '''
    taille2=imagecadrée.shape
    lignecentre=taille2[0]//2 #On prend la position y du point du centre en divisant par deux la hauteur du chiffre
    colonnecentre=taille2[1]//2 #On prend la position x du point du centre en divisant par deux la largeur du chiffre
    return imagecadrée[lignecentre,colonnecentre] #On renvoit la couleur du pixel voulu(0 pour noir et 1 pour blanc ...)
    
def pointhautcentre(imagecadrée):
    '''fonction qui prend la couleur du point central de la ligne délimitant le premier quart  du deuxieme quart de l'image du chiffre centré'''
    taille2=imagecadrée.shape
    lignecentre=taille2[0]//4 # On prend la position y de la ligne délimitant le premier quart  du deuxieme quart de l'image en divisant par quatre la hauteur du chiffre
    colonnecentre=taille2[1]//2 # On prend la position x du point du centre en divisant par deux la largeur du chiffre
    return imagecadrée[lignecentre,colonnecentre] # On renvoit la couleur du pixel voulu
    
def pointbascentre(imagecadrée):
    '''fonction qui prend la couleur du point central de la ligne délimitant l'avant dernier quart du dernier quart de l'image du chiffre centré '''
    taille2=imagecadrée.shape
    lignecentre=(taille2[0]//4)*3#On prend la position y de la ligne délimitant l'avant dernier quart du dernier quart de l'image  en multipliant par 3/4 la hauteur du chiffre
    colonnecentre=taille2[1]//2 #On prend la position x du point du centre en divisant par deux la largeur du chiffre
    return imagecadrée[lignecentre,colonnecentre] #On renvoit la couleur du pixel voulu
    
def pointbastiers(imagecadrée):
    '''fonction qui prend la couleur du point central de la ligne delimitant le deuxieme et troisieme tiers de l'image du chiffre centré '''
    taille2=imagecadrée.shape
    lignecentre=(taille2[0]//3)*2#On prend la position y de la ligne delimitant le deuxieme et troisieme tiers de l'image en multipliant par 2/3 la hauteur du chiffre
    colonnecentre=taille2[1]//2#On prend la position x du point du centre en divisant par deux la largeur du chiffre 
    return imagecadrée[lignecentre,colonnecentre] #On renvoit la couleur du pixel voulu

def pointcotemilieudroitgauche(imagecadrée,colonne):
    '''fonction qui prend la couleur du point central du bords droit ou gauche de l'image du chiffre centré'''
    taille2=imagecadrée.shape
    lignecentre=taille2[0]//2 #On prend la position y du point du centre en divisant par deux la hauteur du chiffre      
    imagecadrée[lignecentre,colonne]# colonne vaut soit 0, c'est à dire la premiere colonne soit taille[1]-1 qui correspond à la dernière colonne
    return imagecadrée[lignecentre,colonne]#On renvoit la couleur du pixel voulu
    
def pointcotetiershautgauchedroite(imagecadrée,colonne):
    '''fonction qui prend la couleur du point situé à 1/3 du bord droit ou gauche de l'image du chiffre centré'''
    taille2=imagecadrée.shape
    lignecentre=taille2[0]//3 #On prend la position y de la ligne délimitant le premièr et deuxieme tiers de l'image en multipliant par 1/3 la hauteur du chiffre
    imagecadrée[lignecentre,colonne]# colonne vaut soit 0, c'est à dire la premiere colonne soit taille[1]-1 qui correspond à la dernière colonne
    return imagecadrée[lignecentre,colonne] #On renvoit la couleur du pixel voulu
    
def pointcotetiersbasgauchedroite(imagecadrée,colonne):
    '''fonction qui prend la couleur du point situé à 2/3 du bord droit ou gauche de l'image du chiffre centré'''
    taille2=imagecadrée.shape
    lignecentre=(taille2[0]//3)*2#On prend la position y de la ligne delimitant le deuxieme et troisieme tiers de l'image en multipliant par 2/3 la hauteur du chiffre
    imagecadrée[lignecentre,colonne]# Colonne vaut soit 0, c'est à dire la premiere colonne soit taille[1]-1 qui correspond a la dernière colonne
    return imagecadrée[lignecentre,colonne] # on renvoit la couleur du pixel voulu

def imagemoitieligneh(imagecadrée):
    '''fonction qui prend le rapport de pixels de la partie supérieure (c'est à dire la proportion de pixels noirs par rapport à la proportion de pixels blancs) '''
    taille2=imagecadrée.shape
    lignecentre=taille2[0]//2
    demie=imagecadrée[0:lignecentre,:]# Les bords droit et gauche restent inchangés, par contre on coupe l'image à sa moitié en ne prenant que la moitié haute
    rapport=np.mean(demie)
    return rapport
    
def imagemoitieligneb(imagecadrée):
    '''fonction qui prend le rapport de pixels de la partie inférieure (c'est à dire la proportion de pixesl noirs par rapport à la proportion de pixels blancs) '''
    taille2=imagecadrée.shape
    lignecentre=taille2[0]//2
    demie=imagecadrée[lignecentre:,:] # Les bords droit et gauche restent inchangés, par contre on coupe l'image à sa moitié en ne prenant que la moitié basse
    rapport=np.mean(demie)
    return rapport    
   
def imagemoitiecolonneg(imagecadrée):
    '''fonction qui prend le rapport de pixels de la partie gauche (c'est à dire la proportion de pixels noirs par rapport à la proportion de pixels blancs) '''
    taille2=imagecadrée.shape
    demie=taille2[1]//2
    demie=imagecadrée[:,0:demie] # Les bords haut et bas restent inchangés, par contre on coupe l'image à sa moitié en ne prenant que la moitié gauche
    rapport=np.mean(demie)
    return rapport
    
def imagemoitiecolonned(imagecadrée):
    '''fonction qui prend le rapport de pixels de la partie droite (c'est à dire la proportion de pixels noirs par rapport à la proportion de pixels blancs) '''
    taille2=imagecadrée.shape
    demie=taille2[1]//2
    demie=imagecadrée[:,demie:] # Les bords haut et bas restent inchangés, par contre on coupe l'image à sa moitié en ne prenant que la moitié droite
    rapport=np.mean(demie)
    return rapport

def vector(imagecadrée):
    '''fonction qui construit le vecteur du chiffre, c'est à dire un tableau contenant les diverses caractéristiques du chiffre, en appelant les fonctions spécifiques définies plus haut'''
    
    vecteur=[0]*18 # liste qui prend les caractéristiques du chiffre
    # On appelle une par une les fonctions définies plus haut en leur envoyant la matrice associée à un chiffre et parfois d'autres données comme la taille de cette matrice
    h=rapportfrontauxhautbas(imagecadrée,0)
    b=rapportfrontauxhautbas(imagecadrée,imagecadrée.shape[0]-1)
    g=rapportfrontauxdroitegauche(imagecadrée,0)
    d=rapportfrontauxdroitegauche(imagecadrée,imagecadrée.shape[1]-1)
    rc=rapportfrontalcentre(imagecadrée)
    
    c=pointcentre(imagecadrée)
    bc=pointbascentre(imagecadrée)
    hc=pointhautcentre(imagecadrée)
    bt=pointbastiers(imagecadrée)
    
    ilh=imagemoitieligneh(imagecadrée)
    ilb=imagemoitieligneb(imagecadrée)
    il=abs(ilh-ilb)# Permet de savoir si les parties haute et basse ont la meme proportion de pixels noirs et ainsi déceler une symétrie par exemple
    icg=imagemoitiecolonned(imagecadrée)
    icd=imagemoitiecolonneg(imagecadrée)
    ic=abs(icg-icd)# Permet de savoir si les parties droite et gauche ont la meme proportion de pixels noirs et ainsi déceler une symétrie par exemple
    
    pcmg=pointcotemilieudroitgauche(imagecadrée,0)
    pcmd=pointcotemilieudroitgauche(imagecadrée,imagecadrée.shape[1]-1)
    pcthg=pointcotetiershautgauchedroite(imagecadrée,0)
    pcthd=pointcotetiershautgauchedroite(imagecadrée,imagecadrée.shape[1]-1)
    pctbd=pointcotetiersbasgauchedroite(imagecadrée,imagecadrée.shape[1]-1)
    pctbg=pointcotetiersbasgauchedroite(imagecadrée,0)
    
    vecteur=[h,b,g,d,c,bc,hc,bt,pcmg,pcmd,pcthg,pctbd,pcthd,pctbg,np.mean(imagecadrée),il,ic,rc]
    # les éléments np.mean(imagecadrée) et rc ne sont pas utilisés directement dans le programme mais ont été utiles dans la fabrication des vecteurs
    return vecteur 

##Fonction de reconnaissance de caractère

def devinechiffre(vecteurtrouvé):
    '''Fonction qui reconnait un caractère grace à des vecteurs de référence composés de 14 données statistiques'''
    
    # Exemple : on envoit le vecteur [0.53846157, 0.69230771, 0.68181819, 0.68181819, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.63636363, 0.13986015, 0.042207837, 0.46153846], à quel nombre correspond ce vecteur ?
    
    tableaudevecteursdereference=[[0.75 , 0.35 , 0.85 , 0.85 ,0.0, 0.2, 0.2, 0.0, 1.0, 1.0, 0.5, 0.8, 0.8 , 1.0  ],[0.7 , 0.0 , 0.78, 0.75, 0.5, 1.0, 1.0, 0.2, 1.0, 1.0, 1.0, 1.0, 0.5 , 1.0 ],[0.55 , 0.5 , 0.75 , 0.7,0.2, 1.0, 1.0, 1.0 ,1.0, 1.0 , 1.0, 0.5, 0.5 , 1.0],[0.78 , 0.79 , 0.84 , 0.85, 1.0, 0.2, 0.8, 0.2, 1.0, 1.0, 1.0, 0.2, 1.0, 0.2],[0.25 , 0.55 , 0.85 , 0.70 ,1.0, 1.0, 1.0, 1.0, 1.0, 0.6, 0.8, 0.0, 1.0, 1.0],[0.66 , 0.6 , 0.6 , 0.6 , 1.0, 1.0, 1.0, 1.0, 0.0, 0.8, 0.5, 0.2, 1.0 , 0.2],[0.0 , 0.75, 0.88 , 0.84, 0.4, 0.6, 1.0, 0.4, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 ],[0.55 , 0.75 , 0.6 , 0.7 ,0.1, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7, 0.2, 0.8 , 0.2],[0.75 , 0.7 , 0.75 , 0.72 , 0.7, 1.0, 1.0, 0.6, 0.8, 0.2, 0.1, 0.5, 0.2, 1.0],[0.72, 0.6 , 0.83, 0.1 , 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.8, 0.0, 0.0, 1.0 ]]
   # Vecteur de référence des chiffres 1 à 9 avec un dizième vecteur destiné aux 1 sans la barre du bas, ils ont été fabriqués empiriquement avec plusieurs chiffres de polices différentes
   
    tableaudesoustactions=np.zeros((10,14) , float)# Création du tableau qui prend les écarts entre le vecteur de référence et le vecteur trouvé. 10 lignes car dix comparaisons (une par vecteur) et 14 colonne car 14 écarts pour chaque comparaison
    
    for  i in range (0,10,1): # On fait défiler un part un les vecteurs de référence (vecteur de référence du 1 puis vecteur de référence du 2, etc)
        for j in range(0,14,1): # On calcul l'écart entre un élément du vecteur de référence et celui du vecteur trouvé correspondant .....
            tableaudesoustactions[i][j]=abs(vecteurtrouvé[j]-tableaudevecteursdereference[i][j])#...que l'on place dans le tableau de soustractions
   
    # Suite de l'exemple, on obtient le tableaudesoustraction suivant  :   
    #[[ 0.21153843  0.34230771  0.16818181  0.16818181  1.          0.8         0.8
    #   1.          0.          1.          0.5         0.2         0.8         0.        ]valeur absolue(vecteur - vecteur du 1)
    # [ 0.16153843  0.69230771  0.09818181  0.06818181  0.5         0.          0.
    #   0.8         0.          1.          1.          0.          0.5         0.        ]valeur absolue(vecteur - vecteur du 2)
    # [ 0.01153843  0.19230771  0.06818181  0.01818181  0.8         0.          0.
    #   0.          0.          1.          1.          0.5         0.5         0.        ]valeur absolue(vecteur- vecteur du 3 )
    # [ 0.24153843  0.09769229  0.15818181  0.16818181  0.          0.8         0.2
    #   0.8         0.          1.          1.          0.8         1.          0.8       ]valeur absolue(vecteur - vecteur du 4)
    # [ 0.28846157  0.14230771  0.16818181  0.01818181  0.          0.          0.
    #   0.          0.          0.6         0.8         1.          1.          0.        ]valeur absolue(vecteur - vecteur du 5)
    # [ 0.12153843  0.09230771  0.08181819  0.08181819  0.          0.          0.
    #   0.          1.          0.8         0.5         0.8         1.          0.8       ]valeur absolue(vecteur - vecteur du 6)
    # [ 0.53846157  0.05769229  0.19818181  0.15818181  0.6         0.4         0.
    #   0.6         0.          1.          1.          0.          1.          0.        ]valeur absolue(vecteur- vecteur du 7)
    # [ 0.01153843  0.05769229  0.08181819  0.01818181  0.9         0.          0.
    #   0.          0.          1.          0.7         0.8         0.8         0.8       ]valeur absolue(vecteur - vecteur du 8)
    # [ 0.21153843  0.00769229  0.06818181  0.03818181  0.3         0.          0.
    #   0.4         0.2         0.2         0.1         0.5         0.2         0.        ]valeur absolue(vecteur - vecteur du 9)
    # [ 0.18153843  0.09230771  0.14818181  0.58181819  0.          0.          1.
    #   0.          0.          0.          0.8         1.          0.          0.        ]]valeur absolue(vecteur - vecteur du 1 sans barre)

    tableaudesommes=[0.0]*10 #Tableau qui prend la somme des écarts observés pour chaque comparaison
    
    for i in range (0,10,1):
        somme=np.sum(tableaudesoustactions[i])#On somme les écarts observés pour chaque comparaison ....

        tableaudesommes[i]=somme#... que l'on place dans le tableau de sommes
        
    #Suite de l'exemple, tableaudesommes vaut: [6.9902097702026369, 4.820209770202637, 4.0902097702026365, 7.0655943489074708, 4.0171329021453861, 5.2774825191497801, 5.55251748085022, 5.1692307233810419, 2.225594348907471, 3.8038461446762089], le vecteur se rapproche donc le plus d'un 9 car c'est la somme des : valeur absolue(vecteur - vecteur du 9) qui donne le plus petit résultat : 2.225594348907471.
       
        #La comparaison aboutissant à une somme d'écart la plus petite est celle mettant en jeu le vecteur de référence se rapprochant le plus du caractère mis à l'épreuve    
    for  i in range (15,17,1):#Quelques caractéristiques fondamentales qui permettent d'éliminer d'office un chiffre (sa somme de différences est remplacée par 10 pour l'éliminer dans tableaudesommes)
        if vecteurtrouvé[15]<0.1 and vecteurtrouvé[16]<0.1:#symetrie surface haut/bas droite/gauche élevée par exemple caractéristique d'un 8
            tableaudesommes[2]=10.0 #pas 3 car plus de pixels noirs à droite qu'à gauche
            tableaudesommes[3]=10.0 #pas 4 car plus de pixels noirs à droite qu'à gauche
        if vecteurtrouvé[15]>0.1 and vecteurtrouvé[16]>0.1:#symetrie surface haut/bas droite/gauche faible
            tableaudesommes[7]=10.0 #pas 8
        if vecteurtrouvé[0]>0.5:    #peu de pixels noirs première ligne du haut
            tableaudesommes[4]=10.0 #pas 5 (car formé d'une barre horizontale en haut)
            tableaudesommes[6]=10.0 #pas 7  (car formé d'une barre horizontale en haut)
        if vecteurtrouvé[1]<0.2:    #beaucoup de pixels noirs sur la dernière ligne du bas
            tableaudesommes[3]=10   #pas 4 car non formé d'une barre horizontale en bas
            tableaudesommes[6]=10   #pas 7 car non formé d'une barre horizontale en bas
            tableaudesommes[8]=10   #pas 9 car non formé d'une barre horizontale en bas
        if vecteurtrouvé[1]>0.2:    #peu de pixels noirs bas
            tableaudesommes[1]=10   #pas 2 car formé d'une barre horizontale en bas
        if vecteurtrouvé[16]<0.10:  #symetrie surface droite/gauche élevée
            tableaudesommes[2]=10   #pas 3 car nettement plus de pixels noirs sur moitié droite
            tableaudesommes[3]=10   #pas 4 car nettement plus de pixels noirs sur moitié droite
        if vecteurtrouvé[16]>0.15:  #symétrie droite/gauche faible
            tableaudesommes[7]=10   #pas 8
        if np.argmin(tableaudesommes)+1==10:#cas du 11ème vecteur qui correspespond au 2ème cas du 1. Si le vecteur  ressemble le plus au vecteur du 1 sans barre, alors c'est un 1 d'où la suite
            tableaudesommes[0]=0
            
    etlechiffreest=np.argmin(tableaudesommes)+1    
    # Le chiffre mystère est celui dont le vecteur caractéristique se rapproche le plus du vecteur à déterminer (c'est a dire dont la somme des différences terme à terme est la plus faible)
    return etlechiffreest
    
## Fonctions de traitement de la grille
 
def grillescan(image4d,image1d,taillex,tailley,ep): #prend en paramètre le sudoku sur une couche et sur 4 couches, la  largeur et la hauteur de la grille et l'épaisseur du bord de la grille
    ''' Fonction qui 'scanne' l'ensemble de la grille dans le but de restituer une liste associée contenant les nombres présents dans la grille'''  
    listedeschiffres=[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # listedeschiffres  reproduit la structure de la grille de sudoku, on va y placer les chiffres detectés. 
    chiffrepourtitre=""
    
    
    for y in range(0,9,1): #On fait défiler les 9 lignes de chiffres du sudoku
        for x in range(0,9,1):# On fait défiler les 9 chiffres d'une ligne du sudoku
            imagecadrée4d=pointage(image4d,image1d,taillex,tailley,x,y,ep) #On appelle la fonction qui va pointer uns case du sudoku et voir s'il y a ou non un nombre dans cette case. 
            imagecadrée1d=imagecadrée4d[:,:,0] #On travaille uniquement sur une couche de l'image car les seules couleurs présentes sont le noir et le blanc
           
            if imagecadrée1d.shape[0]<2: # Si la case pointée à un très petite taille, cela veut tout simplement dire qu'elle est vide
                listedeschiffres[y][x]=0 # On place un 0 dans la liste reproduisant  le remplissage du sudoku
                mpimg.imsave("rien",imagecadrée4d) #Pas particulierement utile, on sauvegarde une image appelée "rien" et contenant une image d'une case vide
            else: # Sinon on pointe une case pleine, c'est à dire contenant un chiffre qui à été cadré et centré par la fonction pointage.
                vecteurtrouvé=vector(imagecadrée1d) # On soumet donc ce chiffre centré à la fonction qui va fabriquer son vecteur caractéristique ...
                listedeschiffres[y][x]=devinechiffre(vecteurtrouvé)#... puis l'envoyer dans la fonction de reconnaissance de caractère. Le caractère trouvé est directement placé dans listedeschiffres.
                chiffrepourtitre=str(listedeschiffres[y][x]) # Transforme le chiffre trouvé en chaine de caractère ...
                mpimg.imsave(chiffrepourtitre,imagecadrée4d) #... pour pouvoir ensuite nommer le fichier image correspondant à l'image du chiffre. 
# Ainsi chaque chiffre, de 1 à 9 fourni une image de lui même qui sera ensuite utilisée dans l'étape de report des chiffres sur la grille. Tout les chiffres de 1 à 9 doivent être présents dans la grille initiale

    return listedeschiffres # Renvoit  une liste contenant les chiffres présents dans le sudoku au départ à leur place.

    
    
def plusdelignenicolonne(image4d,image1d,taillex,tailley):
    '''fonction qui efface la grille du sudoku'''
    for i in range(0,tailley):# On teste chaque ligne du sudoku. Si sa moyenne est inférieure a 0.5, on la rend blanche. On prend 0.5 et pas moins car il arrive qu'une des ligne de la grille ne soit pas completement noire on se reserve donc un  peu de marge sans risquer d'effacer une ligne avec des chiffres.
        if np.mean(np.floor(image1d[i]))<0.5 : # La fonction np.floor arrondi par le bas chaque pixel, ainsi même un gris très claire devient noir. Cela permet de ne pas laisser de pixel gris qui polluent la grille et rendent difficile la detection des chiffres
            image4d[i]=1 # Si la moyenne est inférieure a 0.5, on  rend blanche la ligne (1 = pixel blanc)
    for i in range(0,taillex):# même chose pour les colonnes...
        if np.mean(np.floor(image1d[:,i]))<0.5:
            image4d[:,i]=1
    return image4d # On renvoit ainsi le sudoku ... sans la grille !
 

def analyseligne(image,tailley): # Prend l'image d'une case du sudoku pointée ainsi que sa hauteur
    '''fonction qui détecte les lignes ni toutes noires, ni toutes blanches, utilisée pour le centrage d'un nombre '''
    tableaudelignes=[0]*2 # Ce tableau prend la position y de la première et la dernière ligne d'un nombre.
    for i in range(0,tailley): # On fait défiler  les lignes de l'image de haut en bas jusqu'à tomber sur la première ligne ni toute noire ni toute blanche à partir du haut
        if np.mean(image[i])!=0 and np.mean(image[i])!=1 : # Si ligne ni toute noire ni toute blanche
            tableaudelignes[0]=i # On prend la position y de cette ligne (première ligne du nombre).
            break # On sort pour passer au second test
    for j in range(tailley-1,-1,-1): # On fait défiler les lignes de l'image de bas en haut jusqu'à tomber sur la première ligne ni toute noire ni toute blanche à partir du bas
        if np.mean(image[j])!=0 and np.mean(image[j])!=1 :# Si ligne ni toute noire ni toute blanche
            tableaudelignes[1]=j # On prend la position y de cette ligne (dernière ligne du nombre).
            break # On sort définitivement
    return tableaudelignes      # renvoit un tableau de deux cases contenant la premiere et la derniere ligne du nombre
    
def analysecolonne(image,taillex):# Prend l'image d'une case du sudoku pointée ainsi que sa largeur, même principe que analyseligne
    '''fonction qui détecte les colonnes ni toutes noires, ni toutes blanches, utilisée pour le centrage d'un nombre '''
    tableaudecolonnes=[0]*2 # Ce tableau prend la position x de la première et la dernière colonne d'un nombre.
    for i in range(0,taillex):
        if np.mean(image[:,i])!=0 and np.mean(image[:,i])!=1:
            tableaudecolonnes[0]=i
            break
    for j in range(taillex-1,-1,-1):
        if np.mean(image[:,j])!=0 and np.mean(image[:,j])!=1:
            tableaudecolonnes[1]=j
            break
    return tableaudecolonnes        # renvoit un tableau de deux cases contenant la premiere et la derniere colonne du nombre.

    
def recherchebordure(image1d,tailley): # non utilisée dans le programme actuel mais peut être utile pour quelques réajustements si besoin
    '''fonction qui  calcule l'épaisseur de la bordure'''
    ligne=analyseligne(image1d,tailley) 
    epaisseurligne=ligne[0] # On obtient la première ligne non toute noire de la grille et ainsi l'épaisseur de la bordure.
    return epaisseurligne
    
     
def centrage(image4d,image1d,taillex,tailley,x,y):
    '''fonction qui centre le chiffre cadré(enlève les bordures blanches restantes) '''
    ligne=analyseligne(image1d,tailley) # On appelle la fonction qui va délimiter le haut et le bas du chiffre
    colonne=analysecolonne(image1d,taillex) # On appelle la fonction qui va délimiter le coté droit et gauche du chiffre
    
    tableaudecoordonnéesx[x][y]=tableaudecoordonnéesx[x][y]+colonne[0] # Chaque groupe de neuf cases de tableaudecoordonnéesx correspond à la coordonnée x de tous les chiffres d'une colonne du sudoku
    tableaudecoordonnéesy[y][x]=tableaudecoordonnéesy[y][x]+ligne[0] # Chaque groupe de neuf cases de tableaudecoordonnéesy correspond à la coordonnée y de tous les chiffres d'une ligne du sudoku
    # On rajoute aux coordonnées grossières la distance du chiffre par rapport au bords de l'image (qui ont ces coordonnées grossières !)
    imagecadrée4d=image4d[ligne[0]:ligne[1]+1,colonne[0]:colonne[1]+1] # Grace au information recueillies par analyseligne et analysecolonne, on cadre (ou centre) le chiffre
    
    return imagecadrée4d # On renvoit le chiffre cadré.
    
    
def pointage(image4d,image1d,taillex,tailley,x,y,ep):# taillex et tailley correspondent à la largeur et à la hauteur de la grille de sudoku
    '''fonction qui renvoit le chiffre cadré d'une case ciblée'''
    largeurcase=(taillex)/9 #On détermine grossierement la largeur d'une case
    hauteurcase=(tailley)/9 #On détermine grossierement la hauteur d'une case
    
    tableaudecoordonnéesx[x][y]=largeurcase*x #Coordonnées grossières de chaque chiffre auxquelles on rajoutera la distance par rapport à cette coordonnées y du chiffre.
    tableaudecoordonnéesy[y][x]=hauteurcase*y #Coordonnées grossières de chaque chiffre auxquelles on rajoutera la distance par rapport à cette coordonnées x du chiffre.
    
    imagepointée4d=image4d[hauteurcase*y:hauteurcase*(y+1),largeurcase*x:largeurcase*(x+1)]#On pointe une case du sudoku en particuliers
    
    taille=imagepointée4d.shape #On prend la taille (largeur et hauteur) de l'image du chiffre pointé
    taillexx=taille[1]
    tailleyy=taille[0]
    imagepointée1d=imagepointée4d[:,:,0] #On crée une image ne prenant que la première couche de l'image du chiffre pointé
    imagecadrée4d=centrage(imagepointée4d,imagepointée1d,taillexx,tailleyy,x,y) #Maintenant que l'on a ciblé une case, on centre le chiffre centré (s'il existe) de cette case ciblée
    return imagecadrée4d # On renvoit le chiffre centré ( ou cadré)
    
## Fonction qui renvoit les coordonnées de tous les chiffres de la grille
     
def coordonnees(listedeschiffres):
    '''Fonction qui renvoit les coordonnées de tous les chiffres de la grille'''
    
    # Une fois l'ensemble des cases scannées, on obtient tableaudecoordonnéesx et tableaudecoordonnéesy remplies. Seulement certaines cases vides scannées donnent des coordonnées inutiles ! De plus pour chaque chiffre d'une ligne par exemple, la coordonnée x du haut de chacun d'entre eux n'est pas tout a fait la même, on va ainsi prendre la coordonnées x du chiffre ayant la face haute la plus basse pour chaque ligne. On fera de même pour les colonnes.
    
    coordonnéesx=[0]*9 # Prend les coordonnées maximales x (haut du chiffre) pour chaque ligne
    coordonnéesy=[0]*9 # Prend les coordonnées maximales y (coté gauche du chiffre) pour chaque colonne
    matricedeschiffres=np.asarray(listedeschiffres) # On transforme la liste listedeschiffres en matrice
    n=-1
    p=-1
    ecartx,ecarty,coordy,coordx=0,0,0,0
    
    for i in range(0,9): # On prend la coordonnées x du chiffre ayant la face haute la plus basse pour chaque ligne
        coordonnéesx[i]=np.max(tableaudecoordonnéesx[i])
        
    for i in range(0,9):# On prend la coordonnées y du chiffre ayant la face gauche la  plus à droite pour chaque colonne
        coordonnéesy[i]=np.max(tableaudecoordonnéesy[i])
    
    # Il arrive que certaines grilles possèdent des ligne(s) ou colonne(s) entièrement vide(s), ce sont souvent des sudokus de niveaux élevés ! La suite est ainsi destiné à ce cas. Pour faire simple, on va trouver l'écart moyen entre deux chiffres successifs et ainsi définir une suite arithmétique de raison l'écart.
    
    for i in range(0,9): # On fait défiler toutes les lignes de matricedeschiffres(reproduisant on le rapelle, la structure du sudoku).
        if np.max(matricedeschiffres[i])==0:# vérifie s'il existe des lignes vides ...
            coordonnéesy[i]=0 # ...si c'est le cas on remplace la coordonnée x du chiffre ayant la face haute la plus basse pour chaque ligne (ici il n'y avait pas de chiffre sur cette ligne donc la coordonnée choisie n'etait pas intéressante) par 0
        else:#Si la ligne du sudoku comporte bien au moins un chiffre, on calcul l'écart séparant cette ligne de la précédente non vide (si existente) On se base sur le principe Ui=Un+(i-n)*raison 
            ecarty=(coordonnéesy[i]-coordy)/(i-n)# On cherche l'écart entre la face gauche de 2 chiffres d'une meme ligne consécutifs
            n=i # On prend la position de la derniere ligne non nulle(de 1 a 9)
            coordy=coordonnéesy[i]# On prend la position de la derniere ligne non nulle ( coordonnée y)
        if np.max(matricedeschiffres[:,i])==0:# vérifie s'il existe des colonnes vides... même principe que pour les lignes, d'ailleurs, bien souvent, ecartx et ecarty sont similaires !
            coordonnéesx[i]=0 
        else:
            ecartx=(coordonnéesx[i]-coordx)/(i-p)# On cherche l'écart entre le haut de 2 chiffres d'une meme colonne consécutifs
            p=i
            coordx=coordonnéesx[i]
    
    for i in range(0,9):
        if np.max(matricedeschiffres[i])==0:# On donne aux lignes vides du sudoku pour coordonnées coordy (cet à dire la coordonnées x du chiffre ayant la face haute la plus basse de la dernière ligne non nulle) à laquelle on enlève (ou rajoute) un cetains nombre de fois l'ecarty sur le principe Ui=Un-(n-i)*raison
            coordonnéesy[i]=coordy-ecarty*(n-i) 
        if np.max(matricedeschiffres[:,i])==0:# 
            coordonnéesx[i]=coordx-ecartx*(p-i) 
        
    return  coordonnéesx,coordonnéesy # On renvoit les coordonnées des actuels et futurs nombres de la grille de sudoku

## Fonctions de remplissage de la grille

def imagedunombre(nombreint):
    '''Fonction qui lie à un nombre une image de lui même'''
    nombrestr=str(nombreint) # On tranforme le nombre en chaine de caractère
    nombre=mpimg.imread(nombrestr+".png") # On ouvre une image de lui même, créee précedemment (vers ligne 250)
    
    return nombre # On retourne l'image du nombre voulu
    
    
def replacechiffre(image4d,nombre,colonne,ligne): # colonne et ligne correspondent aux coordonnées x et y du point le plus en haut à gauche de l'endroit où l'on va placer un chiffre
    '''Fonction qui place un nombre trouvé dans la grille'''
    
    # On va remplir toute les cases vides du sudoku par les nombres trouvés
    
    taille=nombre.shape #On prend la largeur et la hauteur du chiffre cadré
    taillex=taille[1]
    tailley=taille[0]
    for i in range(colonne,colonne+taillex,1):# On fait défiler les colonnes de la grille, de la colonne la plus à gauche composant le futur chiffre à celle la plus à droite (ainsi i varie taillex fois)
        for j in range(ligne,ligne+tailley,1):# On fait défiler les lignes de la grille, de la ligne la plus en haut composa&nt le futur chiffre à celle la plus en bas (ainsi i varie tailley fois)
            image4d[j,i,0]=nombre[j-ligne,i-colonne,0] # On remplace chaque pixel pointé de la grille du sudoku par celui du chiffre que l'on veut placer dans la case
            image4d[j,i,1]=nombre[j-ligne,i-colonne,1]
            #image4d[j,i,2]=nombre[j-ligne,i-colonne,2] # On peut jouer sur les couleurs en enlevant une ou plusieurs couches du nombre afin de faire ressortir les chiffres rajoutés !
    
    return image4d # On retourne la grille avec un chiffre en plus
    
    
def completergrille(coordonneesx,coordonneesy,listedesresutats,listedeschiffres,image4d): # listedesresutats est composée de l'ensemble des chiffres du sudoku
    '''Fonction qui place tous les nombres trouvés dans la grille'''
    grilleresolue=np.copy(image4d)
    for y in range(0,9,1): # On fait défiler les lignes de la grille (plus précisement de la liste listedeschiffres, qui représente la grille de sudoku)
        for x in range(0,9,1): # On fait défiler les colonnes de la grille (plus précisement de la liste listedeschiffres, qui représente la grille de sudoku)
            if listedeschiffres[y][x]==0: # Si la case est vide ...
                nombre=imagedunombre(listedesresutats[y][x])
                grilleresolue=replacechiffre(grilleresolue,nombre,int(coordonneesx[x]),int(coordonneesy[y])) #...on place le nombre trouvé dans la grille (on applique la fonction floor sur les coordonnées pour avoir un arrondi des coordonnnées). On a associé le nombre à une image de nombre créee et enregistrée précedemment grace à l'instruction "nombre=imagedunombre(listedesresutats[y][x])"
    
    return grilleresolue # On retourne la grille remplie


## Fonction auxiliaire d'affichage du sudoku


def affich(SUD):
    '''Fonction qui affiche le sudoku pour plus de lisibilité. Utilisée lors de la confection du programme uniquement et non dans le programme final'''
    for i in range(0,9):
        for j in range(0,9):
            if type(SUD[i][j])==int:
                print(SUD[i][j], end='')
            else:
                print("0", end='')
            print(" ", end='')
            if j%3==2: print(" ", end='')
        print("\n", end='')
        if i%3==2: print("\n", end='')
        
        
## Fonction de résolution du sudoku


def resol1(SUD,nul):                     #définition de la fonction de simplification utilisant les éléments donnés
    g=[]
    test=False
    for i in range(0,len(nul)):  
        '''on retire dans un premier temps les impossibilités de placement'''
        x=0
        y=0
        z=0
        for n in SUD[nul[i][0]]:
            SUD[nul[i][0]][nul[i][1]]=[x for x in SUD[nul[i][0]][nul[i][1]] if x!=n]    #élimination des doublons sur les lignes
        for m in range(0,9):
            SUD[nul[i][0]][nul[i][1]]=[y for y in SUD[nul[i][0]][nul[i][1]] if y!=SUD[m][nul[i][1]]]    #élimination des doublons sur les colonnes
        for o in range(0,9):
            l=int((nul[i][0])-(nul[i][0])%3)
            c=int((nul[i][1])-(nul[i][1])%3)
            '''repérage de la case du nombre manquant'''
            SUD[nul[i][0]][nul[i][1]]=[z for z in SUD[nul[i][0]][nul[i][1]] if z!=SUD[l+int(o%3)][c+int((o-o%3)/3)]]     #élimination des doublons dans les cases
        if len(SUD[nul[i][0]][nul[i][1]])==1: 
            SUD[nul[i][0]][nul[i][1]]=SUD[nul[i][0]][nul[i][1]][0]      #remplacement des possibilités uniques par leur valeur
            g.append(i)
            test=True
    a=0
    for j in g:
        nul.remove(nul[j-a])     #supression de la liste des "0" des nouveaux éléments définis
        a+=1
    return(test)
    
    
def resol2(SUD,nul):    
    '''par la suite, on cherche a imposer la présence de chaque chiffre pour simplifier encore la grille'''
    test=False
    for i in range(0,9):
        for j in range(1,10):        #défilement des chiffres à vérifier
            l=0
            for k in range(0,9):
                if type(SUD[i][k])==list and SUD[i][k].count(j)>0:  #repérage des listes d'une ligne possédant un chiffre unique
                    l+=1
                    tmp=k
            if l==1:
                SUD[i][tmp]=j       #remplacement de cette liste par ce chiffre
                nul.remove([i,tmp])
                test=True
    return(test)
    
    
def resol3(SUD,nul):    
    test=False
    for i in range(0,9):
        for j in range(1,10):        #défilement des chiffres à vérifier        
            l=0
            for k in range(0,9):
                if type(SUD[k][i])==list and SUD[k][i].count(j)>0:  #repérage des listes d'une colonne possédant un chiffre unique
                    l+=1
                    tmp=k
            if l==1:
                SUD[tmp][i]=j       #remplacement de cette liste par ce chiffre
                nul.remove([tmp,i])
                test=True
    return(test)
    
def resol4(SUD,nul):    
    test=False
    for i in range(0,9):
        for j in range(1,10):        #défilement des chiffres à vérifier                    
            l=0
            for k in range(0,9):
                if type(SUD[(int((i-i%3)))+int((k-k%3)/3)][(3*int(i%3))+int(k%3)])==list and SUD[(int((i-i%3)))+int((k-k%3)/3)][(3*int(i%3))+int(k%3)].count(j)>0:  #repérage des listes d'un carré possédant un chiffre unique
                    l+=1
                    tmp=k
            if l==1:
                SUD[(int((i-i%3)))+int((tmp-tmp%3)/3)][(3*int(i%3))+int(tmp%3)]=j       #remplacement de cette liste par ce chiffre
                nul.remove([(int((i-i%3)))+int((tmp-tmp%3)/3),(3*int(i%3))+int(tmp%3)])
                test=True
    return(test)

def verif(SUD):
    '''vérifie les cases ou il n'y a pas de possibilités (indique donc si une supposition est valable ou pas)'''
    for i in range(0,9):
        for j in range(0,9):
            if SUD[i][j]==[]:
                return(True)
                    
def resolution(test,SUD,nul):
    global tableaudecopiedenul
    global tableaudecopiedeSUD
    global soluce
    global tableaudecopiedecompteur
    test=True
    while test:
        test=False
        '''on éxecute une à une chaque fonction de résolution en boucle, jusqu'à-ce que celle ci ne modifie plus la grille afin qu'elle n'interfere pas avec les autres fonctions nécessitant une grille "propre", reformée à l'aide de la fonction 1 executée systématiquement entre les autres fonctions'''
        while resol1(SUD,nul):
          
            test=True
        while resol4(SUD,nul):
          
            test=True
        while resol1(SUD,nul):
           
            test=True
        while resol3(SUD,nul):
           
            test=True
        while resol1(SUD,nul):
            
            test=True
        while resol2(SUD,nul):
            
            test=True 

 
    soluce=copy.deepcopy(SUD)
    if nul!=[]:#S'il reste des cases a remplir. Si ce n'est plus le cas, c'est fini !
    

        if verif(SUD)==True:#supposition mauvaise 
        
            SUD=copy.deepcopy(tableaudecopiedeSUD[-1])#On recharge la sauvegarde précédente
            nul=copy.deepcopy(tableaudecopiedenul[-1])#On recharge la sauvegarde précédente
            tableaudecopiedecompteur[-1]=tableaudecopiedecompteur[-1]+1#En incrementant son compteur de 1
            
            
        else:#Supposition qui ne pose pour le moment pas de probleme

            tableaudecopiedeSUD.append(copy.deepcopy(SUD))#On crée une nouvelle sauvegarde
            tableaudecopiedenul.append(copy.deepcopy(nul))#On crée une nouvelle sauvegarde
            tableaudecopiedecompteur.append(0)#On remet le compteur a zero
            
        suggest=SUD[nul[0][0]][nul[0][1]]
        nombreimp=suggest[tableaudecopiedecompteur[-1]]#nombreimp prend un chiffre en particuliers a tester
        SUD[nul[0][0]][nul[0][1]]=nombreimp#On remplace la case du sudoku concernée par le chiffre imposé
        nul.remove(nul[0])#On enlève la premiere case de nul
        
        #Si on vient de prendre le dernier chiffre, on reviendra en arriere pour le prochain si il y a une erreur
        if tableaudecopiedecompteur[-1]==len(suggest)-1:
            tableaudecopiedecompteur.pop()
            tableaudecopiedeSUD.pop()
            tableaudecopiedenul.pop()
        
        resolution(test,SUD,nul)
        

## Appel des fonctions 
  
chdir("F:\\test")

fichier=input("Comment s'appelle la photo de la grille?: ")#ex : sudoku13.png
sudoku=mpimg.imread(fichier)   # On charge l'image de la grille de sudoku

to=clock() # Début du chronomètre

image4d=np.copy(sudoku) # On fait une copie de l'image de la grille de sudoku
image1d=image4d[:,:,0] # On prend uniquement la première couche de l'image de la grille de sudoku  pour faciliter les opérations (elles sont toutes similaires car le sudoku est en noir et blanc !)


taille=image4d.shape # On prend la taille de l'image de la grille de sudoku (largeur et hauteur)
taillex=taille[1]
tailley=taille[0] 

image4d=plusdelignenicolonne(image4d,image1d,taillex,tailley)# On enlève la grille
image4d=np.round(image4d) # On prend uniquement la première couche de l'image de la grille de sudoku sans grille pour faciliter les opérations. Note : round peut être remplacer par floor qui arrondi à l'entier inférieure. On préfère round mais parfois floor donne de meilleurs résultats !
image1d=np.round(image1d) # Idem
ep=recherchebordure(image1d,tailley)  # On calcule l'épaisseur de la bordure du sudoku. Non utilisée ici mais peut être utilisée pour divers ajustements.


    
listedeschiffres=grillescan(image4d,image1d,taillex,tailley,ep) # On récupère l'ensemble des chiffres du sudoku dans une liste (voir plus haut dans la fontion dédiée)
SUD=copy.deepcopy(listedeschiffres)

listedesresutats=[[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0]]


nul=[]
for i in range(0,9):
    for j in range(0,9):
        if SUD[i][j]==0:
            nul.append([i,j])       #rangement des coordonnées des "0" dans une matrice
            SUD[i][j]=[1,2,3,4,5,6,7,8,9]       #remplacement des "0" par les chiffres à trier
           
test=False

soluce=[] 
tableaudecopiedeSUD=[]
tableaudecopiedenul=[]
tableaudecopiedecompteur=[]
resolution(test,SUD,nul)


listedesresutats=copy.deepcopy(soluce)

coordonneesx=coordonnees(listedeschiffres)[0] # On applique la fontion de récupération des coordonnées en envoyant comme paramètres listedeschiffres, utile si certaines colonnes du sudoku sont vides
coordonneesy=coordonnees(listedeschiffres)[1] # On applique la fontion de récupération des coordonnées en envoyant comme paramètres listedeschiffres, utile si certaines lignes du sudoku sont vides


grilleresolue=completergrille(coordonneesx,coordonneesy,listedesresutats,listedeschiffres,sudoku) # Donne la grille résolue et complétée...

plt.imshow(grilleresolue) # ... que l'on va ensuite afficher 
plt.show()


print("Le temps d'éxecution du programme est :",clock()-to,"s")  # Fin du chronomètre et affichage du temps d'execution du programme


















