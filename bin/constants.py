# ---------
# CONSTANTS
# ---------

# --- PIXELS ---

WIDTH = 800                                 # WIDTH OF GAME WINDOW
HEIGHT = 500                                # HEIGHT OF GAAME WINDOW
PADX = WIDTH - HEIGHT                       # PADDING AT LEFT SIDE IN THE PLAYIING GAME AREA
MARGIN = 3                                  # MARGIN OF THE PLAYING GAME AREA
GAME_TITLE = "Tic Tac Toe - Utpal"          # TITLE OF THE GAME
BOT_NAME = "Undefeatable"                   # NAME OF THE COMPUTER
FPS = 60                                    # FRAME RATE FOR THE GAME

ROWS = 3                                    # ROWS IN THE GAME AREA
COLS = 3                                    # COLUMNS IN THE GAME AREA
SQSIZE = (WIDTH - PADX) // COLS             # BOX SIZE (IN WHICH PLAYER GIVES EITHER X OR O)

LINE_WIDTH = 15                             # WIDTH OF LEACH LINE OF THE GAME
CIRC_WIDTH = 15                             # O ITEM WIDTH [GAME SYMBOL]
CROSS_WIDTH = 20                            # X ITEM WIDTH [GAME SYMBOL]

RADIUS = SQSIZE // 4                        # O ITEM RADIUS [GAME SYMBOL]
OFFSET = 50                                 # AFTER THIS MUSH PADDING PLACE O OR X WHEN USERS CLICKS THE BOX

# --- COLORS ---

BG_COLOR = (28, 170, 156)                   # BG COLOR OF THE GAME WINDOW [SKY BLUE SHADE]
FG_COLOR = (0, 0, 0)                        # TEXT COLOR [BLACK]
FOCUS_COLOR = (242, 239, 234)               # WHOSE MOVE DETECT COLOR [WHITE SHADE]
OVER_COLOR = (251, 139, 36)                 # TEXT COLOR OF GAME OVER MESSAGE [ORANGE SHADE]
LINE_COLOR = (23, 145, 135)                 # GAME AREA LINES COLOR [LIGHT GREY SHADE]
CIRC_COLOR = (239, 231, 200)                # O GAME ITEM COLOR [GREY SHADE]
CROSS_COLOR = (66, 66, 66)                  # X GAME ITEM COLOR [GREY SHADE]


# ----- FILES -------
HEADING = "files/heading.png"                                   # PATH OF HEADING IMAGE [TIC TAC TOE]
MUSIC_ON, MUSIC_OFF = "files/m_on.png", "files/m_off.png"       # PATH OF MUSIC ON AND OFF IMAGES
SOUND_ON, SOUND_OFF = "files/s_on.png", "files/s_off.png"       # PATH OF SOUND ON AND OFF IMAGES
PLAY, EXIT = "files/play.png", "files/exit.png"                 # PATH OF PLAY BUTTON AND EXIT BUTTON IMAGES

PLAY_BVP, PLAY_PVP = "files/computer.png", "files/friend.png"   # PATH OF PLAY WITH COMPUTER AND PLAY WITH FRIEND IMAGES
SUBMIT = "files/submit.png"                                     # PATH OF SUBMIT BUTTON IMAGE
