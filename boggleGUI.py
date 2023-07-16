from tkinter import *
from PIL import Image, ImageTk, ImageOps
from boggleClass import *


class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("BOGGLE")
        self.pack(fill=BOTH, expand=1)
        self.setBasicParameters()
        self.setBackground()
        self.loadTileImages()
        self.loadStartButton()
        self.showStartButton()
        self.loadAllWordsButton()
        self.showAllWordsButton()

    def setBasicParameters(self):
        self.w = 800
        self.h = 600
        self.tilesLoaded = []
        self.useTilesMosaic = False

    def setBackground(self):
        imgPath = 'Resources/background.jpg'
        bg = Image.open(imgPath)
        width, height = bg.size
        newWidth = 1200
        newHeight = int(height * newWidth / width)
        bg = bg.resize((newWidth, newHeight), Image.LANCZOS)
        bgProcessed = ImageTk.PhotoImage(bg)
        bgLabel = Label(self, image=bgProcessed)
        bgLabel.image = bgProcessed
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

    def loadTileImages(self):
        imgName = 'a'
        self.tilesMosaic = []
        for i in range(26):
            imgPath = 'Resources/mosaic/' + imgName + '.jpg'
            letterImg = Image.open(imgPath)
            letterImg = letterImg.resize((100, 100), Image.LANCZOS)
            letterImg = ImageOps.expand(letterImg, border=5)
            self.tilesMosaic.append(letterImg)
            # Convert using ImageTk.PhotoImage() before using it inside Label
            imgName = chr(ord(imgName) + 1)

    def loadStartButton(self):
        self.startButton = Button(
            self, text='START', font='Phosphate 35', command=self.startGame, wraplength=800 * 0.20)

    def showStartButton(self):
        self.startButton.place(relx=0.05, rely=0.1, relwidth=0.20)

    def hideStartButton(self):
        self.startButton.place_forget()

    def loadAllWordsButton(self):
        self.allWordsButton = Button(
            self, text='LIST ALL WORDS', font='Baskerville 12', command=self.showWords, wraplength=800 * 0.20)

    def showAllWordsButton(self):
        self.allWordsButton.place(relx=0.05, rely=0.85, relwidth=0.20)

    def startGame(self):
        if hasattr(self, 'wordsList'):
            self.wordsList.place_forget()
        row, col = 5, 5
        self.genBoggleBoard(row, col)
        if self.useTilesMosaic is True:
            self.loadBoggleTiles(row, col)
        else:
            self.loadBoggleTiles(row, col)

    def genBoggleBoard(self, row, col):
        self.boggle = Boggle(row, col)

    def loadBoggleTiles(self, row, col):
        if not len(self.tilesLoaded) == 0:
            self.unloadBoggleTiles()
        startPosX, strideX, startPosY, strideY = self.getTilesFormatting(
            row, col)
        relxPos = startPosX
        relyPos = startPosY
        for i in range(row):
            for j in range(col):
                letterChar = self.boggle.board[i][j]
                letterTile = self.getLetterTile(letterChar,
                                                strideX * self.winfo_width(),
                                                strideY * self.winfo_height())
                letterTile.place(relx=relxPos, rely=relyPos)
                self.tilesLoaded.append(letterTile)
                relxPos += strideX
            relxPos = startPosX
            relyPos += strideY

    def unloadBoggleTiles(self):
        for i in range(len(self.tilesLoaded)):
            self.tilesLoaded[i].place_forget()
        self.tilesLoaded = []

    def getTilesFormatting(self, row, col):
        startPosX = 0.25 + 0.075
        startPosY = 0.1
        strideX = 0.6 / max(row, col)
        strideY = 0.8 / max(row, col)
        return [startPosX, strideX, startPosY, strideY]

    def getLetterTile(self, letterChar, width, height):
        ind = ord(letterChar) - ord('a')
        letterImg = self.tilesMosaic[ind].resize((int(width), int(height)),
                                                 Image.LANCZOS)
        tileTk = ImageTk.PhotoImage(letterImg)
        tileLabel = Label(self, image=tileTk)
        tileLabel.image = tileTk
        return tileLabel

    def showWords(self):
        self.boggle.findAllWords()
        self.words = self.boggle.getWords()
        if hasattr(self, 'wordsList'):
            self.wordsList.place_forget()

        self.wordsList = Listbox(self, font='copperplate 20')

        occupy = len(str(len(self.words)))
        for i in range(len(self.words)):
            num = (occupy - len(str(i + 1))) * '0' + str(i + 1)
            self.wordsList.insert(END, num + '.\t' + self.words[i])

        self.wordsList.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.6)
