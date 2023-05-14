import window
import engine

class CGame:
    def __init__(self):
        self.engine = engine.CChessEngine(game=self)
        self.window = window.CGUIWindow(game=self)

    def play(self):
        self.engine.run()
        self.window.mainloop()

    def play_game(self):
        self.engine.play_game()
    
    def restart_game(self):
        self.engine.restart_game()
        self.window.reset_board()

    def selected_field(self,position):
        self.engine.selected(position)

    def is_field_occupied(self,position):
        return self.engine.is_field_occupied(position)

    def change_board(self,position,what_image):
        self.window.change_board(position,what_image)

    def highlight_field(self,position):
        self.window.highlight_field(position)

    def unhighlight_all_fields(self):
        self.window.unhighlight_all_fields()

    def flash_alert(self,position,mistake=False):
        self.window.flash_alert(position,mistake=mistake)

    def settings(self):
        return
