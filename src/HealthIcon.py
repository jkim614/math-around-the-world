import pygame as pg
import os

class HealthIcon:
    '''
        This class creates objects that represent the number of questions
            the user can get wrong before the game ends
    '''
    def __init__(self, lives=3):
        self.health = lives

        # get and rescale the image
        base_path = os.path.dirname(__file__)
        self.dict = {
            'China': pg.transform.scale(pg.image.load(os.path.join(base_path, '..', 'assets', 'health_icons', 'china_health.png')), (32, 32)),
            'Egypt': pg.transform.scale(pg.image.load(os.path.join(base_path, '..', 'assets', 'health_icons', 'egypt_health.png')), (32, 32)),
            'Italy': pg.transform.scale(pg.image.load(os.path.join(base_path, '..', 'assets', 'health_icons', 'italy_health.png')), (32, 32))
        }

        self.image = pg.Surface((96, 32), pg.SRCALPHA, 32).convert_alpha()
        
        self.icon = None

        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)
        # so, after initialization (i.e., after the object is created), the image is actually a blank image with nothing
        
    def update(self, amount = -1):
        '''
            Updates the health status
            args: none
            return: none
        '''
        self.health += amount
        self.image = pg.Surface((96, 32), pg.SRCALPHA, 32).convert_alpha() # this step resets the image, or it will only draw upon the original image
    
    def byCountry(self, country):
        '''
            Sets the Health Icon image according to the country
            args: country ('str') the country chosen for the game screen
            return: none
        '''
        self.icon = self.dict[country]
        for i in range(self.health):
            self.image.blit(self.icon, (i*32,0))
        return self.image


