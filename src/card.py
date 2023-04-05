from enum import Enum


class Suit(Enum):
    HEARTS = 0
    CLUBS = 1
    DIAMONDS = 2
    SPADES = 3


class Rank(Enum):
    SEVEN = 0
    EIGHT = 1
    NINE = 2
    JACK = 3
    QUEEN = 4
    KING = 5
    TEN = 6
    ACE = 7


class Card:
    def __init__(self, rank, suit):
        self.c_rank = rank
        self.c_suit = suit
        self.designation = self.get_name()

    def get_rank(self, r):
        if r == Rank.SEVEN:
            return "7"
        elif r == Rank.EIGHT:
            return "8"
        elif r == Rank.NINE:
            return "9"
        elif r == Rank.JACK:
            return "j"
        elif r == Rank.QUEEN:
            return "q"
        elif r == Rank.KING:
            return "k"
        elif r == Rank.TEN:
            return "10"
        elif r == Rank.ACE:
            return "a"

    def get_name(self):
        rankString = self.get_rank(self.c_rank)
        suitString = str(self.c_suit.name).lower()[0]
        designation = rankString + "_" + suitString
        return designation
