#Rocco & Logan 351 Final Project

#60 second time limit

players = {}
history = {} #all of these will be given by the Table class the prof made
lastMove = {} 

class Player(object):

    def __init__(self):
        self.hasBet = False #we can only bet once so once we do set to true
        #need to reset it every hand

    def __str__():
        pass

    def action(self, players, history, lastAction, MAX_BID):
        pass
        #return (action, amount)

    def getBestHand(self):
        pass
        #returns the best hand aka list of ints 0-51
        #use %13 to check for pairs (same remainder = pair)

    def getWinner(self, hand): #pass it the opponents hand and it returns true if we win and false if not
        #will use this in the getProb function to determine if we win or not
        pass

    def getProb(self, hand): #pass it our best hand
        #this function assumes no cards have been flipped
        #if we make the probabiliy of us losing a decimal the probability of us losing is n * pob we lose (n is number of players) so we can use that to get the exact probability
        #https://en.wikipedia.org/wiki/Poker_probability_(Texas_hold_%27em)
        #might be useful ^
        #I was thinking we could start b from 1 and c from 2 ect but that would change the probability and would be wrong
        #this is super brute force and i feel like theres a better way to do this but idk how
        #im thinking there could be something using actual math (what a concept) 
        used = () #maybe use a tuple and do a in used b in used ect instead of or or or or

        for a in range(0,52):
            if a in hand:
                continue
            for b in range(0,52):
                if b == a or b in hand:
                    continue
                for c in range(0,52):
                    if c == a or c == b or c in hand:
                        continue
                    for d in range(0,52):
                        if d == a or d == b or d == c or d in hand:
                            continue
                        for e in range(0,52):
                            if e == a or e == b or e == c or e == d or e in hand:
                                continue
                            for f in range(0,52):
                                if f == a or f == b or f == c or f == d or f == e or f in hand:
                                    continue
                                for g in range(0,52):
                                    if g == a or g == b or g == c or g == d or g == f or g in hand:
                                        continue
                                    pass

class Table(object):
    pass