import pygame
from pygame import *
 
pygame.init()
 
pygame.display.set_mode((800, 600))
 
boucle = True
while True :
   for event in pygame.event.get():
      if event.type==KEYDOWN :
         print event.key
         if event.key==K_RETURN :
            boucle = False

