from random import randint

class Enemy:
    def __init__(self):
        self.no_of_enemies = 5
        self.x = [randint(0, 735) for _ in range(self.no_of_enemies)]
        self.y = [randint(0, 100) for _ in range(self.no_of_enemies)]
        self.x_change = [2 for _ in range(self.no_of_enemies)]
        self.bullet_x = [self.x[i] for i in range(self.no_of_enemies)] 
        self.bullet_y = [self.y[i] for i in range(self.no_of_enemies)]
        self.bullet_speed = 5
        self.bullet_ready = [True for _ in range(self.no_of_enemies)]
        
    def movement(self):
        for i in range(self.no_of_enemies):
            if self.x[i] >= 736:
                self.x_change[i] = -2
                self.y[i] += 50
            if self.x[i] <= 0:
                self.x_change[i] = 2
                self.y[i] += 50
            self.x[i] += self.x_change[i]
            
    def fire(self): return False
    
