# mazeGenerator

A breadth-first search maze generator

```
import maze
t = maze.Maze(15,10)
t
```

produces:
```
______________________________  
| | |_  | | ______|_  __  |_  
|   __|_  | __  __| |_  |     |  
| |   | __|_| ____  __| | | |_|  
| | |   __| |_|___    | | |___|  
| | |_|     | __  |_|   |_| | |  
|_|___| |_| | __|_  |_|   | | |  
|___  |_| | |_|_  __  __|_|_  |  
|_  __|   __| |_  |___|_  __  |  
| ______| |   | __    |   |   |  
________|___|_____|_|___|_|_|_|  
```

By default, the south-west corner - coordinates (0,0) contains the entrance, and the north-east corner (X,Y) contains the exit.

The wall encoding (from maze.draw()) is a list of length Y+1 containing a list of length X+1, with encoding:  
0: # (no walls)  
1: | (westerly wall)  
2: _ (southerly wall)  
3: |_ (both walls)  

Due to the nature of the search algorithm, all walls are connected (i.e. no wall islands). This could be changed after the fact by inserting other paths.
   