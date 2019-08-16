import pygame as pg
from QuestionBox import QuestionBox
from ScoreBoard import ScoreBoard

def main():
    pg.init()
    print('##### Testing question box generator #####')
    testQB = QuestionBox(100, 1)
    testQB.update()
    assert testQB.rect.y == -27
    print('##### Test completed #####')

    print('##### Testing score board #####')
    testSB = ScoreBoard()
    testSB.update()
    assert testSB.score == 1
    print('##### Test completed #####')

main()
