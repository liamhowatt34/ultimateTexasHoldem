import random
import time
import math
from typing import List, Tuple
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
def getChips() -> int:
    chips = 0

    while True:
        chips = int(input("Enter amound of chips you'd like: "))
        if math.isnan(chips):
            continue

        return chips


def placeBet() -> int:
    bet = 0

    while True:
        bet = int(input("Enter a bet amount: "))
        if math.isnan(bet):
            continue

        return bet


def placePreflopBet(ante) -> int:
    bet = 0

    while True:
        bet = int(input(f"Enter 4x you ante(${ante}) amount to bet: "))
        if math.isnan(bet):
            continue

        if (bet != ante * PREFLOP_MULTIPLIER):
            print(f"Error. Bet must be 4x the ante(${ante}).")
            continue

        return bet


def placeFlopBet(ante) -> int:
    bet = 0

    while True:
        bet = int(input(f"Enter 2x your ante(${ante}) amount to bet: "))
        if math.isnan(bet):
            continue

        if (bet != ante * FLOP_MULTIPLIER):
            print(f"Error. Bet must be 2x the ante(${ante}).")
            continue

        return bet


def placeRiverBet(ante) -> int:
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
def betOrCheck() -> str:
    validOptions = ["b", "c"]
    userInput = ""

    while True:
        userInput = input(
            f"Do you want to check or bet? Enter {CHECK_CLR}'c'{RESET_CLR} for {CHECK_CLR}check{RESET_CLR} or {BET_CLR}'b'{RESET_CLR} for {BET_CLR}bet{RESET_CLR}: ").lower()

        if userInput in validOptions:
            return userInput


def playAgain() -> str:
    validOptions = ["y", "n"]
    userInput = ""

    while True:
        userInput = input(
            "Do you want to play again? y for yes, n for no: ").lower()

        if userInput in validOptions:
            return userInput


# Casino and cards functions
def generateDeck() -> List[str]:
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['h', 's', 'd', 'c']
    cards = [rank + suit for suit in suits for rank in ranks]

    random.shuffle(cards)

    return cards


def dealCards(deck) -> Tuple[str, str]:
    playerCard1 = deck.pop()
    dealerCard1 = deck.pop()
    playerCard2 = deck.pop()
    dealerCard2 = deck.pop()

    return [playerCard1, playerCard2], [dealerCard1, dealerCard2]


def dealFlop(deck) -> List[str]:
    card1 = deck.pop()
    card2 = deck.pop()
    card3 = deck.pop()

    return [card1, card2, card3]


def dealTurnAndRiver(deck) -> List[str]:
    card1 = deck.pop()
    card2 = deck.pop()

    return [card1, card2]


# Evaluate hand functions
def straightFaceToInt(cards) -> List[int]:
    ranks = [card[:-1] for card in cards]

    ranks = ['11' if rank == 'J' else rank for rank in ranks]
    ranks = ['12' if rank == 'Q' else rank for rank in ranks]
    ranks = ['13' if rank == 'K' else rank for rank in ranks]

    if '2' in ranks and '3' in ranks and '4' in ranks and '5' in ranks:
        ranks = ['1' if rank == 'A' else rank for rank in ranks]
    else:
        ranks = ['14' if rank == 'A' else rank for rank in ranks]

    intRanks = [int(rank) for rank in ranks]

    return intRanks


def faceToInt(cards) -> List[int]:
    ranks = [card[:-1] for card in cards]

    ranks = ['11' if rank == 'J' else rank for rank in ranks]
    ranks = ['12' if rank == 'Q' else rank for rank in ranks]
    ranks = ['13' if rank == 'K' else rank for rank in ranks]
    ranks = ['14' if rank == 'A' else rank for rank in ranks]

    intRanks = [int(rank) for rank in ranks]

    return intRanks


def isStraightFlush(hand, board) -> int:
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
    int_cards = faceToInt(cards)
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


