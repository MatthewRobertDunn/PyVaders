


class GameKeys:
    def poll(self, keys):
        self.left = keys.is_button_down('arrow_left')
        self.right = keys.is_button_down('arrow_right')
        self.up =  keys.is_button_down('arrow_up')
        self.down =  keys.is_button_down('arrow_down')
        self.fire = keys.is_button_down('space')
        self.select = self.fire or keys.is_button_down('enter')
