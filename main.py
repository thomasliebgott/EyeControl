# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:10:27 2021
rendu 25 mars 
@author: LeGall - Liebgott
"""
# importation des bibliothèques
import cv2
import win32api, win32con

#def variable 
cg = 0; #compteur frame clic gauche  
cd = 0; #compteur frame clic droit 

#determination ouverture camera 
cap = cv2.VideoCapture(0); 

#ouverture camera 
ret, img = cap.read()

#def du template a detecter en allant chercher l'image du template 
template = cv2.imread('Capture.png',0)

#determination taille de l'image 
w, h = template.shape[::-1]

match_method = cv2.TM_SQDIFF_NORMED

#match template pour determiner le template sur image 
def matchTemp():
        #realisation de la recherche du template 
    result = cv2.matchTemplate(image_gray, template,match_method)
    
    #determination des contours du template 
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
    if (match_method == cv2.TM_SQDIFF or match_method == cv2.TM_SQDIFF_NORMED):
         matchLoc = minLoc
    else:
         matchLoc = maxLoc
         
    top_right = (matchLoc[0] + w, matchLoc[1] + h)
    
    #determination du centre de X et Y 
    bottom_right = (matchLoc[0] + w, matchLoc[1] + h)
    top_left = (matchLoc[0], matchLoc[1])
    bottom_left = (matchLoc[0], matchLoc[1] + h)
    centerX = int(matchLoc[0] + w/2)
    centerY = int(matchLoc[1] + h/2)
    
    return bottom_right,bottom_left,top_left,top_right,matchLoc,centerX,centerY

#determine le centre du template pour avoir un point determinant la zone de changement 
def middleSquare(image, h2, w2):
    
    point1 = (int(9*w2/20),int(9*h2/20))
    point2 = (int(11*w2/20),int(11*h2/20))
    
    #affichage du rectangle 
    cv2.rectangle(image, point1 , point2 ,(0,0,255),2)
    
    point1s = (int(8*w2/20),int(8*h2/20))
    point2s = (int(12*w2/20),int(12*h2/20))
    
    #affichage du rectangle
    cv2.rectangle(image, point1s , point2s ,(0,0,255),2)

#fonction permetant de def les rectlangles de click 
def rectangleClick(image,h2,w2):
     
    #affiche carée clic droit bleu
    point1r = (int(9*w2/20),(int)(9*h2/20))
    point2r = (int(10*w2/20),(int)(19*h2/40))
    
    cv2.rectangle(image, point1r , point2r ,(255,159,51),2)
    
    #affiche carée clic gauche bleu
    point1l = (int(10*w2/20),(int)(9*h2/20))
    point2l = (int(11*w2/20),(int)(19*h2/40))
    
    cv2.rectangle(image, point1l , point2l ,(255,159,51),2)
        
while cv2.waitKey(1)<0:
    
    #lecture image de la camera 
    ret, image = cap.read()
    
    #changement colorspace pour trouver le template 
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #appel fonction template
    bottom_right,bottom_left,top_left,top_right,matchLoc,centerX,centerY = matchTemp()
    
    #tracer des indicateur de template 
    cv2.rectangle(image, matchLoc, bottom_right ,(0,255,0),1)
    cv2.circle(image,(centerX,centerY), 5, (51,183,255), 2)
    
    # print("top_right",top_right)
    # print("top_left",top_left)
    # print("bottom_left",bottom_left)    
    # print("center",centerX,centerY)
    
    #size camera  
    w2  = cap.get(3)  # float `width`
    h2 = cap.get(4)  # float `height`
    
    #appel de fonction pour tracer rectangle 
    middleSquare(image,h2,w2)
    rectangleClick(image,h2,w2)
     #récupère la position du curseur
    (x,y) = win32api.GetCursorPos();
    
    # print("x et y",x,y)
    # print("center",centerX , centerY)
    
##detection des zones du point et mouvement du curseur en fonction de la zone vitesse lente
    #zone haut a droite 
    if centerX < 9*w2/20 and centerY < 9*h2/20:
        win32api.SetCursorPos((x+3,y-3));
        
        #zone droite
    elif centerX < 9*w2/20 and centerY < 11*h2/20 and centerY > 9*h2/20:
        win32api.SetCursorPos((x+3,y));
    
    #zone bas a droite
    elif centerX < 9*w2/20 and centerY > 11*h2/20:
        win32api.SetCursorPos((x+3,y+3));
        
    #zone haut
    elif centerX < 11*w2/20 and centerX > 9*w2/20 and centerY < 9*h2/20:
        win32api.SetCursorPos((x,y-3));    
        
    #zone haut gauche 
    elif centerX > 11*w2/20 and centerY < 9*h2/20:
        win32api.SetCursorPos((x-3,y-3));
             
    #zone gauche
    elif centerX > 11*w2/20 and centerY < 11*h2/20 and centerY > 9*h2/20:
        win32api.SetCursorPos((x-3,y));
        
    #zone en bas a gauche 
    elif centerX > 11*w2/20 and centerY > 11*h2/20:
        win32api.SetCursorPos((x-3,y+3));        

    #zone en bas 
    elif centerX < 11*w2/20 and centerX > 9*w2/20 and centerY > 11*h2/20:
        win32api.SetCursorPos((x,y+3));    

##detection des zones du point et mouvement ultra rapide #usain Bolt
    #zone haut a droite 
    if centerX < 8*w2/20 and centerY < 8*h2/20:
        win32api.SetCursorPos((x+15,y-15));
        
        #zone droite
    elif centerX < 8*w2/20 and centerY < 12*h2/20 and centerY > 8*h2/20:
        win32api.SetCursorPos((x+15,y));
    
    #zone bas a droite
    elif centerX < 8*w2/20 and centerY > 12*h2/20:
        win32api.SetCursorPos((x+15,y+15));
        
    #zone haut
    elif centerX < 12*w2/20 and centerX > 8*w2/20 and centerY < 8*h2/20:
        win32api.SetCursorPos((x,y-15));    
        
    #zone haut gauche 
    elif centerX > 12*w2/20 and centerY < 8*h2/20:
        win32api.SetCursorPos((x-15,y-15));
             
    #zone gauche
    elif centerX > 12*w2/20 and centerY < 12*h2/20 and centerY > 8*h2/20:
        win32api.SetCursorPos((x-15,y));
        
    #zone en bas a gauche 
    elif centerX > 12*w2/20 and centerY > 12*h2/20:
        win32api.SetCursorPos((x-15,y+15));        

    #zone en bas 
    elif centerX < 12*w2/20 and centerX > 8*w2/20 and centerY > 12*h2/20:
        win32api.SetCursorPos((x,y+15));    

##determination du clic 
    
    #clic droit dans le carré bleu
    if centerX > 9*w2/20 and centerX < 10*w2/20 and centerY > 9*h2/20 and centerY < 19*h2/40:
        cd += 1;
        if cd == 25:
            print("clic droit")
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0);#Appui sur le bout-ton gauche
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0);#Relachement du bouton gauche
            cd = 0;
            
    #clic gauche dans le carré bleu
    if centerX > 10*w2/20 and centerX < 11*w2/20 and centerY > 9*h2/20 and centerY < 19*h2/40:
        cg +=1;
        if cg == 25:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0);#Appui sur le bout-ton gauche
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0);#Relachement du bouton gauche
            print("clic gauche")
            cg =0;
        
    #retournement de l'image 
    image = cv2.flip(image, 1)
    
    #affichage de l'image 
    cv2.imshow("img", image)
    
    
cap.release();           
cv2.destroyAllWindows();




























