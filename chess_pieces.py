#!/usr/bin/python

class CPiece:
    board = None
    def __init__(self,initial_position,color,rank):
        self.color = color
        self.rank = rank
        self.taken = False
        self.position = initial_position

    def move(self,position):
        self.position = position

    def take(self):
        self.taken = True

    def is_taken(self):
        return self.taken

    def possible_move(self,direction,steps=-1):
        moves = list()
        for dire in direction:
            moves.append(self._general_move(location=self.position,direction=dire, \
                    steps=steps))
        return moves

    def _general_move(self,location,direction,steps):
        fields = list()
        location = [ord(location[0]),int(location[1])]
        while True:
            location[0] += direction[0]
            location[1] += direction[1]
            if not(location[0] >= ord('a') and location[0] <= ord('h') and \
             location[1] >= 1 and location[1] <= 8 and steps != 0):
                break
            position = f"{chr(location[0])}{location[1]}"
            fields.append(position)
            steps -= 1
        return fields

    def current_position(self):
        return self.position

    def what_color(self):
        return self.color

    def what_rank(self):
        return self.rank

    def what_image(self):
        return f"{self.what_color()}-{self.what_rank()}"

class CPawn(CPiece):
    def __init__(self,initial_position,color,rank):
        super().__init__(initial_position,color,rank)
        self.first_move = True
        self.waiting = False

    def move(self,position):
        super().move(position)
        self.at_an_end()
        if(self.is_first_move()):
            self.first_move = False

    def at_an_end(self):
        if(self.position[1] in ("1", self.board[1])):
            self.waiting = True

    def is_first_move(self):
        return self.first_move

    def is_waiting(self):
        return self.waiting

    def possible_move(self):
        moves = list()
        position = (ord(self.position[0]),int(self.position[1]))
        vertical = int()

        if(self.is_waiting()):
            return []

        if(self.color == "white"):
            vertical = 1
        elif(self.color == "black"):
            vertical = -1

        direction = [(0,vertical),(-1,vertical),(1,vertical)]
        if(self.is_first_move()):
            direction.append((0,vertical*2)) # adding double hop
        direction = tuple(direction)
        return super().possible_move(direction,steps=1)

class CRook(CPiece):
    def __init__(self,initial_position,color,rank):
        super().__init__(initial_position,color,rank)
        self.first_move = True

    def possible_move(self):
        direction = ((1,0),(-1,0),(0,1),(0,-1))
        return super().possible_move(direction)

    def move(self,position):
        super().move(position)
        if(self.is_first_move()):
            self.first_move = False

    def is_first_move(self):
        return self.first_move

class CKnight(CPiece):
    def possible_move(self):
        direction = ((1,2),(-1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,1),(-2,-1))
        return super().possible_move(direction,steps=1)

class CBishop(CPiece):
    def possible_move(self):
        direction = ((1,1),(-1,1),(1,-1),(-1,-1)) #(R=1/L=-1/HOLD=0,U=1/D=-1/H=0)
        return super().possible_move(direction)


class CQueen(CPiece):
    def possible_move(self):
        direction = ((1,0),(-1,0),(0,1),(0,-1), \
                (1,1),(-1,1),(1,-1),(-1,-1)) #DIAGONAL
        return super().possible_move(direction)

class CKing(CPiece):
    def __init__(self,initial_position,color,rank):
        super().__init__(initial_position,color,rank)
        self.first_move = True

    def possible_move(self):
        direction = [(1,0),(-1,0),(0,1),(0,-1), \
                (1,1),(-1,1),(1,-1),(-1,-1)]
        if(self.is_first_move()):
            direction.append((2,0))  # adding catling possibility
            direction.append((-2,0)) # 
        direction = tuple(direction)
        return super().possible_move(direction,steps=1)

    def move(self,position):
        super().move(position)
        if(self.is_first_move()):
            self.first_move = False

    def is_first_move(self):
        return self.first_move
