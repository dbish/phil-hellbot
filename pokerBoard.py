import playingCards
import pygame, sys
from pygame.locals import *
from playingCards import *

locs = [300, 380, 460, 540, 620]
players = [400, 100, 700]


if __name__ == '__main__':
        deck = Deck()
        for card in deck.getCards():
                print card

        pygame.init()
        fpsClock = pygame.time.Clock()

        #display board
        windowSurfaceObj = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Heads Up!')

        while True:

                windowSurfaceObj.fill(green)

                #draw deck
                backImage = pygame.image.load("cards/b.gif")
                for i in range(0, 10, 2):
                        windowSurfaceObj.blit(backImage, (locs[0]-130-i, players[0]-50))

                #draw card outlines
                for i in range(2):
                        for j in range(2):
                                pygame.draw.circle(windowSurfaceObj, red, (locs[i+1], players[j+1]), 10, 0)

                for i in range(5):
                        pygame.draw.circle(windowSurfaceObj, red, (locs[i], players[0]), 10, 0)


                deck.getCards()[0].displayCard(windowSurfaceObj, locs[1], players[1], False)

                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                        elif event.type == MOUSEMOTION:
                                mousex, mousey = event.pos
                        elif event.type == MOUSEBUTTONUP:
                                mousex, mousey = event.pos
                                if event.button == 1: #left click
                                        msg = 'left click'

                pygame.display.update()
                fpsClock.tick(30)

