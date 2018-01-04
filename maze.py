def score():
    import random
    return random.gauss(0,1)

def generate(X=4,Y=5,z=0): # Generate a maze using breadth first search
    import numpy as np
    possible = []
    actual = {}
    current = (0,0)
    for add in ((0,1), (1,0), (0,-1), (-1,0)):
        nxt = (current[0] + add[0], current[1] + add[1])
        if nxt[0] < 0 or nxt[0] >= X or nxt[1] < 0 or nxt[1] >= Y:
            continue
        possible.append((current, nxt, score()))
    barred = [current]
    while len(possible) > 0:  
        ix = np.argmin([x[2] for x in possible]) # index of next direction
        current = possible[ix][1]
        try:
            actual[possible[ix][0]].append(current)
        except KeyError:
            actual[possible[ix][0]] = [current]
        try:
            actual[current].append(possible[ix][0])
        except KeyError:
            actual[current] = [possible[ix][0]]
        import pdb
        #pdb.set_trace()
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
            if nxt[0] < 0 or nxt[0] >= X or nxt[1] < 0 or nxt[1] >= Y or nxt in barred:
                continue
            if nxt == ahead:
                possible.append((current, nxt, score()+z))
            else:
                possible.append((current, nxt, score()))
        
    return actual

	
def draw(amaze):
    X = -1
    Y = -1
    for square in amaze.keys():
        X = max(X, square[0])
        Y = max(Y, square[1])
    X += 1
    Y += 1
    repr = [[2,]*X + [0,]]
    #print(X,Y)
    #print(X,Y)
    for i in range(Y):
        row = []
        cury = Y-1-i
        for curx in range(X):
            #print(curx, cury)
            #print(amaze[(curx, cury)])
            c = 0
            if (curx-1, cury) not in amaze[(curx, cury)]:
                c += 1
            if (curx, cury-1) not in amaze[(curx, cury)]:
                c += 2
            row.append(c)
        if i == 0:
            row.append(0)
        else:
            row.append(1)
        repr.append(row)
    repr[-1][0] -= 1
    #print(repr)
    for row in repr:
        s = ''
        for pos in row:
            if pos == 1:
                s += '| '
            elif pos == 2:
                s += '__'
            elif pos == 3:
                s += '|_'
            else:
                s += '  '
        print(s)
        
	
	
	


