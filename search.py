# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state):
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def logExpansion(iteration, state, parent, action, successors, frontierBefore,
                  frontierAfter, explored, g=None, h=None, f=None):
    """
    Hook for evidence/CSV tracing (owned by Person 3's logging module).
    Does nothing by default so all algorithms run fine before the CSV logger
    exists. Person 3 can replace `search.logExpansion` with their own writer.
    """
    pass


# Successor expansion order required by the assignment: N -> E -> S -> W
from game import Directions
_EXPANSION_ORDER = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]

def _orderedSuccessors(problem, state):
    successors = problem.getSuccessors(state)
    def sortKey(successorTriple):
        action = successorTriple[1]
        return _EXPANSION_ORDER.index(action) if action in _EXPANSION_ORDER else len(_EXPANSION_ORDER)
    return sorted(successors, key=sortKey)


def depthFirstSearch(problem: SearchProblem):
    fringe = util.Stack()
    startState = problem.getStartState()
    fringe.push((startState, []))
    explored = set()
    iteration = 0

    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if state in explored:
            continue
        explored.add(state)
        iteration += 1

        if problem.isGoalState(state):
            return actions

        successors = _orderedSuccessors(problem, state)
        generated = []
        for nextState, action, stepCost in successors:
            if nextState not in explored:
                fringe.push((nextState, actions + [action]))
                generated.append(nextState)

        logExpansion(iteration, state, None, actions[-1] if actions else None,
                     generated, None, None, set(explored))

    return []


def breadthFirstSearch(problem: SearchProblem):
    fringe = util.Queue()
    startState = problem.getStartState()

    if problem.isGoalState(startState):
        return []

    fringe.push((startState, []))
    explored = {startState}
    iteration = 0

    while not fringe.isEmpty():
        state, actions = fringe.pop()
        iteration += 1

        if problem.isGoalState(state):
            return actions

        successors = _orderedSuccessors(problem, state)
        generated = []
        for nextState, action, stepCost in successors:
            if nextState not in explored:
                explored.add(nextState)
                fringe.push((nextState, actions + [action]))
                generated.append(nextState)

        logExpansion(iteration, state, None, actions[-1] if actions else None,
                     generated, None, None, set(explored))

    return []


def uniformCostSearch(problem: SearchProblem):
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    fringe.push((startState, [], 0), 0)
    bestGSoFar = {startState: 0}
    explored = set()
    iteration = 0

    while not fringe.isEmpty():
        state, actions, g = fringe.pop()
        if state in explored:
            continue
        explored.add(state)
        iteration += 1

        if problem.isGoalState(state):
            return actions

        successors = _orderedSuccessors(problem, state)
        generated = []
        for nextState, action, stepCost in successors:
            newG = g + stepCost
            if nextState not in explored and (nextState not in bestGSoFar or newG < bestGSoFar[nextState]):
                bestGSoFar[nextState] = newG
                fringe.update((nextState, actions + [action], newG), newG)
                generated.append(nextState)

        logExpansion(iteration, state, None, actions[-1] if actions else None,
                     generated, None, None, set(explored), g=g)

    return []


def nullHeuristic(state, problem=None):
    return 0


def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    startH = heuristic(startState, problem)
    fringe.push((startState, [], 0), startH)
    explored = set()
    iteration = 0

    while not fringe.isEmpty():
        state, actions, g = fringe.pop()
        if state in explored:
            continue
        explored.add(state)
        iteration += 1

        if problem.isGoalState(state):
            return actions

        successors = _orderedSuccessors(problem, state)
        generated = []
        for nextState, action, stepCost in successors:
            if nextState not in explored:
                h = heuristic(nextState, problem)
                fringe.push((nextState, actions + [action], g + stepCost), h)
                generated.append(nextState)

        logExpansion(iteration, state, None, actions[-1] if actions else None,
                     generated, None, None, set(explored), g=g,
                     h=heuristic(state, problem))

    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    startH = heuristic(startState, problem)
    fringe.push((startState, [], 0), startH)
    bestGSoFar = {startState: 0}
    explored = set()
    iteration = 0

    while not fringe.isEmpty():
        state, actions, g = fringe.pop()
        if state in explored:
            continue
        explored.add(state)
        iteration += 1

        if problem.isGoalState(state):
            return actions

        successors = _orderedSuccessors(problem, state)
        generated = []
        for nextState, action, stepCost in successors:
            newG = g + stepCost
            if nextState not in explored and (nextState not in bestGSoFar or newG < bestGSoFar[nextState]):
                bestGSoFar[nextState] = newG
                h = heuristic(nextState, problem)
                fringe.update((nextState, actions + [action], newG), newG + h)
                generated.append(nextState)

        logExpansion(iteration, state, None, actions[-1] if actions else None,
                     generated, None, None, set(explored), g=g,
                     h=heuristic(state, problem), f=g + heuristic(state, problem))

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch