import random
import time
import math
from typing import Tuple
from player import Player

# Constants
STRAIGHT_FLUSH = 9
FOUR_OF_A_KIND = 8
FULL_HOUSE = 7
FLUSH = 6
STRAIGHT = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HI_CARD = 1
BET = "b"
PREFLOP_MULTIPLIER = 4
FLOP_MULTIPLIER = 2
CHECK_CLR = "\033[36m"
BET_CLR = "\033[33m"
RESET_CLR = "\033[0m"

# User input functions
def get_chips() -> int:
    chips = 0

    while True:
        chips = int(input("Enter amound of chips you'd like: "))
        if math.isnan(chips):
            continue

        return chips


def place_bet() -> int:
    bet = 0

    while True:
        bet = int(input("Enter a bet amount: "))
        if math.isnan(bet):
            continue

        return bet


def place_preflop_bet(ante) -> int:
    bet = 0

    while True:
        bet = int(input(f"Enter 4x you ante(${ante}) amount to bet: "))
        if math.isnan(bet):
            continue

        if (bet != ante * PREFLOP_MULTIPLIER):
            print(f"Error. Bet must be 4x the ante(${ante}).")
            continue

        return bet


def place_flop_bet(ante) -> int:
    bet = 0

    while True:
        bet = int(input(f"Enter 2x your ante(${ante}) amount to bet: "))
        if math.isnan(bet):
            continue

        if (bet != ante * FLOP_MULTIPLIER):
            print(f"Error. Bet must be 2x the ante(${ante}).")
            continue

        return bet


def place_river_bet(ante) -> int:
    bet = 0

    while True:
        bet = int(input(f"Enter your ante(${ante}) amount to bet: "))
        if math.isnan(bet):
            continue

        if (bet != ante):
            print(f"Error. Bet must be equivcalent to your ante(${ante}).")
            continue

        return bet


# Flop and river decisions
def bet_or_check() -> str:
    valid_options = ["b", "c"]
    user_input = ""

    while True:
        user_input = input(
            f"Do you want to check or bet? Enter {CHECK_CLR}'c'{RESET_CLR} for {CHECK_CLR}check{RESET_CLR} or {BET_CLR}'b'{RESET_CLR} for {BET_CLR}bet{RESET_CLR}: ").lower()

        if user_input in valid_options:
            return user_input


def play_again() -> str:
    valid_options = ["y", "n"]
    user_input = ""

    while True:
        user_input = input(
            "Do you want to play again? y for yes, n for no: ").lower()

        if user_input in valid_options:
            return user_input


# Casino and cards functions
def generate_deck() -> list[str]:
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['h', 's', 'd', 'c']
    cards = [rank + suit for suit in suits for rank in ranks]

    random.shuffle(cards)

    return cards


def deal_cards(deck) -> Tuple[str, str]:
    player_card1 = deck.pop()
    dealer_card1 = deck.pop()
    player_card2 = deck.pop()
    dealer_card2 = deck.pop()

    return [player_card1, player_card2], [dealer_card1, dealer_card2]


def deal_flop(deck) -> list[str]:
    card1 = deck.pop()
    card2 = deck.pop()
    card3 = deck.pop()

    return [card1, card2, card3]


def deal_turn_and_river(deck) -> list[str]:
    card1 = deck.pop()
    card2 = deck.pop()

    return [card1, card2]


# Evaluate hand functions
def straight_face_to_int(cards) -> list[int]:
    ranks = [card[:-1] for card in cards]

    ranks = ['11' if rank == 'J' else rank for rank in ranks]
    ranks = ['12' if rank == 'Q' else rank for rank in ranks]
    ranks = ['13' if rank == 'K' else rank for rank in ranks]

    if '2' in ranks and '3' in ranks and '4' in ranks and '5' in ranks:
        ranks = ['1' if rank == 'A' else rank for rank in ranks]
    else:
        ranks = ['14' if rank == 'A' else rank for rank in ranks]

    int_ranks = [int(rank) for rank in ranks]

    return int_ranks


