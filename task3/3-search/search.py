# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     # Bookkeeping for display purposes
     self._expanded += 1
     successors = []
     for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        # Add a successor state to the successor list if the action is legal
        x,y = currentPosition
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        hitsWall = self.walls[nextx][nexty]
        if not hitsWall and not ((action == Directions.NORTH and state[1] == Directions.SOUTH) or
                                   (action == Directions.EAST and state[1] == Directions.WEST) or
                                   (action == Directions.SOUTH and state[1] == Directions.NORTH) or
                                   (action == Directions.WEST and state[1] == Directions.EAST)):
            successors.append(((nextx, nexty), action, 42))  # TODO: Implement Cost PLEASE MARTIJN

     return successors

     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


def get_solution(current_node, explored):
    solution = []
    while (current_node[1] >= 0):
        solution.insert(0, current_node[0][1])
        current_node = explored[current_node[1]]
    return solution


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    frontier = [((problem.getStartState(),0,0), -1)]
    explored = []
  #  explored_size = 0
    while ( True ):
        if len(frontier) == 0:
            return -1
        current_node = frontier[-1]
        frontier.remove(frontier[len(frontier) -1])
        if problem.isGoalState(current_node[0][0]):
            return get_solution(current_node, explored)
        if current_node[0][0] not in [state[0][0] for state in explored]:
            for triple in problem.getSuccessors(current_node[0][0]):
                frontier.append((triple, len(explored)))
            explored.append(current_node)
          #  explored_size += 1


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first. [p 81]"""
    frontier = [((problem.getStartState(),0,0), -1)]
    explored = []
  #  explored_size = 0
    while ( True ):
        if len(frontier) == 0:
            return -1
        current_node = frontier[0]
        frontier.remove(frontier[0])
        if problem.isGoalState(current_node[0][0]):
            return get_solution(current_node, explored)
        if current_node[0][0] not in [state[0][0] for state in explored]:
            for triple in problem.getSuccessors(current_node[0][0]):
                frontier.append((triple, len(explored)))
            explored.append(current_node)

def getTotalCost(triple, current_node, explored):
    solution = []
    while (current_node[1] >= 0):
        solution.insert(0, current_node[0][2])
        current_node = explored[current_node[1]]
    return triple[2] + sum(solution)

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    frontier = util.PriorityQueue()
    frontier.push(((problem.getStartState(), "North", 0), -1), 0)
    explored = []
    cost = 0
    while ( True ):
        if frontier.isEmpty():
            return -1
        current_node = frontier.pop()
        if problem.isGoalState(current_node[0][0]):
            return get_solution(current_node, explored)
        if current_node[0][0] not in [state[0][0] for state in explored]:
            for triple in problem.getSuccessors(current_node[0][0]):
                frontier.push((triple, len(explored)), triple[2])
            explored.append(current_node)



def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    frontier = util.PriorityQueue()
    frontier.push(((problem.getStartState(), "North", 0), -1), 0)
    explored = []
    while ( True ):
        if frontier.isEmpty():
            return -1
        current_node = frontier.pop()
        successors = problem.getSuccessors(current_node[0][0])
        if problem.isGoalState(current_node[0][0]):
            return get_solution(current_node, explored)
        if current_node[0][0] not in [state[0][0] for state in explored]:
            for triple in problem.getSuccessors(current_node[0][0]):
                priority = getTotalCost(triple,current_node,explored) + heuristic(triple[0], problem)
                frontier.push((triple, len(explored)), priority)
            explored.append(current_node)

"Bonus assignment: Adjust the getSuccessors() method in CrossroadSearchAgent class"" \
""in searchAgents.py and test with:"
"python pacman.py -l bigMaze -z .5 -p CrossroadSearchAgent -a fn=astar,heuristic=manhattanHeuristic "
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
