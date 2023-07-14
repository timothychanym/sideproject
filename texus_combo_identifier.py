"""
The combo identifier can identify the highest combo in a combination of cards for the game of texus hold'em.
  
Potential update 1: identify all combos in a set of cards
Potential update 2: identify all potential combos given ignoring degeneracy.  

"""
from cards_properties import Card, Cards, Deck
import itertools

class ComboIdentifier:
    # Class variabless
    ALL_COMBOS = ['High Card', 'Pair', 'Two-pair', 'Three of a kind', 'Straight', 'Flush', 'Full house', 'Four of a kind', 'Straight flush']
    SUITS = ['square', 'club', 'heart', 'spade']

    def __init__(self):
        pass

    # def pick_five_all(self, cards):
    #     # Return a list of all combination of five cards from the Cards input.
    #     cards.sort(key='rank', reverse=True)
    #     five_cards_all = list(itertools.combinations(cards, 5))
    #     for index, five_cards in enumerate(five_cards_all):
    #         five_cards_all[index] = Cards(cards=list(five_cards))
    #     return five_cards_all
    
    def unique(self, lst):
        # extract the unique elements in a list and return in a list.
        return list(set(lst))

    # Checking functions. 
    def isStraight(self, cards):
    # Check whether the cards input contain 5 consecutive ranks, return the greatest conseutive ranks if True, else return False.
        if isinstance(cards, list):
            cards = Cards(cards=cards)
        unique_ranks = sorted(self.unique(cards.ranks))
        if len(unique_ranks) < 5:
            return False
        for i in range(4, len(unique_ranks)):
            if unique_ranks[i] - unique_ranks[i-4] == 4:
                return True
        # Check for A
        if unique_ranks[-1] == 14 and unique_ranks[3] == 5:
            return True
        return False

    def find_straight(self, cards):
        # Return the cards that can form a straight. 
        if isinstance(cards, list):
            cards = Cards(cards=cards)
        if self.isStraight(cards):
            consecutive = []
            cards.sort(key='rank')
            # Extract the ranks that are in consecutive order.
            unique_ranks = self.unique(cards.ranks)
            for i in range(len(unique_ranks)-4):
                if unique_ranks[i+4] - unique_ranks[i] == 4:
                    consecutive = consecutive + unique_ranks[i:i+5]
            if unique_ranks[-1] == 14 and unique_ranks[3] == 5:
                if consecutive == []:
                    consecutive = [2, 3, 4, 5, 14]
                else:
                    if 14 not in consecutive:
                        consecutive.append(14)
            consecutive=self.unique(consecutive)
            # Extract the cards that match the current ranks in consecutive
            straight = [[] for i in range(len(consecutive))]
            for card in cards:
                if card.rank in consecutive:
                    # For cards of the same rank in different suits.
                    if cards.count(key='rank', target=card.rank) > 1:
                        straight[consecutive.index(card.rank)].append(card)
                    else:
                        straight[consecutive.index(card.rank)] = card
            return straight
        return None
            
    def find_high_straight(self, cards, tiebreaker='default', reverse=True):
        # Return the highest straight. 
        if isinstance(cards, list):
            cards = Cards(cards=cards)
        straight = self.find_straight(cards)
        if straight is not None:
            for index, card in enumerate(straight):
                if isinstance(card, list):
                    straight[index] = card[-1]
                    if tiebreaker == 'reverse':
                        straight[index] = card[0]
            # Consider A2345 as well 
            if straight[-1].rank - straight[-2].rank > 1:
                if len(straight[1:6]) < 5:
                    high_straight = straight[-1:] + straight[:4] 
                else:
                    high_straight = straight[-6:-1]
            else:
                high_straight = straight[-5:]
            if reverse:
                high_straight.reverse()
            return high_straight 
        return None    

    def find_all_straight(self, cards):
        # Return all combinations of straight. The result groups all degenerated straight in a list. 
        straight = self.find_straight(cards)
        if straight is not None:
            straight = self.convert_to_list(straight)
            all_straight = []
            for index in range((len(straight)-4)):
                five_cards = straight[index: index+5]
                if self.isStraight([card[0] for card in five_cards]):

                    # avoid adding A2345 to other striaght
                    if five_cards[-1][0].rank - five_cards[-2][0].rank == 1:
                        all_straight.append([])

                        all_straight[-1] = list(itertools.product(*five_cards))
                        for straight_index, current_straight in enumerate(all_straight[-1]):
                            all_straight[-1][straight_index] = Cards(current_straight)
                            all_straight[-1][straight_index].cards.reverse()

            if straight[-1][0].rank == 14 and straight[3][0].rank==5:
                straight_Afive = straight[:4]
                straight_Afive.insert(0, straight[-1])
                straight_Afive = self.convert_to_list(straight_Afive)
                straight_Afive = list(itertools.product(*straight_Afive))
                for straight_index, current_straight in enumerate(straight_Afive):
                    straight_Afive[straight_index] = Cards(current_straight)
                    straight_Afive[straight_index].cards.reverse()
                all_straight.insert(0, straight_Afive)
            
            all_straight.reverse()
            return all_straight
        return None
    
    def convert_to_list(self, cards, type=Card):
        # Convert a single card to a list, for use in find_all_straight.
        for index, card in enumerate(cards):
            if isinstance(card, type):
                cards[index] = [card]
        return cards

    def isFlush(self, cards):
        for i in range(4):
            if cards.count(key='suit', target=i) >= 5:
                return True
        return False
    
    def find_flush(self, cards):
        # Return the 5 cards that form the highest flush, return spades, hearts, clubs and squares if tie by default.
        # tiebreaker options: default, reverse, spades, hearts, clubs, squares
        if self.isFlush(cards):
            flush = [[] for i in range(4)]
            for i in range(4):
                count = cards.count(key='suit', target=i)
                if count >= 5:
                    cards.sort(key=self.SUITS[i], reverse=True)
                    flush[i] = cards.cards[0:count]
            return flush
        
        return None

    def find_high_flush(self, cards, tiebreaker='default'):
        flush = self.find_flush(cards)
        if flush:
            high_flush = None
            for suit in flush:
                if suit != []:
                    if not high_flush:
                        high_flush = suit[:5]
                    else:
                        for i in range(5):
                            if suit[i] > high_flush[i]:
                                high_flush = suit[:5]
                                break
                            if suit[i] == high_flush[i]:
                                if i == 4:
                                    if tiebreaker == 'reverse':
                                        continue
                                    high_flush = suit[:5]
                                continue
                            else:
                                break
            return high_flush
        
        else:
            return None

    def find_all_flush(self, cards):
        # Return a list of 5 cards containing a flush arranged in the order of the greatest rank in the flush, result is grouped in 4 list of suits. 
        flush = self.find_flush(cards)
        if flush:
            for i in range(4):
                flush[i] = list(itertools.combinations(flush[i], 5))
                for index, current_suit_cards in enumerate(flush[i]):
                    flush[i][index] = Cards(cards=current_suit_cards)
            return flush   
        else:
            return None
    
    def isStraightFlush(self, cards):
        flush = self.find_flush(cards)
        if flush:
            for flushable in flush:
                if flushable and self.isStraight(flushable):
                    return True
        return False    
                    
    def find_high_straight_flush(self, cards, tiebreaker='default'):
        if self.isStraightFlush(cards):
            flush = self.find_flush(cards)
            straight_flush = None
            for flushable in flush:
                if flushable and self.isStraight(flushable):
                    current_straight_flush = self.find_high_straight(flushable)
                    if not straight_flush:
                        straight_flush = current_straight_flush
                    else:
                        if current_straight_flush[0].rank > straight_flush[0].rank:
                            straight_flush = current_straight_flush
                        if current_straight_flush[0] == current_straight_flush[0]:
                            if tiebreaker == 'default':
                                straight_flush = current_straight_flush
            return straight_flush
        return None

    def find_all_straight_flush(self, cards):
        if self.isFlush(cards) and self.isStraight(cards):
            straight_flush = []
            for straight in self.find_all_straight(cards):
                for individual in straight:
                    if self.isFlush(individual):
                        straight_flush.append(individual)
            if straight_flush != []:
                return straight_flush

        return None
    
    def extract_n(self, cards, number):
        # Return cards of n equal ranks in the given sets of cards. 
        cards.sort(key='rank', reverse=True)
        unique_ranks = sorted(self.unique(cards.ranks))
    
        extracted = {}
        for rank in unique_ranks:
            n_card = cards.count(key='rank', target=rank)
            if  n_card >= number:
                try:
                    extracted[n_card][rank] = []
                except KeyError:
                    extracted[n_card] = {}
                    extracted[n_card][rank] = []
                for card in cards:
                    if card.rank == rank:
                        extracted[n_card][rank].append(card)
        if extracted != {}:
            return extracted
        return None

    def isFourOfaKind(self, cards):
        return any(cards.count(key='rank', target=card.rank) == 4 for card in cards)
    
    def find_four_of_a_kind(self, cards):
        if self.isFourOfaKind(cards):
            extracted = self.extract_n(cards, 4)
            max_rank = max(extracted[4].keys())
            four_of_a_kind = extracted[4][max_rank]
            return four_of_a_kind
        return None
    
    def find_high_four_of_a_kind(self, cards):
        four_of_a_kind = self.find_four_of_a_kind(cards)
        if four_of_a_kind:
            return self.add_to_five(four_of_a_kind, cards)
        return None
    
    def add_to_five(self, combo_cards, cards):
        # if the combo is shorter than five cards, add the highest card to the combo until it has five cards.
        if isinstance(combo_cards, list):
            combo_cards = Cards(cards=combo_cards)
        cards.sort(key='rank', reverse=True)

        for card in cards:
            if card.rank not in combo_cards.ranks:
                combo_cards.cards.append(card)
                if len(combo_cards.cards) == 5:
                    return combo_cards       

    def isFullHouse(self,cards):
        extracted = self.extract_n(cards,2)
        if extracted:
            if len(extracted) >= 2:
                return True 
        return False
    
    def find_high_full_house(self, cards):
        if self.isFullHouse(cards):
            extracted = self.extract_n(cards, 2)
            max_ranks = [0, 0]
            for n_cards in extracted:
                max_ranks_in_n = sorted(extracted[n_cards].keys(), reverse=True)[:2]
                for rank in max_ranks_in_n:
                    if n_cards >= 3:
                        if rank > max_ranks[0]:
                            if max_ranks[0] > max_ranks[1]:
                                max_ranks[1] = max_ranks[0]
                                pair = cards_three[:2]
                            max_ranks[0] = rank
                            cards_three = extracted[n_cards][rank][:3]
                        elif rank > max_ranks[1]:
                            max_ranks[1] = rank
                            pair = extracted[n_cards][rank][:2]
                    else:
                        if rank > max_ranks[1]:
                            max_ranks[1] = rank
                            pair = extracted[n_cards][rank][:2]
            return cards_three + pair
        return None

    def isThreeOfaKind(self, cards):
        return any(cards.count(key='rank', target=card.rank) >= 3 for card in cards)

    def find_three_of_a_kind(self, cards):
        if self.isThreeOfaKind(cards):
            extracted = self.extract_n(cards, 3)
            max_rank = 0
            for n_cards in extracted:
                max_rank_in_n = max(extracted[n_cards].keys())
                if max_rank_in_n > max_rank:
                    max_rank = max_rank_in_n
                    three_of_a_kind = extracted[n_cards][max_rank][:3]
            cards.sort(key='rank', reverse=True)
            return three_of_a_kind
        return None

    def find_high_three_of_a_kind(self, cards):
        three_of_a_kind = self.find_three_of_a_kind(cards)

        if three_of_a_kind:
            return self.add_to_five(three_of_a_kind, cards)
        return None

    def isTwoPair(self, cards):
        extracted = self.extract_n(cards, 2)
        if extracted:
            if len(extracted) >= 2 or any(len(extracted[num]) >=2 for num in extracted.keys()):
                return True
        return False
    
    def find_two_pair(self, cards):    
        if self.isTwoPair(cards):
            extracted = self.extract_n(cards, 2)
            max_ranks = [0, 0]
            for n_cards in extracted:
                max_ranks_in_n = sorted(extracted[n_cards].keys(), reverse=True)[:2]
                for rank in max_ranks_in_n:
                    if rank > max_ranks[0]:
                        if max_ranks[0] > max_ranks[1]:
                            max_ranks[1] = max_ranks[0]
                            pair_2 = pair_1
                        max_ranks[0] = rank
                        pair_1 = extracted[n_cards][rank][:2]
                    elif rank > max_ranks[1]:
                        max_ranks[1] = rank
                        pair_2 = extracted[n_cards][rank][:2]
            two_pair = pair_1 + pair_2
            return two_pair
        return None
    
    def find_high_two_pair(self, cards):
        two_pair = self.find_two_pair(cards)
        if two_pair:
            return self.add_to_five(two_pair, cards)
        return None

    def isPair(self, cards):
        return any(cards.count(key='rank', target=card.rank) >= 2 for card in cards)

    def find_pair(self, cards):
        if self.isPair(cards):
            extracted = self.extract_n(cards, 2)
            max_rank = 0
            for n_cards in extracted:
                max_rank_in_n = max(extracted[n_cards].keys())
                if max_rank_in_n > max_rank:
                    max_rank = max_rank_in_n 
                    pair = extracted[n_cards][max_rank][:2]

            return pair
        return None

    def find_high_pair(self, cards):
        pair = self.find_pair(cards)
        if pair:
            return self.add_to_five(pair, cards)
        return None

    def find_high_combo(self, cards):
        if self.isStraightFlush(cards):
            return Combo(self.find_high_straight_flush(cards), 8)
        if self.isFourOfaKind(cards):
            return Combo(self.find_high_four_of_a_kind(cards), 7)
        if self.isFullHouse(cards):
            return Combo(self.find_high_full_house(cards), 6)
        if self.isFlush(cards):
            return Combo(self.find_high_flush(cards), 5)
        if self.isStraight(cards):
            return Combo(self.find_high_straight(cards), 4)
        if self.isThreeOfaKind(cards):
            return Combo(self.find_high_three_of_a_kind(cards), 3)
        if self.isTwoPair(cards):
            return Combo(self.find_high_two_pair(cards), 2)
        if self.isPair(cards):
            return Combo(self.find_high_pair(cards), 1)
        cards.sort(key='rank', reverse=True)
        return Combo(cards.cards[:5], 0)

    # TODO: return all combos that can be formed by the cards. 
    # def find_all_combos(self, cards):
    #     all_comb = self.pick_five_all(cards)
    #     combos = {}
    
    # TODO: Find the possible combos given a set of cards.
    def find_possible_combos(self, cards, n_cards, cards_remain=None):
        if not cards_remain:
            deck = Deck()
            cards_remain = deck.remove(cards) 
        if len(cards) <= n_cards:
            # Add cards to cards until it's the target's length
            missing = n_cards - len(cards)
            cards_remain.sort(key='rank', reverse=True)
            missing_cards = list(itertools.combinations(cards_remain, missing))
            for index, comb in enumerate(missing_cards):
                missing_cards[index] = Cards(comb)
            possible_combos = {}
            for comb in missing_cards:
                combined = Cards(cards.cards + comb.cards)
                combined_combo = self.find_high_combo(combined)
                try:
                    if combined_combo > possible_combos[combined_combo.order]:
                        possible_combos[combined_combo.order]=combined_combo
                except KeyError:
                    possible_combos[combined_combo.order]=combined_combo
            possible_combos = dict(sorted(possible_combos.items(), key=lambda combo: combo[1], reverse=True))
            return possible_combos
        return self.find_high_combo(cards)