def face_to_int(cards) -> list[int]:
    ranks = [card[:-1] for card in cards]

    ranks = ['11' if rank == 'J' else rank for rank in ranks]
    ranks = ['12' if rank == 'Q' else rank for rank in ranks]
    ranks = ['13' if rank == 'K' else rank for rank in ranks]
    ranks = ['14' if rank == 'A' else rank for rank in ranks]

    int_ranks = [int(rank) for rank in ranks]

    return int_ranks


def is_straight_flush(hand, board) -> int:
    cards = hand + board
    suits = {'h': [], 's': [], 'd': [], 'c': []}

    for card in cards:
        suit = card[-1]
        suits[suit].append(card)

    for suit, suit_cards in suits.items():
        if len(suit_cards) >= 5:
            straight_flush_value = find_straight_flush_value(suit_cards)
            if straight_flush_value:
                return straight_flush_value

    return 0


def find_straight_flush_value(cards) -> int:
    int_cards = face_to_int(cards)
    int_cards.sort()

    longest_straight_flush = []
    current_straight_flush = [int_cards[0]]

    for i in range(1, len(int_cards)):
        if int_cards[i] == int_cards[i - 1]:
            continue

        if int_cards[i] == int_cards[i - 1] + 1 or (int_cards[i] == 14 and len(current_straight_flush) >= 4):
            current_straight_flush.append(int_cards[i])
        else:
            current_straight_flush = [int_cards[i]]

        if len(current_straight_flush) > len(longest_straight_flush):
            longest_straight_flush = current_straight_flush.copy()

    if len(longest_straight_flush) >= 5:
        return sum(longest_straight_flush[-5:])

    return 0


