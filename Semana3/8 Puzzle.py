import math
import copy

class Node:
    def __init__(self, state, g=0, h=0):
        self.state = state
        self.parent = None
        self.action = None
        self.g = g  # Costo acumulado
        self.h = h  # Heurística

    def print(self):
        if len(self.state) == 9:
            print(" ".join(self.state[0:3]))
            print(" ".join(self.state[3:6]))
            print(" ".join(self.state[6:9]))
        else:
            print(self.state)
        print("")

    @classmethod
    def backwardList(cls, node):
        answerList = [node]
        while answerList[0].parent != None:
            answerList.insert(0, answerList[0].parent)
        return answerList

class Problem:
    def __init__(self, initialState, goalState):
        self.initialNode = Node(initialState)
        self.goalState = goalState
        self.size = int(math.sqrt(len(initialState)))

    def isGoal(self, node):
        if node.state == self.goalState:
            return True
        else:
            return False

    def actions(self, node):
        moves = []
        empty = node.state.index('0')
        [row, col] = [empty // self.size, empty % self.size]
        if row < self.size - 1:
            moves.append([1, 0])
        if row > 0:
            moves.append([-1, 0])
        if col < self.size - 1:
            moves.append([0, 1])
        if col > 0:
            moves.append([0, -1])
        return moves

    def transition(self, node, action):
        old = node.state.index('0')
        new = old + self.size * action[0] + action[1]
        transitionedNode = copy.deepcopy(node)
        lst = list(transitionedNode.state)
        lst[old], lst[new] = lst[new], lst[old]
        transitionedNode.state = ''.join(lst)
        return transitionedNode

    def expand(self, node):
        newNodes = []
        for action in self.actions(node):
            newNode = self.transition(node, action)
            newNode.parent = node
            newNode.action = action
            newNode.g = node.g + 1  # Incrementa el costo acumulado
            newNode.h = misplaced_tiles_heuristic(newNode.state, self.goalState)  # Calcula la heurística
            newNodes.append(newNode)
        return newNodes

def BFS(problem):
    frontier = []
    reached = set()
    frontier.append(problem.initialNode)
    reached.add(problem.initialNode.state)
    while len(frontier) != 0:
        currentNode = frontier.pop(0)
        if problem.isGoal(currentNode):
            print("There are {0} nodes in the frontier".format(len(frontier)))
            print("There are {0} reached nodes".format(len(reached)))
            return currentNode
        for child in problem.expand(currentNode):
            if child.state not in reached:
                frontier.append(child)
                reached.add(child.state)
    return None

def astar(problem):
    frontier = []
    reached = set()
    frontier.append(problem.initialNode)
    reached.add(problem.initialNode.state)
    while len(frontier) != 0:
        frontier.sort(key=lambda x: x.g + x.h)  # Ordena la frontera por el costo total
        currentNode = frontier.pop(0)
        if problem.isGoal(currentNode):
            print("There are {0} nodes in the frontier".format(len(frontier)))
            print("There are {0} reached nodes".format(len(reached)))
            return currentNode
        for child in problem.expand(currentNode):
            if child.state not in reached:
                frontier.append(child)
                reached.add(child.state)
    return None

# Heurística admisible: Conteo de fichas mal colocadas
def misplaced_tiles_heuristic(state, goal_state):
    misplaced = 0
    for i in range(len(state)):
        if state[i] != goal_state[i] and state[i] != '0':
            misplaced += 1
    return misplaced

# Heurística no admisible: Distancia Manhattan
def manhattan_distance_heuristic(state, goal_state):
    size = int(math.sqrt(len(state)))
    total_distance = 0
    for i in range(size):
        for j in range(size):
            tile = state[i * size + j]
            if tile != '0':
                goal_pos = goal_state.index(tile)
                goal_row = goal_pos // size
                goal_col = goal_pos % size
                total_distance += abs(i - goal_row) + abs(j - goal_col)
    return total_distance

# Test cases
initialState = "143706582"
goalState = "123456780"
print("BFS:")
answer_bfs = BFS(Problem(initialState, goalState))
if answer_bfs is not None:
    path_bfs = Node.backwardList(answer_bfs)
    print("These are the {0} steps to reach the goal node:".format(len(path_bfs) - 1))
    for n in path_bfs:
        n.print()
else:
    print("The BFS search has failed!")
    print("The initial state was:")
    Node(initialState).print()

print("\nA* with Misplaced Tiles Heuristic:")
answer_astar_misplaced = astar(Problem(initialState, goalState))
if answer_astar_misplaced is not None:
    path_astar_misplaced = Node.backwardList(answer_astar_misplaced)
    print("These are the {0} steps to reach the goal node:".format(len(path_astar_misplaced) - 1))
    for n in path_astar_misplaced:
        n.print()
else:
    print("The A* search with misplaced tiles heuristic has failed!")
    print("The initial state was:")
    Node(initialState).print()

print("\nA* with Manhattan Distance Heuristic:")
answer_astar_manhattan = astar(Problem(initialState, goalState))
if answer_astar_manhattan is not None:
    path_astar_manhattan = Node.backwardList(answer_astar_manhattan)
    print("These are the {0} steps to reach the goal node:".format(len(path_astar_manhattan) - 1))
    for n in path_astar_manhattan:
        n.print()
else:
    print("The A* search with Manhattan distance heuristic has failed!")
    print("The initial state was:")
    Node(initialState).print()