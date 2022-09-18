class Maze():
    '''maze.Maze(X, Y, turning_penalty=0)
    generates a random maze of size (X, Y). Variable turning_penalty penalises turns, so 
    a negative value of this results in a maze with more long passageways.
    
    generate() generates a new maze of size (X, Y), producing dpaths a dictionary of 
               paths (exits) for each position in the maze (x,y), 0<=x<X, 0<=y<Y.
    draw() converts the dpaths dictionary into a list of lists for rendering of the maze 
           see help(maze.draw) for details'''
    def __init__(self, X, Y, generate=True,
                 turning_penalty=0,
                 random_seed=None):
        self.X = X
        self.Y = Y
        self.turning_penalty = turning_penalty
        if generate:
            self.random_seed = random_seed
            self.generate()
            self.draw()
    
        
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
    def generate(self): # Generate a maze using breadth first search
        '''Generate a new maze'''
        import random
        if self.random_seed is not None:
            random.seed(self.random_seed)
        def _score(nxt, ahead, turning_penalty):
            '''The maze generator chooses the minimum score from all possible unexplored options.
            Currently, the score is a normal random variate with a possible penalty for turning.'''
            if nxt == ahead:
                return random.gauss(turning_penalty,1)
            else:
                return random.gauss(0,1)    

        def _argmin(alist):
            return min(enumerate(alist), key=lambda x: x[1])[0]    

        
        possible = []
        actual = {}
        current = (0,0)
        for add in ((0,1), (1,0), (0,-1), (-1,0)):
            nxt = (current[0] + add[0], current[1] + add[1])
            if nxt[0] < 0 or nxt[0] >= self.X or nxt[1] < 0 or nxt[1] >= self.Y:
                continue
            ahead = nxt
            possible.append((current, nxt,
                             _score(nxt, ahead, self.turning_penalty)))
        barred = [current]
        while len(possible) > 0:  
            ix = _argmin([x[2] for x in possible]) # index of next direction
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
                possible.append((current, nxt,
                                 _score(nxt, ahead, self.turning_penalty)))
        
        self.dpaths = actual
    
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

def from_grid( grid = [[2, 2, 2, 2, 2, 2, 2, 0],
                       [3, 0, 0, 0, 2, 3, 0, 0],
                       [3, 0, 3, 3, 1, 2, 1, 1],
                       [2, 2, 2, 2, 2, 2, 2, 1]]):
    dpaths = {}
    for i,row in enumerate(grid[::-1][:-1]):
        for j, val in enumerate(row[:-1]):
            dpaths[(j,i)] = []
            if val % 2 == 0:
                dpaths[(j,i)].append((j-1, i))
                try:
                    dpaths[(j-1,i)].append((j, i))
                except KeyError:
                    pass
            if val < 2:
                dpaths[(j, i)].append((j, i-1))
                try:
                    dpaths[(j, i-1)].append((j,i))
                except KeyError:
                    pass
        for x in dpaths.keys():
            print(x, dpaths[x])
        print()
    dpaths[(0,0)].remove((-1, 0))
    
    #return dpaths
    newmaze = Maze(X = len(grid[0]) - 1,
                   Y = len(grid) - 1,
                   generate = False)
    newmaze.dpaths = dpaths
    prevgrid = grid
    newmaze.draw()
    newgrid = newmaze.repr
    assert prevgrid == newgrid
    return newmaze
