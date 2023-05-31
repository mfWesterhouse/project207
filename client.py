import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
playerTurn = None
player1Name = 'joining'
player2Name = 'joining'
player1Label = None
player2Label = None

player1Score = 0
player2Score = 0
player2ScoreLabel = None
player2ScoreLabel = None

dice = None

rollButton = None
resetButton = None

winingMessage = None

winingFunctionCall = 0


def checkColorPosition(boxes, color):
    for box in boxes:
        boxColor = box.cget("bg")
        if(boxColor == color):
            return boxes.index(box)
    return False

def movePlayer1(steps):
    global leftBoxes

    boxPosition = checkColorPosition(leftBoxes[1:],"red")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(steps == remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            global finishingBox

            finishingBox.configure(bg='red')

            global SERVER
            global playerName

            greetMessage = f'Red wins the game.'
            SERVER.send(greetMessage.encode())

        elif(steps < remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            leftBoxes[nextStep].configure(bg='red')
        else:
            print("Move False")
    else:
        leftBoxes[steps].configure(bg='red')

def movePlayer2(steps):
    global rightBoxes

    tempBoxes = rightBoxes[-2::-1]

    boxPosition = checkColorPosition(tempBoxes,"yellow")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(diceValue == remainingSteps):
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')

            global finishingBox

            finishingBox.configure(bg='yellow', fg="black")

            global SERVER
            global playerName

            greetMessage = f'Yellow wins the game.'
            SERVER.send(greetMessage.encode())

        elif(diceValue < remainingSteps):
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            rightBoxes[::-1][nextStep].configure(bg='yellow')
        else:
            print("Move False")
    else:

        rightBoxes[len(rightBoxes) - (steps+1)].configure(bg='yellow')



def createTicket():
    global gameWindow
    global ticketGrid

    nianLabel = Label(gameWindow, width=65, height=16, relief="ridge", borderwidth=5, bg="white")
    nianLabel.place(x=95, y=119)

    xPos = 185
    yPos = 130

def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xPos = 30
    for box in range(0,11):
        if(box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="red")
            boxLabel.place(x=xPos, y=screen_height/2 - 88)
            leftBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2- 100)
            leftBoxes.append(boxLabel)
            xPos +=75


def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xPos = 988
    for box in range(0,11):
        if(box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="yellow")
            boxLabel.place(x=xPos, y=screen_height/2-88)
            rightBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xPos +=75


def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 68, y=screen_height/2 -160)



def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winingMessage
    global resetButton
    global flashNumberLabel


    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    canvas2.create_image( 0, 0, image = bg, anchor = "nw")
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    winingMessage = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 250, text = "", font=("Chalkboard SE",100), fill='#fff176')

    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)

    flashNumberLabel = canvas2.create_text(400, screen_height/2.3, text="Waiting for others to join...", font=("Chalkboard SE", 30), fill="#3e2723d")

    leftBoard()
    rightBoard()
    finishingBox()

    global rollButton

    rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)

    global playerTurn
    global playerType
    global playerName
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel

    if(playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
    else:
        rollButton.pack_forget()

    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    player1Label = canvas2.create_text(400,  screen_height/2 + 100, text = player1Name, font=("Chalkboard SE",80), fill='#fff176' )
    player2Label = canvas2.create_text(screen_width - 300, screen_height/2 + 100, text = player2Name, font=("Chalkboard SE",80), fill='#fff176' )

    player1ScoreLabel = canvas2.create_text(400,  screen_height/2 - 160, text = player1Score, font=("Chalkboard SE",80), fill='#fff176' )
    player2ScoreLabel = canvas2.create_text(screen_width - 300, screen_height/2 - 160, text = player2Score, font=("Chalkboard SE",80), fill='#fff176' )


    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Tambola")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)

    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def restGame():
    global SERVER
    SERVER.send("reset game".encode())


def handleWin(message):
    global playerType
    global rollButton
    global canvas2
    global winingMessage
    global screen_width
    global screen_height
    global resetButton

    #destroying button
    if('Red' in message):
        if(playerType == 'player2'):
            rollButton.destroy()

    if('Yellow' in message):
        if(playerType == 'player1'):
            rollButton.destroy()

    # Adding Wining Message
    message = message.split(".")[0] + "."
    canvas2.itemconfigure(winingMessage, text = message)

    #Placing Reset Button
    resetButton.place(x=screen_width / 2 - 80, y=screen_height - 220)

def updateScore(message):
    global canvas2
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel


    if('Red' in message):
        player1Score +=1

    if('Yellow' in message):
        player2Score +=1

    canvas2.itemconfigure(player1ScoreLabel, text = player1Score)
    canvas2.itemconfigure(player2ScoreLabel, text = player2Score)



def handleResetGame():
    global canvas2
    global playerType
    global gameWindow
    global rollButton
    global dice
    global screen_width
    global screen_height
    global playerTurn
    global rightBoxes
    global leftBoxes
    global finishingBox
    global resetButton
    global winingMessage
    global winingFunctionCall

    canvas2.itemconfigure(dice, text='\u2680')

    # Handling Reset Game
    if(playerType == 'player1'):
        # Creating roll dice button
        rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
        playerTurn = True

    if(playerType == 'player2'):
        playerTurn = False

    for rBox in rightBoxes[-2::-1]:
        rBox.configure(bg='white')

    for lBox  in leftBoxes[1:]:
        lBox.configure(bg='white')


    finishingBox.configure(bg='green')
    canvas2.itemconfigure(winingMessage, text="")
    resetButton.destroy()

    # Again Recreating Reset Button for next game
    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)
    winingFunctionCall = 0
#----------------- Boilerplate Code End ---------------


def recivedMsg():
    global SERVER
    global canvas2
    global flashNumberList
    global flashNumberLabel
    global gameOver

    numbers = [ str(i) for i in range(1, 91)]

    while True:
        chunk = SERVER.recv(2048).decode()
        if(chunk in numbers and flashNumberLabel and not gameOver):
            flashNumberList.append(int(chunk))
            canvas2.itemconfigure(flashNumberLabel, text=chunk, font = ('Chalkboard SE', 60))
        elif('wins the game' in chunk):
            gameOver = True
            canvas2.itemconfigure(flashNumberLabel, text=chunk, font= ('Chalkboard SE', 40))
 
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 8000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()




setup()