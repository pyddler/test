import tkinter as tk
import widgets
from PIL import Image, ImageTk

class CGUIBoard:
    def __init__(self,parent,root=None):
        self.root = root
        self.parent = parent
        self.board = list()
        self.label = list()
        self.width = 8
        self.height = 8
        self.color = ["DarkOliveGreen4","lemon chiffon", "DarkGoldenrod2", \
                "light goldenrod", "IndianRed4","light coral"]
        self.highlighted = set()
        self.field_size = (12,5)
        self.board_frame = widgets.CFrame(parent,bg="black")
        self.pieces = ["pawn","king","queen","bishop","knight","rook","move"]
        self.piece_images = { "white": dict(), "black" : dict() }
        self.image_path_template = "images/{color}{piece}.png"
    
    def _load_piece_images(self):
        for piece in self.pieces:
            for color in self.piece_images:
                image_path = self.image_path_template.format(color=color[0],piece=piece)
                print(image_path)
                image = Image.open(image_path)
                if(not piece in ("move","queen")): #make all images same size !!! to remove this:
                    image = image.resize((40,50))
                self.piece_images[color][piece] = ImageTk.PhotoImage(image)

    def click(self,event,x,y):
        position = self.__coordinates_chess(row=y,column=x)
        print(f"field:{position}")
        self.root.selected_field(position)

    def flash_alert(self,position,mistake=False):
        self.change_board(position,None,hi_bg=True,mistake=mistake)
        self.root.after(250,lambda x=position : self.change_board(x,None,hi_bg=False))

    def highlight_field(self,fields,for_color="white"):
        self.highlighted = self.highlighted.union(fields)
        for position in fields:
            if(self.root.is_field_occupied(position)):
                self.change_board(position,None,hi_bg=True)
            else:
                self.change_board(position,f"{for_color}-move")

    def unhighlight_all_fields(self):
        for position in self.highlighted:
            if(self.root.is_field_occupied(position)):
                self.change_board(position,None,hi_bg=False)
            else:
                self.change_board(position,'')
        self.highlighted.clear()

    def __create_board(self):
        "very ugly, when bored, try to change this:"
        for x in range(self.height):
            self.board.append(list())
        
        for y in range(self.height):
            for x in range(self.width):
                self.board[y].append(tk.Label(self.board_frame,bg=self.color[(y+x)%2], \
                        width=self.field_size[0],height=self.field_size[1]))
                self.board[y][x].grid(row=self.height-1-y,column=x,sticky="nesw")
                        #ipadx=self.ipadx, ipady=self.ipady)
                self.board[y][x].bind('<Button-1>', \
                        lambda event,a=x,b=y: self.click(event,a,b))

            self.label.append(tk.Label(self.board_frame,text=str(self.height - y), \
                    bg=self.color[(y+x)%2],fg=self.color[(y+x+1)%2], \
                    width=self.field_size[0]//2,height=self.field_size[1]))
            self.label[y].grid(row=y,column=self.width,sticky="nesw")

        for x in range(self.width):
            self.label.append(tk.Label(self.board_frame,text=chr(x + 97), \
                    bg=self.color[(x+self.height+1)%2],fg=self.color[(x+self.height)%2], \
                    width=self.field_size[0],height=self.field_size[1]//2))
            self.label[self.height+x].grid(row=self.height,column=x,sticky="nesw")

        self.label.append(tk.Label(self.board_frame, \
                bg=self.color[(self.width+self.height+1)%2], \
                fg=self.color[(self.width+self.height)%2], \
                width=self.field_size[0]//2,height=self.field_size[1]//2))
        self.label[self.height+self.width].grid(row=self.height,column=self.width, \
                sticky="nesw")

    def change_board(self,position,what_image,hi_bg=False,mistake=False):
        print(f"Changing bakcground:::{position}")
        (y,x) = self.__coordinates_array(position)
        image = ''
        if(not what_image is None and what_image != ''):
            rc = what_image.split("-")
            image = self.piece_images[rc[0]][rc[1]]
        if(not(what_image is None)):
            self.board[y][x].config(image=image)
            if(not(hi_bg)):
                return
        bg = self.board[y][x]["bg"]
        if(hi_bg and mistake):
            if(bg == self.color[0]):
                bg = self.color[4]
            elif(bg == self.color[1]):
                bg = self.color[5]
        elif(hi_bg):
            if(bg == self.color[0]):
                bg = self.color[2]
            elif(bg == self.color[1]):
                bg = self.color[3]
        else:
            if(bg in (self.color[2],self.color[4])):
                bg = self.color[0]
            elif(bg in (self.color[3],self.color[5])):
                bg = self.color[1]
        self.board[y][x].config(bg=bg)

    @staticmethod
    def __coordinates_array(position):
        column = ord(position[0]) - 97
        row = int(position[1]) - 1
        return (row,column)

    @staticmethod
    def __coordinates_chess(row,column):
        y = row + 1
        x = chr(97+column)
        return f"{x}{y}"

    def create(self):
        self.__create_board()
        self._load_piece_images()
        self._pack()

    def reset(self):
        return

    def _pack(self):
        self.board_frame.pack(fill="both",expand=1)

class CCLIBoard:
    def __init__(self):
        self.test = None
