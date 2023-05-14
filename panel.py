import widgets

class CPanel:
    def __init__(self,parent,root):
        self.parent = parent
        self.root = root
        self.btns = ["Play","Restart","Settings"]
        self.button = dict()
        self.button_template = widgets.CButton

    def create(self):
        for btn in self.btns:
            self.button[btn] = self.button_template(self.parent, \
                    text=btn,comm=lambda x=btn : self.button_press(x))
            self.button[btn].pack()

    def button_press(self,btn):
        if(btn == "Play"):
            self.root.play_game()
        elif(btn == "Restart"):
            self.root.restart_game()
        elif(btn == "Settings"):
            self.root.settings()
