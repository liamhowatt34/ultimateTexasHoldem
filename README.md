Ultimate Texas Hold'em - Console Game

This project is a Python-based console game that simulates Ultimate Texas Hold'em, a popular casino card game. 
The player competes against the dealer, making bets and decisions throughout the game. 
The goal is to build the best possible poker hand using a combination of two hole cards and five community cards, following traditional Texas Hold'em rules.

Features:
    User Input for Bets and Decisions: Place ante, blind, and additional bets based on the hand at preflop, flop, and river stages.
    Poker Hand Evaluation: Automatically evaluates poker hands (e.g., Straight Flush, Full House, Two Pair, etc.).
    Dealer vs. Player Mechanics: Both the player and dealer receive hands, with the winner determined based on poker hand rankings.
    Chip Management: Players start with a specific number of chips and can place various types of bets, with wins and losses affecting the player's chip total.
    Replay Option: The player can choose to play multiple rounds with running statistics.

Requirements:
    Python 3.x +
    No external dependencies required (standard Python libraries only).

How to Play:
    Setup: Upon starting the game, you will be prompted to enter the number of chips you wish to start with.
    Place Bets:
        You'll first place an ante bet.
        You will then have opportunities to raise or check at different stages of the game (preflop, flop, and river).
    Hand Evaluation: After all community cards are dealt, the game evaluates the player's and dealer's hands, determining the winner.
    Winnings/Losses: Depending on the strength of your hand, you either win or lose the round, and your total chips are updated.
    Play Again: At the end of each round, you can choose to play again or quit the game.

Game Flow:
    Preflop: Both you and the dealer receive two hole cards. You can either place a preflop bet (4x your ante) or check.
    Flop: Three community cards (flop) are dealt. If you checked preflop, you can place a bet (2x your ante) or check again.
    Turn & River: Two additional community cards are dealt. If you checked on both previous rounds, you must decide to bet (equal to your ante) or check.
    Showdown: The player and dealer reveal their hands, and the game determines the winner based on standard poker rankings.

Poker Hand Rankings:
    Straight Flush: Highest possible hand (e.g., A, K, Q, J, 10 of the same suit)
    Four of a Kind: Four cards of the same rank (e.g., four 8s)
    Full House: Three of a kind and a pair (e.g., three 6s and two 4s)
    Flush: Five cards of the same suit (e.g., 2, 4, 6, 8, 10 of hearts)
    Straight: Five consecutive cards of mixed suits (e.g., 7, 8, 9, 10, J)
    Three of a Kind: Three cards of the same rank (e.g., three 5s)
    Two Pair: Two pairs of different ranks (e.g., two 9s and two Jacks)
    One Pair: A single pair (e.g., two Kings)
    High Card: If no one has any of the above, the hand with the highest card wins (e.g., Ace high).
	

HOW TO RUN:

Clone this repository:
	git clone https://github.com/your-username/ultimate-texas-holdem.git


Navigate to the project directory:
	cd ultimate-texas-holdem

Run the game:
	python main.py
	or python3 main.py
	or py main.py
	
	
Example Output:

	Ultimate Texas Holdem

	Enter amount of chips you'd like: 100
	Enter a bet amount: 10
	Player Hand: Kd 7h

	Do you want to check or bet? Enter 'c' for check or 'b' for bet: c

	Flop:  3d  5h  9s

	Do you want to check or bet? Enter 'c' for check or 'b' for bet: b
	Enter 2x your ante(10) amount to bet: 20

	Board:  3d  5h  9s  8d  10s

	Player Hand: Kd 7h
	Dealer Hand: Qs Jh

	Player Wins!!!
	Player +$60
	

Enjoy the game! 🎮
