from src.card import Card, Suit, Rank
import random


class deck:
    def __init__(self):
        self.m_cards = []
        self.card_map = {}
        for rank in Rank:
            for suit in Suit:
                car = Card(rank, suit)
                self.m_cards.append(car)
                self.card_map[car.designation] = car

    def Shuffle(self):
        random.shuffle(self.m_cards)

    def string_to_cards(self, e):
        p = []
        for el in e:
            p.append(self.card_map[el])
        return p

    def decide_mekla(self, klash):
        if not klash:
            return -1  # Or some other value indicating that no card can win the trick
        table = self.string_to_cards(klash)
        strong_suit = table[0].c_suit
        max_value = Rank.SEVEN.value  # Initialize to minimum rank
        max_index = 0
        for i in range(len(table)):
            if table[i].c_suit == strong_suit:
                if table[i].c_rank.value > max_value:
                    max_value = table[i].c_rank.value
                    max_index = i
        return max_index

    def get_hand(self, num_player):
        start_index = num_player * 8
        end_index = start_index + 8
        hand = self.m_cards[start_index:end_index]
        hand.sort(key=lambda c: (c.c_suit.value, -c.c_rank.value))
        hand_str = ";".join(c.designation for c in hand)
        return hand_str
