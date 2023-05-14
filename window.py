#!/usr/bin/bash

import tkinter as tk
import tkinter.ttk as ttk
import board
import widgets
import panel

class CGUIWindow(tk.Tk):
    def __init__(self,game):
        super().__init__()
        self.geometry("950x870")
        self.game = game
        self._style = ttk.Style()
        self.frm_cls = widgets.CFrame
        self.frm_cls.window = self
        self.frame = { "board" : None, "panel" : None }
        for frame in self.frame:
            self.frame[frame] = self.frm_cls(self,name=frame,bg="black")
        self.board = board.CGUIBoard(parent=self.frame["board"],root=self)
        self.panel = panel.CPanel(parent=self.frame["panel"],root=self)
        self.board.create()
        self.panel.create()
        for frame in self.frame:
            self.frame[frame].pack(side="left",fill="both",expand=1)

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self,value):
        self._style.configure(value["name"], \
                background=value["bg"])

    def selected_field(self,position):
        self.game.selected_field(position)

    def is_field_occupied(self,position):
        return self.game.is_field_occupied(position)

    def change_board(self,position,what_image):
        self.board.change_board(position,what_image)

    def highlight_field(self,position):
        self.board.highlight_field(position)

    def unhighlight_all_fields(self):
        self.board.unhighlight_all_fields()

    def flash_alert(self,position,mistake):
        self.board.flash_alert(position,mistake)

    def play_game(self):
        self.game.play_game()

    def restart_game(self):
        self.game.restart_game()

    def settings(self):
        self.game.settings()

    def reset_board(self):
        self.board.reset()
