import pygame as pg
from sprites.Bird import Bird
from sprites.Pipe import Pipe

class Play:
    def __init__(self):
        self.width = 500
        self.height = 600

        self.scale_factor = 1.4
        self.move_speed = 200  # pixels per sec

        self.bird = Bird(self.scale_factor)
        self.pipes = []
        self.pipe_generate_counter = 101
        self.setup_bg()

        self.key_pressed = False
        self.game_over = False
        self.hit_ground = False
        self.start_monitoring = False 
        self.paused = False
        self.show_resume = False

        self.score = 0
        self.font = pg.font.Font("assets/font.ttf", 21)
        self.score_text = self.font.render(f"Score: 0 ", True, (0, 0, 0))
        self.score_text_rect = self.score_text.get_rect(center=(100, 50))

        self.ground_hit_sound_played = False
        self.pipe_hit_sound_played = False

        self.setup_pause()
        self.read_bestscore()
        self.setup_game_over()

        clock = pg.time.Clock()
        self.dt = clock.tick(60) / 1000

    # EVENTS
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN and self.game_over == False:
                    self.key_pressed = True
                    self.bird.gravity_on = True
                if event.key == pg.K_UP and self.key_pressed and not self.game_over and not self.paused:
                        self.bird.flap(self.dt)
                if event.key == pg.K_ESCAPE:
                   if self.show_resume:
                       self.resume()
                   else:
                       self.pause()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.restart_label_rect.collidepoint(event.pos):
                    self.restart_game()
                if self.restart_btn_rect.collidepoint(event.pos):
                    self.restart_game()
                if self.pause_btn_rect.collidepoint(event.pos):
                   self.pause()
                if self.resume_btn_rect.collidepoint(event.pos):
                   self.resume()

    # UPDATE 
    def update(self, dt):
        if self.paused:
            return  
        if self.key_pressed:
            self.move_ground(dt)
            self.update_pipes(dt)
        self.check_collision()
        self.check_score() 
        self.bird.update(dt)

    # DRAW 
    def draw(self, screen):
        screen.blit(self.bg_img, (0, 0))
        for pipe in self.pipes:
            screen.blit(pipe.pipe_up, pipe.rect_up)
            screen.blit(pipe.pipe_down, pipe.rect_down)
        screen.blit(self.ground1_img, self.ground1_rect)
        screen.blit(self.ground2_img, self.ground2_rect)
        screen.blit(self.bird.image, self.bird.rect)
        
        if self.key_pressed:
            screen.blit(self.pause_btn, self.pause_btn_rect)
       
        if self.show_resume:
            screen.blit(self.resume_btn, self.resume_btn_rect)

        if not self.game_over:
            screen.blit(self.score_text, self.score_text_rect)
        if self.hit_ground:
            screen.blit(self.game_over_img, self.game_over_rect)
            screen.blit(self.overbox, self.overbox_rect)

            screen.blit(self.score_label, self.score_label_rect)
            screen.blit(self.score_value, self.score_value_rect)

            screen.blit(self.best_label, self.best_label_rect)
            screen.blit(self.best_value, self.best_value_rect)

            screen.blit(self.restart_label, self.restart_label_rect)
            screen.blit(self.restart_btn, self.restart_btn_rect)

            screen.blit(self.restart_btn, self.restart_btn_rect)

    # SETTING UP BACKGROUND 

    def setup_bg(self):
        self.bg_img = pg.transform.scale(
            pg.image.load("assets/bg.png").convert(),
            (self.width, self.height)
        )

        self.ground1_img = pg.transform.scale_by(
            pg.image.load("assets/ground.png").convert(),
            self.scale_factor
        )
        self.ground2_img = self.ground1_img.copy()

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right

        self.ground1_rect.y = 450
        self.ground2_rect.y = 450

    # MOVING GROUND

    def move_ground(self, dt):
        movement = int(self.move_speed * dt)

        self.ground1_rect.x -= movement
        self.ground2_rect.x -= movement

        if self.ground1_rect.right <= 0:
            self.ground1_rect.x = self.ground2_rect.right

        if self.ground2_rect.right <= 0:
            self.ground2_rect.x = self.ground1_rect.right

    # SETTING UP PIPES
        
    def update_pipes(self, dt):
        if self.pipe_generate_counter > 100:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0
        self.pipe_generate_counter += 1
       
        for pipe in self.pipes:
                pipe.move_pipes(dt)

        if len(self.pipes) != 0:
            if self.pipes[0].rect_up.right < 0:
                self.pipes.pop(0)

    # CHECKING COLLISION 

    def check_collision(self):
        if(self.bird.rect.colliderect(self.ground1_rect) or 
           self.bird.rect.colliderect(self.ground2_rect)):
            self.key_pressed = False
            self.bird.gravity_on = False
            self.game_over = True
            self.hit_ground = True
            if not self.ground_hit_sound_played:
                self.bird.die_sound.play()
                self.ground_hit_sound_played = True

        if len(self.pipes) != 0:
            if (self.bird.rect.colliderect(self.pipes[0].rect_up) or
                self.bird.rect.colliderect(self.pipes[0].rect_down)):
                 self.key_pressed = False
                 self.game_over = True
                 if not self.pipe_hit_sound_played:
                    self.bird.hit_sound.play()
                    self.pipe_hit_sound_played = True

    # SCORE UPDATION

    def check_score(self):
        if len(self.pipes) > 0:
            if (self.bird.rect.left > self.pipes[0].rect_down.left and 
            self.bird.rect.right < self.pipes[0].rect_down.right and not self.start_monitoring):
                self.start_monitoring = True

            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring == True:
                self.start_monitoring = False
                self.score += 1
                self.bird.point_sound.play()
                self.score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0)) # True or False determines whether the text edges are smoothed (antialiasing)
                self.score_value = self.font.render(f"{self.score}", True, (255, 160, 60))
            
            if self.score > self.best_score:
                self.best_score = self.score
                with open("best_score.txt", "w") as f:
                    f.write(str(self.best_score))
                    self.best_value = self.value_font.render(f"{self.best_score}", True, (255, 160, 60))

    def read_bestscore(self):
        try:
            with open("best_score.txt", "r") as f:
                self.best_score = int(f.read())
        except FileNotFoundError:
            self.best_score = 0

    # PAUSE/RESUME

    def setup_pause(self):
        self.pause_btn = pg.transform.scale_by(pg.image.load("assets/pause.jpg"), 0.3) 
        self.pause_btn_rect = self.pause_btn.get_rect(center=(self.width - 50, 50))

        self.resume_btn = pg.transform.scale_by(pg.image.load("assets/resume.jpg"), 0.3) 
        self.resume_btn_rect = self.resume_btn.get_rect(center=(self.width - 50, 50))

    def pause(self):
        if not self.key_pressed:   
            return
        self.paused = True
        self.show_resume = True
        self.bird.gravity_on = False
        self.bird.y_speed = 0

    def resume(self):
        self.paused = False
        self.show_resume = False
        self.bird.gravity_on = True

    #  RESTART GAME

    def restart_game(self):
        self.score = 0
        self.score_text = self.font.render(f"Score: 0", True, (0, 0, 0))
        self.score_value = self.font.render(f"0", True, (255, 160, 60))
        self.game_over = False
        self.hit_ground = False 
        self.bird.reset_pos()
        self.pipes.clear()
        self.pipe_generate_counter = 101
        self.ground_hit_sound_played = False
        self.pipe_hit_sound_played = False

    # GAME OVER

    def setup_game_over(self):
        box_scale = 0.8
        restart_scale = 0.5

        title_offset_y = -230
        box_offset_y = -40

        padding = 50
        row_spacing = 20
        value_offset_y = 10
        left_col_x = -90
        right_col_x = 80

        # fonts
        self.label_font = self.font
        self.value_font = pg.font.Font("assets/font.ttf", 26)

        # game over title
        self.game_over_img = pg.transform.scale_by(
            pg.image.load("assets/gameover.png").convert_alpha(),
            self.scale_factor
        )
        self.game_over_rect = self.game_over_img.get_rect(
            midtop=(self.width // 2, self.height // 2 + title_offset_y)
        )

        # overbox
        self.overbox = pg.transform.scale_by(
            pg.image.load("assets/overbox.png").convert_alpha(),
            box_scale
        )
        self.overbox_rect = self.overbox.get_rect(
            center=(self.width // 2, self.height // 2 + box_offset_y)
        )

        # score label
        self.score_label = self.label_font.render("Score", True, (0, 0, 0))
        self.score_label_rect = self.score_label.get_rect(
            center=(
                self.overbox_rect.centerx + right_col_x,
                self.overbox_rect.centery - padding
            )
        )

        self.score_value = self.value_font.render("0", True, (255, 160, 60))
        self.score_value_rect = self.score_value.get_rect(
            midtop=(
                self.score_label_rect.centerx,
                self.score_label_rect.bottom + value_offset_y
            )
        )

        # best label
        self.best_label = self.label_font.render("Best", True, (0, 0, 0))
        self.best_label_rect = self.best_label.get_rect(
            center=(
                self.overbox_rect.centerx + right_col_x,
                self.overbox_rect.centery + row_spacing
            )
        )

        self.best_value = self.value_font.render(f"{self.best_score}", True, (255, 160, 60))
        self.best_value_rect = self.best_value.get_rect(
            midtop=(
                self.best_label_rect.centerx,
                self.best_label_rect.bottom + value_offset_y
            )
        )

        # restart
        self.restart_label = self.label_font.render("Restart", True, (0, 0, 0))
        self.restart_label_rect = self.restart_label.get_rect(
            center=(
                self.overbox_rect.centerx + left_col_x,
                self.overbox_rect.centery - padding
            )
        )

        self.restart_btn = pg.transform.scale_by(
            pg.image.load("assets/restart.png").convert_alpha(),
            restart_scale
        )
        self.restart_btn_rect = self.restart_btn.get_rect(
            midtop=(
                self.restart_label_rect.centerx,
                self.restart_label_rect.bottom + value_offset_y
            )
        )
