from pyamaze import maze, agent, COLOR
from collections import deque

class Maze:
    def __init__(self, rows, cols, loopPercent):
        self.m = maze(rows, cols)
        self.m.CreateMaze(loopPercent=loopPercent)
        self.rows = rows
        self.cols = cols
        self.maze_map = self.m.maze_map

    def DFS(self):
        start = (self.rows, self.cols)
        explored = [start]
        frontier = [start]
        dfsPath = {}

        while frontier:
            currCell = frontier.pop()
            if currCell == (1, 1):
                break
            for d in 'ESNW':
                if self.maze_map[currCell][d]:
                    if d == 'E':
                        childCell = (currCell[0], currCell[1] + 1)
                    elif d == 'W':
                        childCell = (currCell[0], currCell[1] - 1)
                    elif d == 'S':
                        childCell = (currCell[0] + 1, currCell[1])
                    elif d == 'N':
                        childCell = (currCell[0] - 1, currCell[1])
                    if childCell in explored:
                        continue
                    explored.append(childCell)
                    frontier.append(childCell)
                    dfsPath[childCell] = currCell

        fwdPath = {}
        cell = (1, 1)
        while cell != start:
            fwdPath[dfsPath[cell]] = cell
            cell = dfsPath[cell]

        return fwdPath

    def BFS(self):
        start = (self.rows, self.cols)
        goal = (1, 1)
        queue = deque([start])
        explored = set([start])
        parent = {}

        while queue:
            currCell = queue.popleft()
            if currCell == goal:
                break
            for d in 'ESNW':
                if self.maze_map[currCell][d]:
                    if d == 'E':
                        childCell = (currCell[0], currCell[1] + 1)
                    elif d == 'W':
                        childCell = (currCell[0], currCell[1] - 1)
                    elif d == 'S':
                        childCell = (currCell[0] + 1, currCell[1])
                    elif d == 'N':
                        childCell = (currCell[0] - 1, currCell[1])
                    if childCell not in explored:
                        explored.add(childCell)
                        queue.append(childCell)
                        parent[childCell] = currCell

        path = {}
        cell = goal
        while cell != start:
            path[parent[cell]] = cell
            cell = parent[cell]

        return path

    def display_solution(self):
        self.DFS()  # On pourrait tracer ce chemin aussi si tu veux le montrer
        path = self.BFS()
        a = agent(self.m, footprints=True, color=COLOR.red)
        self.m.tracePath({a: path})
        self.m.run()


if __name__ == '__main__':
    print("Choisissez un niveau de difficulté :")
    print("1. Facile")
    print("2. Moyen")
    print("3. Difficile")

    niveau = input("Entrez 1, 2 ou 3 : ")

    if niveau == '1':
        rows, cols, loop = 10, 10, 300
    elif niveau == '2':
        rows, cols, loop = 15, 12, 200
    elif niveau == '3':
        rows, cols, loop = 20, 15, 0
    else:
        print("Choix invalide. Niveau 'Facile' sélectionné par défaut.")
        rows, cols, loop = 10, 10, 200

    solver = Maze(rows, cols, loop)
    solver.display_solution()
