import random

import pygame
from pygame import mixer  # For adding sound effects

pygame.init()

screen = pygame.display.set_mode((1280, 750))  # Resolution of the pygame window

pygame.display.set_caption("Hangman")  # Caption and Icon
icon = pygame.image.load('hangman-game.png')
pygame.display.set_icon(icon)
# fonts
hangmanfont = pygame.font.Font("hangmanfont.ttf", 100)  # font used to show title
wordfont = pygame.font.Font("hangmanfont.ttf", 85)   # font used to show the typed words
loadfont = pygame.font.Font("Vogue.ttf", 25)   # font used in the load word screen
loadfont2 = pygame.font.Font("Vogue.ttf", 40)  # font used in the load word screen
chancefont = pygame.font.Font("Vogue.ttf", 20)   # font for showing chances left(also used in load screen)
chancefont2 = pygame.font.Font("Vogue.ttf", 30)   # font for showing chances left(also used in load screen)
gameoverfont1 = pygame.font.Font("Vogue.ttf", 120)   # font to show the "game over" message
gameoverfont2 = pygame.font.Font("Vogue.ttf", 35)     # font to show the "game over" message

letterlist = []
running = True
color = (0, 60, 70)
begin = False
a = "Welcome Screen"  # a will be used to switch between welcome, load and game screen
array = []
word = ""
worddecided = False
countdown = 10
wordguessed = False
i = 30
inputrect = pygame.Rect(600, 155, 300, 60)  # Input rectangle for loading screen
pressedkey = ''  # Pressed key during running of the game
coloractive = pygame.Color(0, 200, 200)  # colour when inputbox selected
colorpassive = pygame.Color(255, 255, 255)  # colour when inputbox not selected
colora = colorpassive
active = False  # to denote if inputbox is selected
usertext = ""  # contains user input that will be saved in text file
typedletters = {}
wrongletters = []
prevkey = 0
h = ""
t = 0
k = 0
soundcount = 0  # to keep count of winning or losing sound


def title(x, y):  # to load the title
    name = hangmanfont.render("HANGMAN", True, (255, 255, 0))
    screen.blit(name, (x, y))


def enterword(x, y):  # instructions regarding entering the word
    name = loadfont2.render("Enter your word here", True, (255, 255, 0))
    name2 = loadfont.render("Click the input box to enter the word.", True, (255, 255, 0))
    name3 = loadfont.render("This word will be added to the Hangman Word Database.", True, (255, 255, 0))
    name4 = loadfont.render("Please do not enter a word more than 10 letters long.", True, (255, 255, 0))
    name5 = loadfont.render("The application will save the word and terminate after pressing the Enter key.", True,
                            (255, 255, 0))
    screen.blit(name, (x, y))
    screen.blit(name2, (x, y + 100))
    screen.blit(name3, (x, y + 140))
    screen.blit(name4, (x, y + 180))
    screen.blit(name5, (x, y + 220))


def loadbutton(x, y):  # load button on start screen
    name = pygame.image.load("loadcl.png")  # load this image when mouse cursor not on button
    screen.blit(name, (x, y))
    w = 350
    h = 120
    mouse = pygame.mouse.get_pos()  # get position for mouse(used for clicking the button)
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        name = pygame.image.load("loadop.png")  # load this image when mouse cursor on button
        screen.blit(name, (x, y))
        if click[0] == 1:
            global a
            a = "Load Screen"


def loadwords(x,y):  # this function will show the words in the database in the load screen
    name = loadfont2.render("Words present in database are:", True, (153, 168, 255))
    screen.blit(name, (x, y))
    f = open('words.txt', "r")   # open the text file and read the first line
    words = f.readline().split()   # collecting the database words in the list
    f.close()
    m = 0
    for j in range(8):  # number of rows
        if m == len(words):
            break
        for i in range(5):  # number of columns
            m += 1
            if m==len(words):
                break
            word = words[m]
            name = chancefont.render(word, True, (153, 168, 255))
            screen.blit(name, (x-40+j*150, y+50 +i*50))

def startbutton(x, y):  # start button on start screen
    name = pygame.image.load("startcl.png")  # load this image when mouse cursor on button
    screen.blit(name, (x, y))
    w = 350
    h = 120
    mouse = pygame.mouse.get_pos()  # get position for mouse(used for clicking the button)
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        name = pygame.image.load("startop.png")  # load this image when mouse cursor not on button
        screen.blit(name, (x, y))
        if click[0] == 1:
            global a
            a = "Game"


def chancesleft(x, y, countdown, wrongletters):  # here you'll blit the images, as well as the chances left
    if countdown == 1:  # grammar is important, so we'll make the word "chances" to "chance" when countdown is at 1
        name = chancefont2.render("You have " + str(countdown) + " chance left", True, (153, 168, 255))
        screen.blit(name, (x, y))
    else:
        name = chancefont2.render("You have " + str(countdown) + " chances left", True, (153, 168, 255))
        screen.blit(name, (x, y))
    wrongletterstring = ", ".join(wrongletters)
    if countdown < 10:  # Don't show used letters until a mistake is made
        name2 = chancefont.render("used letters are " + wrongletterstring, True, (153, 168, 255))
        screen.blit(name2, (x, y + 50))
    if countdown == 0:  # when the mistake countdown reaches zero, show the "game lost" picture
        name = pygame.image.load("Gameover.png")
        screen.blit(name, (0, 110))
    if countdown >= 1:  # blit images corresponding to chances left
        name = pygame.image.load("hangman" + str(10 - countdown) + ".png")
        screen.blit(name, (0, 110))


