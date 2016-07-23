# encoding=utf-8
# Author: ninadpage

from collections import namedtuple


class Card(namedtuple('Card', ['value', 'suite'])):

    # Settings __slots__ to an empty tuple to keep memory requirements
    # low by preventing the creation of instance dictionaries
    __slots__ = ()

    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    SUITS = ['C', 'D', 'H', 'S']
    # ranks of all different values
    RANKS = {value: index for index, value in enumerate(VALUES, start=2)}
    # 'A' can both be the highest card and lowest card in a Straight hand (T-J-Q-K-A and A-2-3-4-5)
    # The second one is called as Wheel, so let's add a special rank for Ace in a Wheel
    RANKS['AW'] = 1
    # This will create a dict RANKS = {'AW': 1, '2': 2, '3': 3, '4': 4, .., 'K': 13, 'A': 14}

    @classmethod
    def from_string(cls, card_str):
        """
        Constructs a Card object from a string representation of a card. String should be a Value followed by a Suit.

        :param card_str: A card encoded in a string
        :type card_str: str
        :return: A Card
        :rtype: Card
        """
        if len(card_str) != 2 or card_str[0] not in cls.VALUES or card_str[1] not in cls.SUITS:
            raise ValueError('Invalid string value for card')
        return cls(card_str[0], card_str[1])

    def __str__(self):
        return '{}{}'.format(self.value, self.suite)

    # This makes sure our string implementation is used even when
    # a list of Card objects is printed/string formatted
    __repr__ = __str__


class PokerHandType(object):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    @classmethod
    def to_string(cls, hand_type):
        string_repr = {
            cls.HIGH_CARD: 'High Card',
            cls.ONE_PAIR: 'One Pair',
            cls.TWO_PAIR: 'Two Pair',
            cls.THREE_OF_A_KIND: 'Three of a Kind',
            cls.STRAIGHT: 'Straight',
            cls.FLUSH: 'Flush',
            cls.FULL_HOUSE: 'Full House',
            cls.FOUR_OF_A_KIND: 'Four of a Kind',
            cls.STRAIGHT_FLUSH: 'Straight Flush',
            cls.ROYAL_FLUSH: 'Royal Flush',
        }

        return string_repr[hand_type]


