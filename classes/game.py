from .table import Table  # REMEMBER TO DELETE THIS AFTER TESTING IS DONE... OR NOT!
from .renderer import Renderer
from .constants import *


class Game:  # TODO: refactor main.py code to work on this class
    # Game main loop
    @staticmethod
    def start():
        print(HORIZONTAL_LINE)
        print("\nInitializing pygame... ", end='')
        pygame.init()
        clock = pygame.time.Clock()
        print("OK!\n")

        print("\nInitializing variables... ")
        players = int(input("\tPlayers: "))
        current_player = 0
        new_deal = True  # New initial deal
        turn_end = False  # Marks end of player turn
        turn_initiated = False  # Boolean for actions to be taken at turn start
        player_choice_selected = False  # Player has selected what to play on their turn
        time_last_action = 0  # Cooldown between actions
        turn_number = 0
        print("OK!\n")

        print("\nInitializing table... ")
        table = Table(players)
        print(f"OK, table instantiated with {players} players!\n", end='')

        print("\nInitializing renderer... ")
        renderer = Renderer()
        print("Renderer initialized OK!\n")

        print("\nDrawing table... ", end='')
        # NOTE: Using (SCREEN_WIDTH/HEIGHT - IMG_SIZE) / 2 as X or Y positioning
        # will perfectly center the surface on the screen
        renderer.render(TABLE, ((SCREEN_WIDTH - 1392) / 2, 0))
        renderer.render(renderer.UPSIDE_DOWN_CARD, (CARD_SCREEN_CENTER_X - 170, 20))
        print("OK!\n")

        print("\nDrawing buttons... ", end='')
        renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")  # Hit button
        renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")  # Stand button
        renderer.render_button(DARK_GRAY, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")  # Double button
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
                    # Allow movement only when it's their turn, unless escape is pressed
                    if event.key in MOVEMENT_KEYS and turn_initiated:
                        # Redraw buttons to clean outline from other boxes besides current selection
                        renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")  # Hit button
                        renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")  # Stand button
                        renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")  # Double button

                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            print("\tLeft arrow key or A pressed")
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            print("\tRight arrow key or D pressed")
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            print("\tUp arrow key or W pressed")
                            player_choice = 2 if player_choice == 2 else player_choice + 1
                            renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            print("\tDown arrow key or S pressed")
                            player_choice = 0 if player_choice == 0 else player_choice - 1
                            renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))
                        if event.key == pygame.K_SPACE:
                            print("\tSpace bar pressed")
                            player_choice_selected = True

            # Check if enough time has passed between last action and now
            if time_now - time_last_action >= ACTION_COOLDOWN:
                if new_deal:  # Dealing initial two cards
                    if table.get_card_count(0) == 0:
                        print("Start dealing initial hand...")

                    if table.up_for_initial_deal(current_player):  # Dealer or player must receive card
                        card = table.deal(current_player)  # Get a new card
                        renderer.render_new_card(card, current_player, table.get_card_count(current_player))
                        turn_end = True  # After card has be dealt, turn has ended
                        time_last_action = pygame.time.get_ticks()

                    new_deal = not table.finished_dealing()  # Check if initial deal is over

                    if not new_deal:
                        turn_number = 1
                        print("Finished dealing initial hand")
                else:  # Ready for player turn
                    if not turn_initiated:  # Has player turn already started?
                        print(f"\nStarted turn for player {current_player+ 1} on turn {turn_number}")
                        player_choice = 0

                        # Rerender player action buttons with BLACK color
                        # and outline the first option
                        renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 90, 150, 60, "Hit")  # Hit button
                        renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 180, 150, 60, "Stand")  # Stand button
                        renderer.render_button(BLACK, 40, SCREEN_HEIGHT - 270, 150, 60, "Double")  # Double button
                        renderer.render_option(40, SCREEN_HEIGHT - (90 + 90 * player_choice - 1))

                        player_choice_selected = False
                        turn_initiated = True

                    if player_choice_selected:  # Player pressed the spacebar on a button
                        if player_choice == 0:
                            print(f"\tPlayer {current_player + 1} hit")
                            card = table.deal(current_player)  # Get a new card

                            if card is not None:
                                renderer.render_new_card(card, current_player, table.get_card_count(current_player))
                            else:
                                print("\tNO MORE CARDS AVAILABLE FOR DEAL!!")
                        elif player_choice == 1:
                            print(f"\tPlayer {current_player + 1} stood")
                        else:
                            print(f"\tPlayer {current_player + 1} will double")
                        turn_end = True

            if turn_end:
                if turn_end and player_choice_selected:
                    print(f"Turn finished for player {current_player + 1} on turn {turn_number}")

                if current_player == players - 1:
                    turn_number += 1
                    current_player = -1
                else:
                    current_player += 1

                turn_end = False
                turn_initiated = False
                player_choice_selected = False

            renderer.update(clock)  # Update
