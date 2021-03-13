from .table import Table  # REMEMBER TO DELETE THIS AFTER TESTING IS DONE... OR NOT!
from .renderer import Renderer
from .constants import *


class Game:
    def __init__(self):
        self.players = int(input("\tPlayers: "))
        print("\n[AUTO] Initializing table... ")
        self.table = Table(self.players)
        print(f"[AUTO] OK, table instantiated with {self.players} players!\n", end='')
        self.renderer = None  # Create variable with None value, initialize later

    # Game main loop
    def start(self):
        print(HORIZONTAL_LINE)
        print("\n[AUTO] Initializing pygame... ", end='')
        pygame.init()
        clock = pygame.time.Clock()
        print("OK!\n")

        print("\n[AUTO] Initializing variables... ", end='')
        player = 0
        player_aux = 0  # Auxiliary variable to check current player
        new_deal = True  # New initial deal
        turn_end = False  # Marks end of player turn
        turn_initiated = False  # Boolean for actions to be taken at turn start
        player_choice_selected = False  # Player has selected what to play on their turn
        game_over = False  # This hand has ended
        time_last_action = 0  # Cooldown between actions
        current_ace = 1
        turn_number = 0
        player_choice = 0
        print("OK!\n")

        print("\n[AUTO] Initializing renderer... ")
        self.renderer = Renderer()
        print("[AUTO] Renderer initialized OK!\n")

        print("\n[AUTO] Drawing table... ", end='')
        self.renderer.render(TABLE, ((SCREEN_WIDTH - 1392) / 2, 0))
        self.renderer.render(self.renderer.UPSIDE_DOWN_CARD, (CARD_SCREEN_CENTER_X - 170, 20))
        print("OK!\n")

        print("\n[AUTO] Drawing buttons... ", end='')
        self.renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")  # Hit button
        self.renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")  # Stand button
        self.renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")  # Double button
        print("OK!\n")

        print(HORIZONTAL_LINE)
        print(f"\n\n[AUTO] Game starting.\n\tRunning with a resolution of {SCREEN_WIDTH}x{SCREEN_HEIGHT} "
              f"(current scale is {SCALE[0]:.2f} horizontal and {SCALE[1]:.2f} vertical) at target {FPS} fps."
              f"\n\t{ACTION_COOLDOWN}ms of cooldown between actions\n")
        print(HORIZONTAL_LINE)

        while True:
            time_now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\n[AUTO] Quitting...")
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    # Allow movement only when it's their turn
                    if event.key in MOVEMENT_KEYS and turn_initiated:
                        # Redraw buttons to clean outline from other boxes besides current selection
                        if not self.table.have_all_players_stood_or_busted():
                            self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")
                            self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")
                            self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")
                        else:
                            self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 90, 150, 60, "Yes")
                            self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 180, 150, 60, "No")
                            self.renderer.render_button(DARK_RED, 40,
                                                        SCREEN_HEIGHT - 270, 150, 60, "Will ace be soft", "M")

                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            print("\t[USER] Up arrow key or W pressed")
                            if not self.table.have_all_players_stood_or_busted():
                                player_choice = 2 if player_choice == 2 else player_choice + 1
                            else:
                                player_choice = 1 if player_choice == 1 else player_choice + 1
                            self.renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            print("\t[USER] Down arrow key or S pressed")
                            player_choice = 0 if player_choice == 0 else player_choice - 1
                            self.renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))
                        if event.key == pygame.K_SPACE:
                            print("\t[USER] Space bar pressed")
                            player_choice_selected = True

            if not game_over:
                # Game main logic, do while all players are playing
                if not self.table.have_all_players_stood_or_busted():
                    # Check if enough time has passed between last action and now
                    if time_now - time_last_action >= ACTION_COOLDOWN:
                        if new_deal:  # Dealing initial two cards
                            if self.table.get_card_count(0) == 0 and self.table.can_player_play(0):
                                print("[AUTO] Start dealing initial hand...")

                            if player != -1:  # Dealer does not bet
                                if not self.table.initialize_player_bet(player):  # Player does not have enough score
                                    print(f"{self.table.get_player_name(player)} does not have "
                                          f"enough score to play, they will be skipped!")

                            if self.table.up_for_initial_deal(player):  # Dealer or player must receive card
                                card = self.table.deal(player)  # Get a new card
                                self.renderer.render_new_card(card, player, self.table.get_card_count(player))
                                time_last_action = pygame.time.get_ticks()

                            turn_end = True  # After card has be dealt, turn has ended
                            new_deal = not self.table.finished_dealing()  # Check if initial deal is over
                            self.table.is_player_busted(player)

                            if not new_deal:
                                turn_number = 1
                                print("[AUTO] Finished dealing initial hand")
                        else:  # Ready for player turn
                            if ((not self.table.is_player_busted(player) and not self.table.is_player_standing(player))
                                or self.table.have_all_players_stood_or_busted()) \
                                    and self.table.can_player_play(player):
                                if not turn_initiated:  # Has player turn already started?
                                    print(f"\n[AUTO] Started turn for "
                                          f"{'Dealer' if player == -1 else self.table.get_player_name(player)} "
                                          f"on turn {turn_number}")
                                    player_choice = 0

                                    if player != -1:
                                        # Rerender player action buttons with BLACK color
                                        # and outline the first option
                                        self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")
                                        self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")
                                        self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")
                                        self.renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))
                                        player_choice_selected = False
                                    else:
                                        # Dealer does not get to choose whether they can draw a card or not
                                        # If their soft score equals 17 or more, then they will stand before
                                        # starting the turn. If their score is lower, they will draw a card
                                        player_choice = 0
                                        player_choice_selected = True
                                        print(not self.table.dealer.hand.stand and not self.table.dealer.hand.busted)
                                        print(self.table.get_player_score(-1))
                                    turn_initiated = True

                                if player_choice_selected:  # Player pressed the spacebar on a button
                                    if player_choice == 0:
                                        print(f"\t[USER] "
                                              f"{'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                              f" hit")
                                        self.deal(player)
                                    elif player_choice == 1:
                                        print(f"\t[USER] "
                                              f"{'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                              f" stood")
                                        self.table.player_stand(player)
                                    else:
                                        print(f"\t[USER] "
                                              f"{'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                              f" will double")
                                        self.deal(player)  # Get a new card

                                        # Players must put up a bet equal to their initial one
                                        self.table.bets[player] = self.table.bets[player] * 2

                                        if not self.table.is_player_busted(player):
                                            # If player is not busted, then stand
                                            self.table.player_stand(player)
                                    turn_end = True
                                    time_last_action = pygame.time.get_ticks()
                            else:  # Current player is standing, busted or does not have enough score to play
                                if self.table.is_player_standing(player):
                                    print(f"\n[AUTO] {'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                          f" is standing! Skipping to next player...")
                                elif self.table.is_player_busted(player):
                                    print(f"\n[AUTO] {'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                          f" is busted! Skipping to next player...")
                                else:
                                    print(f"\n[AUTO] {self.table.get_player_name(player)} "
                                          f"does not have enough score to play! Skipping to next player...")
                                turn_end = True

                        if turn_end:
                            if turn_end and player_choice_selected:
                                print(f"[AUTO] Turn finished for "
                                      f"{'Dealer' if player == -1 else self.table.get_player_name(player)} "
                                      f"on turn {turn_number}")

                            if player == self.players - 1:
                                turn_number += 1
                                player = -1
                            else:
                                player += 1

                            print("\n[AUTO] Drawing player names... ", end='')
                            for i in range(self.players):
                                name = self.table.get_player_name(i)
                                color = WHITE

                                if self.table.is_player_busted(i):
                                    name += " [BUSTED]"
                                    color = DARK_GRAY

                                if self.table.is_player_standing(i):
                                    name += " [STAND]"
                                    color = DARK_GRAY

                                if i == player:
                                    color = DARK_LIME

                                self.renderer.render(
                                    self.renderer.get_text_surface(f"Player {i + 1}: " + name, color, "S"),
                                    (SCREEN_WIDTH - 200, SCREEN_HEIGHT - (40 * (self.players - i))))
                            print("OK!")

                            turn_end = False
                            turn_initiated = False
                            player_choice_selected = False
                else:  # No players nor dealer are playing, start checking for winner
                    aces = self.table.get_amount_of_aces(player_aux)

                    if (player_choice_selected and aces > 0) or aces == 0:
                        if aces > 0:  # Player chose whether to use their ace as 1 or 11
                            self.table.assign_value_to_aces(player, player_choice, current_ace)

                        turn_initiated = False
                        time_last_action = pygame.time.get_ticks()

                        # Check whether player won or lost
                        if current_ace == aces or aces == 0:
                            self.table.check_player_win(player_aux)
                    else:
                        # Player has an aced, he has to choose whether they want to play it as a 1 or 11
                        if not turn_initiated:
                            self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 90, 150, 60, "Yes")
                            self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 180, 150, 60, "No")
                            self.renderer.render_button(DARK_RED, 40,
                                                        SCREEN_HEIGHT - 270, 150, 60, "Will ace be soft?", "M")

                        turn_initiated = True

                    if player_aux == self.players - 1:
                        self.table.dealer.hand.cards[1].visible = True
                        self.renderer.render_new_card(self.table.dealer.hand.cards[1], -1, 1)
                        game_over = True

                    if (player_choice_selected and current_ace == aces) or aces == 0:
                        player_choice_selected = False
                        player_aux += 1
                        current_ace = 1
                    elif current_ace < aces:
                        current_ace += 1
            else:
                # DON'T FORGET TO CHANGE THIS!!!!
                if not turn_end:
                    print("This game has ended")
                    turn_end = True

            self.renderer.update(clock)  # Update

    # Small function to draw a new card or print if there are no more cards in the deck
    def deal(self, player):
        card = self.table.deal(player)  # Get a new card
        if card is not None:
            self.renderer.render_new_card(card, player, self.table.get_card_count(player))
            self.table.is_player_busted(player)
        else:
            print("\t[WARN] NO MORE CARDS AVAILABLE FOR DEAL!!")
