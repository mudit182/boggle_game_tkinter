import random
import bisect


class Boggle:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = []
        for i in range(self.row):
            rowList = []
            rowList.extend([0] * self.col)
            self.board.append(rowList)

        self.vowelDensity = "eeeaaaoooiiuuy"
        self.consonantDensity = "nnnnrrrrttttllllssssdddggghhhmmmbbccffppvvwwjkqxz"
        self.genVowelIndicators()
        self.genLetters()

    def findAllWords(self):
        self.createDatabase()
        self.validWords = []
        self.boardBeenHere = []
        for i in range(self.row):
            rowList = []
            rowList.extend([False] * self.col)
            self.boardBeenHere.append(rowList)
        self.startSequences()
        self.validWords = sorted(set(self.validWords))

    def getWords(self):
        return self.validWords

    def printWords(self):
        for i in range(10):
            print("***")
        for word in self.validWords:
            print(word)
        for i in range(10):
            print("***")

    def isOutside(self, r, c):
        if r > -1 and r < self.row and c > -1 and c < self.col:
            return False
        else:
            return True

    def getNeighborIndicators(self, r, c):
        neighborIndicators = []
        if not self.isOutside(r, c - 1):
            neighborIndicators.append(self.board[r][c - 1])
        if not self.isOutside(r - 1, c - 1):
            neighborIndicators.append(self.board[r - 1][c - 1])
        if not self.isOutside(r - 1, c):
            neighborIndicators.append(self.board[r - 1][c])
        if not self.isOutside(r - 1, c + 1):
            neighborIndicators.append(self.board[r][c + 1])
        return neighborIndicators

    def genVowelIndicators(self):
        for i in range(self.row):
            for j in range(self.col):
                neighborIndicators = self.getNeighborIndicators(i, j)
                numVowels = sum(v for v in neighborIndicators if v == 1)
                numConsonants = sum(c for c in neighborIndicators if c == 0)
                vowelSurplus = numVowels - numConsonants
                decider = random.randint(-4, 4)
                if decider > vowelSurplus:
                    self.board[i][j] = 1
                else:
                    self.board[i][j] = 0

    def genLetters(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j] == 1:
                    vowelIndex = random.randint(0, len(self.vowelDensity) - 1)
                    self.board[i][j] = self.vowelDensity[vowelIndex]
                else:
                    consonantIndex = random.randint(
                        0,
                        len(self.consonantDensity) - 1)
                    self.board[i][j] = self.consonantDensity[consonantIndex]

    def printBoard(self):
        for i in range(self.row):
            for j in range(self.col):
                print(self.board[i][j], end=" ")
            print('\n')

    def createDatabase(self):
        try:
            with open("Resources/corncob_lowercase.txt") as file:
                wordsAsString = file.read()
        except FileNotFoundError:
            print("File containing valid words not found!")
            wordsAsString = ''
        self.allWords = wordsAsString.split('\n')

    def isInDatabase(self, word):
        wordIndex = bisect.bisect_left(self.allWords, word)
        if wordIndex != len(
                self.allWords) and self.allWords[wordIndex] == word:
            return True
        else:
            return False

    def sequenceStillValid(self, word):
        wordIndex = bisect.bisect_left(self.allWords, word)
        if wordIndex != len(self.allWords) and len(word) <= len(
                self.allWords[wordIndex]) and self.allWords[wordIndex][:len(
                    word)] == word:
            return True
        else:
            return False

    def getAllAdjacentCells(self, r, c):
        allAdjacentCells = []
        possibleAdjacentCells = [(r, c + 1), (r + 1, c + 1), (r + 1, c),
                                 (r + 1, c - 1), (r, c - 1), (r - 1, c - 1),
                                 (r - 1, c), (r - 1, c + 1)]
        for possibleCell in possibleAdjacentCells:
            if not self.isOutside(possibleCell[0], possibleCell[1]):
                allAdjacentCells.append(possibleCell)
        return allAdjacentCells

    def startSequences(self):
        for i in range(self.row):
            for j in range(self.col):
                self.extendSequenceFromCell(i, j)

    def extendSequenceFromCell(self, r, c, sequence=None):
        if sequence is None:
            sequence = self.board[r][c]
        else:
            sequence += self.board[r][c]
        self.boardBeenHere[r][c] = True

        adjacentCells = self.getAllAdjacentCells(r, c)
        for cell in adjacentCells:
            if not self.boardBeenHere[cell[0]][cell[1]]:
                possibleSequence = sequence + self.board[cell[0]][cell[1]]
                if self.sequenceStillValid(possibleSequence):
                    self.extendSequenceFromCell(cell[0], cell[1], sequence)
        if len(sequence) > 3 and self.isInDatabase(sequence):
            self.validWords.append(sequence)

        self.boardBeenHere[r][c] = 0
