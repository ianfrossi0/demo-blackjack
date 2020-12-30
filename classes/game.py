from .table import Table  # REMEMBER TO DELETE THIS AFTER TESTING IS DONE... OR NOT!
from .renderer import Renderer
from .constants import *


class Game:  # TODO: refactor main.py code to work on this class
    def __init__(self):
        self.players = int(input("\tPlayers: "))
        print("\nInitializing table... ")
        self.table = Table(self.players)
        print(f"OK, table instantiated with {self.players} players!\n", end='')
        self.renderer = None  # Create variable with None value, initialize later

    # Game main loop
    def start(self):
        print(HORIZONTAL_LINE)
        print("\nInitializing pygame... ", end='')
        pygame.init()
        clock = pygame.time.Clock()
        print("OK!\n")

        print("\nInitializing variables... ")
        player = 0
        new_deal = True  # New initial deal
        turn_end = False  # Marks end of player turn
        turn_initiated = False  # Boolean for actions to be taken at turn start
        player_choice_selected = False  # Player has selected what to play on their turn
        time_last_action = 0  # Cooldown between actions
        turn_number = 0
        player_choice = 0
        print("OK!\n")

        print("\nInitializing renderer... ")
        self.renderer = Renderer()
        print("Renderer initialized OK!\n")

        print("\nDrawing table... ", end='')
        self.renderer.render(TABLE, ((SCREEN_WIDTH - 1392) / 2, 0))
        self.renderer.render(self.renderer.UPSIDE_DOWN_CARD, (CARD_SCREEN_CENTER_X - 170, 20))
        print("OK!\n")

        print("\nDrawing buttons... ", end='')
        self.renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")  # Hit button
        self.renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")  # Stand button
        self.renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")  # Double button
        print("OK!\n")

        print(HORIZONTAL_LINE)
        print(f"\n\nGame starting.\n\tRunning with a resolution of {SCREEN_WIDTH}x{SCREEN_HEIGHT} "
              f"(current scale is {SCALE[0]:.2f} horizontal and {SCALE[1]:.2f} vertical) at target {FPS} fps."
              f"\n\t{ACTION_COOLDOWN}ms of cooldown between actions\n")
        print(HORIZONTAL_LINE)

        while True:
            time_now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\nQuitting...")
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    # Allow movement only when it's their turn
                    if event.key in MOVEMENT_KEYS and turn_initiated:
                        # Redraw buttons to clean outline from other boxes besides current selection
                        self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")  # Hit button
                        self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")  # Stand button
                        self.renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")  # Double button

                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            print("\tLeft arrow key or A pressed")
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            print("\tRight arrow key or D pressed")
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            print("\tUp arrow key or W pressed")
                            player_choice = 2 if player_choice == 2 else player_choice + 1
                            self.renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            print("\tDown arrow key or S pressed")
                            player_choice = 0 if player_choice == 0 else player_choice - 1
                            self.renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))
                        if event.key == pygame.K_SPACE:
                            print("\tSpace bar pressed")
                            player_choice_selected = True

            # Game main logic, do while all players are playing
            if not self.table.have_all_players_stood_or_busted():
                # Check if enough time has passed between last action and now
                if time_now - time_last_action >= ACTION_COOLDOWN:
                    if new_deal:  # Dealing initial two cards
                        if self.table.get_card_count(0) == 0:
                            print("Start dealing initial hand...")

                        if self.table.up_for_initial_deal(player):  # Dealer or player must receive card
                            card = self.table.deal(player)  # Get a new card
                            self.renderer.render_new_card(card, player, self.table.get_card_count(player))
                            turn_end = True  # After card has be dealt, turn has ended
                            time_last_action = pygame.time.get_ticks()

                        new_deal = not self.table.finished_dealing()  # Check if initial deal is over
                        self.table.is_player_busted(player)

                        if not new_deal:
                            turn_number = 1
                            print("Finished dealing initial hand")
                    else:  # Ready for player turn
                        if not self.table.is_player_busted(player) and not self.table.is_player_standing(player):
                            if not turn_initiated:  # Has player turn already started?
                                print(f"\nStarted turn for "
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

                                turn_initiated = True

                            if player_choice_selected:  # Player pressed the spacebar on a button
                                if player_choice == 0:
                                    print(f"\t{'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                          f" hit")
                                    self.deal(player)
                                elif player_choice == 1:
                                    print(f"\t{'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                          f" stood")
                                    self.table.player_stand(player)
                                else:
                                    print(f"\t{'Dealer' if player == -1 else self.table.get_player_name(player)}"
                                          f" will double")
                                    self.deal(player)  # Get a new card
                                    
                                    if not self.table.is_player_busted(player):
                                        # If player is not busted, then stand
                                        self.table.player_stand(player)
                                turn_end = True
                                time_last_action = pygame.time.get_ticks()
                        else:  # Current player is standing or busted
                            if self.table.is_player_standing(player):
                                print(f"\n{'Dealer' if player == -1 else self.table.get_player_name(player)} "
                                      f"is standing! Skipping to next player...")
                            else:
                                print(f"\n{'Dealer' if player == -1 else self.table.get_player_name(player)} "
                                      f"is busted! Skipping to next player...")
                            turn_end = True

                if turn_end:
                    if turn_end and player_choice_selected:
                        print(f"Turn finished for "
                              f"{'Dealer' if player == -1 else self.table.get_player_name(player)} "
                              f"on turn {turn_number}")

                    if player == self.players - 1:
                        turn_number += 1
                        player = -1
                    else:
                        player += 1

                    turn_end = False
                    turn_initiated = False
                    player_choice_selected = False
            else:
                # No players nor dealer are playing, start checking for winner
                print("Game over")

            self.renderer.update(clock)  # Update

    # Small function to draw a new card or just scream
    # if there are no more cards in the deck
    def deal(self, player):
        card = self.table.deal(player)  # Get a new card
        if card is not None:
            self.renderer.render_new_card(card, player, self.table.get_card_count(player))
            self.table.is_player_busted(player)
        else:
            print("\tNO MORE CARDS AVAILABLE FOR DEAL!!")
