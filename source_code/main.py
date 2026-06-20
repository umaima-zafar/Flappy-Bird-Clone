import pygame as pg
import sys

from scenes.Menu import Menu
from scenes.Play import Play

pg.init()

# WINDOW
WIDTH, HEIGHT = 500, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")

clock = pg.time.Clock() 

# SCENE 
scene = Menu()   

# MAIN LOOP
while True:
    dt = clock.tick(60) / 1000  
  
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    #current scene handles input
    result = scene.handle_events(events)

    # scene switching
    if result == "PLAY":
        scene = Play()

    # updating & drawing current scene
    scene.update(dt)
    scene.draw(screen)

    pg.display.update()  #drawing the screen or elements on screen doesn't show it; this line is needed to actually show and update the frames



