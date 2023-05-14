import chess_pieces as cp_mod
import numpy as np_mod
import itertools as it_mod

class CChessEngine:
    def __init__(self,game):
        self.game = game
        self.board = list()
        self.label = list()
        self.width = 8
        self.height = 8
        self.occupied_field = dict()
        self.pieces = dict()
        self.is_moving = False
        self.moving_piece = None
        self.piece_moves = list()
        self.possible_move = None
        self.last_moved = None
        self.player_active = False
        self.color_position = { "white" : (1,2) , "black" : (8,7) }

    def selected(self,position):
        if(not self.player_active):
            return
        elif(self.is_moving == False and position in self.occupied_field and \
          ((self.last_moved is None and \
          self.occupied_field[position].what_color() == "white") or \
          (not (self.last_moved is None) and \
          self.last_moved.what_color() != self.occupied_field[position].what_color()))):
            self.possible_move = self.occupied_field[position].possible_move()
            self.moving_piece = self.occupied_field[position]
            self.trim_moves()
            print(f"Possible_move:{self.possible_move}")
            if(self.possible_move == set()):
                self.game.flash_alert(position)
                self.moving_piece = None
                self.possible_move = None
            else:
                self.game.highlight_field(self.possible_move)
                self.is_moving = True
        elif(self.is_moving == True):
            self.game.unhighlight_all_fields()
            self.chess_move(self.moving_piece,position)
            self.is_moving = False
            self.moving_piece = None
            self.possible_move = None
        elif(not (position in self.occupied_field)):
            pass
        else:
            self.game.flash_alert(position,mistake=True)

    def trim_moves(self):
        """change this method to approve possible_moves not to trim moves"""
        "add en passant, don't forget to add en passant!!!"
        trimed = set([move for move_list in self.possible_move for move in move_list])
        print(f"TRIMED:{trimed}")
        for move_list in self.possible_move:
            for move in move_list:
                if(self.is_field_occupied(move) and \
                 self.moving_piece.what_color() == self.occupied_field[move].what_color()):
                    trimed.remove(move) # removing possibility to jump on your own pieces
                elif(self.moving_piece.what_rank() != "knight" and \
                 self.are_fields_occupied_inb(self.moving_piece.current_position(),move)):
                    trimed.remove(move) # when changed to approval, break from continuation
                                        # of second for loop, other positions in the list are
                                        # further from the location and therefore obsolete
                elif(self.moving_piece.what_rank() == "pawn" and \
                 self.moving_piece.current_position()[0] == move[0] and \
                 self.is_field_occupied(move)):
                    trimed.remove(move)
                elif(self.moving_piece.what_rank() == "pawn" and \
                 (not self.is_field_occupied(move)) and \
                 self.moving_piece.current_position()[0] != move[0]): #diagonal move
                    trimed.remove(move)                               #for pawn
                elif(self.moving_piece.what_rank() == "king"):
                    self.king_trim(trimed,move)
        x = self.possible_move
        self.possible_move = trimed
        del x

    def king_trim(self,trimed,move):
        jump_length = ord(self.moving_piece.current_position()[0]) - ord(move[0])
        if(np_mod.abs(jump_length) != 2):
            return
        if(not self.moving_piece.is_first_move()): 
            trimed.remove(move)
        else:
            rooks = self.pieces[self.moving_piece.what_color()]["rook"]
            for position in rooks:
                rook = rooks[position]
                is_inbetween = True if np_mod.abs(ord(move[0]) - \
                        ord(rook.current_position()[0])) < 2 \
                        else False
                if(is_inbetween):
                    occupied_inbetween = self.are_fields_occupied_inb( \
                            rook.current_position(), \
                            self.moving_piece.current_position())
                if(is_inbetween and (not rook.is_first_move() or rook.is_taken() or \
                        occupied_inbetween)):
                    trimed.remove(move)

    def are_fields_occupied_inb(self,start,end):
        direction = (np_mod.sign(ord(start[0]) - ord(end[0])) * (-1), \
                np_mod.sign(int(start[1]) - int(end[1])) * (-1))
        fields = list()
        start = f"{chr(ord(start[0]) + direction[0])}{int(start[1]) + direction[1]}"
        if(start == end):
            return False
        def find_range(start,end,direction):
            if(start == end):
                f_range = it_mod.repeat(start)
            else:
                f_range = range(start,end,direction)
            return f_range

        column_range = find_range(ord(start[0]),ord(end[0]),direction[0])
        row_range = find_range(int(start[1]),int(end[1]),direction[1])

        for row,column in zip(row_range,column_range):
            position = f"{chr(column)}{row}"
            print(position)
            fields.append(self.is_field_occupied(position))
        print("\n"*2)
        print(f"FIELDS {fields}")
        return any(fields)

    def is_field_occupied(self,position):
        return position in self.occupied_field

    def _initialize_pieces(self):
        self.last_moved = None
        cls = None
        clpo = self.color_position
        for color in clpo:
            self.pieces[color] = { 
             "pawn"  : { f'{chr(97+z)}{clpo[color][1]}':None \
                     for z in range(self.width)},\
             "rook"  : { f'a{clpo[color][0]}':None, f'h{clpo[color][0]}':None }, \
             "knight": { f'b{clpo[color][0]}':None, f'g{clpo[color][0]}':None }, \
             "bishop": { f'c{clpo[color][0]}':None, f'f{clpo[color][0]}':None }, \
             "queen" : { f'd{clpo[color][0]}':None }, \
             "king"  : { f'e{clpo[color][0]}':None } }
        for color in self.pieces:
            for rank in self.pieces[color]:
                for position in self.pieces[color][rank]:
                    if(rank == "pawn"):
                        cls = cp_mod.CPawn
                    elif(rank == "rook"):
                        cls = cp_mod.CRook
                    elif(rank == "knight"):
                        cls = cp_mod.CKnight #change
                    elif(rank == "bishop"):
                        cls = cp_mod.CBishop
                    elif(rank == "queen"):
                        cls = cp_mod.CQueen
                    elif(rank == "king"):
                        cls = cp_mod.CKing
                    piece = cls(position,color,rank)
                    self.pieces[color][rank][position] = piece
                    self.game.change_board(position,piece.what_image())
                    self.occupied_field[position] = piece

    def chess_move(self,piece,position):
        jump = ""
        if(not(position in self.possible_move)):
            return #create class exception
        if(position in self.occupied_field):
            self.occupied_field[position].take()
            jump = "x"

        del self.occupied_field[piece.current_position()]
        self.occupied_field[position] = piece
        rank = self.pieces[piece.what_color()][piece.what_rank()]
        del rank[piece.current_position()]
        rank[position] = piece
        self.piece_moves.append(f"{piece.current_position()}{jump}{position}")

        self.game.change_board(piece.current_position(),'')
        piece.move(position)
        self.game.change_board(position,piece.what_image())
        self.last_moved = piece
        return

    def run(self):
        cp_mod.CPiece.board = (self.height,self.width)
        self._initialize_pieces()

    def play_game(self):
        self.player_active = True

    def clear_game(self):
        for color in self.pieces:
            for rank in self.pieces[color]:
                for position in self.pieces[color][rank]:
                    piece = self.pieces[color][rank][position]
                    self.pieces[color][rank][position] = None
                    if(not piece.is_taken()):
                        self.occupied_field[position] = None
                        del self.occupied_field[position]
                    print(self.pieces)
                    print(piece)
                    print("here\n\n")
                    self.game.change_board(piece.current_position(),'')
                    del piece
            self.pieces[color].clear()

    def restart_game(self):
        self.clear_game()
        self._initialize_pieces()
