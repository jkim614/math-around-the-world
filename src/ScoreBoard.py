import pygame as pg

class ScoreBoard:
    '''
        The instance of this class displays the user's current score
    '''
    def __init__(self, score=0, pos=(30,59), size=28, color=(0,255,255)):
        self.score = score
        self.size = size
        self.color = color
        self.image = pg.font.SysFont('arial', self.size).render(str(self.score), True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
    def update(self, amount=1):
        '''
            Updates the score when the user answers a question correctly
            args: none
            return: none
        '''
        self.score += amount
        self.image = pg.font.SysFont('arial', self.size).render(str(self.score), True, self.color)
