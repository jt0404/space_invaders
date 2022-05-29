import pygame as pg
from pygame import mixer
from random import randint
from math import sqrt
from player import Player
from enemy import Enemy

class App:
    def __init__(self):
        pg.init()
        self.run = True
        self.screen = pg.display.set_mode((800, 600)) 
        self.player = Player()
        self.enemy = Enemy()
        self.font = pg.font.SysFont('Arial', 40)
        self.game_over_flag = False
        mixer.music.load('audio/bg.mp3')
        mixer.music.play(-1)    

    def draw(self):
        bg = pg.image.load('img/bg.jpg')
        self.screen.blit(bg, (0, 0))

        spaceship = pg.image.load('img/spaceship.png')
        self.screen.blit(spaceship, (self.player.x, self.player.y))
        
        ufo = pg.image.load('img/ufo.png')
        for i in range(self.enemy.no_of_enemies):
            self.screen.blit(ufo, (self.enemy.x[i], self.enemy.y[i]))
        
        if not self.player.bullet_ready:
            player_bullet = pg.image.load('img/bullet.png')
            self.screen.blit(player_bullet, (self.player.bullet_x, self.player.bullet_y))
            
        pg.draw.rect(self.screen, (0, 255, 0), (self.player.x-15, self.player.y+70, self.player.hp, 10))
        
        score_text = self.font.render("SCORE: "+str(self.player.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10)) 
        
        pg.display.update()
        
    def collision(self, x, y):return sqrt( (x - self.player.bullet_x)**2 + ( y - self.player.bullet_y )**2 ) <= 40
    
    def collision2(self, x, y): return sqrt( ( self.player.x - x )**2 + ( self.player.y - y )**2 ) <= 40
    
    def game_over(self):
        bg = pg.image.load('img/bg.jpg')
        self.screen.blit(bg, (0, 0))
        font = pg.font.SysFont('Arial', 60)
        text = font.render("GAME OVER! Your score: "+str(self.player.score), True, (255, 255, 255))
        self.screen.blit(text, (700-text.get_rect().width, 300-text.get_rect().height))
        pg.display.update()
        return True
    
    def message_box(self):
        import tkinter as tk
        from tkinter import messagebox
        mixer.music.stop()
        root = tk.Tk()
        root.attributes('-topmost', True)
        root.withdraw()
        msg = messagebox.askyesno('Replay', 'Play again')
        if msg:
            self.__init__()
        else:
            self.run = False

    def main(self):
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False 
                 
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        self.player.x_change = -2
                        self.player.y_change = 0
                    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                        self.player.x_change = 2
                      
                    if event.key == pg.K_SPACE:
                        if self.player.bullet_ready:
                            player_bullet_sound = mixer.Sound('audio/laser.wav')
                            player_bullet_sound.play()
                            self.player.bullet_x = self.player.x + 16 
                            self.player.bullet_y = self.player.y + 5
                            self.player.fire()
                            
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT and self.player.x_change == -2 or event.key == pg.K_a and self.player.x_change == -2:
                        self.player.x_change = 0
                    if event.key == pg.K_RIGHT and self.player.x_change == 2 or event.key == pg.K_d and self.player.x_change == 2:
                        self.player.x_change = 0
                        
            if self.player.bullet_y <= 0:
                self.bullet_x = self.player.x + 16 
                self.player.bullet_y = self.player.y + 5
                self.player.bullet_ready = True     
                
            if not self.player.bullet_ready:
                self.player.bullet_y -= self.player.bullet_speed       
            
            for i in range(self.enemy.no_of_enemies):
                if self.enemy.y[i] >= 466:
                    self.player.hp = 0
                    
                if self.enemy.bullet_ready[i]:
                    enemy_bullet_sound = mixer.Sound('audio/enemy_laser.wav')
                    enemy_bullet_sound.play()
                    self.enemy.bullet_x[i] = self.enemy.x[i]
                    self.enemy.bullet_y[i] = self.enemy.y[i]
                    self.enemy.bullet_ready[i] = self.enemy.fire()
                    
                if not self.enemy.bullet_ready[i]:
                    if not self.game_over_flag:
                        enemy_bullet = pg.image.load('img/enemy_bullet.png')
                        self.screen.blit(enemy_bullet, (self.enemy.bullet_x[i], self.enemy.bullet_y[i]))
                        self.enemy.bullet_y[i] += 5
                        pg.display.update()
                
                collision = self.collision(self.enemy.x[i], self.enemy.y[i])
                if collision:
                    explosion_sound = mixer.Sound('audio/explosion.wav')
                    explosion_sound.play()
                    self.player.bullet_ready = True
                    self.player.bullet_x = self.player.x + 16 
                    self.player.bullet_y = self.player.y + 5
                    self.enemy.x[i] = randint(0, 735)
                    self.enemy.y[i] = randint(0, 100)
                    self.player.score += 50
                    
                collision2 = self.collision2(self.enemy.bullet_x[i], self.enemy.bullet_y[i])
                if collision2:
                    enemy_hit_sound = mixer.Sound('audio/enemy_hit.wav')
                    enemy_hit_sound.play() 
                    self.enemy.bullet_ready[i] = True
                    self.enemy.bullet_x[i] = self.enemy.x[i]
                    self.enemy.bullet_y[i] = self.enemy.y[i]
                    self.player.hp -= 10
                    
                if self.enemy.bullet_y[i] == self.enemy.y[i] and self.enemy.bullet_x[i] == self.enemy.x[i] and self.enemy.x[i] % 2 == 0:
                    self.enemy.bullet_ready[i] = True    
                
                if self.enemy.bullet_y[i] >= 800:
                    self.enemy.bullet_x[i] = self.enemy.x[i]
                    self.enemy.bullet_y[i] = self.enemy.y[i]
            
            if self.player.hp == 0:
                self.game_over_flag = self.game_over()
            
            self.player.movement()
            self.enemy.movement() 
            if not self.game_over_flag:    
                self.draw()
            else:
                self.message_box()
                                                             
app = App()
app.main()