# tests.py
import unittest
from main import getHandRank

STRAIGHT_FLUSH = 9
FOUR_OF_A_KIND = 8
FULL_HOUSE = 7
FLUSH = 6
STRAIGHT = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HI_CARD = 1


class TestHandRank(unittest.TestCase):

    def test_straight_flush(self):
        playerHand = ['9h', '8h']
        board = ['10h', 'Jh', 'Qh', '8s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (STRAIGHT_FLUSH, 50, 0, 0))

    def test_four_of_a_kind(self):
        playerHand = ['As', 'Ad']
        board = ['Ah', '8h', 'Ac', '10s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (FOUR_OF_A_KIND, 14, 0, 66))

    def test_full_house(self):
        playerHand = ['9h', '9s']
        board = ['9c', '8d', '8h', '10s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (FULL_HOUSE, 9, 8, 0))

    def test_flush(self):
        playerHand = ['9h', '7h']
        board = ['10h', 'Jh', 'Qh', '8s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (FLUSH, 49, 0, 0))

    def test_straight(self):
        playerHand = ['9h', '7h']
        board = ['10h', 'Jh', 'Qs', '8s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (STRAIGHT, 50, 0, 0))

    def test_three_of_a_kind(self):
        playerHand = ['9h', '9s']
        board = ['10h', '9d', 'Qh', '8s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (THREE_OF_A_KIND, 9, 0, 49))

    def test_two_pair(self):
        playerHand = ['9h', '9s']
        board = ['10h', '10d', 'Qh', '8s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (TWO_PAIR, 10, 9, 50))

    def test_one_pair(self):
        playerHand = ['9h', '9s']
        board = ['2h', 'Jd', 'Qh', '8s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (ONE_PAIR, 9, 0, 49))

    def test_high_card(self):
        playerHand = ['Ah', '9s']
        board = ['2h', 'Jd', '7h', '10s', '6d']
        result = getHandRank(playerHand, board)
        self.assertEqual(result, (HI_CARD, 51, 0, 0))


if __name__ == '__main__':
    unittest.main()
