"""Define the essential class for identifying the combos later"""
import random 

class Card:
    # Class variables
    CARD_DEF = {'suit':['Squares', 'Clubs', 'Hearts', 'Spades'],
            'rank':['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']}
    RANKS = CARD_DEF['rank']
    SUITS = CARD_DEF['suit']

    def __init__(self, num=-1, **properties):
        """Accept a number from 0 to 51 and convert it into suit and rank, or
        accept the suit and rank as strings to create a Card object."""

        if num < 0 or num > 51:
            suit = properties.get('suit')
            rank = str(properties.get('rank'))
            if suit in self.SUITS and rank in self.RANKS:
                self.num = self.SUITS.index(suit) * 13 + self.RANKS.index(rank)
        else:
            self.num = num

        self.suit = self.num // 13
        if self.num % 13 == 0: 
            self.rank = 14
        else:
            self.rank = self.num % 13 +1

    # Comparison of cards. Only compare the ranks. 
    def __eq__(self, anotherCard):
        return self.rank == anotherCard.rank and self.suit == anotherCard.suit
    
    def __ne__(self, anotherCard):
        return self.rank != anotherCard.rank
    
    def __lt__(self, anotherCard):
        return self.rank < anotherCard.rank
    
    def __le__(self, anotherCard):
        return self.rank <= anotherCard.rank
    
    def __gt__(self, anotherCard):
        return self.rank > anotherCard.rank
    
    def __ge__(self, anotherCard):
        return self.rank >= anotherCard.rank

    def __str__(self):
        return  '{} of {}'.format(self.RANKS[self.rank-1], self.SUITS[self.suit])
    
    def __repr__(self):
        return '{} {}'.format(self.SUITS[self.suit].rstrip('s'), self.RANKS[self.rank-1])


class Cards():
    # The parent class for objects with more than one card.
    
    def __init__(self,  cards=None, cardnums=[]):
        # Accept a list of integer or a list of Card objects to create a card collection
        if cards is None:
            self.cards = [Card(i) for i in cardnums]
        else:
            assert (isinstance(cards, list) or isinstance(cards, tuple)), 'Type Error: cards must be a list or tuple'
            assert isinstance(cards[0], Card), 'Type Error: cards must contain Card object only'
            if isinstance(cards, tuple):
                cards = list(cards)
            self.cards = cards

    @property
    def size(self):
        return len(self.cards)
    
    @property
    def ranks(self):
        return [card.rank for card in self.cards]
    
    @property
    def suits(self):
        return [card.suit for card in self.cards]

    def sort(self, key='suit', reverse=False):
        # Key: 'suit': sort the cards by suits in the order of squares, clubs, hearts and spades. 
        #      'square', 'club', 'heart' or 'spade' : sort the cards by the selected suits first, then other suits in default order.  
        #      'rank: sort the cards by ranks
        suits = ['square', 'club', 'heart', 'spade']
        if key == 'suit' or key.lower().rstrip('s') in suits:
            self.cards = sorted(self.cards, key=lambda card:(card.suit, card.rank), reverse=reverse)
            if key.lower().rstrip('s') in suits:
                self.cards = sorted(self.cards, key=lambda card: card.suit==suits.index(key.lower().rstrip('s')), reverse=True)
        if key == 'rank':
            self.cards = sorted(self.cards, key=lambda card: (card.rank, card.suit), reverse=reverse)    
        return 
    
    def count(self, key='rank', target=1):
        if key == 'rank':
            if isinstance(target, str):
                ranks_str  = ['J', 'Q', 'K', 'A']
                if target in ranks_str:
                    target = ranks_str.index(target)+11
            if isinstance(target, Card):
                target = target.rank
            target = int(target)
            assert 2 <= target <= 14, 'Value Error: target must be between 2 and 14 (A = 14).'
            return self.ranks.count(target)
        if key == 'suit':
            if isinstance(target, str):
                suits_str = ['square', 'club', 'heart', 'spade']
                if target.lower().rstrip('s') in suits_str:
                    target = suits_str.index(target.lower().rstrip('s'))
            target = int(target)
            assert 0 <= target <= 3, 'Value Error: target must be between 0 and 3.'
            return self.suits.count(target) 

    def remove(self, anotherCards):
        if isinstance(anotherCards, Card):
            if anotherCards in self.cards:
                self.cards.remove(card)
        for card in anotherCards:
            if card in self.cards:
                self.cards.remove(card)
        

    def __iter__(self):
        self.current_idx = 0
        return self
    
    def __next__(self):
        try:
            nxt = self.cards[self.current_idx]
        except IndexError:
            raise StopIteration
        self.current_idx += 1
        return nxt

    def __len__(self):
        return len(self.cards)

    def __eq__(self, anotherCards):
        self.sort()
        anotherCards.sort()
        return self.cards == anotherCards.cards

    def __str__(self):
        return str(self.cards)
    
    def __repr__(self):
        return str(self.cards)


class Deck(Cards):
    # Create 52 cards by default. 
    def __init__(self):
        cardnums = [i for i in range(52)]
        super().__init__(cardnums=cardnums)

    def shuffle(self):
        random.shuffle(self.cards)
        return

    def draw(self, n_cards):
        drawn = []
        for i in range(n_cards):
            try:
                drawn.append(self.cards.pop(0))
            except IndexError:
                continue
        return Hand(drawn)

    def distribute(self, n_players, n_cards):
        assert n_players * n_cards <= self.size, 'Value Error: number of cards drawn fewer than cards in deck'

        hands = []
        for player in range(n_players):
            hands.append(self.draw(n_cards))
        return hands 


class Hand(Cards):
    def __init__(self, cards=None, cardnums=[]):
        if cards is None:
            super().__init__(cardnums=cardnums)
        else:
            self.cards = cards

def testing():
    deck = Deck()
    deck.shuffle()

    hand = deck.draw(6)
    print(hand.ranks)


    deck2 = Deck()

    deck2.remove(hand)

    print(deck)
    print(deck2)

    print(deck==deck2)




# testing()










                 

