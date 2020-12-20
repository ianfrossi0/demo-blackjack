from .table import Table  # REMEMBER TO DELETE THIS AFTER TESTING IS DONE... OR NOT!
from .renderer import Renderer
from .constants import *


class Game:
    # Game main loop
    @staticmethod
    def start():
        print(HORIZONTAL_LINE)
        print("\nInitializing pygame... ", end='')
        pygame.init()
        clock = pygame.time.Clock()  # TODO: check what this is for
        print("OK!\n")

        print("\nInitializing variables... ")
        players = int(input("\tPlayers: "))
        current_player = 0
        new_deal = True  # New initial deal
        turn_end = False  # Marks end of player turn
        time_last_action = 0  # Cooldown between actions
        print("OK!\n")

        print("\nInitializing table... ")
        table = Table(players)
        print(f"OK, table instantiated with {players} players!\n", end='')

        print("\nInitializing renderer... ")
        renderer = Renderer()
        print("Renderer initialized OK!\n")

        print("\nDrawing table... ")
        # NOTE: Using (SCREEN_WIDTH/HEIGHT - IMG_SIZE) / 2 as X or Y positioning
        # will perfectly center the surface on the screen
        renderer.render(TABLE, ((SCREEN_WIDTH - 1392) / 2, 0))
        renderer.render(renderer.UPSIDE_DOWN_CARD, (CARD_SCREEN_CENTER_X - 170, 20))
        print("OK!\n")

        print(HORIZONTAL_LINE)
        print(f"\n\nGame starting.\n\tRunning with a resolution of {SCREEN_WIDTH}x{SCREEN_HEIGHT} "
              f"(current scale is {SCALE[0]:.2f} horizontal and {SCALE[1]:.2f} vertical)."
              f"\n\t{ACTION_COOLDOWN}ms of cooldown between actions\n")
        print(HORIZONTAL_LINE)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\nQuitting...")
                    pygame.quit()
                if event.type == pygame.KEYDOWN:  # TODO: Implement movement... and buttons to move through
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        print("You are going left!")
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        print("You are going right!")
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        print("You are going up!")
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        print("You are going down!")
                    if event.key == pygame.K_SPACE:
                        print("You are going to space!")

            time_now = pygame.time.get_ticks()

            # Check if enough time has passed between last action and now
            if time_now - time_last_action >= ACTION_COOLDOWN:
                if new_deal:  # Dealing initial two cards
                    if table.get_card_count(0) == 0:
                        print("Start dealing initial hand...")

                    if table.up_for_initial_deal(current_player):  # Dealer or player must receive card
                        card = table.deal(current_player)
                        renderer.render_new_card(card, current_player, table.get_card_count(current_player))
                        turn_end = True
                        time_last_action = pygame.time.get_ticks()

                    new_deal = not table.finished_dealing()  # Check if initial deal is over

                    if not new_deal:
                        print("Finished dealing initial hand")

            if turn_end:
                current_player = current_player + 1 if current_player < players - 1 else -1
                turn_end = False

            pygame.display.flip()  # Update
