from colour import Color
from enum import Enum
from random import shuffle

def color(name):
    return tuple(round(255*c) for c in Color(name).rgb)
colors = ['black','cyan','yellow','purple','green','red','blue','orange']

positions = {
    'I': [[(0,2),(1,2),(2,2),(3,2)],
          [(2,3),(2,2),(2,1),(2,0)],
          [(3,1),(2,1),(1,1),(0,1)],
          [(1,0),(1,1),(1,2),(1,3)]],
    'J': [[(0,1),(0,2),(1,1),(2,1)],
          [(1,2),(2,2),(1,1),(1,0)],
          [(2,1),(2,0),(1,1),(0,1)],
          [(1,0),(0,0),(1,1),(1,2)]],
    'L': [[(0,1),(1,1),(2,1),(2,2)],
          [(1,2),(1,1),(1,0),(2,0)],
          [(2,1),(1,1),(0,1),(0,0)],
          [(1,0),(1,1),(1,2),(0,2)]],
    'O': [[(0,0),(0,1),(1,0),(1,1)],
          [(0,0),(0,1),(1,0),(1,1)],
          [(0,0),(0,1),(1,0),(1,1)],
          [(0,0),(0,1),(1,0),(1,1)]],
    'S': [[(0,1),(1,1),(1,2),(2,2)],
          [(1,2),(1,1),(2,1),(2,0)],
          [(2,1),(1,1),(1,0),(0,0)],
          [(1,0),(1,1),(0,1),(0,2)]],
    'T': [[(0,1),(1,1),(1,2),(2,1)],
          [(1,2),(1,1),(2,1),(1,0)],
          [(2,1),(1,1),(1,0),(0,1)],
          [(1,0),(1,1),(0,1),(1,2)]],
    'Z': [[(0,2),(1,1),(1,2),(2,1)],
          [(2,2),(1,1),(2,1),(1,0)],
          [(2,0),(1,1),(1,0),(0,1)],
          [(0,0),(1,1),(0,1),(1,2)]]
}

def trans4(pos, xy):
    x,y = xy
    return [(x+i,y+j) for (i,j) in pos]
def trans(q,xy):
    x,y = xy
    z,w = q
    return x+z,y+w

class Tile(Enum):
    E,I,O,T,S,Z,J,L = map(color,colors)

class Tetromino:
    def __init__(self,typ,field,zero=None):
        self.typ = typ
        self.field = field
        self.rot = 0
        self.zero=zero
        if typ=='I':
            if not zero:
                self.zero = 3,18
            self.pos = trans4(positions['I'][0], self.zero)
        elif typ=='O':
            if not zero:
                self.zero = 4,20
            self.pos = trans4(positions['O'][0], self.zero)
        else:
            if not zero:
                self.zero = 3,19
            self.pos = trans4(positions[typ][0], self.zero)

        field.put(self)
        self.ok = self.down()

    def try_move(self,new_pos):
        if self.field.can_move(self.pos,new_pos):
            self.field.move(self.pos,new_pos)
            self.pos = new_pos
            return True
        return False

    def trans(self,diff):
        if self.try_move(trans4(self.pos,diff)):
            self.zero = trans(self.zero,diff)
            return True
        return False

    def down(self):
        return self.trans((0,-1))
    def right(self):
        return self.trans((1,0))
    def left(self):
        return self.trans((-1,0))

    def rotright(self):
        if self.try_move(trans4(positions[self.typ][(self.rot+1)%4],self.zero)):
            self.rot+=1
            return True
        return False
    def rotleft(self):
        if self.try_move(trans4(positions[self.typ][(self.rot-1)%4],self.zero)):
            self.rot-=1
            return True
        return False

class Field:
    def __init__(self):
        self.field = [[Tile.E for j in range(22)] for i in range(10)]
        self.bag = self.generate_bag()
        self.mino = None
        self.peek_field = None

    def get(self,x,y):
        return self.field[x][y]

    @staticmethod
    def generate_bag():
        q = list('IJLOSTZ')
        shuffle(q)
        return q

    def spawn(self):
        self.mino = Tetromino(self.bag.pop(),self)
        if not self.bag:
            self.bag = self.generate_bag()
        self.peek_field = PeekField(self.bag[-1])

        return self.mino

    def put(self,mino):
        tile = Tile[mino.typ]
        for (x,y) in mino.pos:
            self.field[x][y] = tile

    def can_move(self,frm,to):
        tiles = [self.field[x][y] for (x,y) in frm]
        for (x,y) in frm:
            self.field[x][y] = Tile.E
        can = all(0<=x<10 and 0<=y<22 and self.field[x][y]==Tile.E for (x,y) in to)
        for (x,y),t in zip(frm,tiles):
            self.field[x][y] = t
        return can

    def move(self,frm,to):
        tiles = [self.field[x][y] for (x,y) in frm]
        for (x,y) in frm:
            self.field[x][y] = Tile.E
        for (x,y),t in zip(to,tiles):
            self.field[x][y] = t

    def need_clear(self):
        return any(all(self.field[x][y]!=Tile.E for x in range(10)) for y in range(20))

    def clear(self):
        y = 0
        while y<20:
            if all(self.field[x][y]!=Tile.E for x in range(10)):
                for x in range(10):
                    self.field[x][y] = Tile.E
                self.move([(i,j) for i in range(10) for j in range(y+1,22)],
                          [(i,j) for i in range(10) for j in range(y,21)])
                self.mino.pos = trans4(self.mino.pos, (0,-1))
                self.mino.zero = trans(self.mino.zero,(0,-1))
            else:
                y+=1
class PeekField(Field):
    def __init__(self,typ):
        self.field = [[Tile.E for j in range(4)] for i in range(4)]
        Tetromino(typ,self,(0,0))