def underlines(x, y):  # blit the underlines for the hangman words
    name = pygame.image.load("underline.png")
    screen.blit(name, (x, y))


def lettersoverunderline():  # to blit the letters that were correctly guessed by the user
    lex = 60
    ley = 628
    k = 120
    global typedletters
    for i, j in typedletters.items():
        name = wordfont.render(j.upper(), True, (255, 255, 0))  # render the words in uppercase
        screen.blit(name, (lex + k * i, ley))


def rungame():  # most important function
    undx = 50  # x coord of underlines
    undy = 700  # y coord of underlines
    global worddecided  # a few global variables would be required here
    global word
    global countdown
    global letterlist
    global prevkey
    global typedletters
    if worddecided == False:  # if word not decided, choose a random word from file
        f = open('words.txt', "r")  # words will only be saved in the first line
        lines = f.readlines()
        array = lines[0].split()
        p = random.randint(0, len(array) - 1)  # generate a random integer to select a word from the text file
        word = array[p]  # assign the word corresponding to the random integer
        for i in word:
            letterlist.append(i)
        letterlist = list(set(letterlist))
        worddecided = True
    for i in range(len(word)):
        underlines(undx, undy)
        undx += 120
    for i in range(len(word)):
        if pressedkey == word[i] and i not in typedletters.keys():  # commands for when the correct letter is guessed
            typedletters[i] = pressedkey
    if pressedkey not in word and pressedkey not in wrongletters:  # count down if wrong letter entered
        wrongletters.append(pressedkey)
        countdown -= 1

    lettersoverunderline()  # blit the letters over the lines when they are typed by the player
    chancesleft(840, 140, countdown, wrongletters)
    if len(word) == len(typedletters.keys()):
        victory(700, 280)  # initiate victory sequence when all the letters are typed


def gameover(x, y, w):  # actions for when the player loses
    global h
    global soundcount
    name = gameoverfont1.render("GAME", True, (255, 255, 0))
    name2 = gameoverfont1.render("OVER!", True, (255, 255, 0))
    name3 = gameoverfont2.render("The correct word was " + w, True, (255, 255, 0))
    screen.blit(name, (x + 150, y))
    screen.blit(name2, (x + 150, y + 100))
    screen.blit(name3, (x + 30, y + 250))
    if soundcount == 0:
        losesound = mixer.Sound("lose.wav")  # losing sound
        losesound.play()
        soundcount = 1  # this soundcount variable was necessary to avoid repetition of sound with every frame update
    h = "gameover"


def victory(x, y):  # actions for when the player wins
    global t
    global h
    global soundcount
    name = pygame.image.load("win.png")
    screen.blit(name, (0, 110))
    name = pygame.image.load("happyguy.png")  # the hangman mascot smiles when we win
    screen.blit(name, (383, 180 + t))
    if t < 120:
        t += 5
    name = gameoverfont1.render("You Won!", True, (255, 255, 0))
    screen.blit(name, (x, y))
    name = gameoverfont2.render("Congratulations!", True, (255, 255, 0))
    screen.blit(name, (x + 60, y + 140))

    if soundcount == 0:
        winsound = mixer.Sound("win.wav")  # winning sound
        winsound.play()
        soundcount = 1  # this soundcount variable was necessary to avoid repetition of sound with every frame update
    h = "gameover"


# Changing surface color
screen.fill(color)
# Changing surface color
clock = pygame.time.Clock()
while running:  # actual execution starts here
    screen.fill(color)

    if a == "Welcome Screen":  # Welcome screen properties
        startbutton(430, 300)
        loadbutton(430, 450)
        title(355, 30)
    elif a == "Load Screen":  # Load screen properties
        title(355, 30)
        if active == True:
            colora = coloractive
        else:
            colora = colorpassive
        loadwords(100,450)
        pygame.draw.rect(screen, colora, inputrect, 2)
        textsurface = gameoverfont2.render(usertext, True, (255, 255, 0))
        screen.blit(textsurface, (inputrect.x + 5, inputrect.y + 10))
        enterword(100, 180)
    elif a == "Game":  # execute games
        i -= 4
        if i <= 0:
            i = 0
        title(355, i)
        rungame()  # rungame contains all the important codes
        if countdown == 0:
            gameover(580, 250, word)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # quit
        if a == "Game" and h == "":  # getting letters for game screen
            if event.type == pygame.KEYDOWN:  # check if any key is pressed
                Pressedkey = event.unicode  # collect text input letter
                pressedkey = Pressedkey.lower()  # convert it to lowercase, to avoid uppercase/lowercase issues
        if a == "Load Screen":  # actions for the load word screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputrect.collidepoint(event.pos):
                    active = True
            if event.type == pygame.KEYDOWN:
                if active == True:
                    if event.key == pygame.K_BACKSPACE:  # backspace functionality
                        usertext = usertext[:-1]
                    elif event.key == pygame.K_RETURN:  # When the user presses the enter key, this executes
                        f = open('words.txt', "r+")
                        data = f.readline()  # Reading this line might seem unnecessary, but it helps to set the cursor at the very end of  the list of words, so that we don't lose data during write
                        f.write(" " + usertext.lower())  # convert the word to lowercase and write into file
                        f.close()
                        pygame.quit()  # closes game when word is added
                    else:
                        usertext += event.unicode  # collects text input

    pygame.display.flip()
    clock.tick(20)  # 20 sec delay between frame updates