class Combo:
    ALL_COMBOS = ['High Card', 'Pair', 'Two-pair', 'Three of a kind', 'Straight', 'Flush', 'Full house', 'Four of a kind', 'Straight flush']

    def __init__(self, cards, order):
        if not isinstance(cards, Cards):
            cards = Cards(cards=cards)
        self.cards = cards
        self.order = order
        self.name = self.ALL_COMBOS[self.order]

    def __eq__(self, anotherCombo):
        if self.order == anotherCombo.order:
            return self.cards == anotherCombo.cards
        return self.order == anotherCombo.order 
    
    def __ne__(self, anotherCombo):
        if self.order == anotherCombo.order:
            return self.cards != anotherCombo.cards
        return self.order != anotherCombo.order

    def __gt__(self, anotherCombo):
        if self.order == anotherCombo.order:
            for index, card in enumerate(self.cards):
                if card == anotherCombo.cards.cards[index]:
                    if index == 4: 
                        return False
                    continue
                return card > anotherCombo.cards.cards[index]
                    
        return self.order > anotherCombo.order
    
    def __ge__(self, anotherCombo):
        if self.order == anotherCombo.order:
            for index, card in enumerate(self.cards):
                if card == anotherCombo.cards.cards[index]:
                    if index == 4: 
                        return True
                    continue
                return card > anotherCombo.cards.cards[index]

        return self.order > anotherCombo.order

    def __lt__(self, anotherCombo):
        if self.order == anotherCombo.order:
            for index, card in enumerate(self.cards):
                if card == anotherCombo.cards.cards[index]:
                    if index == 4: 
                        return False
                    continue
                return card < anotherCombo.cards.cards[index]
        return self.order < anotherCombo.order

    def __le__(self, anotherCombo):
        if self.order == anotherCombo.order:
            for index, card in enumerate(self.cards):
                if card == anotherCombo.cards.cards[index]:
                    if index == 4: 
                        return True
                    continue
                return card < anotherCombo.cards.cards[index]
        return self.order < anotherCombo.order

    def __str__(self):
        return '{}: {}'.format(self.name, self.cards)
    def __repr__(self):
        return '{}: {}'.format(self.name, self.cards)

def testing():
    identify = ComboIdentifier()
    deck = Deck()
    deck.shuffle()

    hand = deck.draw(5)
    hand.sort(key='rank')
    print(hand)
    # print(identify.isFourOfaKind(cards))
    # print(identify.isFullHouse(cards))
    # print(identify.isThreeOfaKind(cards))
    # print(identify.isTwoPair(cards))
    # print(identify.isPair(cards))
    # print(identify.extract_n(cards, 3))
    # print(identify.find_three_of_a_kind(cards))
    # print(identify.find_high_three_of_a_kind(cards))
    # print(identify.find_high_full_house(cards))
    # print(identify.find_high_two_pair(cards))
    # print(identify.find_high_pair(cards))

    print(identify.find_possible_combos(cards=hand, n_cards=7, cards_remain=deck))
    # print(combo, identify.ALL_COMBOS[combo_order])



# testing()
