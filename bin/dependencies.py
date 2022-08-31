from time import sleep
import pygame, copy, numpy as np
from bin.constants import *


class Label:
    """
        User defined class for the implementation of label in pygame module.

        __init__() funtion takes:
            text: Text of the label which is to be displayed.
            rect: Position of the text to be diplayed.
            color: Takes the color with which the text will be filled [optional].

        display() function displays the label when called and takes:
            screen: screen object for drawing the label on the window.

        changeColor() funtion changes the color of label's text and takes:
            screen: screen object for drawing the label on the window.
            color: The color with which the label's text will be filled.
    """

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
    """
        User defined class for the implementation of textbox in pygame module.

        __init__() funtion takes:
            rect: Position of the textbox which is to be diplayed.
            text: If given then textbox default text will be the given value [optional].

        displayText() function displays the textbox when called and takes:
            screen: screen object for drawing the textbox on the window.
    """
    def __init__(self, rect, text=""):
        self.baseFont = pygame.font.SysFont("Cambria", 32)
        self.inputRect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.cursor = ""
        self.userText = text
        self.active = False

    def displayText(self, screen):
        text = self.baseFont.render(self.userText + self.cursor, True, FG_COLOR)
        screen.blit(text, (self.inputRect.x + 5, self.inputRect.y + 5))



class MenuScreen:
    """
        User defined class for the implementation of Menu Window.
        In this window player can see a game screen in which he/she can:
            click play btn and proceed
            manage music and sound(on/off)
            click exit btn and quit the game

        drawAll() function displays the window and it's components which are initalized already when called and takes:
            screen: screen object for drawing all the components on the window.

        changeImg() function changes the image of music and sound btn accordingly and takes:
            type: The type of button [only 2 strings applicable, (music, sound)]
    """
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
    """
        User defined class for the implementation of Mode Window.
        In this window a player gets to choose between two modes:
            Player vs COmputer
            Player vs Player

        drawAll() function displays the window and it's components which are initalized already when called and takes:
            screen: screen object for drawing all the components on the window.
    """
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
    """
        User defined class for the implementation of Asking Name Window.
        In this window([PLAYER vs COMPUTER] or [PLAYER vs PLAYER]) a player gets to enter his/her name

        __init__() funtions takes:
            pLbl: The text which is to be displayed for asking player's name
            pLbl: The text which is to be displayed dipicting the value -> Computer's name or -> asking Opponent's Name.

        drawAll() function displays the window and it's components which are initalized already when called and takes:
            screen: screen object for drawing all the components on the window.
    """
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
    """
        User defined class for the implementation of Game Area Window.
        In this window a player(s) play the game

        setPlayers() funtion sets the names of the players with their scores aside their names and takes:
            player: iterable object with 2 items -> it's name, it's score
            opponent: iterable object with 2 items -> it's name, it's score
            playerRect: position of player
            opponentRect: position of opponent

        drawAll() function displays the window and it's components which are initalized already when called and takes:
            screen: screen object for drawing all the components on the window.
    """
    def __init__(self):
        self.playerName, self.opponentName = None, None
        self.playerScore, self.opponentScore = None, None
        self.playerRect, self.opponentRect = None, None

    def setPlayers(self, player, opponent, playerRect, opponentRect):
        self.playerName, self.opponentName = player[0], opponent[0]
        self.playerScore, self.opponentScore = player[1], opponent[1]
        
        self.playerRect, self.opponentRect = playerRect, opponentRect
        self.pName = Label(f"{self.playerName.capitalize()} - {self.playerScore}", (1, 1, self.playerRect.width, self.playerRect.height), FOCUS_COLOR)
        self.oName = Label(f"{self.opponentName.capitalize()} - {self.opponentScore}", (1, HEIGHT - self.opponentRect.height + 3, self.opponentRect.width, opponentRect.height))

    def drawAll(self, screen):
        self.pName.display(screen)
        self.oName.display(screen)


class Board:
    """
        User defined class for the implementation of Board [backend = not displayed to player].
        This class is the manager of backend board in which player(s) will be playing.

        finalState() function return the output accordingly:
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        and takes input:
            screen: screen object for drawing all the components on the window.
            show: boolean & if passed true then the funtion will create a line to the area where a player won (just like in the actual game)

        markSqr() funtion alters the position of item from 0 to 1 and hence marking it (O or X) and takes:
            row: row number from the game
            col: column number from the game

        emptySqr() funtion checks whether given position is a empty box or not and takes:
            row: row number from the game
            col: column number from the game

        getEmptySqrs() funtion returns a list of all the empty squares in the format of each item (row, col)

        isfull() funtion chercks whether all the boxes are filled or not

        isempty() funtion checks wheter all the boxes are empty or not
    """

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0

    def finalState(self, screen, show=False):
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

    def markSqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def emptySqr(self, row, col):
        return self.squares[row][col] == 0

    def getEmptySqrs(self):
        emptySqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.emptySqr(row, col):
                    emptySqrs.append( (row, col) )
        
        return emptySqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class AI:
    """
        User defined class for the implementation of AI [backend = not displayed to player].
        This class uses Minimax algo to always win from the player or end the match in tie of them.

        minimax() funtion uses minimax algo:
            it alaysis the whole game by making a copy of board object and chooses the best possible move to prevent player from maximizing(wining)
            and it takes:
                board: a board object which is defined above [for analyzing the game]
                screen: screen object for drawing all the components on the window.
                maximizing: boolean value [for starting the algorithm]

        eval() funtion is a trigger point of the minimax algo and takes:
            mainBoard: a board object which is defined above [for analyzing the game in minimax algo]
            screen: screen object for drawing all the components on the window.
    """
    def __init__(self):
        self.player = 2


    # --- MINIMAX ---
    def minimax(self, board, screen, maximizing):
        # terminal case
        case = board.finalState(screen)

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
            empty_sqrs = board.getEmptySqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.markSqr(row, col, 1)
                eval = self.minimax(temp_board, screen, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.getEmptySqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.markSqr(row, col, self.player)
                eval = self.minimax(temp_board, screen, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    # --- MAIN EVAL ---
    def eval(self, mainBoard, screen):
        # minimax algo
        eval, move = self.minimax(mainBoard, screen, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move # row, col


class MusicManager:
    """
        User defined class for managing the music in the game.

        __init__() funtion takes:
            file: path of the music
            loop: whether to play music in loop[true] or not[false] [default = true]

        play() funtion starts playing the music [on loop or not]
        pause() funtion pauses the music
        unpause() funtion unpauses the music
    """
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
    """
        User defined class for managing the sounds in the game.

        __init__() funtion takes:
            file: path of the sound effect

        play() funtion starts playing the sound effect
    """
    def __init__(self, file):
        self.file = file
        self.sound = pygame.mixer.Sound(self.file)

    
    def play(self, condition):
            if condition: self.sound.play()