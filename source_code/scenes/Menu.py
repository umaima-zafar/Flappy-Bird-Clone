import pygame as pg
import sys

class Menu:
    def __init__(self):
        self.width = 500
        self.height = 600

        self.load_assets()

    # EVENTS 
    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.play_rect.collidepoint(event.pos):
                    return "PLAY"
                elif self.quit_rect.collidepoint(event.pos):
                    pg.quit() 
                    sys.exit()
        return None

    # UPDATE
    def update(self, dt):
        pass  

    # DRAW
    def draw(self, screen):
        screen.blit(self.bg_img, (0, 0))
        screen.blit(self.play_img, self.play_rect)
        screen.blit(self.logo, self.logo_rect)
        screen.blit(self.quit_img, self.quit_rect)

    # SETUP 
    def load_assets(self):
        # background
        self.bg_img = pg.image.load("assets/bg.png").convert()
        self.bg_img = pg.transform.scale(self.bg_img, (self.width, self.height))

        # LOGO 
        self.logo = pg.image.load("assets/logo.png").convert_alpha()
        self.logo = pg.transform.scale_by(self.logo, 0.3)  
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.midtop = (self.width // 2, 100)

        # PLAY BUTTON
        self.play_img = pg.image.load("assets/play.png").convert_alpha()
        self.play_img = pg.transform.smoothscale(self.play_img, (115, 45))

        # QUIT BUTTON
        self.quit_img = pg.image.load("assets/quit_btn.png").convert_alpha()
        self.quit_img = pg.transform.smoothscale(self.quit_img, (115, 45))

        # layout
        spacing = 70
        center_y = 400 

        self.play_rect = self.play_img.get_rect()
        self.play_rect.centery = center_y
        self.play_rect.centerx = self.width // 2 - spacing    

        self.quit_rect = self.quit_img.get_rect()
        self.quit_rect.centery = center_y
        self.quit_rect.centerx = self.width // 2 + spacing
 


