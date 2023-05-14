import tkinter.ttk as ttk

class CFrame(ttk.Frame):
    window = None
    instance = 0
    def __init__(self,parent,window=None,name="MyFrame", \
                 bg="grey",style=None):
        __class__.instance += 1
        self.style_name = "{name}{self.instance}.TFrame"
        if(style is None):
            __class__.window.style = {"name" : self.style_name, \
                    "bg" : bg}
        super().__init__(parent,style=self.style_name)

class CButton(ttk.Button):
    def __init__(self,parent,text,comm):
        super().__init__(parent,text=text,comm=comm)

