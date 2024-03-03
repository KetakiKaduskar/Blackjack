import random

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}-{self.suit}"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))
    
class Deck:
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['d', 's', 'h', 'c']
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        
        self.shuffle()
        return self.cards.pop()
    
    def __str__(self):
        return ", ".join(str(c) for c in self.cards)
    
if __name__ == "__main__":
    deck = Deck()
    print(deck)
    print(str(deck.deal()))