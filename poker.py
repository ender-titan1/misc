from enum import Enum
from dataclasses import dataclass
from typing import List

CHAR_TO_RANK = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
RANK_TO_CHAR = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

class Suit(Enum):
    DIAMONDS = 1
    SPADES = 2
    HEARTS = 3
    CLUBS = 4

class Rank:
    def __init__(self, value):
        if type(value) == int:
            self.value = value
        elif type(value) == str:
            self.value = CHAR_TO_RANK[value]

    def __repr__(self):
        if self.value > 9:
            return RANK_TO_CHAR[self.value]
        else:
            return f"{self.value}"

@dataclass
class Card:
    suit: Suit
    rank: Rank

    def __repr__(self):
        return f"({self.rank} of {self.suit})"

@dataclass
class Value:
    vlaue: int
    ranks: List[Rank]
    name: str

class HandChecker:
    def straight(self, cards):
        ranks = [card.rank.value for card in cards]
        ranks.sort()

        total = sum(ranks)
        consecutive_check = len(ranks)/2 * (ranks[0] + ranks[-1])

        return (total == consecutive_check, ranks, [ranks[-1]])

    def check_straight(self, cards):
        (true, _, ranks) = self.straight(cards)
        return (true, ranks)

    def flush(self, cards):
        suit = None
        for card in cards:
            if suit == 0:
                suit = card.suit
            elif suit != card.suit:
                return (False, None)
            
        ranks = [card.rank.value for card in cards]
        ranks.sort(reverse=True)

        return (True, ranks)

    def check_straight_flush(self, cards, royal=False):

        (is_flush, ranks) = self.flush(cards)

        if not is_flush:
            return (False, None)

        # This is also very hacky, and only works for a full hand

        (straight, _, _) = self.straight(cards)
        
        if royal:
            return (straight and ranks[-1] == 10, ranks)
        else:
            return (straight, ranks)

    def same_rank(self, cards):
        ranks = [card.rank.value for card in cards]
        amounts = {i:ranks.count(i) for i in ranks}

        same_rank = {}

        for key, value in amounts.items():
            same_rank[Rank(key)] = value

        return same_rank

    def royal_flush(self, cards):
        return self.check_straight_flush(cards, True)

    def straight_flush(self, cards):
        return self.check_straight_flush(cards)
    
    def one_same_set(self, cards, amount):
        dictionary = self.same_rank(cards)
        is_true = amount in dictionary.values()
        ranks = []

        if is_true:
            inverse_dict = {v:k for k, v in dictionary}
            set_rank = inverse_dict.pop(amount)

            remaining_ranks = [rank.value for _, rank in inverse_dict]
            remaining_ranks.sort(reverse=True)
            ranks.append(set_rank)
            ranks.append(remaining_ranks)
    
        return (is_true, ranks)
    
    def four_of_a_kind(self, cards):
        return self.one_same_set(cards, 4)

    def three_of_a_kind(self, cards):
        return self.one_same_set(cards, 3)
    
    def one_pair(self, cards):
        return self.one_same_set(cards, 2)
    
    def two_pair(self, cards):
        dictionary = self.same_rank(cards)
        pairs = list(filter(lambda kv: kv[1] == 2, dictionary.items()))

        is_true = 2 in dictionary.values() and not 3 in dictionary.values() and len(pairs) == 2

        if not is_true:
            return (False, None)


        pair_ranks = [k.value for k,_ in pairs]
        pair_ranks.sort(reverse=True)

        ranks = [card.rank.value for card in cards]
        ranks.remove(pair_ranks[0])
        ranks.remove(pair_ranks[1])

        pair_ranks.append(ranks[0])

        return (is_true, pair_ranks)
        
    
    def full_house(self, cards):
        dictionary = self.same_rank(cards)

        is_true = 2 in dictionary.values() and 3 in dictionary.values()

        if not is_true:
            return (False, None)

        three = filter(lambda kv: kv[1] == 3, dictionary.items())
        two = filter(lambda kv: kv[1] == 2, dictionary.items())
        kicker = filter(lambda kv: kv[1] == 1, dictionary.items())

        ranks = [three, two, kicker]

        return (is_true, ranks)

    
    def check_hand(self, cards):
        (rf, ranks) = self.royal_flush(cards)
        if rf:
            return Value(10, ranks, "Royal Flush")
        
        (sf, ranks) = self.straight_flush(cards)
        if sf:
            return Value(9, ranks, "Straight Flush")
        
        (k4, ranks) = self.four_of_a_kind(cards)
        if k4:
            return Value(8, ranks, "Four of a Kind")
        
        (fh, ranks) = self.full_house(cards)
        if fh:
            return Value(7, ranks, "Full House")
        
        (f, ranks) = self.flush(cards)
        if f:
            return Value(6, ranks, "Flush")
        
        (s, ranks) = self.check_straight(cards)
        if s:
            return Value(5, ranks, "Straight")
        
        (k3, ranks) = self.three_of_a_kind(cards)
        if k3:
            return Value(4, ranks, "Three of a Kind")

        (p2, ranks) = self.two_pair(cards)
        if p2:
            return Value(3, ranks, "Two Pair")
        
        (p1, ranks) = self.one_pair(cards)
        if p1:
            return Value(2, ranks, "One Pair")
        
        return Value(1, [self.get_highest(cards)], "High Card")
        
    def get_highest(self, cards):
        return max([card.rank.value for card in cards])

c = HandChecker()

hand = [ Card(Suit.DIAMONDS, Rank("A")),
        Card(Suit.CLUBS, Rank("A")),
        Card(Suit.SPADES, Rank("J")),
        Card(Suit.HEARTS, Rank(8)),
        Card(Suit.CLUBS, Rank(9))
]

print(c.check_hand(hand))