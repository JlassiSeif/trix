import sys
import os
import socket
import threading
import time
from src.deck import deck, Suit, Rank

PICK_GAME = 0
MANCHE = 1
CALCEL_SCORE = 2
RESET_HANDS = 3


class Logic:
    def __init__(self, client_fds):
        self.state = RESET_HANDS
        self.jarya = 1
        self.client_fds = client_fds
        self.played_cards = []
        self.mekla_taa_kol_wehed = [[] for _ in range(4)]
        self.scores = [0, 0, 0, 0]
        self.chosen_fil_games = 0
        self.chosen_fil_pli = 0
        self.m_deck = deck()
        self.chosen_game = ""

    def step(self):
        if self.state == RESET_HANDS:
            self.reset_hand()
            self.state = PICK_GAME
        elif self.state == PICK_GAME:
            self.pick_game()
            self.state = MANCHE
        elif self.state == MANCHE:
            self.manche()
            self.state = CALCEL_SCORE
            self.chosen_fil_games = (self.chosen_fil_games + 1) % 4
        elif self.state == CALCEL_SCORE:
            self.declare_winner()
            self.jarya += 1
            self.state = RESET_HANDS
            for score in self.scores:
                if score > 1000:
                    return True
        return False

    def reset_hand(self):
        self.m_deck.Shuffle()
        mess = "new_hand,"
        for i in range(4):
            h = mess + self.m_deck.get_hand(i)
            self.client_fds[i].send(h.encode())
        time.sleep(0.5)

    def manche(self):
        self.chosen_fil_pli = self.chosen_fil_games
        for i in range(8):
            if self.pli():
                break

    def pick_game(self):
        message = ""
        message2 = ""
        for i in range(4):
            if i == self.chosen_fil_games:
                message = "ekhtar"
            else:
                message = "stanna"
            self.client_fds[i].send(message.encode())
        time.sleep(0.1)
        buffer = self.client_fds[self.chosen_fil_games].recv(1024).decode()
        if len(buffer) <= 0:
            sys.stderr.write(
                "Client "
                + str(self.client_fds[self.chosen_fil_games])
                + " disconnected\n"
            )
            sys.exit(1)
        self.chosen_game = buffer
        l = "game," + self.chosen_game
        for i in range(4):
            self.client_fds[i].send(l.encode())
        time.sleep(0.1)

    def pli(self):
        FIRST_CARD = True
        for i in range(self.chosen_fil_pli, self.chosen_fil_pli + 4):
            index = i % 4
            hala = 0
            for j in range(index, index + 4):
                client_index = j % 4
                if j == index:
                    mes = "your_turn"
                    self.client_fds[client_index].send(mes.encode())
                else:
                    rata = str(hala)
                    mes = "turn," + rata
                    self.client_fds[client_index].send(mes.encode())
                    hala += 1
            time.sleep(0.1)

            buffer = bytearray(1024)
            played = self.client_fds[index].recv(1024).decode()

            if FIRST_CARD:
                for i in range(4):
                    rata = "strong_suit," + played
                    self.client_fds[i].send(rata.encode())
                time.sleep(0.1)
                FIRST_CARD = False

            self.played_cards.append(played)
            j = 0
            for k in range(index + 1, index + 4):
                client_index = k % 4
                rata = "car_played," + str(j) + "," + played
                self.client_fds[client_index].send(rata.encode())
                j += 1
            time.sleep(0.1)

        self.chosen_fil_pli = (
            self.chosen_fil_pli + self.m_deck.decide_mekla(self.played_cards)
        ) % 4
        for el in self.played_cards:
            self.mekla_taa_kol_wehed[self.chosen_fil_pli].append(el)
        rata = "end_of_pli"
        for i in range(4):
            self.client_fds[i].send(rata.encode())
        self.played_cards.clear()
        if self.chosen_game == "ray":
            for el in self.played_cards:
                if el == "k_h":
                    return True

        time.sleep(0.1)
        return False

    def get_score(self, index: int) -> int:
        game_type = self.chosen_game
        cards_str = self.mekla_taa_kol_wehed[index]
        cards = self.m_deck.string_to_cards(cards_str)
        score = 0

        if game_type == "dineri":
            for card in cards:
                if card.c_suit == Suit.DIAMONDS:
                    score += 10

        elif game_type == "damet":
            for card in cards:
                if card.c_rank == Rank.QUEEN:
                    score += 20

        elif game_type == "ray":
            for card in cards:
                if card.c_rank == Rank.KING and card.c_suit == Suit.HEARTS:
                    score += 100

        elif game_type == "pli":
            num_cards = len(cards)
            if num_cards >= 4:
                num_plis = num_cards // 4
                score = num_plis * 10

        elif game_type == "farcha":
            if index == self.chosen_fil_pli:
                score = 100

        elif game_type == "general":
            # Calculate scores for all game types
            score += self.calculate_score(
                cards, "dineri", (index == self.chosen_fil_pli)
            )
            score += self.calculate_score(
                cards, "damet", (index == self.chosen_fil_pli)
            )
            score += self.calculate_score(cards, "ray", (index == self.chosen_fil_pli))
            score += self.calculate_score(cards, "pli", (index == self.chosen_fil_pli))
            score += self.calculate_score(
                cards, "farcha", (index == self.chosen_fil_pli)
            )

        return score

    def calculate_score(cards, game_type, cond):
        score = 0

        if game_type == "dineri":
            for card in cards:
                if card.c_suit == Suit.DIAMONDS:
                    score += 10

        elif game_type == "damet":
            for card in cards:
                if card.c_rank == Rank.QUEEN:
                    score += 20

        elif game_type == "ray":
            for card in cards:
                if card.c_rank == Rank.KING and card.c_suit == Suit.HEARTS:
                    score += 100

        elif game_type == "pli":
            num_cards = len(cards)
            if num_cards >= 4:
                num_plis = num_cards // 4
                score = num_plis * 10

        elif game_type == "Farcha":
            if cond:
                score = 100

        elif game_type == "trix":
            if cond:
                score = 100

        return score

    def declare_winner(self) -> None:
        names = ["lam3i", "bochra", "ldhaw", "klafez"]
        print("jarya nummer: ", self.jarya)
        for i in range(4):
            self.scores[i] += self.get_score(i)
            print(names[i], self.scores[i])
