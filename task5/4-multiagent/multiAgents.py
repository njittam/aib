# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newFood =  successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    foodlist = []
    for h in range(newFood.height):
        for w in range(newFood.width):
            if oldFood[w][h]:
                foodlist.append((w,h))
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghostDistance = [util.manhattanDistance(newPos, ghost.configuration.pos)for ghost in newGhostStates]
    foodDist = [util.manhattanDistance(newPos, food)for food in foodlist]
    "*** YOUR CODE HERE ***"
   # return min(ghostDistance)
    if successorGameState.isWin():
        return float("Inf")
    if successorGameState.isLose():
        return -float("Inf")
    if currentGameState.getScore() > successorGameState.getScore() and min(ghostDistance) > 5:
        return -min (foodDist)
    if min(ghostDistance) > 2:
        return -min (foodDist)
    if ghostDistance.__len__() != 0:
        return  -50+min(ghostDistance)
    else:
        return  -min (foodDist)

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent for one opponent (assignment 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    def max_value(state, currentDepth):
      currentDepth = currentDepth + 1
      if state.isWin() or state.isLose() or currentDepth == self.depth:
        return self.evaluationFunction(state)
      v = float('-Inf')
      for pAction in state.getLegalActions(0):
        v = max(v, min_value(state.generateSuccessor(0, pAction), currentDepth, 1))
      return v

    def min_value(state, currentDepth, ghostNum):
      if state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = float('Inf')
      for pAction in state.getLegalActions(ghostNum):
        if ghostNum == gameState.getNumAgents() - 1:
          v = min(v, max_value(state.generateSuccessor(ghostNum, pAction), currentDepth))
        else:
          v = min(v, min_value(state.generateSuccessor(ghostNum, pAction), currentDepth, ghostNum + 1))
      return v

    # Body of minimax_decision starts here: #
    pacmanActions = gameState.getLegalActions(0)
    maximum = float('-Inf')
    maxAction = ''
    for action in pacmanActions:
      currentDepth = 0
      currentMax = min_value(gameState.generateSuccessor(0, action), currentDepth, 1)
      if currentMax > maximum:
        maximum = currentMax
        maxAction = action
    return maxAction
  #  a= self.minimax(gameState, self.depth, True)
    current = gameState
    pacman= True
    for _ in range(self.depth):
        for child in self.childeren(current,pacman):
            if child[0].isWin():
                current = child[0]
        pacman = not pacman
    a = self.minimax(current, self.depth, True,Directions.STOP)
    return a[1]

  def getHeuristic(self, node):
      return node.getScore()

  def childeren(self, node, pacman):
    if pacman:
        for action in node.getLegalActions(0):
            yield (node.generateSuccessor(0, action), action)
    else:
        for action in node.getLegalActions(1):
            yield (node.generateSuccessor(1, action),action)

  def isterminal(self,gameState):
      return  gameState.isWin()

  def minimax(self, node, depth, maximizingPlayer, action):
    if depth == 0 or node is self.isterminal(node):
        return (self.getHeuristic(node),action)
    if maximizingPlayer:
        bestValue = -float("Inf")
        bestChild = (node,Directions.STOP)
        for child in self.childeren(node,maximizingPlayer):
            val = self.minimax(child[0], depth - 1, False, child[1])
            b_old = bestValue
            bestValue = max(bestValue, val[0])
            if b_old != bestValue:
                bestChild = child
        return (bestValue,bestChild[1])
    else:
        bestValue = float("inf")
        bestChild = (node,Directions.STOP)
        for child in self.childeren(node,maximizingPlayer  ):
            val = self.minimax(child[0], depth - 1, True,child[1])
            b_old = bestValue
            bestValue = min(bestValue, val[0])
            if b_old != bestValue:
                bestChild = child
        return (bestValue,bestChild[1])






class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning for one ghost (assignment 3)
  """
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

class MultiAlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning for several ghosts (Extra credit assignment B)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (not used in this course)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function for one ghost (extra credit assignment A).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest (not used in this course)
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

