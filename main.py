from classes.table import Table

# TODO: ADD DEALER! Check wiki for dealer rules...
# TODO: ADD COMPARISON OF NATURAL VS DEALER
# TODO: ADD NATURAL WIN AGAINST PLAYERS / DEALER

# Ask for number of players
players = input("Amount of players (2-5): ")
table = Table(players)
current_player = 0
turn = 1
print(f"\n\n********************************** TURN {turn} **********************************")

# Continue game while players are still up
while not table.haveAllPlayersStoodOrBusted():
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
        print(f"\n\n********************************** TURN {turn} **********************************")
    print("\n_____________________________________________________________________________")

print("\n\n")

# Show player scores
for i in range(int(players)):
    print(f"Player {i+1}")
    table.assignValueToAces(i+1)
    print(f"Score for player {i+1}: {table.getPlayerScore(i+1)}\n\n")