class PokerHand(object):

    def __init__(self, cards):
        """
        Constructs a Poker Hand object from a list of 5 Card objects.

        :param cards: 5 cards of the hand
        :type cards: [Card, ]
        """
        # Check if all elements in the list 'cards' are of correct type
        if not all(isinstance(card, Card) for card in cards):
            raise ValueError('Invalid type for cards')
        # A Poker Hand contains exactly 5 cards
        if len(cards) != 5:
            raise ValueError('Length of the hand must be 5')
        self.cards = cards
        self.hand_type, self.rank_counts = self._get_hand_details()

    @classmethod
    def from_string(cls, hand_str):
        """
        Constructs a Poker Hand object from a list 5 cards represented in a string, separated by a space.
        Each card is a represented by a Value letter and a Suit letter.
        Possible Values: 23456789TJQKA (Two, Three, .., Ten, Jack, Queen, King, Ace)
        Possible Suits: CDHS (Clubs, Diamonds, Hearts, Spades)
        Example hand_str: '4D 3D 3H TS AD'

        :param hand_str: A hand of 5 cards encoded in a string
        :type hand_str: str
        :return: A Poker Hand object
        :rtype: PokerHand
        """
        # Split hand_str and make a Card object from each element from the result
        cards = list(map(lambda card_str: Card.from_string(card_str), hand_str.split()))
        return cls(cards)

    @staticmethod
    def _get_sorted_rank_counts(rank_counts):
        """
        Sorts and unpacks ranks and counts given a rank_counts association. They are sorted in descending order
        by count, and if count is equal, then by rank. Returned ranks and counts sequences maintain the association
        implicitly by maintaining the order.

        :param rank_counts: dict with {ranks: counts}
        :type rank_counts: dict
        :return: ranks and counts sorted and unpacked
        :rtype: ((int,), (int,))
        """
        # To achieve the specific sorting order, we'll use secondary key to sort the data first
        # (it works because sorting in Python 2.2+ is guaranteed to be stable)
        rank_counts_sorted = sorted(rank_counts.items(), key=lambda rank_count: rank_count[0], reverse=True)
        rank_counts_sorted = sorted(rank_counts_sorted, key=lambda rank_count: rank_count[1], reverse=True)
        # Unpack ranks & counts while maintaining the order
        return zip(*rank_counts_sorted)

    def _get_hand_details(self):
        """
        Returns the type of this poker hand and its ranks & counts (frequency of each value in hand associated with
        one of Card.RANKS).

        :return: A 2-tuple: hand type, ranks counts
        :rtype: (PokerHandType(Enum), dict)
        """
        # Let's first calculate the frequency of each value in card, and associate it with the rank of that value
        all_values = [c.value for c in self.cards]
        rank_counts = {Card.RANKS[value]: all_values.count(value) for value, suite in self.cards}
        # e.g. for 2D, 2C, 2H, KH, 3H, this will create a dictionary {2: 3, 13: 1, 3: 1}
        # where 2, 13, 3 is the rank of '2', 'K', '3' resp.,
        # and 3, 1, 1 is the frequency (in this hand) of '2', 'K', '3' resp.

        # For flushes, there's a special case: Five high Straight (A-2-3-4-5), also called as wheel
        wheel_rank_counts = {
            Card.RANKS['A']: 1,
            Card.RANKS['5']: 1,
            Card.RANKS['4']: 1,
            Card.RANKS['3']: 1,
            Card.RANKS['2']: 1,
        }
        # In that case, we need to manually replace the rank of Ace from 'A' to 'AW'
        if rank_counts == wheel_rank_counts:
            rank_counts[Card.RANKS['AW']] = 1
            del rank_counts[Card.RANKS['A']]

        # Now let's sort the rank, count pairs by counts (if count is equal, sort by rank)
        ranks, counts = self._get_sorted_rank_counts(rank_counts)
        # In above example, this would set ranks = (2, 13, 3) and counts = (3, 1, 1)

        if len(counts) < 5:
            # If there are multiple cards with same value, it eliminates the possibility of a Straight or a Flush,
            # so let's first look for that match. In such cases, length of rank_counts will be < 5 as there'd be
            # at least one rank with value >= 2.
            if counts[0] == 4:
                return PokerHandType.FOUR_OF_A_KIND, rank_counts
            if counts[0] == 3 and counts[1] == 2:
                return PokerHandType.FULL_HOUSE, rank_counts
            if counts[0] == 3 and counts[1] == 1:
                return PokerHandType.THREE_OF_A_KIND, rank_counts
            if counts[0] == 2 and counts[1] == 2:
                return PokerHandType.TWO_PAIR, rank_counts
            # Otherwise only possible combination left when length < 5 is (2, 1, 1, 1)
            return PokerHandType.ONE_PAIR, rank_counts
        else:
            # This leaves open Flushes, Straights and High Card
            all_suites = [c.suite for c in self.cards]
            # Check if all suites are equal
            is_flush = all(s == all_suites[0] for s in all_suites[1:])

            # In case of a straight, difference between highest & lowest count is 4 (including five-high straight
            # since we replaced the rank of A with that of AW)
            is_straight = ranks[0] - ranks[4] == 4

            if is_flush and is_straight:
                if ranks[0] == Card.RANKS['A'] and ranks[1] == Card.RANKS['K']:
                    return PokerHandType.ROYAL_FLUSH, rank_counts
                return PokerHandType.STRAIGHT_FLUSH, rank_counts
            if is_flush:
                return PokerHandType.FLUSH, rank_counts
            if is_straight:
                return PokerHandType.STRAIGHT, rank_counts
            # No match found until now means it's High Card
            return PokerHandType.HIGH_CARD, rank_counts

    def __cmp__(self, other):
        # Let's first check if hand types are different
        if self.hand_type != other.hand_type:
            return self.hand_type - other.hand_type

        # Otherwise we need to compare the ranks for two hands of same type
        # We do this by finding a mismatch in ranks after going through reverse-sorted list of ranks (which are
        # grouped by counts first)
        self_ranks, _ = self._get_sorted_rank_counts(self.rank_counts)
        other_ranks, _ = self._get_sorted_rank_counts(other.rank_counts)
        for self_rank, other_rank in zip(self_ranks, other_ranks):
            if self_rank != other_rank:
                return self_rank - other_rank

        # If no mismatch found in ranks of same type, the hands are pot-splittingly equal
        return 0

    def __str__(self):
        return "<hand {}, '{}'>".format(self.cards, PokerHandType.to_string(self.hand_type))
