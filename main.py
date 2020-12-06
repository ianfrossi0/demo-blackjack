from classes.table import Table

# TODO: ADD NATURAL WIN AGAINST PLAYERS / DEALER

# Ask for number of players
players = input("Amount of players (2-5): ")
table = Table(players)
current_player = 0
turn = 1

# Show initial hands
print(f"\n\nInitial hand for dealer ({table.dealer.hand.getScore()} / {table.dealer.hand.getSoftScore()})")
table.showDealerHand()

print("\n")

for i in range(int(players)):
    print(f"Initial hand for player {i+1} ({table.getPlayerScore(i+1)} / {table.getPlayerSoftScore(i+1)})")
    table.showHand(i+1)
    print("\n")

# Start of game
if not table.dealer.hand.natural and not table.anyPlayerHasNatural():
    # No one has a natural in their deal. Start game normally
    # Continue game while players and dealer are still up
    while not table.haveAllPlayersStoodOrBusted() or not table.hasDealerStoodOrBusted():
        if current_player == 0:
            print(f"\n\n********************************** TURN {turn} **********************************")
        current_player += 1

        print(f"\n\nHand for player {current_player} ({table.getPlayerScore(current_player)}", end='')
        print(f" / {table.getPlayerSoftScore(current_player)}):\n")
        table.showHand(current_player)

        # Ask if player wants to be hit or stay as long
        # as they didn't stay or are busted
        if not table.isPlayerStanding(current_player) and not table.isPlayerBusted(current_player):
            if option := input("\n1. Hit\n2. Stand\n") == '1':
                table.addCard(current_player)
            else:
                table.playerStand(current_player)
        elif table.isPlayerStanding(current_player):
            print(f"\nPlayer {current_player} has stood! Skipping to next player...\n")
        else:
            print(f"\nPlayer {current_player} is busted! Skipping to next player...\n")

        # Dealer's turn and return to first player
        if current_player == int(players):
            current_player = 0
            turn += 1

            if not table.hasDealerStoodOrBusted():
                table.dealer.hand.addCard(table.getNewCard())
            print(f"\n\nHand for dealer ({table.dealer.hand.getScore()})\n")
            table.showDealerHand()
        print("\n_____________________________________________________________________________")
elif table.dealer.hand.natural:
    # Dealer has a natural, check against every single player if they also have one
    print("\n\nDealer has a natural! All players that do not have one must pay up their bet!\n")
    for i in range(int(players)):
        if table.checkPlayerNatural(i+1):
            print(f"Player {i+1} has a natural as well! Stand-off, player keeps their bet\n")
        else:
            print(f"Player {i+1} does not have a natural. Player loses their bet\n")
else:
    # A player has a natural and the dealer does not, check who
    for i in range(int(players)):
        if table.checkPlayerNatural(i+1):
            print(f"\nPlayer {i+1} has a natural while the dealer does not! Player wins 1.5 times their bet")

print("\n\n")

# Show player and dealer scores
print(f"Dealer's score: {table.getDealerScore()}")
for i in range(int(players)):
    print(f"Player {i+1}")
    table.assignValueToAces(i+1)
    print(f"Score for player {i+1}: {table.getPlayerScore(i+1)}\n\n")

# Must check which players win. AFAIK, all players that are not busted and closer to 21
# than the dealer win their bet plus that of those who didn't.
# TODO: Haven't found anything regarding this, but if the dealer is busted I'll allow busted players to participate
