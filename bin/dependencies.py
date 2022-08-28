import pygame, copy, numpy as np
from bin.constants import *


class Label:
    def __init__(self, text, rect, color=FG_COLOR):
        self.text = text
        self.baseFont = pygame.font.SysFont("Cambria", 32)
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.color = color

    def display(self, screen):
        text = self.baseFont.render(self.text, True, self.color)
        pygame.draw.rect(screen, BG_COLOR, self.rect)
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

    def changeColor(self, screen, color):
        self.color = color
        text = self.baseFont.render(self.text, True, self.color)
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

class TextBox:
    def __init__(self, rect, text=""):
        self.baseFont = pygame.font.SysFont("Cambria", 32)
        self.inputRect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.userText = text
        self.active = False

    
    def displayText(self, screen):
        text = self.baseFont.render(self.userText, True, FG_COLOR)
        screen.blit(text, (self.inputRect.x + 5, self.inputRect.y + 5))


class MenuScreen:
    def __init__(self):
        self.headingImg = pygame.image.load(HEADING).convert_alpha()
        self.headingRect = self.headingImg.get_rect(center=(WIDTH / 2, HEIGHT / 3.3))

        self.playImg = pygame.image.load(PLAY).convert_alpha()
        self.playRect = self.playImg.get_rect(center=(WIDTH / 2, HEIGHT / 1.7))

        self.musicImg = pygame.image.load(MUSIC_ON).convert_alpha()
        self.music = True
        self.musicRect = self.musicImg.get_rect(center=(40, HEIGHT - 40))
        
        self.soundImg = pygame.image.load(SOUND_ON).convert_alpha()
        self.sound = True
        self.soundRect = self.soundImg.get_rect(center=(120, HEIGHT - 40))

        self.exitImg = pygame.image.load(EXIT).convert_alpha()
        self.exitRect = self.exitImg.get_rect(center=(WIDTH - 40, HEIGHT - 40))

    
    def drawAll(self, screen):
        screen.blit(self.headingImg, self.headingRect)
        screen.blit(self.playImg, self.playRect)
        screen.blit(self.musicImg, self.musicRect)
        screen.blit(self.soundImg, self.soundRect)
        screen.blit(self.exitImg, self.exitRect)


    def chamgeImg(self, type):
        if type == "music":
            if self.music:
                self.musicImg = pygame.image.load(MUSIC_OFF).convert_alpha()
                self.music = False
            else:
                self.musicImg = pygame.image.load(MUSIC_ON).convert_alpha()
                self.music = True
        elif type == "sound":
            if self.sound:
                self.soundImg = pygame.image.load(SOUND_OFF).convert_alpha()
                self.sound = False
            else:
                self.soundImg = pygame.image.load(SOUND_ON).convert_alpha()
                self.sound = True

        


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


class NameScreen:
    def __init__(self, pLbl, oLbl):

        self.headingImg = pygame.image.load(HEADING).convert_alpha()
        self.headingRect = self.headingImg.get_rect(center=(WIDTH / 2, 80))

        self.pLabel = Label(pLbl, (WIDTH / 12, 200, 300, 50))
        self.pNameField = TextBox((WIDTH / 2.5, 200, 400, 50))

        self.oLabel = Label(oLbl, (WIDTH / 12, 300, 300, 50))
        if (oLbl == "Computer Name:"):
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


class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0

    def final_state(self, screen, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (PADX + (col * SQSIZE + SQSIZE // 2), 20)
                    fPos = (PADX + (col * SQSIZE + SQSIZE // 2), HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (PADX + 20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (PADX + 20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (PADX + 20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class AI:
    def __init__(self, player=2):
        self.player = player


    # --- MINIMAX ---
    def minimax(self, board, screen, maximizing):
        # terminal case
        case = board.final_state(screen)

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, screen, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, screen, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    # --- MAIN EVAL ---
    def eval(self, main_board, screen):
        # minimax algo
        eval, move = self.minimax(main_board, screen, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move # row, col


class MusicManager:
    def __init__(self, file, loop: bool=True):
        self.file = file
        self.loop = -1 if loop == True else 0
        pygame.mixer.music.load(self.file)

    
    def play(self):
        pygame.mixer.music.play(self.loop)


    def pause(self):
        pygame.mixer.music.pause()

    
    def unpause(self):
        pygame.mixer.music.unpause()

class SoundManager:
    def __init__(self, file):
        self.file = file
        self.sound = pygame.mixer.Sound(self.file)

    
    def play(self, condition):
            if condition: self.sound.play()