from __future__ import annotations
from PIL import Image, ImageGrab
import pytesseract

class Resources:
    """This class lets you manage your ressources
    """
    def __init__(self: Resources, gold: int = 0, minerals: int = 0, chips: int = 0, star_battery: int = 0, mana_light : int = 0) -> None:
        self.gold = gold
        self.minerals = minerals
        self.star_battery = star_battery
        self.mana_light = mana_light

    @staticmethod
    def _get_value_from_screen(bbox: tuple[int, int, int, int]) -> int:
        """Obtain an integer value from a region of the screen

        Args:
            bbox (tuple[int, int, int, int]): Bounding box of the screenshot

        Returns:
            int: Extracted number
        """
        sc: Image.Image = ImageGrab.grab(bbox=bbox)
        value: str = pytesseract.image_to_string(
            sc, lang='eng', config="--psm 7")
        return int("".join([v for v in value.split() if v.isdigit()]))

    def get_gold_from_screen(self: Resources, bbox: tuple[int, int, int, int]) -> None:
        """Obtains and stores the amount of gold from a screenshot

        Args:
            bbox (tuple[int, int, int, int]): Bounding box of the screenshot
        """
        self.gold = Resources._get_value_from_screen(bbox)

    def get_minerals_from_screen(self: Resources, bbox: tuple[int, int, int, int]) -> None:
        """Obtains and stores the amount of minerals from a screenshot

        Args:
            bbox (tuple[int, int, int, int]): Bounding box of the screenshot
        """
        self.minerals = Resources._get_value_from_screen(bbox)
    
    def get_chips_from_screen(self: Resources, bbox: tuple[int, int, int, int]) -> None: ...

    def get_resources_from_screen(self: Resources) -> None:
        """Obtains and stores the amount of minerals and gold from the top of your screen
        """
        self.get_gold_from_screen((940, 110, 1020, 130))
        self.get_minerals_from_screen((1100, 110, 1175, 130))