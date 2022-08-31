from threading import Thread
from os import environ
from importlib import util
from time import sleep
import pygame, sys, math
from bin.dependencies import *


# CLOSING SPLASH SCREEN IF THERE IS ANY [ONLY APPLICABLE FOR THE BUILD FILE OF THIS GAME]
if '_PYIBoot_SPLASH' in environ and util.find_spec("pyi_splash"):
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()


# --------------- PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

icon = pygame.image.load("files/icon.png").convert_alpha()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()


class Game:
    """
        User defined class for the management of whole game.
        This class is a parent class of all other classes created in dependecies.py file

        isCollideCircle() funtion return true if mouse collides with given circle and takes:
            mouse: posiition of mouse pointer (x, y)
            rect: positonal rectangle of the object

        isCollideRect() funtion return true if mouse collides with given rectangle and takes:
            mouse: posiition of mouse pointer (x, y)
            rect: positonal rectangle of the object

        showLines() funtion displays the lines of the game area window

        drawFig() funtion draws the required game item (O or X) and takes:
            row: row number of the box
            col: col number of the box

        makeMove() funtion draws the game element by passing arguments to drawFig() funtion and changing the turn of players and takes:
            row: row number of the box
            col: col number of the box

        aiMove() funtion is for algo to make move just like previous one [makeMove()]

        nextTurn() funtion changes the turn of the players accordingly

        isover() funtion checks whether the game is over or not i.e:
            game is won by player or ai
            game ends in tie
            it also plays the sound effect accordingly

        reset() funtion resets the game area completelty except the players name and scores

        showEndText() funtion displays the end message (request) to the player when game is over and takes:
            text: text to display in a label at the center
            color: color of the text to be displayed

        updateMenu(), updateMode(), updateNameBvP(), updateNamePvP(), updateGameArea():
            funtions that contains the funtions to draw components on the screen according to the windows in whicih the user is.

        updateNameFocus(): funtion that updates the color according to the move of the players

        updateScores(): funtion that updates the scores after each finished match
    """
    def __init__(self):
        self.MENU = True
        self.MODE = False
        self.NAME_BVP = False
        self.NAME_PVP = False
        self.GAME_AREA = False
        self.player = 1
        self.gameType = ""
        self.runing = False
        self.CLICKED = False
        self.EFFECTS = True
        # self.over = False

        self.menu = MenuScreen()
        self.mode = ModeScreen()
        self.nameBvP = NameScreen("Player's Name:", "Computer Name:")
        self.namePvP = NameScreen("Player's Name:", "Player's Name:")
        self.gameArea = GameArea()
        self.board = Board()
        self.ai = AI()

        self.music = MusicManager("files/sounds/music.mp3")
        self.clickSound = SoundManager("files/sounds/click.wav")
        self.hoverSound = SoundManager("files/sounds/hover.wav")
        self.placeSound = SoundManager("files/sounds/place.wav")
        self.victorySound = SoundManager("files/sounds/victory.wav")
        self.drawSound = SoundManager("files/sounds/draw.wav")
        self.defeatSound = SoundManager("files/sounds/defeat.wav")

    def isCollideCircle(self, mouse, rect):
        radius = rect.width // 2
        distX = mouse[0] - rect.centerx
        distY = mouse[1] - rect.centery
        # Calculate the length of hypotenuse. If it is < the radius, the mouse collides with circle
        if math.hypot(distX, distY) < radius: return True
        return False

    def isCollideRect(self, mouse, rect):
        return rect.collidepoint(mouse[0], mouse[1])

    # BOTTOM - THESE ARE ALL IN GAME FUNC WHEN PLYER PLAYS THE GAME
    def showLines(self):
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (PADX + SQSIZE, 0), (PADX + SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (PADX, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (PADX, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def drawFig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (PADX + (col * SQSIZE + OFFSET), row * SQSIZE + OFFSET)
            end_desc = (PADX + (col * SQSIZE + SQSIZE - OFFSET), row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (PADX + (col * SQSIZE + OFFSET), row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (PADX + (col * SQSIZE + SQSIZE - OFFSET), row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        
        elif self.player == 2:
            # draw circle
            center = (PADX + (col * SQSIZE + SQSIZE // 2), row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---
    def makeMove(self, row, col):
        self.board.markSqr(row, col, self.player)
        self.drawFig(row, col)
        self.next_turn()

    def aiMove(self):
        if self.board.marked_sqrs > 2:
            sleep(1.5)
        row, col = self.ai.eval(self.board, screen)
        self.makeMove(row, col)
        self.placeSound.play(self.EFFECTS)

        if self.isover() and self.runing:
            outcome = self.isover()
            if outcome != -1:

                # --------------- UPDATE SCORES
                if outcome == 1: 
                    self.updateScores(1, 0)
                elif outcome == 2:
                    self.updateScores(0, 1)
            self.showEndText("PRESS SPACEBAR TO RESTART", OVER_COLOR)
            self.runing = False
        self.updateNameFocus()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def isover(self):
        finalState = self.board.finalState(screen)
        if self.gameType == "ai":
            if finalState == 1:
                self.victorySound.play(self.EFFECTS)
            elif finalState == 2:
                self.defeatSound.play(self.EFFECTS)
            elif self.board.marked_sqrs == 9:
                self.drawSound.play(self.EFFECTS)
        elif self.gameType == "normal":
            if finalState == 1 or finalState == 2:
                self.victorySound.play(self.EFFECTS)
            elif self.board.marked_sqrs == 9:
                self.drawSound.play(self.EFFECTS)

        self.board.finalState(screen, show=True)
        if finalState == 1:
            return 1
        elif finalState == 2:
            return 2
        elif self.board.isfull():
            return -1

    def reset(self):
        self.board = Board()
        self.player = 1
        self.runing = True
        self.gameArea.setPlayers((self.gameArea.playerName, self.gameArea.playerScore), (self.gameArea.opponentName, self.gameArea.opponentScore), self.gameArea.playerRect, self.gameArea.opponentRect)
        self.updateGameArea()
        self.updateNameFocus()

    def showEndText(self, text, color):
        baseFont = pygame.font.SysFont("Corbel", 45, True)
        lbl = baseFont.render(text, True, color)
        lblRect = lbl.get_rect()
        left = ((WIDTH // 2) - (lblRect.width // 2)) - 10
        top = ((HEIGHT // 2) - (lblRect.height // 2)) - 12
        rect = pygame.Rect(left, top, lblRect.width + 20, lblRect.height + 20)
        pygame.draw.rect(screen, FOCUS_COLOR, rect, border_radius=4)
        screen.blit(lbl, lbl.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
  
    # ---------------- UPDATE FUNCTIONS ---------------- #
    def updateMenu(self):
        screen.fill(BG_COLOR)
        self.menu.drawAll(screen)

    def updateMode(self):
        screen.fill(BG_COLOR)
        self.mode.drawAll(screen)

    def updateNameBvP(self):
        screen.fill(BG_COLOR) 
        self.nameBvP.drawAll(screen)
        self.nameBvP.oNameField.displayText(screen)
        self.nameBvP.pNameField.displayText(screen)

    def updateNamePvP(self):
        screen.fill(BG_COLOR)
        self.namePvP.drawAll(screen)
        self.namePvP.oNameField.displayText(screen)
        self.namePvP.pNameField.displayText(screen)

    def updateGameArea(self):
        screen.fill(BG_COLOR)
        self.gameArea.drawAll(screen)
        self.showLines()

    def updateNameFocus(self):
        if self.player == 1: 
            self.gameArea.pName.changeColor(screen, FOCUS_COLOR)
            self.gameArea.oName.changeColor(screen, FG_COLOR)
        else:
            self.gameArea.pName.changeColor(screen, FG_COLOR)
            self.gameArea.oName.changeColor(screen, FOCUS_COLOR)
        pygame.display.update()

    def updateScores(self, pScore, oScore):
        self.gameArea.playerScore += pScore
        self.gameArea.opponentScore += oScore


def main():

    game = Game()               # OBJECT OF THE GAME CLASS
    game.music.play()           # STARTS PLAYING THE BG MSUIC
    game.updateMenu()           # THIS FUNTIONS DRAWS THE COMONENT OF THE MENU WINDOW ON THE SCREEN

    while True:
        for event in pygame.event.get():
            # IF PLAYER TRIES TO QUIT THE GAME USING RED CLOSE BTN OR SHORTCUT THEN GAME CLOSES
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # EVENTS OF THE GAME [MOUSE BUTTON CLICK EVENTS]
            if event.type == pygame.MOUSEBUTTONDOWN:
                 
                # EVENTS FOR MENU WINDOW
                if game.MENU:
                    if game.isCollideCircle(pygame.mouse.get_pos(), game.menu.playRect):
                        game.clickSound.play(game.EFFECTS)
                        game.CLICKED = True
                        game.MENU = False
                        game.MODE = True
                        game.CLICKED = False
                        game.updateMode()
                            

                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.menu.musicRect):
                        game.clickSound.play(game.EFFECTS)
                        game.menu.chamgeImg("music")
                        screen.fill(BG_COLOR)
                        game.menu.drawAll(screen)

                        if game.menu.music:
                            game.music.unpause()
                        elif not game.menu.music:
                            game.music.pause()


                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.menu.soundRect):
                        game.clickSound.play(game.EFFECTS)
                        game.menu.chamgeImg("sound")
                        screen.fill(BG_COLOR)
                        game.menu.drawAll(screen)

                        if game.menu.sound:
                            game.EFFECTS = True
                        elif not game.menu.sound:
                            game.EFFECTS = False


                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.menu.exitRect):
                        game.clickSound.play(game.EFFECTS)
                        pygame.quit()
                        sys.exit()


                # EVENTS FOR MODE WINDOW
                elif game.MODE:

                    if game.isCollideRect(pygame.mouse.get_pos(), game.mode.playBVPRect):
                        game.clickSound.play(game.EFFECTS)
                        game.CLICKED = True
                        game.MODE = False
                        game.NAME_BVP = True
                        game.CLICKED = False
                        game.updateNameBvP()
                            

                    elif game.isCollideRect(pygame.mouse.get_pos(), game.mode.playPVPRect):
                        game.clickSound.play(game.EFFECTS)
                        game.CLICKED = True
                        game.MODE = False
                        game.NAME_PVP = True
                        game.CLICKED = False
                        game.updateNamePvP()
                            
                    
                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.mode.exitRect):
                        game.clickSound.play(game.EFFECTS)
                        game.CLICKED = True
                        game.MODE = False
                        game.MENU = True
                        game.CLICKED = False
                        game.updateMenu()

                
                # EVENTS FOR NAME_BVP WINDOW
                elif game.NAME_BVP:
                    if game.nameBvP.pNameField.inputRect.collidepoint(pygame.mouse.get_pos()):
                        game.hoverSound.play(game.EFFECTS)
                        game.nameBvP.pNameField.active = True
                        game.nameBvP.pNameField.cursor = "|"
                        game.updateNameBvP()
                    else:
                        game.nameBvP.pNameField.active = False
                        game.nameBvP.pNameField.cursor = ""
                        game.updateNameBvP()


                    if game.isCollideRect(pygame.mouse.get_pos(), game.nameBvP.submitRect):
                        player = game.nameBvP.pNameField.userText
                        opponent = game.nameBvP.oNameField.userText
                        if player != "":
                            game.clickSound.play(game.EFFECTS)
                            game.music.pause()
                            game.gameArea.setPlayers((player, 0), (opponent, 0) , game.nameBvP.pNameField.inputRect, game.nameBvP.oNameField.inputRect)
                            game.CLICKED = True
                            game.NAME_BVP = False
                            game.GAME_AREA = True
                            game.CLICKED = False
                            game.gameType = "ai"
                            game.runing = True
                            game.updateGameArea()


                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.nameBvP.exitRect):
                        game.clickSound.play(game.EFFECTS)
                        game.nameBvP.pNameField.userText = ""
                        game.CLICKED = True
                        game.NAME_BVP = False
                        game.MODE = True
                        game.CLICKED = False
                        game.updateMode()


                # EVENTS FOR NAME_PVP WINDOW
                elif game.NAME_PVP:
                    if game.namePvP.pNameField.inputRect.collidepoint(pygame.mouse.get_pos()):
                        game.hoverSound.play(game.EFFECTS)
                        game.namePvP.oNameField.cursor = ""
                        game.namePvP.oNameField.active = False
                        game.namePvP.pNameField.cursor = "|"
                        game.namePvP.pNameField.active = True
                        game.updateNamePvP()
                    elif game.namePvP.oNameField.inputRect.collidepoint(pygame.mouse.get_pos()):
                        game.hoverSound.play(game.EFFECTS)
                        game.namePvP.pNameField.cursor = ""
                        game.namePvP.pNameField.active = False
                        game.namePvP.oNameField.cursor = "|"
                        game.namePvP.oNameField.active = True
                        game.updateNamePvP()
                    else:
                        game.namePvP.pNameField.cursor = ""
                        game.namePvP.oNameField.cursor = ""
                        game.namePvP.pNameField.active = False
                        game.namePvP.oNameField.active = False
                        game.updateNamePvP()


                    if game.isCollideRect(pygame.mouse.get_pos(), game.namePvP.submitRect):
                        player = game.namePvP.pNameField.userText
                        opponent = game.namePvP.oNameField.userText
                        if player != "" and opponent != "":
                            game.clickSound.play(game.EFFECTS)
                            game.music.pause()
                            game.gameArea.setPlayers((player, 0), (opponent, 0), game.namePvP.pNameField.inputRect, game.namePvP.oNameField.inputRect)
                            game.gameType = "normal"
                            game.CLICKED = True
                            game.NAME_PVP = False
                            game.GAME_AREA = True
                            game.CLICKED = False
                            game.runing = True
                            game.updateGameArea()


                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.namePvP.exitRect):
                        game.clickSound.play(game.EFFECTS)
                        game.namePvP.pNameField.userText = ""
                        game.namePvP.oNameField.userText = ""
                        game.CLICKED = True
                        game.NAME_PVP = False
                        game.MODE = True
                        game.CLICKED = False
                        game.updateMode()


                # EVENTS FOR GAME AREA WINDOW
                elif game.GAME_AREA and game.runing:
                    pos = event.pos
                    if ((pos[0] >= PADX and pos[0] <= WIDTH - MARGIN) and (pos[1] >= 0 and pos[1] <= HEIGHT - MARGIN)):
                        row = pos[1] // SQSIZE
                        col = (pos[0] - PADX) // SQSIZE

                        if game.gameType == "normal":
                            if game.board.empty_sqr(row, col) and game.runing:
                                game.placeSound.play(game.EFFECTS)
                                game.makeMove(row, col)
                                pygame.display.update()

                        elif game.gameType == "ai":
                            if game.board.emptySqr(row, col) and game.player == 1 and game.runing:
                                game.placeSound.play(game.EFFECTS and game.player == 1)
                                game.makeMove(row, col)
                                pygame.display.update()

                                if game.board.marked_sqrs != 9:
                                    Thread(target=game.aiMove).start()
                                    
                        game.updateNameFocus()

                        if game.isover() and game.runing:
                            outcome = game.isover()

                            # --------------- UPDATE SCORES
                            if outcome == 1: 
                                game.updateScores(1, 0)
                            elif outcome == 2:
                                game.updateScores(0, 1)


                            # if game.gameArea.playerScore == 5 or game.gameArea.opponentScore == 5:
                            #     game.showEndText("GAMEOVER - ECS TO GO BACK", OVER_COLOR)
                            #     pygame.display.update()
                            #     # game.over = True
                            #     game.runing = False

                        
                            game.showEndText("PRESS SPACEBAR TO RESTART", OVER_COLOR)
                            pygame.display.update()
                            game.runing = False


            # KEYBOARD EVENTS FOR TYPING NAMES, ETC...
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    if game.nameBvP.pNameField.active or game.namePvP.pNameField.active:
                        if game.NAME_BVP:
                            game.nameBvP.pNameField.userText = game.nameBvP.pNameField.userText[:-1]
                            game.updateNameBvP()
                        else:
                            game.namePvP.pNameField.userText = game.namePvP.pNameField.userText[:-1]
                            game.updateNamePvP()

                    elif game.namePvP.oNameField.active:
                        game.namePvP.oNameField.userText = game.namePvP.oNameField.userText[:-1]
                        game.updateNamePvP()


                elif (event.key <= 90 and event.key >= 65) or (event.key <= 122 and event.key >= 97):
                    if game.nameBvP.pNameField.active or game.namePvP.pNameField.active:
                        if game.NAME_BVP:
                            game.nameBvP.pNameField.userText += event.unicode if len(game.nameBvP.pNameField.userText) < 10 else ""
                            game.updateNameBvP()
                        else:
                            game.namePvP.pNameField.userText += event.unicode if len(game.namePvP.pNameField.userText) < 10 else ""
                            game.updateNamePvP()
                    
                    elif game.namePvP.oNameField.active:
                        game.namePvP.oNameField.userText += event.unicode if len(game.namePvP.oNameField.userText) < 10 else ""
                        game.updateNamePvP()


                elif event.key == pygame.K_SPACE and not game.runing and game.GAME_AREA:
                    game.reset()

                # elif event.key == pygame.K_ESCAPE and not game.runing and game.over and game.GAME_AREA:
                #     game.reset()
                #     game.GAME_AREA = False
                #     game.MENU = True
        

        pygame.display.update()         # UPDATES THE GAME
        clock.tick(FPS)                 # THIS WILL MAINTAIN THE FRAME RATE OF 60FPS


if __name__ == '__main__':
    main()          # ENTRY POINT OF THE GAME
