from random import shuffle
from time import sleep
from tkinter import *

#custom widget-class för våra memory kort
class MemoryCard(Frame):
    def __init__(self, parent, imgUrl):
        Frame.__init__(self, parent)

        self.front = PhotoImage(file=imgUrl)
        self.imgUrl = imgUrl
        self.back = PhotoImage(file="images/logo.gif")
        self.button = Button(self, image=self.back)
        self.button.pack()
        
    def turnCard(self, side):
        if side == "front":
            self.button.configure(image=self.front)
        else:
            self.button.configure(image=self.back)

    def reset(self, i):
        self.button.configure(command=lambda:flip(i), state=NORMAL, bg="white")
        self.button.configure()
        
    def disable(self, color):
        self.button.configure(state=DISABLED, bg=color)

#globala variabler för att hålla koll på spelet
secondCard = False
prevId = 0
activePlayer = "red"
rScore = 0
bScore = 0

#Funktion för att ge en spelare mer poäng
def score():
    global activePlayer
    global rScore
    global bScore
    
    if activePlayer == "red":
        rScore += 1
        scoreRed.configure(text="Score: " + str(rScore))
    else:
        bScore += 1
        scoreBlue.configure(text="Score: " + str(bScore))
    
#Funktion för att byta mellan spelarna
def playerSwitch():
    global activePlayer
    global PlayerLabel
    
    if activePlayer == "red":
        activePlayer = "blue"
    else:
        activePlayer = "red"
    playerLabel.configure(text="Player: " + activePlayer,fg=activePlayer)
    

#Flip funktion för att faktiskt flippa korten, och kolla om de är samma
def flip(num):
    global secondCard
    global prevId

    # Om samma ruta som förra gången, avbryt
    if num == prevId: 
        return
    
    #vänd själva kortet
    cardlist[num].turnCard("front")
    main.update()

    #se om man behöver jämföra korten
    if secondCard:

        sleep(1)
        
        #Om kortens bilder är samma, disable:a båda knapparna
        if cardlist[num].imgUrl == cardlist[prevId].imgUrl:
            score()
            cardlist[num].disable(activePlayer)
            cardlist[prevId].disable(activePlayer)
            
        #annars, vänta en sekund och vänd sedan tillbaka korten
        else:
            cardlist[prevId].turnCard("back")
            cardlist[num].turnCard("back")
            playerSwitch()
            
        secondCard = False
    #om inte, spara vad det första kortet var och ändra så att click() jämför korten nästa gång
    else:
        prevId = num
        secondCard = True

#reset funktion för hela bordet
def reset():
    global playerLabel, scoreRed, scoreBlue

    
    #blanda korten
    shuffle(cardlist)
    i = 0
    
    #Lägg ut korten i ett 4x4 grid
    for r in range(1,5):
        for c in range(4):
            cardlist[i].reset(i)
            cardlist[i].turnCard("back")
            cardlist[i].grid(row=r,column=c)
            i+=1
            
    #stoppa ner knappen längst ner till vänster
    resetButton = Button(main, text="reset", command=lambda:reset()).grid(column=0,row=0)

    playerLabel.configure(text="Player: red", fg="red")
    playerLabel.grid(column=1,row=0)

    scoreRed.configure(text="Score: 0")
    scoreRed.grid(column=2, row=0)

    scoreBlue.configure(text="Score: 0")
    scoreBlue.grid(column=3, row=0)



main = Tk()
main.wm_title("Memory")

#skapa en lista med två kort för varje bild
cardlist = []
for i in range(8):
    fil = "images/" + str(i) + ".gif"
    cardlist.append(MemoryCard(main, fil))
    cardlist.append(MemoryCard(main, fil))
playerLabel = Label(main)
scoreRed = Label(main, fg="red")
scoreBlue = Label(main, fg="blue")
  
#starta bordet  
reset()
main.mainloop()
