import pygame as pg
from random import randint

class Pipe:
    def __init__(self, scale_factor, move_speed):
        self.pipe_up = pg.transform.scale_by(pg.image.load('assets/pipeup.png'), scale_factor)
        self.pipe_down = pg.transform.scale_by(pg.image.load('assets/pipedown.png'), scale_factor)

        self.rect_up = self.pipe_up.get_rect() 
        self.rect_down = self.pipe_down.get_rect()

        self.pipe_distance = 150 

        self.rect_up.x = 500
        self.rect_up.y = randint(250, 500)

        self.rect_down.x = 500
        self.rect_down.y = self.rect_up.y - self.pipe_distance - self.rect_up.height

        self.move_speed = move_speed

    def move_pipes(self, dt):
        self.rect_up.x -= int(self.move_speed * dt)
        self.rect_down.x -= int(self.move_speed * dt)