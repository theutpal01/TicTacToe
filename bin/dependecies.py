
import pygame
from bin.constants import *



class MenuScreen:
    def __init__(self):
        self.headingImg = pygame.image.load(HEADING).convert_alpha()
        self.headingRect = self.headingImg.get_rect(center=(WIDTH / 2, HEIGHT / 3.3))

        self.playImg = pygame.image.load(PLAY).convert_alpha()
        self.playRect = self.playImg.get_rect(center=(WIDTH / 2, HEIGHT / 1.7))

        self.musicImg = pygame.image.load(MUSIC_ON).convert_alpha()
        self.musicRect = self.musicImg.get_rect(center=(40, HEIGHT - 40))
        
        self.soundImg = pygame.image.load(SOUND_ON).convert_alpha()
        self.soundRect = self.soundImg.get_rect(center=(120, HEIGHT - 40))

        self.exitImg = pygame.image.load(EXIT).convert_alpha()
        self.exitRect = self.exitImg.get_rect(center=(WIDTH - 40, HEIGHT - 40))

    
    def drawAll(self, screen):
        screen.blit(self.headingImg, self.headingRect)
        screen.blit(self.playImg, self.playRect)
        screen.blit(self.musicImg, self.musicRect)
        screen.blit(self.soundImg, self.soundRect)
        screen.blit(self.exitImg, self.exitRect)


class ModeScreen:
    def __init__(self):
        self.headingImg = pygame.image.load(HEADING).convert_alpha()
        self.headingRect = self.headingImg.get_rect(center=(WIDTH / 2, 80))

        self.playBVPImg = pygame.image.load(PLAY_BVP).convert_alpha()
        self.playBVPRect = self.playBVPImg.get_rect(center=(WIDTH / 2, 250))

        self.playPVPImg = pygame.image.load(PLAY_PVP).convert_alpha()
        self.playPVPRect = self.playPVPImg.get_rect(center=(WIDTH / 2, 350))

        self.exitImg = pygame.image.load(EXIT).convert_alpha()
        self.exitRect = self.exitImg.get_rect(center=(WIDTH - 40, HEIGHT - 40))

    def drawAll(self, screen):
        screen.blit(self.headingImg, self.headingRect)
        screen.blit(self.playBVPImg, self.playBVPRect)
        screen.blit(self.playPVPImg, self.playPVPRect)
        screen.blit(self.exitImg, self.exitRect)


class Label:
    def __init__(self, text, rect, color=FG_COLOR):
        self.text = text
        self.baseFont = pygame.font.SysFont("Cambria", 32)
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.color = color

    def display(self, screen):
        pygame.draw.rect(screen, BG_COLOR, self.rect)
        text = self.baseFont.render(self.text, True, self.color)
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

    def changeColor(self, color):
        self.color = color

class TextBox:
    def __init__(self, rect, text=""):
        self.baseFont = pygame.font.SysFont("Cambria", 32)
        self.inputRect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.userText = text
        self.active = False

    
    def displayText(self, screen):
        text = self.baseFont.render(self.userText, True, FG_COLOR)
        screen.blit(text, (self.inputRect.x + 5, self.inputRect.y + 5))


class NameScreen:
    def __init__(self, pLbl, oLbl):

        self.headingImg = pygame.image.load(HEADING).convert_alpha()
        self.headingRect = self.headingImg.get_rect(center=(WIDTH / 2, 80))

        self.pLabel = Label(pLbl, (WIDTH / 12, 200, 300, 50))
        self.pNameField = TextBox((WIDTH / 2.5, 200, 400, 50))

        self.oLabel = Label(oLbl, (WIDTH / 12, 300, 300, 50))
        if (oLbl == "Computer Name:"):
            print("BOT PLAY")
            self.oNameField = TextBox((WIDTH / 2.5, 300, 400, 50), text=BOT_NAME)
        else:
            self.oNameField = TextBox((WIDTH / 2.5, 300, 400, 50))

        self.exitImg = pygame.image.load(EXIT).convert_alpha()
        self.exitRect = self.exitImg.get_rect(center=(40, HEIGHT - 40))

        self.submitImg = pygame.image.load(SUBMIT).convert_alpha()
        self.submitRect = self.submitImg.get_rect(center=(WIDTH - 126, HEIGHT - 40))


    def drawAll(self, screen):
        screen.blit(self.headingImg, self.headingRect)
        
        self.pLabel.display(screen)
        pygame.draw.rect(screen, (255, 255, 255), self.pNameField.inputRect, border_radius=5)
        
        self.oLabel.display(screen)
        pygame.draw.rect(screen, (255, 255, 255), self.oNameField.inputRect, border_radius=5)

        screen.blit(self.exitImg, self.exitRect)
        screen.blit(self.submitImg, self.submitRect)
        
        

class GameArea:
    def __init__(self):
        pass

    def setPlayers(self, player, opponent, playerRect, opponentRect):
        self.pName = Label(player.capitalize(), (1, 1, playerRect.width, playerRect.height), FOCUS_COLOR)
        self.oName = Label(opponent.capitalize(), (1, HEIGHT - opponentRect.height + 3, opponentRect.width, opponentRect.height))

    def drawAll(self, screen):
        self.pName.display(screen)
        self.oName.display(screen)
