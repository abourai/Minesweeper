#Abdelwahab Bourai + abourai + section B

from easygui import *
import random
import os
from Tkinter import*
import tkFont
from PIL import Image, ImageTk

#fires ones after each delay
#used to run the AI at variable speeds
def timerFired(canvas):
    delay = canvas.data.delay # milliseconds
    #only runs when the autoplay is on and the game is still running
    if (canvas.data.isAuto == True and canvas.data.gameOver == False):
        delay = canvas.data.autoDelay # milliseconds
        autoPlay(canvas)
    def f(): timerFired(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

#used to run the timer display in the main game at a constant speed
def scoreTime(canvas):
    delay = canvas.data.delay
    canvas.data.time += 1
    if canvas.data.gameOver == False:
        #checks for victory every second
        checkMines(canvas)
        redrawAll(canvas)
    def f(): scoreTime(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

#left-click
def mousePressed1(event,canvas):
    scanGrid(canvas)
    if(event.y >= 0 and event.y <= canvas.data.scoreBox):
        pass
    #the grid of the game excludes the score box at the top
    row = (event.y - canvas.data.scoreBox)/canvas.data.cellSize
    col = (event.x)/canvas.data.cellSize
    #get bounds for the restart button
    smileyLeft = canvas.data.width/2 - canvas.data.scoreBox /2 
    smileyRight = canvas.data.width/2 + canvas.data.scoreBox /2
    #get bounds for the AI toggle button
    aiLeft = 5 * canvas.data.width/6
    aiRight = canvas.data.width
    #if restart area is pressed, reinitialize the board
    if (event.num == 1 and event.x >= smileyLeft and event.x <= smileyRight
        and event.y <= canvas.data.scoreBox and event.y >= 0):
        init(canvas)
    #display a help screen at the user's request
    elif (event.num == 1 and event.x >= 0 and event.x <= canvas.data.width/6
        and event.y <= canvas.data.scoreBox and event.y >= 0):
        helpMessage()
    #choose an AI if an AI has not been chosen yet, otherwise stop or restart
    elif (event.num == 1 and event.x >= aiLeft and event.x <= aiRight
        and event.y <= canvas.data.scoreBox and event.y >= 0):
        initializeAI(canvas)
    #if the click is on the grid complete the appropriate move
    elif (event.num == 1 and event.y >= canvas.data.scoreBox
          and canvas.data.gameOver == False):
        completeMove(canvas,row,col)
    #only redraw the board when the game has not been lost or won
    if canvas.data.gameOver == False:
        redrawAll(canvas)

#takes in a row and col and completes the appropriate move
def completeMove(canvas,row,col):
    #if there are no mines around the square, recursively reveal
    #tiles until a mine is reached
    if(canvas.data.bottomLayer[row][col] == 0):
            recursive(canvas,row,col)
            canvas.data.count += 1
    elif(canvas.data.bottomLayer[row][col] != 0):
        #cannot die on first move, move mine to top left corner if mine
        #is clicked on during the first move and then recalculate the board
        if(canvas.data.bottomLayer[row][col]
           == 10 and canvas.data.count == 0 and canvas.data.isAuto == False):
            moveMine(canvas, 0,0)
            fixBoard(canvas,row,col)
            canvas.data.topLayer[row][col] = canvas.data.bottomLayer[row][col]
            canvas.data.count += 1
        #if the click reveals a mine, end the game
        elif(canvas.data.bottomLayer[row][col]==10 and canvas.data.count!=0):
            canvas.data.topLayer[row][col] = 10
            print 'Game Over'
            displayMines(canvas)
            canvas.data.win = 2
            redrawAll(canvas)
            gameOver(canvas)
        #if the click simply reveals a number, display the number
        else:
            canvas.data.topLayer[row][col] = canvas.data.bottomLayer[row][col]
            canvas.data.count += 1

#right-click
def mousePressed3(event,canvas):
    scanGrid(canvas)
    if(event.y >= 0 and event.y <= canvas.data.scoreBox):
        pass
    #grid does not include scoreBox at the top
    row = (event.y - canvas.data.scoreBox)/canvas.data.cellSize
    col = (event.x)/canvas.data.cellSize
    if (event.num == 3 and event.y >= canvas.data.scoreBox
        and canvas.data.gameOver == False):
        #if the clicked space was empty, place a flag
        if canvas.data.topLayer[row][col] == 0:
            canvas.data.topLayer[row][col] = 15
            canvas.data.mines -= 1
            redrawAll(canvas)
        #if the clicked space is a flag, place a question mark
        elif canvas.data.topLayer[row][col] == 15:
            canvas.data.topLayer[row][col] = 12
            canvas.data.mines += 1
        #if the clicked space is a question mark, return back to empty
        elif canvas.data.topLayer[row][col] == 12:
            canvas.data.topLayer[row][col] = 0
    redrawAll(canvas)

#handles key events
def keyPressed(event,canvas):
    #restart game
    if event.char == 'r':
        init(canvas)
    #begin an AI solver
    elif event.char == 'a':
        initializeAI(canvas)

def initializeAI(canvas):
    #used when cycling through AI button commands
    canvas.data.originalAuto = True
    #toggle the autosolver mode on/off
    canvas.data.isAuto = not canvas.data.isAuto
    #only choose an AI when one is not currently chosen.
    #to choose a different AI, restart the board
    if canvas.data.isAuto == True and canvas.data.aiLevel == '':
        #displays a dialog box from easyGUI allowing the user three choices
        a = buttonbox(msg='Choose the AI\'s intelligence level', title=
                              'Configuration',
                      choices = ['I have no idea what I\'m doing',
                                 'Decent Minesweeper Player', 'Godly',
                                 'Cancel'])
        #dumb AI that only guesses
        if a[0] == 'I':
            canvas.data.aiLevel = 'stupid'
            #play super slow
            canvas.data.autoDelay = 1000
        #close to human AI, runs two steps per second and occasionally
        #dies, but plays like a human with decent experience in the game
        elif a[0] == 'D':
            canvas.data.aiLevel = 'decent'
            #play at a humanly pace
            canvas.data.autoDelay = 500
        #as the name implies, never dies
        elif a[0] == 'G':
            canvas.data.aiLevel = 'godly'
            #play at an obscene pace
            canvas.data.autoDelay = 25
        #cancel AI selection
        elif a[0] == 'C':
            canvas.data.aiLevel = ''
    #the AI removes any wrong flags, it wants to ensure it solves it right
    removeFalseFlags(canvas)

#uses easyGUI
def game_new():
    #create an entry window for user's name
    n = enterbox(msg='Enter your name.', title='Welcome new user!',
                 strip=True)
    #remind user to enter name
    while n.strip() == "":
        n = enterbox(msg='You forgot to enter a name!', title
                     ='Welcome new player!', strip=True)
    a = buttonbox(msg='Choose a game difficulty', title='Configuration',
                  choices = ['Beginner','Intermediate','Expert'])
    #set up board for either beginner, intermediate, or expert level
    if a[0] == 'B':
        return n, 9, 9, 10
    elif a[0] == 'I':
        return n, 16, 16, 40
    elif a[0] == 'E':
        return n, 25, 25, 99

#show at beginning of game only
#uses easyGUI
def startMessage():
    #ask if users want to learn how to play
    c = ynbox(msg='Hello! Click Yes to learn how to play!', title=' ',
              choices=('Yes', 'No'), image = None)
    #if yes
    if c == 1:
        #import the help file and display in a separate window
        filename = os.path.normcase("manual.txt")
        f = open(filename, "r")
        text = f.readlines()
        f.close()
        textbox("", "Show File Contents", text)
    #if no, wish them luck
    else:
        msgbox(msg='Okay, good luck!', title=' ',
               ok_button='OK', image=None)

#uses easyGUI
#display when user asks for help
def helpMessage():  
    filename = os.path.normcase("manual.txt")
    f = open(filename, "r")
    text = f.readlines()
    f.close()
    textbox("Review the Gameplay", "Show File Contents", text)

#display all mines when a mine is clicked
def displayMines(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.bottomLayer[row][col] == 10:
                canvas.data.topLayer[row][col] = 10

#uses easyGUI
#called when a game is lost
def gameOver(canvas):
    #reset the click/move count
    canvas.data.count = 0
    canvas.data.gameOver = True
    redrawAll(canvas)
    #display a dialog box asking whether or not user wishes to continue
    n = msgbox(msg='You lose ' + canvas.data.name, title='GAME OVER')
    c = ynbox(msg='Would you like to restart?', title=' ',
              choices=('Yes', 'No'), image = None)
    #if yes
    if c == 1:
        #restart
        init(canvas)
    #if no
    else:
        #ask user to close window since root.mainloop() prevents closing window
        #directly from program
        msgbox(msg='Okay, good bye! Close the window on your way out please',
               title=' ', ok_button='OK', image=None)
        canvas.data.stopGame = True

#randomly place mines at the beginning of the game
def plantMines(canvas,m):
    while m > 0:
        a = random.randrange(0,canvas.data.rows)
        b = random.randrange(0,canvas.data.cols)
        if(canvas.data.bottomLayer[a][b] == 0):
            canvas.data.bottomLayer[a][b] = 10
            m -= 1

#recursively move mine to top left corner if first move of game is on a mine
def moveMine(canvas,x,y):
    if canvas.data.bottomLayer[x][y] != 10:
        canvas.data.bottomLayer[x][y] = 10
    else:
        #if the top left corner already has a mine, move to square adjacent
        moveMine(canvas,x,y+1)

#when a mine is moved, set mine's previous spot to empty
def fixBoard(canvas,row,col):
    canvas.data.bottomLayer[row][col] = 0
    #recalculate grid
    scanGrid(canvas)

#calculate values for the bottom layer 
def scanGrid(canvas):
    c = canvas
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if(canvas.data.bottomLayer[row][col] != 10):
                #set each cell equal to the number of mines around it
                c.data.bottomLayer[row][col]=checkNeighbors(c,row,col)

#return the number of mines surrounding the cell
def checkNeighbors(canvas,x,y):
    #reset mine count each time
    mineCount = 0
    #search through adjacent cells and increment mineCount if a mine is found
    for row in xrange(-1 , 2):
        for col in xrange(-1 ,2):
            if(row + x < canvas.data.rows and row + x >= 0 and
               col + y < canvas.data.cols and col + y >= 0):
                if(canvas.data.bottomLayer[x][y] != 10):
                    if(canvas.data.bottomLayer[row + x][col + y] == 10):
                        mineCount+= 1
    return mineCount

#used in testing phases. Prints the bottom layer
def printGrid(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            print '%3d'% canvas.data.bottomLayer[row][col],
        print

#removes all values from the board
def clearGrid(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            canvas.data.bottomLayer[row][col] = 0

#recursively reveals as many empty cells as it can
def recursive(canvas,row,col):
    c = canvas
    c.data.topLayer[row][col] = 11
    c.data.bottomLayer[row][col] = 11
    for a in xrange(-1,2):
        for b in xrange(-1,2):
            if((row + a >= 0) and (row + a < c.data.rows) and
               (col + b >= 0) and (col + b < c.data.cols)):
                if(a != 0 or b != 0):
                    #if the cell is empty, keep revealing
                    if(c.data.bottomLayer[row + a][col + b] == 0):
                        recursive(c,row + a, col + b)
                    #otherwise display its number
                    elif(c.data.bottomLayer[row + a][col + b] > 0 and
                         c.data.bottomLayer[row + a][col + b] < 9):
                        c.data.topLayer[row+a][col+b]=c.data.bottomLayer[row+a][col + b]

#choose either a smiley, dead, or cool face for the restart button
def pickFace(canvas):
    if canvas.data.win == 0:
        #if game is playing
        return canvas.data.smiley
    elif canvas.data.win == 1:
        #if game is won
        return canvas.data.cool
    else:
        #if game is lost
        return canvas.data.dead

#draw menu on top of the board
def drawMenu(canvas):
    w = canvas.data.width
    s = canvas.data.scoreBox
    face = pickFace(canvas)
    canvas.create_rectangle(0,0,w,s,fill='gray', outline = 'gray')
    canvas.create_rectangle(0,0,w/6,s,fill = 'light slate gray')
    canvas.create_text(w/12,s/2, text = 'HELP')
    canvas.create_rectangle(5 * w/6,0,w,s,fill = 'light slate gray')
    #cycle through AI button commands
    if canvas.data.isAuto == True:
        canvas.create_text(11 * w/12,s/2,text = 'Stop AI')
    elif canvas.data.isAuto == False and canvas.data.originalAuto == False:
        canvas.create_text(11 * w/12,s/2,text = 'Pick AI')
    else:
        canvas.create_text(11 * w/12,s/2,text = 'Restart AI')
    canvas.create_image(w/2,s/2,image = face)
    #create scoreboard and timer display
    canvas.create_rectangle(w/6, 0, 2 * w/6,s,fill = 'black', outline='white')
    canvas.create_rectangle(4 * w/6, 0, 5 * w/6,s,fill = 'black',
                            outline = 'white')
    canvas.create_text(3 * w/12,s/2,text = str(canvas.data.mines), fill='Red')
    canvas.create_text(9 * w/12,s/2,text = str(canvas.data.time),fill = 'Red')

#redrawAll calls this to draw the board based on each cells' contents
def drawMineBoard(canvas):
    drawMenu(canvas)
    #uses the bottom layer to draw the the top layer
    for row in xrange(len(canvas.data.bottomLayer)):
        for col in xrange(len(canvas.data.bottomLayer[0])):
            if canvas.data.topLayer[row][col] == 0:
                drawMineCell(canvas,row,col)
            elif canvas.data.topLayer[row][col] == 15:
                drawFlag(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 12):
                 drawQuestionMark(canvas,row,col)
            elif canvas.data.topLayer[row][col] == 1:
                drawOne(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 2):
                 drawTwo(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 3):
                drawThree(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 11):
                 drawEmpty(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 10):
                drawMine(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 4):
                drawFour(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 5):
                drawFive(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 6):
                drawSix(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 7):
                drawSeven(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 8):
                drawEight(canvas,row,col)

def drawMineCell(canvas, row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.blank, anchor = NW)

def drawMine(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.mine, anchor = NW)

def drawFlag(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.flag, anchor = NW)

def drawQuestionMark(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.qmark, anchor = NW)

def drawOne(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.one, anchor = NW)

def drawTwo(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.two, anchor = NW)

def drawThree(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.three, anchor = NW)

def drawFour(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.four, anchor = NW)

def drawEmpty(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_rectangle(left,top,left + canvas.data.cellSize,
                            top + canvas.data.cellSize, fill = 'gray',
                            outline = 'dim gray')

def drawFive(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.five, anchor = NW)

def drawSix(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.six, anchor = NW)

def drawSeven(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.seven, anchor = NW)

def drawEight(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.eight, anchor = NW)

#checks for a win every time scoreTime is fired
def checkMines(canvas):
    flagCount = 0
    mineCount = 0
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.topLayer[row][col] != 0:
                if ((canvas.data.topLayer[row][col] == 15 or
                     canvas.data.topLayer[row][col] == 0)
                    and canvas.data.bottomLayer[row][col] == 10):
                    mineCount += 1
    #only way to win is when all the mines are flagged
    if mineCount == countMines(canvas) and mineCount != 0:
        print 'YOU WIN'
        canvas.data.win = 1
        #reveal all the mines
        finishBoard(canvas)
        redrawAll(canvas)
        canvas.data.gameOver = True
        #display a win message
        winScreen(canvas)

#count the total number of mines in the board
def countMines(canvas):
    count = 0
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.bottomLayer[row][col] == 10:
                count += 1
    return count
    
def redrawAll(canvas):
    canvas.delete(ALL)
    drawMineBoard(canvas)

#calculates the total percentage of tiles that have been revealed
def percentRevealed(canvas):
    count = 0
    for r in xrange(canvas.data.rows):
        for c in xrange(canvas.data.cols):
            if (canvas.data.topLayer[r][c] < 12
                and canvas.data.topLayer[r][c] != 0):
                count += 1
    return count * 1.0 /(canvas.data.rows**2)

#counts the number of blank unrevealed cells in the board
def countBlank(canvas):
    count = 0
    for r in xrange(canvas.data.rows):
        for c in xrange(canvas.data.cols):
            if canvas.data.topLayer[r][c] == 0:
                count += 1
    return count

#loops through board and revels all the mines and other values
def finishBoard(canvas):
    c = canvas
    print 'finishing..'
    for row in xrange(c.data.rows):
        for col in xrange(c.data.cols):
            if(c.data.bottomLayer[row][col] == 0):
                recursive(c,row,col)
            elif(c.data.bottomLayer[row][col] != 0
                 and c.data.bottomLayer[row][col] != 10):
                c.data.topLayer[row][col]=c.data.bottomLayer[row][col]

#displayed when the game is won
def winScreen(canvas):
    canvas.data.delay = 1000
    n = msgbox(msg='You WIN!!! ' + canvas.data.name, title='GAME OVER')
    c = ynbox(msg='Would you like to restart?', title=' ',
              choices=('Yes', 'No'), image = None)
    if c == 1:   
        init(canvas) 
    else:
        msgbox(msg='Okay, good bye! Close the window on your way out please',
               title=' ',ok_button='OK', image=None)
    #resets move count
    canvas.data.count = 0

#calculates number of flags placed by the AI
def flagPercentage(canvas):
    count = 0
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.topLayer[row][col] == 15:
                count += 1
    return 1.0 * count / canvas.data.totalMines * 100

#AI
def autoPlay(canvas):
    if canvas.data.aiLevel == 'stupid':
        #for the low level AI, it simply guesses all over the board
        phaseOne(canvas)
        redrawAll(canvas)
    elif canvas.data.aiLevel == 'decent' and canvas.data.stopGame == False:
        #the smarter AI guesses until 5% of the board is revealed 
        if(percentRevealed(canvas) * 100) < 5:
            phaseOne(canvas)
            redrawAll(canvas)
        #then plants flags based on calculations until 80% of mines are found
        if flagPercentage(canvas) < 80:
            phaseTwo(canvas)
        #phase four finishes the game
        elif flagPercentage(canvas) >= 80 and canvas.data.gameOver == False:
            phaseFour(canvas)
            checkMines(canvas)
    #godly follows the same process as the decent player but at a faster pace
    elif canvas.data.aiLevel == 'godly':
        if(percentRevealed(canvas) * 100) < 5:
            phaseOne(canvas)
            redrawAll(canvas)
        if flagPercentage(canvas) < 90:  phaseTwo(canvas)
        elif flagPercentage(canvas) >= 90 and canvas.data.gameOver == False:
            phaseFour(canvas)
            checkMines(canvas)    

#the AI removes flags marked by a human that are incorrect
def removeFalseFlags(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.topLayer[row][col] == 15:
                if canvas.data.bottomLayer[row][col] != 10:
                    canvas.data.topLayer[row][col] = 0
                    canvas.data.mines += 1

#guessing phase
def phaseOne(canvas):
    print 'Choosing random squares...'
    #choose a random cell
    r = random.randrange(0,canvas.data.rows)
    c = random.randrange(0,canvas.data.cols)
    if(canvas.data.bottomLayer[r][c] == 0 and
       canvas.data.topLayer[r][c] != 15):
        #if cell is blank, reveal
        recursive(canvas,r,c)
        canvas.data.count += 1
    elif(canvas.data.bottomLayer[r][c] != 10 and
         canvas.data.topLayer[r][c] != 15):
        canvas.data.topLayer[r][c] = canvas.data.bottomLayer[r][c]
        canvas.data.count += 1
        redrawAll(canvas)
    elif(canvas.data.bottomLayer[r][c] == 10 and
         canvas.data.topLayer[r][c] != 15 and
         canvas.data.topLayer[r][c] != 10 and canvas.data.count == 0):
        print 'mine moved!!!!!'
        #if mine found on first move, move mine to top left corner
        moveMine(canvas,0,0)
        fixBoard(canvas,r,c)
        canvas.data.topLayer[r][c] = canvas.data.bottomLayer[r][c]
        canvas.data.count += 1
    elif(canvas.data.bottomLayer[r][c] == 10 and
         canvas.data.topLayer[r][c] != 15 and
         canvas.data.topLayer[r][c] != 10 and canvas.data.count!= 0
         and canvas.data.aiLevel == 'godly'):
        #if the game mode is godly, backtrack by recalling phaseOne
        #the reason it is backtracking is because we randomly choose
        #a row and col each time, so we simply choose another one
        #and do not display the mine found
        phaseOne(canvas)
        print 'GAME OVER'
        redrawAll(canvas)
    elif(canvas.data.bottomLayer[r][c] == 10 and
         canvas.data.topLayer[r][c] != 15 and
         canvas.data.topLayer[r][c] != 10 and canvas.data.count!= 0
         and canvas.data.aiLevel != 'godly'):
        #for other levels, when a mine is found end the game
        canvas.data.topLayer[r][c] = 10
        canvas.data.win = 2
        redrawAll(canvas)
        print 'Game Over'
        displayMines(canvas)
        gameOver(canvas)

#phase two of AI solving algorithm
def phaseTwo(canvas):
    value, blankCount = 0,0
    #randomly choosing cells is more efficient that creating a double for loop
    #for all the cells. Calculations are done on one cell per move rather than
    #all cells 
    row = random.randrange(0,canvas.data.rows)
    col = random.randrange(0,canvas.data.cols)
    if canvas.data.topLayer[row][col] == 11: pass
    elif canvas.data.topLayer[row][col] == 15: pass
    elif(canvas.data.bottomLayer[row][col] != 0 and
         canvas.data.bottomLayer[row][col] != 10 and
         canvas.data.topLayer[row][col] != 11):
        value = canvas.data.topLayer[row][col]
        #subtract the number of flags from the value of the cell if that cell
        #is a number. Calculate number of blank cells as well
        for a in xrange(-1,2):
            for b in xrange(-1,2):
                if(row + a >= 0 and row + a < canvas.data.rows and col
                   + b >= 0 and col + b < canvas.data.cols):
                    if(a != 0 or b != 0):
                        if canvas.data.topLayer[row + a][col + b] == 0:
                            blankCount += 1
                        elif canvas.data.topLayer[row + a][col + b] == 15:
                            value -= 1
        #if the number of blank cells is <=  the value of the cell minus
        #adjacent flags, then flag all the blank cells next to that cell
        if blankCount <= value:
            for a in xrange(-1,2):
                for b in xrange(-1,2):
                    if(row + a >= 0 and row + a < canvas.data.rows and col
                       + b >= 0 and col + b < canvas.data.cols):
                        if(a != 0 or b != 0):
                            if canvas.data.topLayer[row + a][col + b] == 0:
                                canvas.data.topLayer[row + a][col + b] = 15
                                canvas.data.mines -= 1
    #call phase three for next step of algorithm
    phaseThree(canvas,row,col)

def phaseThree(canvas,row,col):
    mineCount = 0
    #find the number of flags around the cell
    for e in xrange(-1,2):
        for f in xrange(-1,2):
            if(row + e >= 0 and row + e < canvas.data.rows and col
               + f >= 0 and col + f < canvas.data.cols):
                if(e != 0 or f != 0):
                    if(canvas.data.topLayer[row + e][col + f] == 15):
                        mineCount += 1
    #if the number of flags is equal to the cell's value, reveal all blank
    #cells adjacent to that cell
    if mineCount == canvas.data.topLayer[row][col]:
        for a in xrange(-1,2):
            for b in xrange(-1,2):
                if(row + a >= 0 and row + a < canvas.data.rows and col
                   + b >= 0 and col + b < canvas.data.cols):
                    if(a != 0 or b != 0):
                        if canvas.data.topLayer[row + a][col + b] == 0:
                            recursiveAI(canvas,row+a,col+b)
    redrawAll(canvas)

#this function is similar to phase 3 but modified for phase 4 not phase 2
def removeBlanks(canvas,row,col):
    c = canvas
    if (canvas.data.topLayer[row][col] != 11 and
        canvas.data.topLayer[row][col] != 0):
        mineCount = 0
        for e in xrange(-1,2):
            for f in xrange(-1,2):
                if(row + e >= 0 and row + e < canvas.data.rows and col
                   + f >= 0 and col + f < canvas.data.cols):
                    if(e != 0 or f != 0):
                        if(canvas.data.topLayer[row + e][col + f] == 15):
                            mineCount += 1
        if mineCount == canvas.data.topLayer[row][col]:
            for a in xrange(-1,2):
                for b in xrange(-1,2):
                    if(row + a >= 0 and row + a < canvas.data.rows and col
                       + b >= 0 and col + b < canvas.data.cols):
                        if(a != 0 or b != 0):
                            if canvas.data.topLayer[row + a][col + b] == 0:
                                if canvas.data.bottomLayer[row+a][col+b]==0:
                                    canvas.data.topLayer[row + a][col + b] = 11
                                else:
                                    c.data.topLayer[row+a][col+b]=c.data.bottomLayer[row+a][col+b]
        redrawAll(canvas)

#used in the final stages of the solving algorithm
#instead of randomly choosing like in phase 2, looks for empty cells and
#completes the calculations
def phaseFour(canvas):
    #scans all cells in the board
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            value, blankCount = 0,0
            if (canvas.data.bottomLayer[row][col] != 0 and
                canvas.data.bottomLayer[row][col] != 10 and
                canvas.data.topLayer[row][col] != 11):
                value = canvas.data.topLayer[row][col] 
                for a in xrange(-1,2):
                    for b in xrange(-1,2):
                        if(row + a >= 0 and row + a < canvas.data.rows and col
                           + b >= 0 and col + b < canvas.data.cols):
                            if(a != 0 or b != 0):
                                if canvas.data.topLayer[row + a][col + b] == 0:
                                    blankCount += 1
                                elif canvas.data.topLayer[row+a][col+b]==15:
                                    value -= 1
                if blankCount <= value:
                    for a in xrange(-1,2):
                        for b in xrange(-1,2):
                            if(row+a >= 0 and row+a < canvas.data.rows and col
                               + b >= 0 and col + b < canvas.data.cols):
                                if(a != 0 or b != 0):
                                    if canvas.data.topLayer[row+a][col+b] == 0:
                                        canvas.data.topLayer[row+a][col+b] = 15
                                        canvas.data.mines -= 1
            removeBlanks(canvas,row,col)

#recursive clearing function for AI
def recursiveAI(canvas,row,col):
    c = canvas
    for a in xrange(-1,2):
        for b in xrange(-1,2):
            if((row + a >= 0) and (row + a < canvas.data.rows) and
               (col + b >= 0) and (col + b < canvas.data.cols)):
                if(a != 0 or b != 0):
                    if(canvas.data.bottomLayer[row + a][col + b] == 0):
                        recursive(canvas,row + a, col + b)
                    elif(canvas.data.bottomLayer[row + a][col + b] > 0 and
                         canvas.data.bottomLayer[row + a][col + b] < 9):
                        #this was done for style I wish I didn't have to
                        r = row
                        c.data.topLayer[r+a][col+b
                                             ]=c.data.bottomLayer[r+a][col+b]

#uses PIL to load the faces for the restart button
def loadFaces(canvas):
    im = Image.open('tao-smile.gif')
    im = im.resize((canvas.data.scoreBox,canvas.data.scoreBox),Image.ANTIALIAS)
    smiley = ImageTk.PhotoImage(im)
    canvas.data.smiley = smiley
    im = Image.open('tao-dead.gif')
    im = im.resize((canvas.data.scoreBox,canvas.data.scoreBox),Image.ANTIALIAS)
    dead = ImageTk.PhotoImage(im)
    canvas.data.dead = dead
    im = Image.open('tao-cool.gif')
    im = im.resize((canvas.data.scoreBox,canvas.data.scoreBox),Image.ANTIALIAS)
    cool = ImageTk.PhotoImage(im)
    canvas.data.cool = cool

#uses PIL to load flags, mines, question marks, and blank squares
def loadNonNumbers(canvas):
    im = Image.open('Qmark.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    Qmark = ImageTk.PhotoImage(im)
    canvas.data.qmark = Qmark
    im = Image.open('flag.gif')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    flag = ImageTk.PhotoImage(im)
    canvas.data.flag = flag
    im = Image.open('Blank.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    blank = ImageTk.PhotoImage(im)
    canvas.data.blank = blank
    im = Image.open('mine.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    mine = ImageTk.PhotoImage(im)
    canvas.data.mine = mine

#uses PIL to load all numbers
def loadNumbers(canvas):
    im = Image.open('one.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.one = one = ImageTk.PhotoImage(im)
    im = Image.open('two.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.two = two =  ImageTk.PhotoImage(im)
    im = Image.open('three.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.three = three = ImageTk.PhotoImage(im)
    im = Image.open('four.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.four = four = ImageTk.PhotoImage(im)
    im = Image.open('five.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.five = five = ImageTk.PhotoImage(im)
    im = Image.open('six.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.six = six = ImageTk.PhotoImage(im)
    im = Image.open('seven.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.seven = seven = ImageTk.PhotoImage(im)
    im = Image.open('eight.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.eight = eight = ImageTk.PhotoImage(im)

#loads all the variables needed. also used when restarting game
def init(canvas):
    loadFaces(canvas)
    loadNonNumbers(canvas)
    loadNumbers(canvas)
    canvas.data.count,canvas.data.autoCount = 0,0
    canvas.data.mines = canvas.data.totalMines
    canvas.data.win,canvas.data.time,canvas.data.score = 0,0,0
    canvas.data.aiLevel = ''
    canvas.data.originalAuto = False
    canvas.data.gameOver = False
    canvas.data.delay = 1000
    canvas.data.isAuto = False
    canvas.data.stopGame = False
    canvas.data.autoDelay = canvas.data.delay
    canvas.data.bottomLayer = [[0 for col in xrange(canvas.data.cols)]
                               for row in xrange(canvas.data.rows)]
    canvas.data.topLayer = [[0 for col in xrange(canvas.data.cols)]
                               for row in xrange(canvas.data.rows)]
    plantMines(canvas,canvas.data.mines)
    scanGrid(canvas)
    drawMineBoard(canvas)

#called in run() to begin game
def createGame():
    name, rows, cols, mines = game_new()
    return name,rows,cols,mines

def run():
    #initialize variables from user entry
    name, rows, cols, mines = createGame()
    #welcome player and offer a manual
    startMessage()
    root = Tk()
    #create canvas
    scoreBox,cellSize = 40,30
    canvasWidth = cols*cellSize
    canvasHeight = rows*cellSize + scoreBox
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct()
    #initialize variables
    canvas.data.rows,canvas.data.cols,canvas.data.name = rows,cols,name
    canvas.data.width,canvas.data.height = canvasWidth,canvasHeight
    canvas.data.mines,canvas.data.totalMines = mines,mines
    canvas.data.scoreBox,canvas.data.cellSize = scoreBox,cellSize
    init(canvas)
    redrawAll(canvas)
    #create wrapper functions for events
    def mousePressedFn1(event): mousePressed1(event,canvas)
    def mousePressedFn3(event): mousePressed3(event,canvas)
    root.bind("<Button-3>", mousePressedFn3)
    root.bind("<Button-1>", mousePressedFn1)
    def keyPressedFn(event): keyPressed(event,canvas)
    root.bind("<Key>", keyPressedFn)
    #start timer display's timer fired
    scoreTime(canvas)
    #initialize AI's timer
    timerFired(canvas)
    root.mainloop()  # This call BLOCKS 

run()
