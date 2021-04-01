import random
# POKER TEXAS HOLD'EM

class Card:

    def __init__(self, name, value, suit):
        self._value = value
        self._suit = suit
        self._name = name

    def __repr__(self):
        return str(self._name) + " of " + str(self._suit)

    @property
    def value(self):
        return self._value

    @property
    def suit(self):
        return self._suit

    @property
    def name(self):
        return self._name


class Deck:

    def __init__(self):
        suits = ['hearts', 'spades', 'clubs', 'diamonds']
        values = {
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": 11,
            "Queen": 12,
            "King": 13,
            "Ace": 14
        }
        self.cards = [Card(name, value, suit) for suit in suits for name, value in values.items()]

    def shuffle(self):
        return random.shuffle(self.cards)

    def count(self):
        return len(self.cards)

    def deal_card(self):
        return self.cards.pop(0)

    def __repr__(self):
        return str(self.cards)


class Player:

    def __init__(self, name):
        self._name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)


class HandScore:

    @classmethod
    def flush(cls, cards):
        suits = {}
        for card in cards:
            if card.suit not in suits:
                suits[card.suit] = [card]
            else:
                suits[card.suit].append(card)
        for suit, suited_cards in suits.items():
            if len(suited_cards) >= 5:
                return suited_cards

        return False

    @classmethod
    def straight(cls, cards):
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
        consecutive = 1
        max_card = sorted_cards[0]
        for i in range(len(sorted_cards)):
            if sorted_cards[i].value == 14:
                sorted_cards.append(Card("Ace", 1, sorted_cards[i].suit))
            if sorted_cards[i].value - sorted_cards[i + 1].value == 1:
                consecutive += 1
            else:
                consecutive = 1
                max_card = sorted_cards[i + 1]

            if consecutive == 5:
                return max_card

        return False

    @classmethod
    def straight_flush(cls, cards):
        flush_cards = cls.flush(cards)
        if flush_cards is not False:
            return cls.straight(flush_cards)

        return False

    @classmethod
    def royal_flush(cls, cards):
        straight_flush = cls.straight_flush(cards)
        if straight_flush is not False:
            return straight_flush.name == "Ace"
        return False

    @classmethod
    def four_of_a_kind(cls, cards):
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)

        for i in range(0, len(sorted_cards) - 3):
            if (sorted_cards[i].value == sorted_cards[i + 1].value ==
                    sorted_cards[i + 2].value == sorted_cards[i + 3].value):
                return sorted_cards[i]
            else:
                i += 3

        return False

    @classmethod
    def full_house(cls, cards):
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
        three_of_a_kind = cls.three_of_a_kind(sorted_cards)
        two_pairs = cls.two_pairs(sorted_cards)
        if three_of_a_kind and two_pairs:
                if three_of_a_kind not in two_pairs:
                    return three_of_a_kind, two_pairs[0]
                elif three_of_a_kind == two_pairs[0]:
                    return three_of_a_kind, two_pairs[1]
                else:
                    return three_of_a_kind, two_pairs[0]
        return False

    @classmethod
    def three_of_a_kind(cls, cards):
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
        for i in range(0, len(sorted_cards) - 2):
            if sorted_cards[i].value == sorted_cards[i + 1].value \
                    and sorted_cards[i + 1].value == sorted_cards[i + 2].value:
                return sorted_cards[i]
            else:
                i += 2
        return False

    @classmethod
    def two_pairs(cls, cards):
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
        pairs = []
        for i in range(0, len(sorted_cards) - 1):
            if sorted_cards[i].value == sorted_cards[i + 1].value:
                pairs.append(sorted_cards[i])
            if len(pairs) == 2:
                return pairs
        return False

    @classmethod
    def pair(cls, cards):
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
        for i in range(0, len(sorted_cards) - 1):
            if sorted_cards[i].value == sorted_cards[i + 1].value:
                return sorted_cards[i]
        return False

    @classmethod
    def high_card(cls, cards):
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
        return sorted_cards[0]

    @classmethod
    def best_hand(cls, cards):
        # Given a set of cards ( 5 to 7 ), return the score of the hand.
        if cls.royal_flush(cards):
            return 999, 'royal flush'
        elif cls.straight_flush(cards):
            return 99 + cls.straight_flush(cards).value, "straight flush"
        elif cls.four_of_a_kind(cards):
            return 85 + cls.four_of_a_kind(cards).value, "four of a kind"
        elif cls.full_house(cards):
            pairs = cls.full_house(cards)
            return 70 + pairs[0].value + pairs[1].value / 14, "full-house"
        elif cls.three_of_a_kind(cards):
            return 56 + cls.three_of_a_kind(cards).value, "three of a kind"
        elif cls.two_pairs(cards):
            pairs = cls.two_pairs(cards)
            return 28 + pairs[0].value + pairs[1].value, 'two-pair'
        elif cls.pair(cards):
            return 14 + cls.pair(cards).value, "pair"
        elif cls.high_card(cards):
            return cls.high_card.value, "high card"


class Game:

    def __init__(self, max_players, big_blind, ante, players):
        self._max_players = max_players
        self._big_blind = big_blind
        self._ante = ante
        self.players = players


cards = [
    Card('Ace', 14, 'diamonds'), Card('Ace', 14, 'hearts'),
    Card('Four', 4, 'hearts'), Card('Five', 5, 'hearts'), Card('Six', 6, 'hearts'),
    Card('Seven', 7, 'diamonds')
]

cards1 = [
    Card('King', 13, 'hearts'), Card('King', 13, 'clubs'),
    Card('Ace', 14, 'diamonds'), Card('Two', 2, 'clubs'), Card('Three', 3, 'spades'),
    Card('Seven', 7, 'spades'), Card('Seven', 7, 'hearts')
]

handScore = HandScore()
print(f"Straight (to) : {handScore.straight(cards)}")
print(f"Flush : {handScore.flush(cards)}")
print(f"Royal Flush : {handScore.royal_flush(cards)}")
print(f"Two pairs : {handScore.two_pairs(cards)}")
print(f"Pair : {handScore.pair(cards)}")
print(f"Four of a kind: {handScore.four_of_a_kind(cards)}")
print(f"Three of a kind: {handScore.three_of_a_kind(cards)}")
print(f"High card : {handScore.high_card(cards)}")
print(f"Full house: {handScore.full_house(cards)}")
print(f"Score of best hand and type of hand: {handScore.best_hand(cards)}")
print(f"Score of best hand and type of hand: {handScore.best_hand(cards1)}")