def is_four_of_a_kind(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = face_to_int(cards)
    counts = {}
    quads_rank = 0
    handSum = 0

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    for key in counts:
        if counts[key] == 4:
            quads_rank = key

    if quads_rank:
        remaining_ranks = [rank for rank in ranks if rank != quads_rank]
        remaining_ranks.sort()
        handSum = quads_rank * 4 + remaining_ranks[-1]

        return quads_rank, handSum

    return 0, 0


def is_full_house(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = face_to_int(cards)
    counts = {}
    trips = []
    pairs = []

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    for key in counts:
        if counts[key] == 3:
            trips.append(key)
        elif counts[key] >= 2:
            pairs.append(key)

    trips.sort()
    pairs.sort()

    if trips and pairs:
        highest_trip = max(trips)
        highest_pair = max(pairs)

        return highest_trip, highest_pair

    return 0, 0


def is_flush(hand, board) -> int:
    cards = hand + board
    suits = [[], [], [], []]

    for card in cards:
        if card[-1] == 'h':
            suits[0].append(card)
        if card[-1] == "s":
            suits[1].append(card)
        if card[-1] == "d":
            suits[2].append(card)
        if card[-1] == "c":
            suits[3].append(card)

    for suit in suits:
        if len(suit) > 4:
            int_cards = face_to_int(suit)
            int_cards.sort()
            int_cards[-5:]

            return sum(int_cards)

    return 0


def is_straight(hand, board) -> int:
    cards = hand + board
    int_cards = straight_face_to_int(cards)
    int_cards.sort()

    longest_straight = []
    current_straight = [int_cards[0]]

    for i in range(1, len(int_cards)):
        if int_cards[i] == int_cards[i - 1]:
            continue

        if int_cards[i] == int_cards[i - 1] + 1 or (int_cards[i] == 14 and len(current_straight) >= 4):
            current_straight.append(int_cards[i])
        else:
            current_straight = [int_cards[i]]

        if len(current_straight) > len(longest_straight):
            longest_straight = current_straight.copy()

    if len(longest_straight) >= 5:

        return sum(longest_straight[-5:])

    return 0


def is_three_of_a_kind(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = face_to_int(cards)
    counts = {}
    trips = []
    final_hand = []

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    for key in counts:
        if counts[key] == 3:
            trips.append(key)

    remaining_ranks = [rank for rank in ranks if rank not in trips]
    remaining_ranks.sort()
    final_hand.extend(remaining_ranks[-2:])

    if len(trips) >= 1:
        trips_rank = max(trips)
        final_hand.append(trips_rank * 3)

        return trips_rank, sum(final_hand)

    return 0, 0


def is_two_pair(hand, board) -> Tuple[int, int, int]:
    cards = hand + board
    ranks = face_to_int(cards)
    counts = {}
    pair_ranks = []
    final_hand = []

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    for key in counts:
        if counts[key] == 2:
            pair_ranks.append(key)

    remaining_ranks = [rank for rank in ranks if rank not in pair_ranks]
    final_hand.append(max(remaining_ranks))

    if len(pair_ranks) >= 2:
        final_hand.append(sum(pair_ranks) * 2)
        pair_ranks.sort()

        return pair_ranks[-1], pair_ranks[-2], sum(final_hand)

    return 0, 0, 0


def is_one_pair(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = face_to_int(cards)
    counts = {}
    final_hand = []
    pair_rank = 0

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    pairs = [key for key, value in counts.items() if value == 2]

    if pairs:
        pair_rank = max(pairs)

        remaining_ranks = [rank for rank in ranks if rank != pair_rank]
        remaining_ranks.sort()
        final_hand.extend(remaining_ranks[-3:])

        final_hand.append(pair_rank * 2)

        return pair_rank, sum(final_hand)

    return 0, 0


def best_hi_card(hand, board) -> int:
    cards = hand + board
    ranks = face_to_int(cards)
    ranks.sort()

    return sum(ranks[-5:])


def get_hand_rank(hand, board) -> Tuple[int, int, int, int]:
    straight_flush = is_straight_flush(hand, board)
    quads_rank, quads_hi = is_four_of_a_kind(hand, board)
    boats_trip, boats_pair = is_full_house(hand, board)
    flush = is_flush(hand, board)
    straight = is_straight(hand, board)
    trips_rank, trips_hi = is_three_of_a_kind(hand, board)
    pair1, pair2, two_pair_hi = is_two_pair(hand, board)
    pair_rank, pair_hi = is_one_pair(hand, board)
    hi_card = best_hi_card(hand, board)

    if straight_flush:
        return STRAIGHT_FLUSH, straight_flush, 0, 0
    if quads_rank:
        return FOUR_OF_A_KIND, quads_rank, 0, quads_hi
    if boats_trip:
        return FULL_HOUSE, boats_trip, boats_pair, 0
    if flush:
        return FLUSH, flush, 0, 0
    if straight:
        return STRAIGHT, straight, 0, 0
    if trips_rank:
        return THREE_OF_A_KIND, trips_rank, 0, trips_hi
    if pair1:
        return TWO_PAIR, pair1, pair2, two_pair_hi
    if pair_rank:
        return ONE_PAIR, pair_rank, 0, pair_hi

    return HI_CARD, hi_card, 0, 0


# Main game function
def main() -> None:

    print("Ultimate Texas Holdem\n")
    player_roll = get_chips()
    player = Player(player_roll)

    playing = True
    while playing:
        winner = ""
        winnings = 0
        bet_total = 0
        preflop_bet = 0
        flop_bet = 0
        river_bet = 0

        deck = generate_deck()

        ante_bet = place_bet()
        bet_total += ante_bet

        blind_bet = ante_bet
        bet_total += blind_bet

        player_hand, dealer_hand = deal_cards(deck)

        print(f"\nPlayer Hand: {player_hand[0]} {player_hand[1]}")

        preflop_choice = bet_or_check()
        if preflop_choice == BET:
            preflop_bet = place_preflop_bet(ante_bet)
            bet_total += preflop_bet

        board = deal_flop(deck)
        print(f"\nFlop: {board[0]}  {board[1]}  {board[2]}\n")

        if preflop_bet == 0:
            flop_choice = bet_or_check()
            if flop_choice == BET:
                flop_bet = place_flop_bet(ante_bet)
                bet_total += flop_bet

        river = deal_turn_and_river(deck)
        board.extend(river)
        print(f"\nBoard: {board[0]}  {board[1]}  {board[2]}  {board[3]}  {board[4]}\n")

        if preflop_bet == 0 and flop_bet == 0:
            river_choice = bet_or_check()
            if river_choice == BET:
                river_bet = place_river_bet(ante_bet)
                bet_total += river_bet

        player_hand_rank, player_key_rank_1, player_key_rank_2, player_hi_sum = get_hand_rank(
            player_hand, board)

        dealer_hand_rank, dealer_key_rank_1, dealer_key_rank_2, dealer_hi_sum = get_hand_rank(
            dealer_hand, board)

        print(f"Player Hand: {player_hand[0]} {player_hand[1]}")
        print(f"Dealer Hand: {dealer_hand[0]} {dealer_hand[1]}")

        if player_hand_rank > dealer_hand_rank:
            winner = "player"
        if dealer_hand_rank > player_hand_rank:
            winner = "dealer"

        if player_hand_rank == dealer_hand_rank:
            if player_key_rank_1 > dealer_key_rank_1:
                winner = "player"
            elif dealer_key_rank_1 > player_key_rank_1:
                winner = "dealer"
            elif player_hand_rank == FULL_HOUSE or player_hand_rank == TWO_PAIR:
                if player_key_rank_2 > dealer_key_rank_2:
                    winner = "player"
                if dealer_key_rank_2 > player_key_rank_2:
                    winner = "dealer"
            else:
                if player_hi_sum > dealer_hi_sum:
                    winner = "player"
                if dealer_hi_sum > player_hi_sum:
                    winner = "dealer"
                if dealer_hi_sum == player_hi_sum:
                    winner = "push"

        if winner == "push":
            print("\nPush.")
            player.update_ties()

        if winner == "dealer":
            print("\nDealer Wins...")
            print(f"Player: -${bet_total}")
            player_roll -= bet_total
            player.roll = player_roll
            player.update_losses()

        if winner == "player":
            print("\nPlayer Wins!!!")
            if dealer_hand_rank >= ONE_PAIR:
                winnings += ante_bet * 2

            if player_hand_rank >= STRAIGHT:
                if player_hand_rank == STRAIGHT_FLUSH:
                    winnings += blind_bet + blind_bet * 50

                if player_hand_rank == FOUR_OF_A_KIND:
                    winnings += blind_bet + blind_bet * 10

                if player_hand_rank == FULL_HOUSE:
                    winnings += blind_bet + blind_bet * 3

                if player_hand_rank == FLUSH:
                    winnings += blind_bet + blind_bet * 1.5

                if player_hand_rank == STRAIGHT:
                    winnings += blind_bet * 2

            if preflop_bet > 0:
                winnings += preflop_bet

            if flop_bet > 0:
                winnings += flop_bet

            if river_bet > 0:
                winnings += river_bet

            print(f"Player +${winnings}")
            player_roll += winnings
            player.roll = player_roll
            player.update_wins()

        time.sleep(1)
        choice = play_again()

        if choice == "y":
            time.sleep(1)
            print(f"\nPlayer Roll: ${player_roll}\n")
            print(f"Player Stats: W{player.wins} - L{player.losses} - T{player.ties}.\n")

            if player_roll <= 0:
                reload_amount = get_chips()
                player_roll += reload_amount
                player.roll = player_roll
            continue
        else:
            time.sleep(1)
            print(f"\nPlayer Stats: W{player.wins} - L{player.losses} - T{player.ties}.\n")
            playing = False
            break


if __name__ == "__main__":
    main()
