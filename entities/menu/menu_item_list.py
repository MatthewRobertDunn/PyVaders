from context_manager import ContextManager
from entities.menu.menu_item import MenuItem
from entities.ticking_trait import TickingTrait

class MenuItemList(TickingTrait):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_items = []
        self.selected_index = 0

    def on_spawn(self):
        self.create_menu_items()
        for menu_item in self.menu_items:
            self.context.spawn_entity(menu_item)

        if(len(self.menu_items) > 0):
            self.menu_items[0].set_focus(True)
        
    #override this to create different menus
    def create_menu_items(self):
        self.menu_items.append(MenuItem(context = self.context,position=(0,10),text="Start Game",on_selected=self.on_selected))
        self.menu_items.append(MenuItem(context = self.context,position=(0,5),text="Also Start",on_selected=self.on_selected))
        self.menu_items.append(MenuItem(context = self.context,position=(0,0),text="Another",on_selected=self.on_selected))


    def select_down(self):
        self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        self.select_update()

    def select_up(self):
        self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        self.select_update()
    
    def select_update(self):
        print(self.selected_index)
        for menu_item in self.menu_items:
            menu_item.set_focus(False)
        self.menu_items[self.selected_index].set_focus(True)

    def tick(self):
        if(self.keys.down):
            self.at_most("select_down", self.select_down,0.2)

        if(self.keys.up):
            self.at_most("select_Up", self.select_up,0.2)



    def on_selected(self):
        ContextManager.next_context = ContextManager.game_context
