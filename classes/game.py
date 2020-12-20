from .table import Table  # REMEMBER TO DELETE THIS AFTER TESTING IS DONE... OR NOT!
from .renderer import Renderer
from .constants import *


class Game:
    # Game main loop
    @staticmethod
    def start():
        print("\n_____________________________________________________________________________")
        print("\nInitializing pygame... ", end='')
        pygame.init()
        clock = pygame.time.Clock()  # TODO: check what this is for
        print("OK!\n")

        print("\nInitializing variables... ")
        players = int(input("\tPlayers: "))
        current_player = 0
        new_deal = True  # New initial deal
        turn_end = False  # Marks end of player turn
        dealer_may_have_natural = False  # Dealer got a 10 or ace in their initial deal
        time_last_action = 0  # Cooldown between actions
        print("OK!\n")

        print("\nInitializing table... ")
        table = Table(players)
        print(f"OK, table instantiated with {players} players!\n", end='')

        print("\nInitializing renderer... ")
        renderer = Renderer()
        print("Renderer initialized OK!\n")

        # NOTE: Using (SCREEN_WIDTH/HEIGHT - IMG_SIZE) / 2 as X or Y positioning
        # will perfectly center the surface on the screen
        renderer.render(TABLE, ((SCREEN_WIDTH - 1392) / 2, 0))
        renderer.render(renderer.UPSIDE_DOWN_CARD, (CARD_SCREEN_CENTER_X - 170, 20))

        print("Start running game")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\nQuitting...")
                    pygame.quit()

            time_now = pygame.time.get_ticks()

            # Check if enough time has passed between last action and now
            if time_now - time_last_action >= ACTION_COOLDOWN:
                if new_deal:  # Dealing initial two cards
                    if current_player == -1:  # Dealer's turn
                        ok_for_deal = True if len(table.dealer.hand.cards) < 2 else False
                        card_number = len(table.dealer.hand.cards)
                    else:  # Player's turn
                        ok_for_deal = True if len(table.player_hands[current_player][1].cards) < 2 else False
                        card_number = len(table.player_hands[current_player][1].cards) + 1

                    if ok_for_deal:  # Dealer or player must receive card
                        card = table.deal(current_player)
                        renderer.render_new_card(card, current_player, card_number)
                        turn_end = True
                        time_last_action = pygame.time.get_ticks()

                    new_deal = not table.finished_dealing()  # Check if initial deal is over

                    if not new_deal:
                        print("Finished dealing initial hand")

            if turn_end:
                current_player = current_player + 1 if current_player < players - 1 else -1
                turn_end = False

            pygame.display.flip()  # Update
