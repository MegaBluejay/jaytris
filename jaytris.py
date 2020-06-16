import pygame as pg
import sys
import pathlib
from pygame.locals import *
from logic import color, Field

pg.init()
cell_size = 50
line_width = 2
size = w,h = round((cell_size*10+line_width*2)*3/2),cell_size*20+line_width*2
black = color('black')
white = color('white')
sidebar_rect = pg.Rect(0,0,w//3,h)
main_game_rect = pg.Rect(w//3,0,w-w//3,h)

screen = pg.display.set_mode(size)
sidebar = screen.subsurface(sidebar_rect)
main_game = screen.subsurface(main_game_rect)
screen.fill(black)
sidebar.fill(white)

def draw_empty():
    main_game.fill(black)
    for i in range(11):
        pg.draw.line(main_game,white,(i*cell_size,0),(i*cell_size,20*cell_size),2)
    for i in range(21):
        pg.draw.line(main_game,white,(0,i*cell_size),(10*cell_size,i*cell_size),2)

def fill_cell(x,y,c):
    return pg.draw.rect(main_game,c,pg.Rect(x*cell_size+line_width,(19-y)*cell_size+line_width,
                                            cell_size-line_width,cell_size-line_width))

field = Field()
mino = field.spawn()
clock = pg.time.Clock()
DOWNCLOCK,CLEARCLOCK = range(USEREVENT,USEREVENT+2)
pg.time.set_timer(DOWNCLOCK,300)
font = pg.font.Font(None,20)

while 1:
    for event in pg.event.get():
        if event.type==QUIT:
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key in [K_UP,K_x]:
                mino.rotright()
            elif event.key==K_z or (event.mod & KMOD_CTRL):
                mino.rotleft()
            elif event.key==K_LEFT:
                mino.left()
            elif event.key==K_RIGHT:
                mino.right()
            elif event.key in [K_DOWN,K_SPACE]:
                while mino.down():
                    pass
                mino = field.spawn()
                if field.need_clear():
                    pg.time.set_timer(CLEARCLOCK, 100)
        elif event.type==DOWNCLOCK:
            if not mino.down():
                mino = field.spawn()
        elif event.type==CLEARCLOCK:
            pg.time.set_timer(CLEARCLOCK,0)
            field.clear()

    if not mino.ok:
        sys.exit()

    clock.tick(60)
    sidebar.fill(white)
    fps = font.render(str(round(clock.get_fps())),True,black)
    sidebar.blit(fps,(0,0))

    draw_empty()
    for i in range(10):
        for j in range(20):
            c = field.get(i,j).value
            fill_cell(i,j,c)
    pg.display.flip()
