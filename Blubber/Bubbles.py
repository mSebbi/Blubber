import pygame
from pygame.constants import( QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN)
import os
from random import randint
import time
import sys

class Settings:
    pygame.display.set_caption("Bubbler")
    w_width = 800
    w_height = 600
    w_border = 50
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "pictures")
    sound_path = os.path.join(file_path, "game_sounds")
    

class Background(object):
    def __init__(self, filename):
        self.imageo = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = pygame.transform.scale(self.imageo, (Settings.w_width, Settings.w_height)).convert()
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Score(object):
    def __init__(self):
        self.black = 0,0,0
        self.count = 0
        self.font = pygame.font.SysFont("comicsans",30, True , True)
        self.text = self.font.render("Score : "+str(self.count),1,self.black)
        
    def show_score(self, screen):
        screen.blit(self.text,(660 ,0))


    def score_up(self):
        self.count += 1
        self.text = self.font.render("Score : "+str(self.count),1,self.black)


class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.diameter = 40
        self.image_og = pygame.image.load(os.path.join(Settings.image_path, "Blase.png ")).convert_alpha()
        self.image = pygame.transform.scale(self.image_og, (self.diameter, self.diameter))
        self.rect = self.image.get_rect()
        self.mousex, self.mousey = pygame.mouse.get_pos()
        self.rect.left = randint(Settings.w_border, Settings.w_width - Settings.w_border)
        self.rect.top = randint(Settings.w_border, Settings.w_height - (Settings.w_border * 2))
        self.cd = pygame.time.get_ticks()
        self.cds = 1400
        self.ran = pygame.time.get_ticks()
   



    def update(self):
        self.scale()
        pass

    def scale(self):
        if self.cooldown_scale():
            self.diameter += randint(1, 4)
            c = self.rect.center
            self.image = pygame.transform.scale(self.image_og, (self.diameter, self.diameter))
            self.rect = self.image.get_rect()
            self.rect.center = c
            self.cd = pygame.time.get_ticks() + self.cds

            if self.diameter > 75:  
                pygame.quit()

            if self.ran > 1000:
                self.cds -= 100

    def cooldown_scale(self):
        return pygame.time.get_ticks() >= self.cd




    def events(self):
        pass
 
    def draw(self, screen):
        screen.blit(self.image,self.rect )

class Cursor(object):
    def __init__(self):
        self.cursorx = pygame.image.load(os.path.join(Settings.image_path, "cursor.png")).convert_alpha()
        self.cursor  = pygame.transform.scale(self.cursorx, (50, 50))
        self.rect = self.cursor.get_rect()

    def drawmouse(self, screen):
        pygame.mouse.set_visible(False)
        screen.blit(self.cursor,(pygame.mouse.get_pos()))

    

class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.w_width, Settings.w_height))
        self.clock = pygame.time.Clock()
        self.runn = False
        self.score = Score()
        self.cursor = Cursor()
        self.bubble = pygame.sprite.Group()
        self.background = Background("Hintergrund.jpg")
        self.sound_mouse = pygame.mixer.Sound(os.path.join(Settings.sound_path, "Click.wav"))
        self.sound_pop = pygame.mixer.Sound(os.path.join(Settings.sound_path, "pop.wav"))
        self.music = pygame.mixer.music.load(os.path.join(Settings.sound_path, "game_music.mp3"))
        self.pause_rect = pygame.draw.rect(self.screen , (136, 136 ,136), [400 , 400,400 , 400])
        self.bubble_cd = pygame.time.get_ticks()
        self.bubble_cds = 1000
        self.k = 1
        self.ram = pygame.time.get_ticks()
        
        


        
    def run(self):
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.runn = True
        self.pause = False


        while self.runn:
            self.clock.tick(60)
            self.watch_for_events()
            
           
 
            if not self.pause:
                self.draw()
                self.events()
                self.bubble.update()
                pygame.mixer.music.unpause()
                

    def bubble_cooldown(self):
        return pygame.time.get_ticks() >= self.bubble_cd

        

    def events(self):
        for i in range(1):
            if self.bubble_cooldown():
                if self.bubble_cd > 1000:
                    self.bubble_cds -= 5                 
                if len(self.bubble)< self.k:
                    self.bubble.add(Bubble())
                    self.bubble_cd = pygame.time.get_ticks() + self.bubble_cds
                    self.k += 1



    def draw(self):
        self.background.draw(self.screen)
        self.bubble.draw(self.screen)
        self.score.show_score(self.screen)
        self.cursor.drawmouse(self.screen)
        
    
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.runn = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.draw.rect(self.screen , (136, 136 ,136), [400 , 400,400 , 400])
                    self.pause = not self.pause
                    

            if not self.pause and event.type == MOUSEBUTTONDOWN:
                self.sound_mouse.play()
                for bubble in self.bubble:
                    if bubble.rect.collidepoint(event.pos):
                        bubble.kill()
                        self.score.score_up()
                        self.sound_pop.play()
                
                    
                
if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOWS_POS'] = "50, 1100"
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    