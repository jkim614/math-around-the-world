import pygame as pg

class AnswerTypein(pg.sprite.Sprite):
    '''
        The sprite in this class displays the answer typed
            by the user
    '''
    def __init__(self, text_color=(33,206,153), bg_color=(214,213,183,100)):
        pg.sprite.Sprite.__init__(self)
        self.text_color = text_color
        self.bg_color = bg_color

        self.result = ''
        self.res = None
        self.image = pg.font.SysFont('arial', 45).render(self.result, True, self.text_color)
        self.rect = pg.Rect(10, 708, 1004, 50)

        self.bg_image = pg.Surface((1004, 50), pg.SRCALPHA) # without pg.SCRALPHA, the surface does not accept transparency
        self.bg_image.fill(self.bg_color)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.topleft = (10, 708)

    def __str__(self):
        '''
            Stringification of AnswerTypein object
            args: none
            return: ('str') the input typed by the user
        '''
        return self.result

    def update(self, event=None):
        '''
            Updates the Typein field with user input
            args: Pygame keyboard constant
            return: none
        '''
        self.res = None
        if event is None:
            self.result = ''
        elif event.key == pg.K_BACKSPACE: # backspace key
            if len(self.result) != 0:
                self.result = self.result[:-1]
            else:
                pass
        elif event.key == pg.K_MINUS and len(self.result) != 0: # minus key; prevent users type in minus if there is number typed in already
            pass
        elif event.key == pg.K_RETURN: # return key (or enter key)
            self.res = self.result
            self.result = ''
        else:
            self.result += event.unicode # this unicode attribute makes life so much easier :) thanks pygame

        self.image = pg.font.SysFont('arial', 45).render(self.result, True, self.text_color)

    def submit(self):
        '''
            Returns the user's answer after the ENTER key has been pressed
            args: none
            return: ('str') the answer entered by the user
        '''
        return self.res
