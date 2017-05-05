 #Rocco & Logan 351 Final Project

#60 second time limit

lastMove = {} 

class Player(object):

    def __init__(self, chips, hand, table):
        self.hasBet = False #we can only bet once so once we do set to true
        #need to reset it every hand
        self.chips = chips
        self.hand = hand
        self.table = table
        
    def action(self, players, history, lastAction, MAX_BID):
        action = ""
        amount = 0
        prob = self.getProb()
        maxBet = 0
        bet = 0

        if prob < 50:
            return ("check", 0) #if this isn't valid the prof's program will make us fold which is okay
        else: #we only want to bet if there is a good chance we win
            maxBet = 0.6 * self.chips
            bet = 0.3 * self.chips
            #need some way to find how much is in the pot and raise/call/fold accordingly*************************
            if table.pot == 3:
                pass


        return (action, amount)

    def getBestHand(self, table): #need to the value function. Make it static, and take a hand aka list. Player.value(hand)
        tempHand = self.hand
        tempHand.extend(table.getFlop())
        bestHand = []
        bestValue = (0, 0)
        possibleHands = itertools.combinations(tempHand, 5)
        handValue = (0, 0)

        for hand in possibleHands:
            handValue = self.value(hand) 
            if handValue[0] < bestValue[0]: #kinda redudant maybe save as a variable>?
                continue
            elif handValue[0] > bestValue[0]:
                bestHand = hand
                bestValue = self.value(bestHand)
            elif handValue[0] == bestValue[0]:
                if bestValue[0] == 6:
                    if handValue[1][0] > bestValue[1][0]:
                        bestHand = hand
                        bestValue = self.value(bestHand)
                    elif handValue[1][0] == bestValue[1][0] and handValue[1][1] > bestValue[1][1]:
                        bestHand = hand
                        bestValue = self.value(bestHand)
                    else:
                        continue
            elif bestValue[0] == 2: #the second element of the list of values (x, this one) will be bigger
                if handValue[1][1] > bestValue[1][1]:
                    bestHand = hand
                    bestValue = self.value(bestHand)
                elif handValue[1][1] == bestValue[1][1] and handValue[1][0] > bestValue[1][0]:
                    bestHand = hand
                    bestValue = self.value(bestHand)
                else:
                    continue

    def getValue(self, hand):

       if self.isStraightFlush(hand) != 0:
           return self.isStraightFlush(hand)
       elif self.ofAKind(hand)[0] == 7: #4 of a kind
           return self.ofAKind(hand)
       elif self.ofAKind(hand)[0] == 6: #full house
           return self.ofAKind(hand)
       elif self.isFlush(hand) != 0: #I could have returned false but it still works so its okay
           return self.isFlush(hand)
       elif self.isStraight(hand):
           return self.isStraight(hand)
       else:
           return self.ofAKind(hand)



        #returns the best hand aka list of ints 0-51
        #returns a number based 0-8 1 being a straight flush 8 being high card and the high card ie (10, 12) aka royal flush (0, 0) being high card 2 (use mod for high card)
        #8 is the best 1 is the worst

    def isStraightFlush(self, hand): #if its true use max(hand) to get the high card of the straight
        if max(hand) - min(hand) <= 4:
            return (8, max(hand))
        else: 
            return 0

    def isStraight(self, hand):
        values = []
        for item in hand:
            values.append(item % 13)

        for item in values: #checks for duplicates
            for item2 in values:
                if item == item2:
                    return 0

        if max(hand) - min(hand) == 4: #checks if its a straight
            return (4, max(hand))

        return 0

    def isFlush(self, hand):
        if max(hand) - min(hand) <= 12:
            return (5, max(hand))
        else:
            return 0

    def ofAKind(self, hand):
        pairs = {
                 0: 0,
                 1: 0,
                 2: 0,
                 3: 0,
                 4: 0,
                 5: 0, 
                 6: 0, 
                 7: 0, 
                 8: 0, 
                 9: 0, 
                 10: 0, 
                 11: 0, 
                 12: 0
                 }

        for card in hand:
            pairs[card % 13] += 1

        vals = list(pairs.values())

        if 4 in vals:
            for i in range(12):
                if pairs[i] == 4:
                    return (7, i) #4 of a king
        if 3 in vals and 2 in vals: #full house
            for i in range(12):
                if pairs[i] == 3:
                    three = i
                elif pairs[i] == 2:
                    two == i
            return (6, (three, two))
        if 3 in vals:
            for i in range(12):
                if pairs[i] == 3:
                    return (3, i)
        if 2 in vals:
            vals.remove(2)
            if 2 in vals: #two pairs
                twos = []
                for i in range(12):
                    if pairs[i] == 2:
                        twos.append(i)
                return (2, twos)
            else: #one pair
                for i in range(12):
                    if pairs[i] == 2:
                        return (1, i)
        else:
            max = 0
            for i in range(12):
                if pairs[i] != 0:
                    max = i
            return (0, max)

    def getProb(self): #pass it our best hand
        possibleHands = 520
        probOfLosing = 0
        winningHands = self.getValue(self.hand)[0] * 52
        winningHands += self.getValue(self.hand)[1]

        probOfLosing = (520 - winningHands) / 520

        probOfLosing *= (self.table.players.length() - 1)

        return (1 - probOfLosing)

class Table(object):
    def __init__(self, players, pot):
        self.players = players
        self.pot = 0
    def getFlop(): #idk what to call this but its just the visible cards in the middle
        pass