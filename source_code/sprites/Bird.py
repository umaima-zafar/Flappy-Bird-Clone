import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self, scale_factor):
        super().__init__()

        self.width = 500
        self.height = 600

        self.image_list = [
            pg.transform.scale_by(pg.image.load('assets/birdup.png').convert_alpha(), scale_factor),
            pg.transform.scale_by(pg.image.load('assets/birddown.png').convert_alpha(), scale_factor)
        ]
        
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = (self.height // 2) - 100

        self.y_speed = 0
        self.gravity = 10
        self.gravity_on = False

        self.flap_acc = 250

        self.animation_counter = 0

        wing = 'assets/audio_wing.wav'
        hit = 'assets/audio_hit.wav'
        point = 'assets/audio_point.wav'
        die = 'assets/audio_die.wav'

        pg.mixer.init()

        self.wing_sound = pg.mixer.Sound(wing)
        self.hit_sound = pg.mixer.Sound(hit)
        self.point_sound = pg.mixer.Sound(point)
        self.die_sound = pg.mixer.Sound(die)

    def update(self, dt):
        if self.gravity_on: 
            self.play_animation()
            self.y_speed += self.gravity*dt
            self.rect.y += self.y_speed 

            if self.rect.y <= 0 and self.flap_acc == 250:
                self.rect.y = 0  
                self.flap_acc = 0  
            elif self.rect.y > 0 and self.flap_acc == 0:
                self.flap_acc = 250

    def flap(self, dt):
        self.y_speed = -self.flap_acc*dt
        self.wing_sound.play() 

    def play_animation(self):
        if self.animation_counter == 5:
            self.image = self.image_list[self.image_index]

            if self.image_index == 0: 
                self.image_index = 1
            else: 
                self.image_index = 0

            self.animation_counter = 0
        
        self.animation_counter += 1

    def reset_pos(self):
        self.rect.centerx = 100
        self.rect.centery = (self.height // 2) - 100
        self.y_speed = 0
        self.animation_counter = 0