from classes.table import Table
from classes.game import Game

Game().start()

# TODO: REFACTOR NEW_DEAL TO WORK WITH THE UPDATE FUNCTION FROM GAME, MAYBE EVEN MOVE THE RENDER NEW CARD \
#       FUNCTION CALL TO GAME.PY?? WILL HAVE TO CHECK HOW TO DO IT PROPERLY
# TODO: ADD NATURAL WIN AGAINST PLAYERS / DEALER

# Pretend everything under this comment does not exist


# Ask for number of players
players = int(input("Amount of players (2-5): "))
table = Table(players)

# -------------------------------------------------------------------------------

table.new_deal()
current_player = -1

# Show initial hands
print(f"\n\nInitial hand for dealer ({table.dealer.hand.get_score()} / {table.dealer.hand.get_soft_score()})")
table.show_dealer_hand()

print("\n")

for i in range(int(players)):
    print(f"Initial hand for {table.get_player_name(i)} " 
          f"({table.get_player_score(i)} / {table.get_player_soft_score(i)})")
    table.show_hand(i)
    print("\n")

# Start of game
if not table.dealer.hand.natural and not table.any_player_has_natural():
    # No one has a natural in their deal. Start game normally
    # Continue game while players and dealer are still up
    while not table.have_all_players_stood_or_busted():
        if current_player == -1:
            print(f"\n\n********************************** TURN {table.turn} **********************************")
        current_player += 1

        print(f"\n\nHand for {table.get_player_name(current_player)} "
              f"({table.get_player_score(current_player)}", end='')
        print(f" / {table.get_player_soft_score(current_player)}):\n")
        table.show_hand(current_player)

        # Ask if player wants to be hit or stay as long
        # as they didn't stay or are busted
        if not table.is_player_standing(current_player) and not table.is_player_busted(current_player):
            if option := input("\n1. Hit\n2. Stand\n") == '1':
                table.add_card(current_player)
            else:
                table.player_stand(current_player)
        elif table.is_player_standing(current_player):
            print(f"\n{table.get_player_name(current_player)} has stood! Skipping to next player...\n")
        else:
            print(f"\n{table.get_player_name(current_player)} is busted! Skipping to next player...\n")

        # Dealer's turn and return to first player
        if current_player == int(players)-1:
            current_player = -1
            table.turn += 1

            if not table.has_dealer_stood_or_busted():
                table.dealer.hand.add_card(table.get_new_card())
            print(f"\n\nHand for dealer ({table.dealer.hand.get_score()})\n")
            table.show_dealer_hand()
        print("\n_____________________________________________________________________________")
elif table.dealer.hand.natural:
    # Dealer has a natural, check against every single player if they also have one
    print("\n\nDealer has a natural! All players that do not have one must pay up their bet!\n")
    for i in range(int(players)):
        if table.check_player_natural(i):
            print(f"{table.get_player_name(i)} has a natural as well! Stand-off, player keeps their bet\n")
        else:
            print(f"{table.get_player_name(i)} does not have a natural. Player loses their bet\n")
else:
    # A player has a natural and the dealer does not, check who
    for i in range(int(players)):
        if table.check_player_natural(i):
            print(f"\n{table.get_player_name(i)} has a natural while the "
                  f"dealer does not! Player wins 1.5 times their bet")

print("\n")

# Show player and dealer scores
dealer_score = table.get_dealer_score()
print(f"Dealer's score: {dealer_score}\n")
for i in range(int(players)):
    print(f"{table.get_player_name(i)}")
    table.assign_value_to_aces(i)
    print(f"Score for {table.get_player_name(i)}: {table.get_player_score(i)}\n")

print("_____________________________________________________________________________\n")

# Must check which players win. All players that are not busted and closer to 21
# than rest win their bet plus that of those who didn't. If the dealer is busted
# and the players are not, the dealer loses. If both the dealer and player bust,
# the player loses. In case of any ties, then the bet of those who tied is
# returned plus that of those who lost.
scores = table.order_hands()
if not table.is_dealer_busted():  # Dealer is not busted, they also play
    if scores[0][1] < dealer_score:  # All hand values are lower than the dealer's hand
        print("Dealer wins, collecting bets of all players...")
        for i in range(int(players)):
            print(f"Collecting bet from {table.get_player_name(i)}")
    elif scores[0][1] == dealer_score:  # Players tied with dealer
        print("At least one player tied with the dealer, checking...")
        last_tied = table.check_tie(scores)

        for i in range(int(players)):
            if i <= last_tied:
                print(f"Returning bet to {table.get_player_name(scores[i][0])}")
            else:
                print(f"Collecting bet from {table.get_player_name(i)}")
    else:  # Player in first position won
        print(f"{table.get_player_name(scores[i][0])} won! Returning bet...")
        for i in range(int(players)):
            if i+1 != scores[0][0]:
                print(f"Collecting bet from {table.get_player_name(i)}")
else:  # Dealer is busted and will not play
    if scores[0][1] > scores[0][1]:  # Player in first position won
        print(f"{table.get_player_name(scores[0][0])} won! Returning bet...")
        for i in range(int(players)):
            if i+1 != scores[0][0]:
                print(f"Collecting bet from {table.get_player_name(i)}")
    else:  # Players tied, check how many
        print("Players tied, checking...")
        last_tied = table.check_tie(scores)

        for i in range(int(players)):
            if i <= last_tied:
                print(f"Returning bet to {table.get_player_name(scores[i][0])}")
            else:
                print(f"Collecting bet from {table.get_player_name(i)}")
