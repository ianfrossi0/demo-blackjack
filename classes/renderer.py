from .constants import *
import math
from .card import Card


class Renderer:
    def __init__(self):
        self.screen = self.__initialize_screen()

        # Dummy card with number 3 as the 3rd image in the
        # fourth row is the upside-down card
        deck_image = Card(3, "dummy")
        deck_image.visible = False
        self.UPSIDE_DOWN_CARD = self.get_card_image(deck_image)

        # Scale image size based on screen size
        self.UPSIDE_DOWN_CARD = pygame.transform.scale(self.UPSIDE_DOWN_CARD,
                                                       (int(CARD_WIDTH * SCALE[0]) // 100,
                                                        int(CARD_HEIGHT * SCALE[1]) // 60))

    # Get corresponding card image and render it.
    def render_new_card(self, card, player, card_number=0):
        card_image = self.get_card_image(card)

        # Scale image size based on screen size
        card_image = pygame.transform.scale(card_image,
                                            (int(CARD_WIDTH * SCALE[0]) // 100,
                                             int(CARD_HEIGHT * SCALE[1]) // 60))

        if player > -1:  # This is a player's turn
            # This formula should return the following:
            # Player = 1 -> y = 250
            # Player = 2 -> y = 500
            # Player = 3 -> y = 500
            # Player = 4 -> y = 250
            y = -125 * (player + 1) ** 2 + 625 * (player + 1) - 250

            # This formula should return the following:
            # Player = 1 -> 250
            # Player = 2 -> 520
            # Player = 3 -> 880
            # Player = 4 -> 1140 (using a slight correction)
            x = int(45 * (player + 1) ** 2 + 135 * (player + 1) + 70) - int(player / 3) * 190

            # When player is on the left side, the second card onwards
            # will be stacking slightly to the right. Do the opposite
            # for players on the right side of the table
            if card_number > 1:
                if player < 2:
                    y += card_number * 10
                    x += card_number * 10
                else:
                    y -= card_number * 10
                    x += card_number * 10

            # Since cards should be angled towards the deck, calculate
            # and get the distance between current card and deck
            distance = (CARD_SCREEN_CENTER_X - x, y - 20)

            # In order to get the correct rotation, apply the following formula:
            # r = 90 - the absolute value of tan^-1(h/x) evaluated in degrees
            r = 90 - abs(math.degrees(math.atan(distance[1]/distance[0])))

            # This players' cards will be on the left
            # side of the table, must flip the angle
            if player < 2:
                r *= -1
        else:  # Dealer's turn
            x = CARD_SCREEN_CENTER_X + CARD_WIDTH * card_number
            y = 20
            r = 0

        self.render(card_image, (x, y), r)

        print(f"Card printed for player {player + 1} at {(x, y)} with rotation {r}°\n")

    # Render a surface on a given position and rotation
    def render(self, surface, position, rotation=0):
        if rotation != 0:
            surface = pygame.transform.rotate(surface, rotation)
        self.screen.blit(surface, position)
        pygame.display.update()

    # Get the surface (sprite) of a desired card from sheet
    def get_card_image(self, card) -> object:
        # Set the origin of the splitting as:
        # x = card width * card number
        # y = card height * card icon value
        icon_value = 4 if not card.visible else self.get_icon_value(card.icon)
        real_number = 3 if icon_value == 4 else card.number
        origin = (CARD_WIDTH * (real_number - 1), CARD_HEIGHT * icon_value)
        return DECK.subsurface(pygame.Rect(origin, (int(CARD_WIDTH), CARD_HEIGHT)))

    # Get screen size and initialize screen
    @staticmethod
    def __initialize_screen() -> object:
        print("\tInitializing screen... ")
        print(f"\t\tWindowed screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # , pygame.FULLSCREEN)
        pygame.display.set_caption("Blackjack - Testing...")
        screen.fill((103, 0, 0))  # Fill screen with dark red, maybe change it later?

        print(f"\t\tImages folder is {IMG_PATH}")
        pygame.display.set_icon(pygame.image.load(os.path.join(IMG_PATH, "logo.png")))
        print("\tScreen initialized OK!")
        return screen

    # Get row of card based on icon
    @staticmethod
    def get_icon_value(icon) -> int:
        if icon == "Clovers":
            value = 0
        elif icon == "Tiles":
            value = 1
        elif icon == "Hearts":
            value = 2
        elif icon == "Pikes":
            value = 3
        else:  # Card is upside-down
            value = 4
        return value
