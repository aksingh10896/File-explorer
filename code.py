import pygame
import os
import distutils.dir_util
import distutils.file_util
import shutil
import pyautogui
import sys
import threading
from pygame.locals import *
pygame.init()
dirs=[]
fontobj=pygame.font.SysFont('arial bold',30)
for a in range(65,91):
    if os.path.exists("%s:"%chr(a)):
        dirs+=[chr(a)]
home_list=dirs
dissurf=pygame.display.set_mode((1300,800),0,32)
pygame.display.set_caption('FILE EXPLORER')
mousex=0
mousey=0
cp=False
f=0
cpf=''
cpfo=''
start=''
save=''
x=0
g=[]
textrect=[]
while True:
    mouseclicked=False
    dissurf.fill((255,255,255))
    textrect=[]
    hisrect=[]
    if x==0:
        for i in range(len(dirs)):
            textobj=fontobj.render(dirs[i],True,(0,0,0),(255,255,255))
            textrect.append(textobj.get_rect())
            textrect[len(textrect)-1].topleft=(120+300*(i//26),15+30*(i%26))
            dissurf.blit(textobj,textrect[len(textrect)-1])
    else:
        for i in range(len(g)):
            if g[i][0]=='#' and g[i][2]==':':
                text=fontobj.render(g[i][1:-1],True,(0,0,0),(255,255,255))
                hisrect.append(text.get_rect())
                hisrect[len(hisrect)-1].topleft=(120+300*((len(hisrect)-1)//26),15+30*((len(hisrect)-1)%26))
                dissurf.blit(text,hisrect[len(hisrect)-1])
    pygame.draw.rect(dissurf,(0,0,0),[100,0,10,800])
    pygame.draw.rect(dissurf,(0,0,0),[0,0,10,800])
    pygame.draw.rect(dissurf,(0,0,0),[1290,0,10,800])
    pygame.draw.rect(dissurf,(0,0,0),[0,0,1300,10])
    pygame.draw.rect(dissurf,(0,0,0),[0,790,1300,10])
    text=fontobj.render("Back",True,(0,0,0),(255,255,255))
    back=text.get_rect()
    back.topleft=(25,40)
    dissurf.blit(text,back)
    text=fontobj.render("Home",True,(0,0,0),(255,255,255))
    home=text.get_rect()
    home.topleft=(25,160)
    dissurf.blit(text,home)
    text=fontobj.render("Delete",True,(0,0,0),(255,255,255))
    delete=text.get_rect()
    delete.topleft=(20,280)
    dissurf.blit(text,delete)
    text=fontobj.render("Copy",True,(0,0,0),(255,255,255))
    copy=text.get_rect()
    copy.topleft=(25,400)
    dissurf.blit(text,copy)
    text=fontobj.render("Paste",True,(0,0,0),(255,255,255))
    paste=text.get_rect()
    paste.topleft=(25,520)
    dissurf.blit(text,paste)
    text=fontobj.render("History",True,(0,0,0),(255,255,255))
    history=text.get_rect()
    history.topleft=(20,640)
    dissurf.blit(text,history)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEMOTION:
            mousex,mousey=event.pos
        elif event.type==MOUSEBUTTONUP:
            mousex,mousey=event.pos
            mouseclicked=True
    if back.collidepoint(mousex,mousey) and mouseclicked:
        if start!='' and start.count('/')>1:
            start=start[:start.rfind('/')]
            dirs=os.listdir(start)
        elif start.count('/')==1:
            dirs=home_list
            start=''
    if home.collidepoint(mousex,mousey) and mouseclicked:
        dirs=home_list
        start=''
    if f==1:
        for i in range(len(textrect)):
            if textrect[i].collidepoint(mousex,mousey) and mouseclicked:
                
                if os.path.isfile(start+'/'+dirs[i]):
                    os.remove(start+'/'+dirs[i])
                else:
                    shutil.rmtree(start+'/'+dirs[i])
                f=0
                dirs=os.listdir(start)
        continue
    if delete.collidepoint(mousex,mousey) and mouseclicked:
        f=1
    if cp:
        for i in range(len(textrect)):
            if textrect[i].collidepoint(mousex,mousey) and mouseclicked:
                cpf=start+'/'+dirs[i]
                cpfo=dirs[i]
                cp=False
                break
        continue
    if copy.collidepoint(mousex,mousey) and mouseclicked:
        cp=True
    if paste.collidepoint(mousex,mousey) and mouseclicked:
        if cpf!="":
            def paste():
                if os.path.isfile(cpf):
                    distutils.file_util.copy_file(cpf,start)
                else:
                    paths=os.mkdir(start+'/'+cpfo)
                    distutils.dir_util.copy_tree(cpf,start+'/'+cpfo)
            threading.Thread(target=paste).start()
        dirs=os.listdir(start)
        continue
    if history.collidepoint(mousex,mousey) and mouseclicked:
        if x==0:
            h=[]
            file=open('file.py','r')
            g=file.readlines()
            file.close()
            for i in range(len(g)):
                if g[i][0]=='#':
                    h+=[g[i]]
            x=1
        else:
            x=0
    for i in range(len(textrect)):
        if textrect[i].collidepoint(mousex,mousey) and mouseclicked:
            if start=='':
                start=dirs[i]+':/'
            else:
                if os.path.isfile(start+'/'+dirs[i]):
                    os.startfile(start+'/'+dirs[i])
                    save=start+'/'+dirs[i]
                else:
                    start=start+'/'+dirs[i]
                    save=start
                file=open('file.py','a')
                file.write('#'+save+'\n')
                file.close()
            dirs=os.listdir(start)
            break
    for i in range(len(hisrect)):
        if hisrect[i].collidepoint(mousex,mousey) and mouseclicked:
            if os.path.isfile(h[i][1:-1]):
                os.startfile(h[i][1:-1])
            else:
                start=h[i][1:-1]
            dirs=os.listdir(start)
            x=0
            break
    pygame.display.update()

