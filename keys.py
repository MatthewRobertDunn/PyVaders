


class GameKeys:
    def poll(self, keys):
        self.left = keys.is_button_down('arrow_left')
        self.right = keys.is_button_down('arrow_right')
        self.fire = keys.is_button_down('space')
