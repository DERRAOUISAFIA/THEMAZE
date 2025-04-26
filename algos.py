# ======= algos.py corrigé =======

from collections import deque
import heapq

# ============================
# Fonction de recherche BFS
# ============================
def bfs(maze_map, start, goal, murs_dynamiques=None):
    if murs_dynamiques is None:
        murs_dynamiques = set()

    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            return reconstruct_path(parent, start, goal)

        for neighbor in get_neighbors(current, maze_map, murs_dynamiques):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return None


def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path


# ============================
# Fonction de recherche A*
# ============================
def a_star_path(start, goal, maze_map, murs_dynamiques=None):
    if murs_dynamiques is None:
        murs_dynamiques = set()

    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0, start))
    
    g_costs = {start: 0}
    f_costs = {start: heuristic(start, goal)}
    came_from = {}

    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_list.add(current)

        for neighbor in get_neighbors(current, maze_map, murs_dynamiques):
            if neighbor in closed_list:
                continue

            tentative_g_cost = g_costs[current] + 1

            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                came_from[neighbor] = current
                g_costs[neighbor] = tentative_g_cost
                f_costs[neighbor] = g_costs[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_costs[neighbor], neighbor))

    return None


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ============================
# Fonction pour obtenir les voisins
# ============================
def get_neighbors(cell, maze_map, murs_dynamiques=None):
    if murs_dynamiques is None:
        murs_dynamiques = set()

    x, y = cell
    neighbors = []
    directions = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1)
    }

    if cell not in maze_map:
        return neighbors

    for dir, (dx, dy) in directions.items():
        if maze_map[cell].get(dir, 0) == 1:
            neighbor = (x + dx, y + dy)
            if neighbor in maze_map and neighbor not in murs_dynamiques:
                neighbors.append(neighbor)

    return neighbors
