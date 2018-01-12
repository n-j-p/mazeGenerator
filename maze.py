def score():
    import random
    return random.gauss(0,1)

def argmin(alist):
    return min(enumerate(alist), key=lambda x: x[1])[0]    

class Maze():
    def __init__(self, X=6, Y=4, z=0):
        self.X = X
        self.Y = Y
        self.z = z
        self.generate()
        
    def generate(self): # Generate a maze using breadth first search
        possible = []
        actual = {}
        current = (0,0)
        for add in ((0,1), (1,0), (0,-1), (-1,0)):
            nxt = (current[0] + add[0], current[1] + add[1])
            if nxt[0] < 0 or nxt[0] >= self.X or nxt[1] < 0 or nxt[1] >= self.Y:
                continue
            possible.append((current, nxt, score()))
        barred = [current]
        while len(possible) > 0:  
            ix = argmin([x[2] for x in possible]) # index of next direction
            current = possible[ix][1]
            try:
                actual[possible[ix][0]].append(current)
            except KeyError:
                actual[possible[ix][0]] = [current]
            try:
                actual[current].append(possible[ix][0])
            except KeyError:
                actual[current] = [possible[ix][0]]
            chg = [current[0]-possible[ix][0][0], current[1]-possible[ix][0][1]]
            ahead = (current[0]+chg[0], current[1]+chg[1])
            
            rmix = []
            for i,x in enumerate(possible):
                if x[1] == current or x[0] == current:
                    rmix.append(i)
            for i in rmix[::-1]:
                possible.pop(i)
            barred.append(current)
            for add in ((0,1), (1,0), (0,-1), (-1,0)):
                nxt = (current[0] + add[0], current[1] + add[1])
                if nxt[0] < 0 or nxt[0] >= self.X or nxt[1] < 0 or nxt[1] >= self.Y or nxt in barred:
                    continue
                if nxt == ahead:
                    possible.append((current, nxt, score()+self.z))
                else:
                    possible.append((current, nxt, score()))
        
        self.dpaths = actual
        self.draw()
    
    def draw(self):
        '''Encodes the dictionary of exits as a list of rows by
        0: No walls
        1: Wall only to the West
        2: Wall only to the South
        3: Wall on South and West sides
        Assuming the bottom left and top right positions are
        entries and exits, for example the 2x3 maze:
        ____
        | __
        |   |
        __|_|
        
        is encoded as
        [[2,2,0],[1,2,0],[1,0,1],[2,3,1]]

        
         2 2 0
        -----
        |1 2 0
        |  -|
        |1 0|1
        | | |
         2|3|1        
        -----
        '''
        X = self.X # We need an extra row and column to represent
        Y = self.Y # the outer walls properly
        repr = [[2,]*X + [0,]] # Represents the top row "above" the maze.
        for i in range(Y):
            row = []
            cury = Y-1-i
            for curx in range(X):
                c = 0 # holds the wall encoding
                if (curx-1, cury) not in self.dpaths[(curx, cury)]:
                    c += 1
                if (curx, cury-1) not in self.dpaths[(curx, cury)]:
                    c += 2
                row.append(c)
            if i == 0:
                row.append(0) # Easterly exit at (X,Y)
            else:
                row.append(1) # Easterly wall otherwise
            repr.append(row)
        repr[-1][0] -= 1 # westerly entrance at (0,0)
        self.repr = repr
    def __repr__(self):
        try:
            repr = self.repr
        except AttributeError:
            self.draw()
        s = ''
        for row in repr:
            for pos in row:
                if pos == 1:
                    s += '| '
                elif pos == 2:
                    s += '__'
                elif pos == 3:
                    s += '|_'
                else:
                    s += '  '
            s += '\n'
                   
        return s
            
        
        
        