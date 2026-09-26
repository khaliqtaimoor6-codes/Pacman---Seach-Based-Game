# searchAgents.py
# ---------------

from typing import List, Tuple, Any
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import pacman


class GoWestAgent(Agent):
    def getAction(self, state):
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP


class SearchAgent(Agent):
    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            self.searchFunction = lambda x: func(x, heuristic=heur)

        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state)
        self.actions = self.searchFunction(problem)
        if self.actions == None:
            self.actions = []
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(search.SearchProblem):
    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):  #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist)  #@UndefinedVariable
        return isGoal

    def getSuccessors(self, state):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)
        return successors

    def getCostOfActions(self, actions):
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost


class StayEastSearchAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)


class StayWestSearchAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)


def manhattanHeuristic(position, problem, info={}):
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclideanHeuristic(position, problem, info={}):
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


class CornersProblem(search.SearchProblem):
    """
    State: (pacman_position, visited_corners)
    visited_corners: tuple of 4 booleans, one per corner in self.corners order
    """

    def __init__(self, startingGameState: pacman.GameState):
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0  # DO NOT CHANGE

    def getStartState(self):
        startPos = self.startingPosition
        visited = tuple(startPos == c for c in self.corners)
        return (startPos, visited)

    def isGoalState(self, state: Any):
        _, visited = state
        return all(visited)

    def getSuccessors(self, state: Any):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            currentPosition, visited = state
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextPos = (nextx, nexty)
                newVisited = tuple(v or (nextPos == c) for v, c in zip(visited, self.corners))
                successors.append(((nextPos, newVisited), action, 1))
        self._expanded += 1  # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        if actions == None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state: Any, problem: CornersProblem):
    """
    Nearest-neighbor chain through unvisited corners using Manhattan distance.
    Admissible (never overestimates) and consistent (triangle inequality holds).
    """
    position, visited = state
    unvisited = [c for c, v in zip(problem.corners, visited) if not v]

    if not unvisited:
        return 0

    total = 0
    current = position
    while unvisited:
        distances = [abs(current[0] - c[0]) + abs(current[1] - c[1]) for c in unvisited]
        minDist = min(distances)
        closest = unvisited[distances.index(minDist)]
        total += minDist
        current = closest
        unvisited.remove(closest)

    return total


class AStarCornersAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem


class FoodSearchProblem:
    """
    State: (pacmanPosition, foodGrid)
    Goal: all food dots collected (foodGrid is empty)
    """

    def __init__(self, startingGameState: pacman.GameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        successors = []
        self._expanded += 1  # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


class AStarFoodSearchAgent(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem


def _manhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def _mstCost(points):
    """Prim's algorithm MST over points using Manhattan distances."""
    if len(points) <= 1:
        return 0

    points = list(points)
    inTree = {0}
    minEdge = [_manhattanDistance(points[0], points[i]) for i in range(len(points))]
    minEdge[0] = 0
    totalCost = 0

    for _ in range(len(points) - 1):
        bestCost = float('inf')
        bestIdx = -1
        for i in range(len(points)):
            if i not in inTree and minEdge[i] < bestCost:
                bestCost = minEdge[i]
                bestIdx = i
        inTree.add(bestIdx)
        totalCost += bestCost
        for i in range(len(points)):
            if i not in inTree:
                d = _manhattanDistance(points[bestIdx], points[i])
                if d < minEdge[i]:
                    minEdge[i] = d

    return totalCost


def _cachedMazeDistance(a, b, gameState, problem):
    """Maze distance with cache in problem.heuristicInfo to avoid repeated BFS."""
    if a == b:
        return 0
    key = (a, b) if a <= b else (b, a)
    cache = problem.heuristicInfo.setdefault('mazeCache', {})
    if key not in cache:
        cache[key] = mazeDistance(a, b, gameState)
    return cache[key]


def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    """
    Exact-distance MST lower bound heuristic. We compute a minimum spanning tree
    over the remaining food using shortest-path (maze) distances, then add the
    distance from the current position to the nearest food. Admissible and
    consistent (maze distances satisfy triangle inequality; MST is a lower
    bound on any tour visiting all food).
    Pairwise maze distances are cached in problem.heuristicInfo['mazeCache']
    so trickySearch runs in seconds instead of minutes.
    """
    position, foodGrid = state
    foodList = foodGrid.asList()

    if not foodList:
        return 0

    cacheKey = (position, frozenset(foodList))
    if cacheKey in problem.heuristicInfo:
        return problem.heuristicInfo[cacheKey]

    nearest = min(_cachedMazeDistance(position, food, problem.startingGameState, problem) for food in foodList)
    if len(foodList) == 1:
        result = nearest
    else:
        # Prim's MST over food using cached maze distances
        liveNodes = list(foodList)
        visited = {0}
        minEdge = [_cachedMazeDistance(liveNodes[0], liveNodes[i], problem.startingGameState, problem) for i in range(len(liveNodes))]
        minEdge[0] = 0
        mstCost = 0

        for _ in range(len(liveNodes) - 1):
            bestCost = float('inf')
            bestNode = -1
            for i in range(len(liveNodes)):
                if i not in visited and minEdge[i] < bestCost:
                    bestCost = minEdge[i]
                    bestNode = i
            if bestNode == -1:
                break
            visited.add(bestNode)
            mstCost += bestCost
            for i in range(len(liveNodes)):
                if i not in visited:
                    d = _cachedMazeDistance(liveNodes[bestNode], liveNodes[i], problem.startingGameState, problem)
                    if d < minEdge[i]:
                        minEdge[i] = d

        result = mstCost + nearest

    problem.heuristicInfo[cacheKey] = result
    return result


class ClosestDotSearchAgent(SearchAgent):
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while currentState.getFood().count() > 0:
            nextPathSegment = self.findPathToClosestDot(currentState)
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState: pacman.GameState):
        problem = AnyFoodSearchProblem(gameState)
        return search.bfs(problem)


class AnyFoodSearchProblem(PositionSearchProblem):
    def __init__(self, gameState):
        self.food = gameState.getFood()
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state: Tuple[int, int]):
        x, y = state
        return self.food[x][y]


def mazeDistance(point1: Tuple[int, int], point2: Tuple[int, int], gameState: pacman.GameState) -> int:
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    # Suspend CSV tracing: nested BFS inside heuristic must not pollute outer trace
    was_paused = search.pauseTracing()
    try:
        return len(search.bfs(prob))
    finally:
        search.resumeTracing(was_paused)