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
    if currentGameState.getScore() > successorGameState.getScore() and min(ghostDistance) > 2:
        return -min (foodDist)
    if min(ghostDistance) > 2:
        return -min (foodDist)
    if ghostDistance.__len__() != 0:
        return  -100+min(ghostDistance)
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
    a = self.minimax(gameState, True, self.depth)
    return a[1]


  def isTerminal (self,gameState):
    return gameState.isWin() or gameState.isLose()


  def minimax(self, gameState , maxi, depth):
        if self.isTerminal(gameState) or depth == 0:
          return (self.evaluationFunction(gameState), Directions.STOP)

        childeren = util.PriorityQueue()
        if maxi:
          actions = gameState.getLegalActions(0)
          for a in actions:
            succsorGamestate = gameState.generateSuccessor(0,a)
            child = self.minimax(succsorGamestate, not maxi, depth - 1)
            childeren.push((child[0], a), -child[0])
        if not maxi:
          actionslists = []
          for i  in range(gameState.getNumAgents() - 1):
            actionsghost = []
            for a in gameState.getLegalActions(i + 1):
              actionsghost.append((a, i + 1))
            actionslists.append(actionsghost)
          actions = self.getSenarios(actionslists)
          for a in actions:
            succsorGamestate = self.getSuccessor(gameState, a)
            child = self.minimax(succsorGamestate, not maxi, depth)
            childeren.push((child[0], a), child[0])
        return childeren.pop()

  def getSenarios(self, actionslist):
    if actionslist == []:
      return [[]]
    else:
      list = self.getSenarios(actionslist[1:])
      list3 = []
      #i = 0
      for a in actionslist[0]:
        list2 = []
        for l in list:
          list2.append([])
          for item in l:
            list2[list2.__len__() - 1].append(item)
        for i in range(list2.__len__()):
          list2[i].append(a)
        for item in list2:
          list3.append(item)
      return list3

  def getSuccessor(self, gameState, actions):
    successor = gameState
    for action in actions:
      successor = successor.generateSuccessor(action[1],action[0])
      if successor.isLose() or successor.isWin():
        return successor
    return successor








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