def isFourOfAKind(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = faceToInt(cards)
    counts = {}
    quadsRank = 0
    handSum = 0

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    for key in counts:
        if counts[key] == 4:
            quadsRank = key

    if quadsRank:
        remaining_ranks = [rank for rank in ranks if rank != quadsRank]
        remaining_ranks.sort()
        handSum = quadsRank * 4 + remaining_ranks[-1]

        return quadsRank, handSum

    return 0, 0


def isFullHouse(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = faceToInt(cards)
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


def isFlush(hand, board) -> int:
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
            intCards = faceToInt(suit)
            intCards.sort()
            intCards[-5:]

            return sum(intCards)

    return 0


def isStraight(hand, board) -> int:
    cards = hand + board
    intCards = straightFaceToInt(cards)
    intCards.sort()

    longestStraight = []
    currentStraight = [intCards[0]]

    for i in range(1, len(intCards)):
        if intCards[i] == intCards[i - 1]:
            continue

        if intCards[i] == intCards[i - 1] + 1 or (intCards[i] == 14 and len(currentStraight) >= 4):
            currentStraight.append(intCards[i])
        else:
            currentStraight = [intCards[i]]

        if len(currentStraight) > len(longestStraight):
            longestStraight = currentStraight.copy()

    if len(longestStraight) >= 5:

        return sum(longestStraight[-5:])

    return 0


def isThreeOfAKind(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = faceToInt(cards)
    counts = {}
    trips = []
    final_hand = []
    tripsRank = 0

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
        tripsRank = max(trips)
        final_hand.append(tripsRank * 3)

        return tripsRank, sum(final_hand)

    return 0, 0


def isTwoPair(hand, board) -> Tuple[int, int, int]:
    cards = hand + board
    ranks = faceToInt(cards)
    counts = {}
    pairRanks = []
    final_hand = []

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    for key in counts:
        if counts[key] == 2:
            pairRanks.append(key)

    remaining_ranks = [rank for rank in ranks if rank not in pairRanks]
    final_hand.append(max(remaining_ranks))

    if len(pairRanks) >= 2:
        final_hand.append(sum(pairRanks) * 2)
        pairRanks.sort()

        return pairRanks[-1], pairRanks[-2], sum(final_hand)

    return 0, 0, 0


def isOnePair(hand, board) -> Tuple[int, int]:
    cards = hand + board
    ranks = faceToInt(cards)
    counts = {}
    final_hand = []
    pairRank = 0

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 1
        else:
            counts[rank] += 1

    pairs = [key for key, value in counts.items() if value == 2]

    if pairs:
        pairRank = max(pairs)

        remaining_ranks = [rank for rank in ranks if rank != pairRank]
        remaining_ranks.sort()
        final_hand.extend(remaining_ranks[-3:])

        final_hand.append(pairRank * 2)

        return pairRank, sum(final_hand)

    return 0, 0


def bestHiCard(hand, board) -> int:
    cards = hand + board
    ranks = faceToInt(cards)
    ranks.sort()

    return sum(ranks[-5:])


def getHandRank(hand, board) -> Tuple[int, int, int, int]:
    straightFlush = isStraightFlush(hand, board)
    quadsRank, quadsHi = isFourOfAKind(hand, board)
    boatTrips, boatPair = isFullHouse(hand, board)
    flush = isFlush(hand, board)
    straight = isStraight(hand, board)
    tripsRank, tripsHi = isThreeOfAKind(hand, board)
    pair1, pair2, twoPairHi = isTwoPair(hand, board)
    pairRank, pairHi = isOnePair(hand, board)
    hiCard = bestHiCard(hand, board)

    if straightFlush:
        return STRAIGHT_FLUSH, straightFlush, 0, 0
    if quadsRank:
        return FOUR_OF_A_KIND, quadsRank, 0, quadsHi
    if boatTrips:
        return FULL_HOUSE, boatTrips, boatPair, 0
    if flush:
        return FLUSH, flush, 0, 0
    if straight:
        return STRAIGHT, straight, 0, 0
    if tripsRank:
        return THREE_OF_A_KIND, tripsRank, 0, tripsHi
    if pair1:
        return TWO_PAIR, pair1, pair2, twoPairHi
    if pairRank:
        return ONE_PAIR, pairRank, 0, pairHi

    return HI_CARD, hiCard, 0, 0


# Main game function
def main() -> None:

    print("Ultimate Texas Holdem\n")
    player_roll = getChips()
    player = Player(player_roll, 0, 0, 0)

    playing = True
    while playing:
        winner = ""
        winnings = 0
        betTotal = 0
        preflopBet = 0
        flopBet = 0
        riverBet = 0

        deck = generateDeck()

        anteBet = placeBet()
        betTotal += anteBet

        blindBet = anteBet
        betTotal += blindBet

        playerHand, dealerHand = dealCards(deck)

        print(f"\nPlayer Hand: {playerHand[0]} {playerHand[1]}")

        preflopChoice = betOrCheck()
        if preflopChoice == BET:
            preflopBet = placePreflopBet(anteBet)
            betTotal += preflopBet

        board = dealFlop(deck)
        print(f"\t\nFlop: {board[0]}  {board[1]}  {board[2]}\n")

        if preflopBet == 0:
            flopChoice = betOrCheck()
            if flopChoice == BET:
                flopBet = placeFlopBet(anteBet)
                betTotal += flopBet

        river = dealTurnAndRiver(deck)
        board.extend(river)
        print(f"\t\nBoard: {board[0]}  {board[1]}  {board[2]}  {board[3]}  {board[4]}\n")

        if preflopBet == 0 and flopBet == 0:
            riverChoice = betOrCheck()
            if riverChoice == BET:
                riverBet = placeRiverBet(anteBet)
                betTotal += riverBet

        playerHandRank, playerKeyRank1, playerKeyRank2, playerHiSum = getHandRank(
            playerHand, board)

        dealerHandRank, dealerKeyRank1, dealerKeyRank2, dealerHiSum = getHandRank(
            dealerHand, board)

        print(f"Player Hand: {playerHand[0]} {playerHand[1]}")
        print(f"Dealer Hand: {dealerHand[0]} {dealerHand[1]}")

        if playerHandRank > dealerHandRank:
            winner = "player"
        if dealerHandRank > playerHandRank:
            winner = "dealer"

        if playerHandRank == dealerHandRank:
            if playerKeyRank1 > dealerKeyRank1:
                winner = "player"
            elif dealerKeyRank1 > playerKeyRank1:
                winner = "dealer"
            elif playerHandRank == FULL_HOUSE or playerHandRank == TWO_PAIR:
                if playerKeyRank2 > dealerKeyRank2:
                    winner = "player"
                if dealerKeyRank2 > playerKeyRank2:
                    winner = "dealer"
            else:
                if playerHiSum > dealerHiSum:
                    winner = "player"
                if dealerHiSum > playerHiSum:
                    winner = "dealer"
                if dealerHiSum == playerHiSum:
                    winner = "push"

        if winner == "push":
            print("\nPush.")
            player.update_ties()

        if winner == "dealer":
            print("\nDealer Wins...")
            print(f"Player: -${betTotal}")
            player_roll -= betTotal
            player.roll = player_roll
            player.update_losses()

        if winner == "player":
            print("\nPlayer Wins!!!")
            if dealerHandRank >= ONE_PAIR:
                winnings += anteBet * 2

            if playerHandRank >= STRAIGHT:
                if playerHandRank == STRAIGHT_FLUSH:
                    winnings += blindBet + blindBet * 50

                if playerHandRank == FOUR_OF_A_KIND:
                    winnings += blindBet + blindBet * 10

                if playerHandRank == FULL_HOUSE:
                    winnings += blindBet + blindBet * 3

                if playerHandRank == FLUSH:
                    winnings += blindBet + blindBet * 1.5

                if playerHandRank == STRAIGHT:
                    winnings += blindBet * 2

            if preflopBet > 0:
                winnings += preflopBet

            if flopBet > 0:
                winnings += flopBet

            if riverBet > 0:
                winnings += riverBet

            print(f"Player +${winnings}")
            player_roll += winnings
            player.roll = player_roll
            player.update_wins()

        time.sleep(1)
        choice = playAgain()

        if choice == "y":
            time.sleep(1)
            print(f"\nPlayer Roll: ${player_roll}\n")
            print(f"Player Stats: W{player.wins} - L{player.losses} - T{player.ties}.\n")

            if player_roll <= 0:
                reloadAmount = getChips()
                player_roll += reloadAmount
                player.roll = player_roll
            continue
        else:
            time.sleep(1)
            print(f"\nPlayer Stats: W{player.wins} - L{player.losses} - T{player.ties}.\n")
            playing = False
            break


if __name__ == "__main__":
    main()
