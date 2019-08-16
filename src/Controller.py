import pygame as pg
from src.QuestionBox import QuestionBox as QB
from src.PopUpQuestionBox import PopUpQuestionBox as PopUp
from src.QuestionGenerator import QuestionGenerator as QG
from src.MenuButton import MenuButton as MB
from src.AnswerTypein import AnswerTypein
from src.ScoreBoard import ScoreBoard as SB
from src.HealthIcon import HealthIcon as HI
import random
from os import path
from time import time, sleep

class Controller:
    '''
        This class mediates between the View and the Models, calling for
            updates to class state, screen presentation, and special effects
            in response to events and user input
    '''
    def __init__(self):
        # initialize a screen
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((1024, 768))
        pg.display.set_caption('Math Around the World')
        self.mouse_x, self.mouse_y = None, None
        self.fps = 30

        # create initial settings and user statistics
        self.questions = pg.sprite.Group()
        self.pop_up = None
        self.pop_show = False
        self.timer = []
        self.count = 0 # currently has no use
        self.lives = 3 # You can change numbers here to test for a particular situation but it only applies once
        self.score = 0 # You can change numbers here to test for a particular situation but it only applies once
        self.density = 90
        self.speed = 1.5 # the speed of question boxes

        # some buttons are created here
        self.start_button = MB((512,404), 'startbasic.png', 'starthover.png')
        self.rules_button = MB((512,489), 'rulesbasic.png', 'ruleshover.png')
        self.credit_button = MB((512,574), 'creditbasic.png', 'credithover.png')
        self.again_button = MB((512,410),'start_again.png', 'start_again.png')
        self.China_button = MB((275,190), path.join('country_selection', 'china_country_selection.png'), path.join('country_selection', 'china_country_selection_blur.png'))
        self.Egypt_button = MB((275,540), path.join('country_selection', 'egypt_country_selection.png'), path.join('country_selection', 'egypt_country_selection_blur.png'))
        self.Italy_button = MB((755,190), path.join('country_selection', 'italy_country_selection.png'), path.join('country_selection', 'italy_country_selection_blur.png'))
        self.ans_typein = AnswerTypein() # the type in box object
        self.ans = pg.sprite.Group() # the sprite group for the type in box object
        self.ans.add(self.ans_typein)

        # scoreboard and health bar objects
        self.score_board = SB(self.score)
        self.health_bar = HI(self.lives)

        self.STATE = 'start'

        # general sound effects
        base_path = path.dirname(__file__)
        self.sound_effect = {
            'wrong': pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'sound_effects', 'buzzer.wav')),
            'right': pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'sound_effects', 'chime.wav')),
            'hit': pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'sound_effects', 'clunk.wav'))
        }
        for i in self.sound_effect.keys():
            self.sound_effect[i].set_volume(0.08)

        # background image
        self.bg_start_screen_index = 0
        self.bg_start_screen = [pg.image.load(path.join(base_path, '..', 'assets', 'Background', 'earth_start_screen', 'start_screen{}.png'.format(x))) for x in range(1,40)]

        self.bg_menu = pg.image.load(path.join(base_path, '..', 'assets', 'Background', 'country_selection_background.jpg'))

        self.bg_rules_and_credit_index = 0
        self.bg_rules_and_credit = [pg.image.load(path.join(base_path, '..', 'assets', 'Background', 'rules_and_credit_bg', 'rules_and_credit_bg{}.png'.format(x))) for x in range(1,40)]

        self.bg_by_country = {
            'China': pg.image.load(path.join(base_path, '..', 'assets', 'Background', 'background_china.png')),
            'Egypt': pg.image.load(path.join(base_path, '..', 'assets', 'Background', 'background_egypt.png')),
            'Italy': pg.image.load(path.join(base_path, '..', 'assets', 'Background', 'background_italy.png'))
        }

        self.rules_text = pg.image.load(path.join(base_path, '..', 'assets', 'text', 'rules_edited.png'))
        self.rules_text = pg.transform.scale(self.rules_text, (909,705))
        self.credits_text = pg.image.load(path.join(base_path, '..', 'assets', 'text', 'credits_edited.png'))
        self.credits_text = pg.transform.scale(self.credits_text, (909,705))

        self.icons_by_country = {
            'China': ['China.png', 'China_bot.png'],
            'Egypt': ['Egypt.png', 'Egypt_bot_0.png'],
            'Italy': ['Italy.png', 'Italy_bot.png']
        }

        # background music
        self.volume = 0
        self.bgm_start = pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'music', 'MenuScreens.wav'))
        self.bgm_start.set_volume(0.15)
        self.bgm_credit = pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'music', 'CreditsScreen.wav'))
        self.bgm_credit.set_volume(0.1)

        self.bgm_by_country = {
            'China': [pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'music', 'China{}.wav'.format(x))) for x in range(1,4)],
            'Egypt': [pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'music', 'Egypt{}.wav'.format(x))) for x in range(1,4)],
            'Italy': [pg.mixer.Sound(path.join(base_path, '..', 'assets', 'sound', 'music', 'Italy{}.wav'.format(x))) for x in range(1,4)]
        }
        for i in self.bgm_by_country.keys():
            for g in self.bgm_by_country[i]:
                g.set_volume(0.1)

    def createQuestionBox(self, country):
        '''
            Creates a Question Box object and puts it in a sprite group
            args: country ('str') name of country
            return: none
        '''
        x = random.randrange(100, 924) # leave 100 pixels on both sides
        problem_obj = QG()

        if country == 'China':
            if self.score <= 5:
                self.density, self.speed = 90, 1.5
                problem = problem_obj.level_1()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 15:
                self.density, self.speed = 90, 1.5
                problem = problem_obj.level_2()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 30:
                self.density, self.speed = 60, 1.5
                problem = problem_obj.level_2()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 50:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 60:
                self.density, self.speed = 90, 1.2
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 80:
                self.density, self.speed = 60, 1.2
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 100:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 130:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 150:
                self.density, self.speed = 60, 1.2
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 175:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_5()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 200:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_5()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            else:
                self.density, self.speed = 90, 1
                problem = [problem_obj.level_5(), problem_obj.level_6()][random.randint(0,1)]
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)

        elif country == 'Egypt':
            if self.score <= 10:
                self.density, self.speed = 90, 1.5
                problem = problem_obj.level_1()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 20:
                self.density, self.speed = 90, 1.5
                problem = problem_obj.level_2()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 30:
                self.density, self.speed = 60, 1.5
                problem = problem_obj.level_2()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 50:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 60:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 80:
                self.density, self.speed = 90, 1.2
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 100:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 130:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 150:
                self.density, self.speed = 90, 1.2
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 175:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_5()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 200:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_5()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            else:
                self.density, self.speed = 90, 1
                problem = [problem_obj.level_5(), problem_obj.level_6()][random.randint(0,1)]
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)

        elif country == 'Italy':
            if self.score <= 15:
                self.density, self.speed = 90, 1.5
                problem = problem_obj.level_1()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 30:
                self.density, self.speed = 90, 1.5
                problem = problem_obj.level_2()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 45:
                self.density, self.speed = 60, 1.5
                problem = problem_obj.level_2()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 60:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 75:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 100:
                self.density, self.speed = 90, 1.2
                problem = problem_obj.level_3()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 120:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 140:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 160:
                self.density, self.speed = 90, 1.2
                problem = problem_obj.level_4()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 180:
                self.density, self.speed = 120, 1
                problem = problem_obj.level_5()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            elif self.score <= 200:
                self.density, self.speed = 90, 1
                problem = problem_obj.level_5()
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)
            else:
                self.density, self.speed = 90, 1
                problem = [problem_obj.level_5(), problem_obj.level_6()][random.randint(0,1)]
                self.questions.add(QB(x, self.speed, self.icons_by_country[country][0], problem[0], problem[1]))
                print(problem)

    def deleteOutscreenBox(self):
        '''
            Deletes Question Box object that is out of the screen
                or touching the ground, plays sound effect,
                and updates user's status
            args: none
            return: none
        '''
        for sp in self.questions:
            if sp.ycor > self.screen.get_rect().size[1] - sp.height - 65:
                self.sound_effect['hit'].play()
                self.questions.remove(sp)
                self.health_bar.update()
                self.lives -= 1
                if self.lives < 0:
                    pg.mixer.fadeout(3000)
                    self.bgm_start.play(-1, 0, 3000)
                    self.STATE = 'end'
            break # it only needs to run once per frame

    def drawStart(self):
        '''
            Displays the Menu Screen
            args: none
            return: none
        '''
        self.screen.blit(self.bg_start_screen[self.bg_start_screen_index//(self.fps//6)], (0,0)) # draw the earth gif
        self.bg_start_screen_index += 1 if self.bg_start_screen_index < self.fps * 39//6 - 1 else -(self.fps * 39//6 - 1)

        for button in [self.start_button, self.rules_button, self.credit_button]:
            if self.isOver(button.rect):
                button.isOver()
            else:
                button.notOver()
        self.screen.blits(((self.start_button.image, self.start_button.rect), (self.rules_button.image, self.rules_button.rect), (self.credit_button.image, self.credit_button.rect)))

    def drawMenu(self):
        '''
            Displays the Country Selection Screen
            args: none
            return: none
        '''
        self.screen.blit(self.bg_menu, (0,0))
        for button in [self.China_button, self.Egypt_button, self.Italy_button]:
            if self.isOver(button.rect): button.isOver()
            else: button.notOver()

        # blits them; the parameter that blits() takes is a sequence, e.g. here we are using 3 tuples inside 1 tuple and that 1 tuple is parsed into blits()
        self.screen.blits(((self.China_button.image, self.China_button.rect), (self.Egypt_button.image, self.Egypt_button.rect), (self.Italy_button.image, self.Italy_button.rect)))

    def drawRules(self):
        '''
            Draws images for Rules Screen
            args: none
            return: none
        '''
        self.screen.blit(self.bg_rules_and_credit[self.bg_rules_and_credit_index//(self.fps//6)], (0,0)) # draw the background gif
        self.bg_rules_and_credit_index += 1 if self.bg_rules_and_credit_index < self.fps * 39//6 - 1 else -(self.fps * 39//6 - 1)
        #self.screen.blit(self.rules_button.image, (50,50))
        self.screen.blit(self.rules_text, (50, 50))

    def drawCredit(self):
        '''
            Draws images for Credits Screen
            args: none
            return: none
        '''
        self.screen.blit(self.bg_rules_and_credit[self.bg_rules_and_credit_index//(self.fps//6)], (0,0)) # draw the background gif
        self.bg_rules_and_credit_index += 1 if self.bg_rules_and_credit_index < self.fps * 39//6 - 1 else -(self.fps * 39//6 - 1)
        #self.screen.blit(self.credit_button.image, (50,50))
        self.screen.blit(self.credits_text, (50, 50))

    def drawGame(self, density, country):
        '''
            Populates Game Screen with Question Boxes
            args:
                  density ('int') represents rate at which Question Boxes
                      are generated
                  country ('str') name of country
            return: density ('int') represents rate at which Question Boxes
                      are generated
        '''
        if self.score in (3,10,20,35,50): # do a pop-up question and freeze the dropping questions
            self.pop_up = PopUp(self.score)
            self.timer.append(time())
            self.screen.blit(self.pop_up.image, self.pop_up.rect)
            if self.pop_show:
                self.pop_up.draw()
                self.pop_show = False
            else:
                pass
            if time() - self.timer[0] >= 90: # if user does answer the pop-up question in a certain amount of time, they would lose their chance
                self.timer = []
                self.pop_up = None
                self.score += 0.01
        else:
            self.screen.blit(self.bg_by_country[country], (0,0))
            if density >= self.density: # the bigger the density is, the slower the game goes
                self.createQuestionBox(country)
                density = 0
            density += 1

            for sp in self.questions:
                sp.filename = self.icons_by_country[country][1] # change the background image of the bottom most question
                break
            self.questions.update()
            self.questions.draw(self.screen)
            self.deleteOutscreenBox()
        return density

    def drawEnd(self):
        '''
            Displays the user's final score and offers the option
                to play again
            args: none
            return: none
        '''
        self.screen.blit(self.bg_rules_and_credit[self.bg_rules_and_credit_index//6], (0,0)) # draw the background gif
        self.bg_rules_and_credit_index += + 1 if self.bg_rules_and_credit_index < 233 else -233

        # display user's final score
        score_record = SB(self.score, (512,270), 60, (244,96,108)) # this is just another scoreboard object with different position, size, and color
        self.screen.blit(score_record.image, score_record.rect)

        if self.isOver(self.again_button.rect):
            self.again_button.isOver()
        else:
            self.again_button.notOver()
        self.screen.blit(self.again_button.image, self.again_button.rect)

    def isOver(self, rect):
        '''
            Checks whether mouse is over a Pygame Rectangle object
            args: rect ('Rectangle') Pygame Rectangle object
            return: ('bool') True if mouse is over the Rectangle object;
                    False if the mouse is not over the Rectangle object
        '''
        if rect.center[0] - rect.size[0]/2 < self.mouse_x < rect.center[0] + rect.size[0]/2 and rect.center[1] - rect.size[1]/2 < self.mouse_y < rect.center[1] + rect.size[1]/2:
            return True
        else:
            return False

    def checkAns(self, ans_submitted, country):
        '''
            Compares answer submitted by user with expected answer;
                updates user status for correct answers
            args: ans_submitted ('str') answer typed and entered by user
            return: none
        '''
        if self.pop_up is not None:
            if ans_submitted in self.pop_up.problems[self.score]['ans'] and ans_submitted != '':
                self.sound_effect['right'].play()
                if self.lives != 3:
                    self.health_bar.update(1)
                    self.lives += 1
                    self.score += 0.01 # see line 171 & 164
                else:
                    self.score_board.update(5)
                    self.score += 5
                self.pop_up = None
            else:
                self.sound_effect['wrong'].play()
        else:
            for sp in self.questions:
                if ans_submitted in sp.answer and ans_submitted != '':
                    self.sound_effect['right'].play()
                    self.score_board.update() # in update(), the score will + 1
                    self.score = int((self.score + 1)//1)
                    if self.score == 30:
                        pg.mixer.fadeout(3000)
                        self.bgm_by_country[country][1].play(-1, 0, 3000)
                    elif self.score == 100:
                        pg.mixer.fadeout(3000)
                        self.bgm_by_country[country][2].play(-1, 0, 3000)
                    self.questions.remove(sp)
                else:
                    self.sound_effect['wrong'].play()
                break
        #print(self.score, self.lives)


    def startLoop(self):
        '''
            Loop for main Menu Screen
            args: none
            return: none
        '''
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.drawStart()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() #sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.start_button.rect.collidepoint(self.mouse_x, self.mouse_y):
                    self.STATE = 'menu'
                elif self.rules_button.rect.collidepoint(self.mouse_x, self.mouse_y):
                    self.STATE = 'rules'
                elif self.credit_button.rect.collidepoint(self.mouse_x, self.mouse_y):
                    pg.mixer.fadeout(3000)
                    self.bgm_credit.play(-1, 0, 3000)
                    self.STATE = 'credit'

    def menuLoop(self):
        '''
            Loop for Country Selection Screen
            args: none
            return: none
        '''
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.drawMenu()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.STATE = 'start'
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.China_button.rect.collidepoint(self.mouse_x, self.mouse_y):
                    pg.mixer.fadeout(3000)
                    self.bgm_by_country['China'][0].play(-1, 0, 5000)
                    self.STATE = 'game China'
                elif self.Italy_button.rect.collidepoint(self.mouse_x, self.mouse_y):
                    pg.mixer.fadeout(3000)
                    self.bgm_by_country['Italy'][0].play(-1, 0, 5000)
                    self.STATE = 'game Italy'
                elif self.Egypt_button.rect.collidepoint(self.mouse_x, self.mouse_y):
                    pg.mixer.fadeout(3000)
                    self.bgm_by_country['Egypt'][0].play(-1, 0, 5000)
                    self.STATE = 'game Egypt'

    def ruleLoop(self):
        '''
            Loop for Rules Screen
            args: none
            return: none
        '''
        self.drawRules()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() #sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.STATE = 'start'

    def creditLoop(self):
        '''
            Loop for Credits Screen
            args: none
            return: none
        '''
        self.drawCredit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() #sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.STATE = 'start'

    def gameLoop(self, density, country):
        '''
            Loop for Country Selection Screen
            args:
                  density ('int') represents rate at which Question Boxes
                      are generated
                  country ('str') name of country
            return: density ('int') represents rate at which Question Boxes
                      are generated
        '''
        # adjust volume to create a fade in here
        density = self.drawGame(density, country)
        self.screen.blit(self.ans_typein.bg_image, self.ans_typein.bg_rect) # draw the background before drawing the text that user types in
        self.ans.draw(self.screen) # draw the text that user types in


        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.STATE = 'menu'
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKQUOTE:
                self.pop_show = not self.pop_show
            elif event.type == pg.KEYDOWN:
                self.ans.update(event)

                ans_submitted = self.ans_typein.submit()
                if ans_submitted is None: pass
                else: self.checkAns(ans_submitted, country) # ans_submitted will not be None if user hit ENTER key with numbers typed in
        self.screen.blits(((self.score_board.image, self.score_board.rect), (self.health_bar.byCountry(country), self.health_bar.rect)))
        return density

    def endLoop(self):
        '''
            Loop for end of game
            args: none
            return: none
        '''
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.drawEnd()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() #sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.again_button.rect.collidepoint(self.mouse_x, self.mouse_y):
                    self.STATE = 'start'

    def mainloop(self):
        '''
            Loop that handles events, updates state, 
                and redraws screen
            args: none
            return: none
        '''
        # loop it, or say, run it

        while True: # without this loop, the game will exit automatically after clicking 'start again', because there is no codes after while STATE == 'end' loop
            density = 0
            self.volume = 0
            pg.mixer.fadeout(3000) # fadeout in 3 seconds
            self.bgm_start.play(-1, 0, 3000) # 3000 here means fadein in 3 seconds
            while self.STATE == 'start':
                self.startLoop()
                pg.time.Clock().tick(self.fps) # set the frame rate to be self.fps per second at most
                pg.display.update()
            while self.STATE == 'menu':
                self.menuLoop()
                pg.time.Clock().tick(self.fps)
                pg.display.update()
            while self.STATE == 'rules':
                self.ruleLoop()
                pg.time.Clock().tick(self.fps)
                pg.display.update()
            while self.STATE == 'credit':
                self.creditLoop()
                pg.time.Clock().tick(self.fps)
                pg.display.update()
            while self.STATE[:4] == 'game': # note the difference here
                #print(pg.display.Info())
                density = self.gameLoop(density, self.STATE[5:])
                pg.time.Clock().tick(self.fps)
                pg.display.update()
            while self.STATE == 'end':
                self.endLoop()
                pg.time.Clock().tick(self.fps)
                pg.display.update()

            # reset everything
            self.pop_up = None
            self.timer = []
            self.questions.empty()
            self.ans_typein.result = ''
            self.ans_typein.update() # empty the type in box
            self.score, self.score_board.score = 0, -1
            self.score_board.update() # have to update to change the image
            self.lives, self.health_bar.health = 3, 4
            self.health_bar.update() # same
