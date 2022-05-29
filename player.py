class Player:
    def __init__(self):
        self.x = 368
        self.y = 500
        self.x_change = 0
        self.bullet_x = self.x + 16 
        self.bullet_y = self.y + 5
        self.bullet_speed = 10
        self.bullet_ready = True
        self.hp = 100
        self.score = 0
        
    def movement(self):
        if self.x <= 0 and self.hp != 0:
            self.x = 0
        if self.x >= 736 and self.hp != 0:
            self.x = 736
        self.x += self.x_change 
        
    def fire(self):self.bullet_ready = False
        
    
        