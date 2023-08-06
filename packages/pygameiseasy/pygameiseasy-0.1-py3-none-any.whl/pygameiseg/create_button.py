import pygame
def get_button_simple(self,width,height,xpos,ypos,mouse,event,mousebutton,screen,color):
    button=pygame.draw.rect(screen,color,pygame.Rect(xpos,ypos,width,height))
    if mouse[0]>=button.x and mouse[0]<=button.x+button.w and mouse[1]>=button.y and mouse[1]<=button.y+button.h:
        if event.type==mousebutton:
            return True
        else:
            return False
    else:
        return False
def get_button_click_animate(self,width,height,xpos,ypos,mouse,event,mousebutton,screen,color,color2):
    button=pygame.draw.rect(screen,color,pygame.Rect(xpos,ypos,width,height))
    if mouse[0]>=button.x and mouse[0]<=button.x+button.w and mouse[1]>=button.y and mouse[1]<=button.y+button.h:
        if event.type==mousebutton:
            color=color2
            return True
        else:
            color=color
            return False
    else:
        return False