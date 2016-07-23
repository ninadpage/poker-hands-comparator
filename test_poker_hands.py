# encoding=utf-8
# Author: ninadpage

import unittest

from poker_hands import PokerHand, PokerHandType


class TestPokerHand(unittest.TestCase):

    def test_string_representation(self):
        self.assertEqual('{}'.format(PokerHand.from_string('KD QH 8C 9H 5S')),
                         "<hand [KD, QH, 8C, 9H, 5S], 'High Card'>")
        self.assertEqual('{}'.format(PokerHand.from_string('KH 5D KD 7H 8D')),
                         "<hand [KH, 5D, KD, 7H, 8D], 'One Pair'>")
        self.assertEqual('{}'.format(PokerHand.from_string('2D 2S 6D 4H 4D')),
                         "<hand [2D, 2S, 6D, 4H, 4D], 'Two Pair'>")
        self.assertEqual('{}'.format(PokerHand.from_string('4D AC AD AH 8D')),
                         "<hand [4D, AC, AD, AH, 8D], 'Three of a Kind'>")
        self.assertEqual('{}'.format(PokerHand.from_string('4D 5D 6D 7H 8D')),
                         "<hand [4D, 5D, 6D, 7H, 8D], 'Straight'>")
        self.assertEqual('{}'.format(PokerHand.from_string('2D 3D 7D QD AD')),
                         "<hand [2D, 3D, 7D, QD, AD], 'Flush'>")
        self.assertEqual('{}'.format(PokerHand.from_string('5H 5C QD QC QS')),
                         "<hand [5H, 5C, QD, QC, QS], 'Full House'>")
        self.assertEqual('{}'.format(PokerHand.from_string('7S TC TH TS TD')),
                         "<hand [7S, TC, TH, TS, TD], 'Four of a Kind'>")
        self.assertEqual('{}'.format(PokerHand.from_string('5S 6S 7S 8S 9S')),
                         "<hand [5S, 6S, 7S, 8S, 9S], 'Straight Flush'>")
        self.assertEqual('{}'.format(PokerHand.from_string('TS JS QS KS AS')),
                         "<hand [TS, JS, QS, KS, AS], 'Royal Flush'>")

    def test_sorting_by_hand_type(self):
        h1 = PokerHand.from_string('KD QH 8C 9H 5S')
        h2 = PokerHand.from_string('KH 5D KD 7H 8D')
        h3 = PokerHand.from_string('2D 2S 6D 4H 4D')
        h4 = PokerHand.from_string('4D AC AD AH 8D')
        h5 = PokerHand.from_string('4D 5D 6D 7H 8D')
        h6 = PokerHand.from_string('2D 3D 7D QD AD')
        h7 = PokerHand.from_string('5H 5C QD QC QS')
        h8 = PokerHand.from_string('7S TC TH TS TD')
        h9 = PokerHand.from_string('5S 6S 7S 8S 9S')
        h10 = PokerHand.from_string('TS JS QS KS AS')
        hands = [h5, h2, h7, h8, h1, h4, h10, h6, h3, h9]
        sorted_hands = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10]
        self.assertEqual(sorted(hands), sorted_hands)

    def test_high_card(self):
        h1 = PokerHand.from_string('KH QH 2C 5D 8D')
        h2 = PokerHand.from_string('KD QH 8C 2H 5S')
        h3 = PokerHand.from_string('QD TS 8H 9D 7S')
        self.assertEqual(h1.hand_type, PokerHandType.HIGH_CARD)
        self.assertEqual(h2.hand_type, PokerHandType.HIGH_CARD)
        self.assertTrue(h3.hand_type == PokerHandType.HIGH_CARD)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 > h3)

    def test_one_pair(self):
        h1 = PokerHand.from_string('KH KD 2C 5D 8D')
        h2 = PokerHand.from_string('KS 8H KC 2H 5S')
        h3 = PokerHand.from_string('KH KD TC 5D 8D')
        self.assertEqual(h1.hand_type, PokerHandType.ONE_PAIR)
        self.assertEqual(h2.hand_type, PokerHandType.ONE_PAIR)
        self.assertEqual(h3.hand_type, PokerHandType.ONE_PAIR)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 < h3)

    def test_two_pair(self):
        h1 = PokerHand.from_string('KH KS JC JD 8D')
        h2 = PokerHand.from_string('KD KC 8C JH JS')
        h3 = PokerHand.from_string('8D 8S 5H 5S AS')
        # Special case: Pair with higher rank should always be checked first
        h4 = PokerHand.from_string('QD QS JH JS 8S')
        self.assertEqual(h1.hand_type, PokerHandType.TWO_PAIR)
        self.assertEqual(h2.hand_type, PokerHandType.TWO_PAIR)
        self.assertEqual(h3.hand_type, PokerHandType.TWO_PAIR)
        self.assertEqual(h4.hand_type, PokerHandType.TWO_PAIR)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 > h3)
        self.assertTrue(h1 > h4)

    def test_three_of_a_kind(self):
        h1 = PokerHand.from_string('JH QH JC JD 8D')
        h2 = PokerHand.from_string('JD QH 8C JH JS')
        h3 = PokerHand.from_string('AD KS TH TD TS')
        self.assertEqual(h1.hand_type, PokerHandType.THREE_OF_A_KIND)
        self.assertEqual(h2.hand_type, PokerHandType.THREE_OF_A_KIND)
        self.assertEqual(h3.hand_type, PokerHandType.THREE_OF_A_KIND)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 > h3)

    def test_straight(self):
        h1 = PokerHand.from_string('4H 5H 6C 7D 8D')
        h2 = PokerHand.from_string('4D 5S 6D 7H 8S')
        h3 = PokerHand.from_string('3D 4S 5H 6D 7S')
        # Special case: Five-high straight (wheel)
        h4 = PokerHand.from_string('AD 3S 5H 2D 4S')
        self.assertEqual(h1.hand_type, PokerHandType.STRAIGHT)
        self.assertEqual(h2.hand_type, PokerHandType.STRAIGHT)
        self.assertEqual(h3.hand_type, PokerHandType.STRAIGHT)
        self.assertEqual(h4.hand_type, PokerHandType.STRAIGHT)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 > h3)
        self.assertTrue(h1 > h4)

    def test_flush(self):
        h1 = PokerHand.from_string('KH AH TH 5H 8H')
        h2 = PokerHand.from_string('KS AS TS 8S 5S')
        h3 = PokerHand.from_string('KH AH 3H 5H 8H')
        self.assertEqual(h1.hand_type, PokerHandType.FLUSH)
        self.assertEqual(h2.hand_type, PokerHandType.FLUSH)
        self.assertEqual(h3.hand_type, PokerHandType.FLUSH)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 > h3)

    def test_full_house(self):
        h1 = PokerHand.from_string('KH KC KS QD QC')
        h2 = PokerHand.from_string('QD QS QH AD AS')
        self.assertEqual(h1.hand_type, PokerHandType.FULL_HOUSE)
        self.assertEqual(h2.hand_type, PokerHandType.FULL_HOUSE)
        self.assertTrue(h1 > h2)

    def test_four_of_a_kind(self):
        h1 = PokerHand.from_string('KH KC KS KD 2C')
        h2 = PokerHand.from_string('QD QS QH QC AS')
        self.assertEqual(h1.hand_type, PokerHandType.FOUR_OF_A_KIND)
        self.assertEqual(h2.hand_type, PokerHandType.FOUR_OF_A_KIND)
        self.assertTrue(h1 > h2)

    def test_straight_flush(self):
        h1 = PokerHand.from_string('8H 9H TH JH QH')
        h2 = PokerHand.from_string('QS JS TS 9S 8S')
        h3 = PokerHand.from_string('9D TD JD QD KD')
        self.assertEqual(h1.hand_type, PokerHandType.STRAIGHT_FLUSH)
        self.assertEqual(h2.hand_type, PokerHandType.STRAIGHT_FLUSH)
        self.assertEqual(h3.hand_type, PokerHandType.STRAIGHT_FLUSH)
        self.assertTrue(h1 == h2)
        self.assertTrue(h1 < h3)

    def test_royal_flush(self):
        h1 = PokerHand.from_string('TD JD QD KD AD')
        h2 = PokerHand.from_string('TH JH QH KH AH')
        self.assertEqual(h1.hand_type, PokerHandType.ROYAL_FLUSH)
        self.assertEqual(h1.hand_type, PokerHandType.ROYAL_FLUSH)
        self.assertNotEqual(h1.hand_type, PokerHandType.STRAIGHT_FLUSH)
        self.assertTrue(h1 == h2)


if __name__ == '__main__':
    unittest.main()
