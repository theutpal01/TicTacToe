from ast import With
import pygame, copy, sys, math
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
        self.player = 1
        self.gameType = ""
        self.runing = False

        self.CLICKED = False

        self.menu = MenuScreen()
        self.mode = ModeScreen()
        self.nameBvP = NameScreen("Player's Name:", "Computer Name:")
        self.namePvP = NameScreen("Player's Name:", "Player's Name:")
        self.gameArea = GameArea()
        self.board = Board()
        self.ai = AI()

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

    # BOTTOM - THESE ARE ALL IN GAME FUNC WHEN PLYER PLAYS THE GAME
    def show_lines(self):
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (PADX - 50, 0), (PADX - 50, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (PADX + SQSIZE, 0), (PADX + SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (PADX, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (PADX, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
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

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def isover(self):
        return self.board.final_state(screen, show=True) != 0 or self.board.isfull()

    def reset(self):
        self.board = Board()
        self.player = 1
        self.runing = True
        self.updateGameArea()

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
        self.show_lines()


def main():

    game = Game()
    game.updateMenu()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # EVENTS OTHER THAN QUIT BY CROSS BTN OR USING SHORTCUT
            if event.type == pygame.MOUSEBUTTONDOWN:

                if not game.runing and game.GAME_AREA:
                    game.reset()
                    
                # EVENTS FOR MENU WINDOW
                if game.MENU:
                    if game.isCollideCircle(pygame.mouse.get_pos(), game.menu.playRect):
                        game.CLICKED = True
                        game.MENU = False
                        game.MODE = True
                        game.CLICKED = False
                        game.updateMode()
                            

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
                        game.updateNameBvP()
                            

                    elif game.isCollideRect(pygame.mouse.get_pos(), game.mode.playPVPRect):
                        game.CLICKED = True
                        game.MODE = False
                        game.NAME_PVP = True
                        game.CLICKED = False
                        game.updateNamePvP()
                            
                    
                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.mode.exitRect):
                        game.CLICKED = True
                        game.MODE = False
                        game.MENU = True
                        game.CLICKED = False
                        game.updateMenu()


                
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
                            game.gameType = "ai"
                            game.runing = True
                            game.updateGameArea()


                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.nameBvP.exitRect):
                        game.CLICKED = True
                        game.NAME_BVP = False
                        game.MODE = True
                        game.CLICKED = False
                        game.updateMode()


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
                            game.gameType = "normal"
                            game.runing = True
                            game.updateGameArea()


                    elif game.isCollideCircle(pygame.mouse.get_pos(), game.namePvP.exitRect):
                        game.CLICKED = True
                        game.NAME_PVP = False
                        game.MODE = True
                        game.CLICKED = False
                        game.updateMode()


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
                    pos = event.pos
                    if (pos[0] >= PADX):
                        row = pos[1] // SQSIZE
                        col = (pos[0] - PADX) // SQSIZE

                        if game.player == 1: 
                            game.gameArea.pName.changeColor(screen, FOCUS_COLOR)
                            game.gameArea.oName.changeColor(screen, FG_COLOR)
                        else:
                            game.gameArea.pName.changeColor(screen, FG_COLOR)
                            game.gameArea.oName.changeColor(screen, FOCUS_COLOR)

                        if game.gameType == "normal":
                            if game.board.empty_sqr(row, col) and game.runing:
                                game.make_move(row, col)
                                pygame.display.update()

                        elif game.gameType == "ai":
                            if game.board.empty_sqr(row, col) and game.player == 1 and game.runing:
                                game.make_move(row, col)
                                pygame.display.update()

                            if game.board.marked_sqrs != 9:
                                row, col = game.ai.eval(game.board, screen)
                                game.make_move(row, col)
                                pygame.display.update()

                        if game.isover() and game.runing:
                            game.runing = False
                            game.showEndText("CLICK ANYWHERE TO RESTART", OVER_COLOR)




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
        

        pygame.display.update()


if __name__ == '__main__':
    main()
