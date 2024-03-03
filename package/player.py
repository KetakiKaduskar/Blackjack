import package.card_deck as card_deck
import random

class Player:
    def __init__(self):
        self.bank = 1000
        self.deck = card_deck.Deck()
        self.playhand = [self.deck.deal(), self.deck.deal()]
        self.dealhand = [self.deck.deal()]

    def addPlayCard(self):
        if len(self.deck.cards) == 0:
            self.deck.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            self.deck.suits = ['d', 's', 'h', 'c']
            self.deck.cards = list(set([card_deck.Card(rank, suit) for rank in self.deck.ranks for suit in self.deck.suits]) - set(self.playhand) - set(self.dealhand))
            # print(self.deck.cards, self.playhand, self.dealhand)
        random.shuffle(self.deck.cards)
        self.playhand.append(self.deck.cards.pop())

    def addDealCard(self):
        if len(self.deck.cards) == 0:
            self.deck.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            self.deck.suits = ['d', 's', 'h', 'c']
            self.deck.cards = list(set([card_deck.Card(rank, suit) for rank in self.deck.ranks for suit in self.deck.suits]) - set(self.playhand) - set(self.dealhand))
            # print(self.deck.cards, self.playhand, self.dealhand)
        random.shuffle(self.deck.cards)
        self.dealhand.append(self.deck.cards.pop())

    def newRoundHand(self):
        if len(self.deck.cards) < 4:
            self.deck.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            self.deck.suits = ['d', 's', 'h', 'c']
            self.deck.cards = [card_deck.Card(rank, suit) for rank in self.deck.ranks for suit in self.deck.suits]
        self.playhand.clear()
        self.addPlayCard()
        self.addPlayCard()
        self.dealhand.clear()
        self.addDealCard()

    def getCardValue(self, card):
        if card.rank in ['J', 'Q', 'K']:
            return 10
        elif card.rank == 'A':
            return 11
        else:
            return int(card.rank) 
        
    def getPlayerHandValue(self):
        playerhandValue = 0
        for i in range(len(self.playhand)):
            playerhandValue += self.getCardValue(self.playhand[i])
        playhandList = list(map(str, self.playhand))
        if ('A-h' in playhandList) or ('A-s' in playhandList) or ('A-c' in playhandList) or ('A-d' in playhandList):
            if playerhandValue > 21:
                playerhandValue -= 10
        return playerhandValue
    
    def getDealerHandValue(self):
        dealerhandValue = 0
        for i in range(len(self.dealhand)):
            dealerhandValue += self.getCardValue(self.dealhand[i])
        return dealerhandValue
    

if __name__ == "__main__":
    player = Player()
    print(player.playhand[0], player.playhand[1])
    print(player.getPlayerHandValue())
    print(player.dealhand[0], player.dealhand[1])
    print(player.getDealerHandValue())