#Rocco & Logan 351 Final Project

#60 second time limit

players = {}
history = {} #all of these will be given by the Table class the prof made
lastMove = {} 

class Player(object):

    def __init__(self, chips):
        self.hasBet = False #we can only bet once so once we do set to true
        #need to reset it every hand
        self.chips = chips

    def __str__():
        pass

    def action(self, players, history, lastAction, MAX_BID):
        pass
        #return (action, amount)

    def getBestHand(hand, table): #static takes a hand and the cards on the table
        pass
        #returns the best hand aka list of ints 0-51
        #use %13 to check for pairs (same remainder = pair)

    def getWinner(self, hand): #pass it the opponents hand and it returns true if we win and false if not
        

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

        wins = 0
        losses = 0

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
                                    if self.getWinner(getBestHand([a, b], [c, d, e, f, g])):
                                        wins += 1
                                    else:
                                        losses += 1
                                    #we can do an alpha beta type thing where if the hand had enough to win reguardless of the other cards then we add all the instances
                                    #that would occur after so like (51 - c) + (51 - d) ... ect - how many cards are before it times the amount of cards after. So if the A B cards are enough to win 
                                    #you would do (51 - c) + (51 - d) ... (51 - g) - ( 5 * 2) because there are 10 invalid options. ie if A is 2H then g cant be 2H. This is kinda like alpha beta and
                                    #would really help with the runtime.
        return wins / (wins + losses)

class Table(object):
    pass