from engine.game_context import GameContext
from entities.menu.menu_item_list import MenuItemList


class MenuContext(GameContext):
    def __init__(self, keys, loader):
        super().__init__(keys, loader)
        self.create_world()

    def create_world(self):
        button = MenuItemList(context=self)
        self.spawn_entity(button)
