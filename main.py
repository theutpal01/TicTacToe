from math import radians
import math
import pygame, copy, sys, random, numpy as np
from bin.constants import *
from bin.dependecies import *

# --------------- PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

icon = pygame.image.load("files/icon.png").convert_alpha()
pygame.display.set_icon(icon)


class Game:
    def __init__(self):
        self.MENU = True
        self.MODE = False
        self.NAME_BVP = False
        self.NAME_PVP = False
        self.GAME_AREA = False

        self.CLICKED = False

        self.menu = MenuScreen()
        self.mode = ModeScreen()
        self.nameBvP = NameScreen("Player's Name:", "Computer Name:")
        self.namePvP = NameScreen("Player's Name:", "Player's Name:")
        self.gameArea = GameArea()

    
    # def onClick(self, image, scale):
    #     if not self.CLICKED:
    #         size = image.get_size()
    #         pygame.transform.smoothscale(image, (size[0] - scale, size[1] - scale))
    #         pygame.display.update()
    #         self.CLICKED = True

    
    def isCollideCircle(self, mouse, rect):
        radius = rect.width // 2
        distX = mouse[0] - rect.centerx
        distY = mouse[1] - rect.centery
        # Calculate the length of hypotenuse. If it is < the radius, the mouse collides with circle
        if math.hypot(distX, distY) < radius: return True
        return False

    def isCollideRect(self, mouse, rect):
        return rect.collidepoint(mouse[0], mouse[1])



def main():

    game = Game()


    while True:

        screen.fill(BG_COLOR)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # EVENTS OTHER THAN QUIT BY CROSS BTN OR USING SHORTCUT

            if event.type == pygame.MOUSEBUTTONDOWN:

                # EVENTS FOR MENU WINDOW
                if game.MENU:
                    if game.isCollideCircle(pygame.mouse.get_pos(), game.menu.playRect):
                        game.CLICKED = True
                        game.MENU = False
                        game.MODE = True
                        game.CLICKED = False
                    
                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.menu.musicRect):
                        pass

                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.menu.soundRect):
                        pass

                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.menu.exitRect):
                        pygame.quit()
                        sys.exit()

                # EVENTS FOR MODE WINDOW
                elif game.MODE:

                    if game.isCollideRect(pygame.mouse.get_pos(), game.mode.playBVPRect):
                        game.CLICKED = True
                        game.MODE = False
                        game.NAME_BVP = True
                        game.CLICKED = False

                    elif game.isCollideRect(pygame.mouse.get_pos(), game.mode.playPVPRect):
                        game.CLICKED = True
                        game.MODE = False
                        game.NAME_PVP = True
                        game.CLICKED = False
                    
                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.mode.exitRect):
                        game.CLICKED = True
                        game.MODE = False
                        game.MENU = True
                        game.CLICKED = False

                
                # EVENTS FOR NAME_BVP WINDOW
                elif game.NAME_BVP:
                    if game.isCollideRect(pygame.mouse.get_pos(), game.nameBvP.submitRect):
                        player = game.nameBvP.pNameField.userText
                        opponent = game.nameBvP.oNameField.userText
                        if player != "":
                            game.gameArea.setPlayers(player, opponent, game.nameBvP.pNameField.inputRect, game.nameBvP.oNameField.inputRect)
                            game.CLICKED = True
                            game.NAME_BVP = False
                            game.GAME_AREA = True
                            game.CLICKED = False
                    
                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.nameBvP.exitRect):
                        game.CLICKED = True
                        game.NAME_BVP = False
                        game.MODE = True
                        game.CLICKED = False

                    if game.nameBvP.pNameField.inputRect.collidepoint(pygame.mouse.get_pos()):
                        game.nameBvP.pNameField.active = True
                    else:
                        game.nameBvP.pNameField.active = False

                # EVENTS FOR NAME_PVP WINDOW
                elif game.NAME_PVP:
                    if game.isCollideRect(pygame.mouse.get_pos(), game.namePvP.submitRect):
                        player = game.namePvP.pNameField.userText
                        opponent = game.namePvP.oNameField.userText
                        if player != "" and opponent != "":
                            game.gameArea.setPlayers(player, opponent, game.namePvP.pNameField.inputRect, game.namePvP.oNameField.inputRect)
                            game.CLICKED = True
                            game.NAME_PVP = False
                            game.GAME_AREA = True
                            game.CLICKED = False

                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.namePvP.exitRect):
                        game.CLICKED = True
                        game.NAME_PVP = False
                        game.MODE = True
                        game.CLICKED = False

                    if game.namePvP.pNameField.inputRect.collidepoint(pygame.mouse.get_pos()):
                        game.namePvP.pNameField.active = True
                        game.namePvP.oNameField.active = False
                    elif game.namePvP.oNameField.inputRect.collidepoint(pygame.mouse.get_pos()):
                        game.namePvP.pNameField.active = False
                        game.namePvP.oNameField.active = True
                    else:
                        game.namePvP.pNameField.active = False
                        game.namePvP.oNameField.active = False

                # EVENTS FOR GAME AREA WINDOW
                elif game.GAME_AREA:
                    pass                

            
            # KEYBOARD EVENTS FOR TYPING NAMES, ETC...
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    if game.nameBvP.pNameField.active or game.namePvP.pNameField.active:
                        if game.NAME_BVP:
                            game.nameBvP.pNameField.userText = game.nameBvP.pNameField.userText[:-1]
                        else:
                            game.namePvP.pNameField.userText = game.namePvP.pNameField.userText[:-1]
                    
                    elif game.namePvP.oNameField.active:
                        game.namePvP.oNameField.userText = game.namePvP.oNameField.userText[:-1]
                
                else:
                    if game.nameBvP.pNameField.active or game.namePvP.pNameField.active:
                        if game.NAME_BVP:
                            game.nameBvP.pNameField.userText += event.unicode if len(game.nameBvP.pNameField.userText) < 20 else ""
                        else:
                            game.namePvP.pNameField.userText += event.unicode if len(game.namePvP.pNameField.userText) < 20 else ""
                    
                    elif game.namePvP.oNameField.active:
                        game.namePvP.oNameField.userText += event.unicode if len(game.namePvP.oNameField.userText) < 20 else ""


        if game.MENU: 
            game.menu.drawAll(screen)
        
        elif game.MODE: 
            game.mode.drawAll(screen)
        
        elif game.NAME_BVP: 
            game.nameBvP.drawAll(screen)
            game.nameBvP.oNameField.displayText(screen)
            game.nameBvP.pNameField.displayText(screen)

        elif game.NAME_PVP:
            game.namePvP.drawAll(screen)
            game.namePvP.oNameField.displayText(screen)
            game.namePvP.pNameField.displayText(screen)

        elif game.GAME_AREA:
            game.gameArea.drawAll(screen)

        pygame.display.update()

if __name__ == '__main__':
    main()
