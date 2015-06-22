# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance, nearestPoint
from game import Directions, Agent
import random
import util
import distanceCalculator
import math
class SeekerClassifier:
    def __init__(self):
        util.raiseNotDefined()


class Corridors:
    def __init__(self, layout):
        self.layout = layout

    def compute_corridors(self):
        # print (layout.walls.data)
        layout_data = self.layout.walls.data
        explored = []
        for h in range(layout.height):
            for w in range(layout.width):
                if layout_data[h][w]:
                    explored.append((h,w))
                else:
                    legal_actions()
        return

class CompetitionAgent(Agent):
    """
    A base class for competition agents.  The convenience methods herein handle
    some of the complications of the game.

    Recommended Usage:  Subclass CompetitionAgent and override getAction.
    """

    #############################
    # Methods to store key info #
    #############################

    def __init__( self, index=0, timeForComputing = .1 ):
      """
      Lists several variables you can query:
      self.index = index for this agent
      self.distancer = distance calculator (contest code provides this)
      self.timeForComputing = an amount of time to give each turn for computing maze distances
          (part of the provided distance calculator)
      """
    # Agent index for querying state, N.B. pacman is always agent 0
    self.index = index

    # Maze distance calculator
    self.distancer = None

    # Time to spend each turn on computing maze distances
    self.timeForComputing = timeForComputing

    # Access to the graphics
    self.display = None

    # useful function to find functions you've defined elsewhere..
    # self.usefulFunction = util.lookup(usefulFn, globals())
    self.getDistance = self.distancer.getDistance
    self.next_food = None
    self.food_list = []

    def registerInitialState(self, game_state):
        """
        This method handles the initial setup of the
        agent to populate useful fields.

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)
        """
        self.distancer = distanceCalculator.Distancer(game_state.data.layout)
        self.distancer.getMazeDistances()
        #get_tunnels(game_state.data.layout)
        food = game_state.getFood()
        self.food_list = []
        for h in range(food.height):
            for w in range(food.width):
                if food[w][h]:
                    self.food_list.append((w, h))
        foods = [(self.distancer.getDistance(game_state.getPacmanPosition(), food),food) for food in self.food_list]
        close_foods = [f[1] for f in foods if f[0] == min(food[0] for food in foods)]
        self.next_food = close_foods[random.choice(range(close_foods.__len__()))]
        # comment this out to forgo maze distance computation and use manhattan distances
        # self.distancer.getMazeDistances()

        import __main__
        if '_display' in dir(__main__):
            self.display = __main__._display

    #################
    # Action Choice #
    #################

    def getAction(self, game_state):
        """
        Override this method to make a good agent. It should return a legal action within
        the time limit (otherwise a random legal action will be chosen for you).
        """
        util.raiseNotDefined()

    #######################
    # Convenience Methods #
    #######################

    def getFood(self, game_state):
        """
        Returns the food you're meant to eat. This is in the form of a matrix
        where m[x][y]=true if there is food you can eat (based on your team) in that square.
        """
        return game_state.getFood()

    def getCapsules(self, game_state):
        return game_state.getCapsules()

    def getScore(self, game_state):
        """
        Returns how much you are beating the other team by in the form of a number
        that is the difference between your score and the opponents score.  This number
        is negative if you're losing.
        """
        return game_state.getScore()

    def getMazeDistance(self, pos1, pos2):
        """
        Returns the distance between two points; These are calculated using the provided
        distancer object.

        If distancer.getMazeDistances() has been called, then maze distances are available.
        Otherwise, this just returns Manhattan distance.
        """
        d = self.distancer.getDistance(pos1, pos2)
        return d


class BaselineAgent(CompetitionAgent):
    """
      This is a baseline reflex agent to see if you can do better.
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
    """

    def getAction(self, game_state):
        """
        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.getLegalActions()

        # try each of the actions and pick the best one
        scores=[]
        for action in legal_moves:
            successor_game_state = game_state.generatePacmanSuccessor(action)
            scores.append(self.evaluationFunction(successor_game_state))

        # get the best action
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legal_moves[chosen_index]

    def evaluationFunction(self, state):
        # Useful information you can extract from a GameState (pacman.py)
        return state.getScore()
  
   
class TimeoutAgent( Agent ):
    """
    A random agent that takes too much time. Taking
    too much time results in penalties and random moves.
    """
    def __init__(self, index=0):
        self.index = index
    
    def getAction(self, state):
        import random
        import time
        time.sleep(2.0)
        return random.choice(state.getLegalActions(self.index))

class MyPacmanAgent(CompetitionAgent):
    """
    This is going to be your brilliant competition agent.
    You might want to copy code from BaselineAgent (above) and/or any previos assignment.
    """

    # The following functions have been declared for you,
    # but they don't do anything yet (getAction), or work very poorly (evaluationFunction)

    def getAction(self, game_state):
        """
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous projects, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}.
        """
        evaluation_scores = [(action, self.evaluationFunction2(game_state,game_state.generatePacmanSuccessor(action), action)) for action in game_state.getLegalActions(0)]
        best_actions = [action[0] for action in evaluation_scores if action[1] == max([score[1] for score in evaluation_scores])]
        return best_actions[random.choice(range(best_actions.__len__()))]

    def evaluationFunction(self, state):
        """
        A very poor evsaluation function. You can do better!
        """
        pacman_pos = state.getPacmanPosition()
        food = state.getFood()
        ghost_states = state.getGhostStates()
        ghost_distance = [self.getDistance(pacman_pos, ghost.configuration.pos)for ghost in ghost_states if ghost.scaredTimer == 0]
        scared_distance = [self.getDistance(pacman_pos, ghost.configuration.pos)for ghost in ghost_states if ghost.scaredTimer != 0]
        capsule_distance = [self.getDistance(pacman_pos, capsule)for capsule in state.getCapsules()]
        food_list = []

        for h in range(food.height):
            for w in range(food.width):
                if food[w][h]:
                    food_list.append((w,h))
        food_distance = [self.getDistance(pacman_pos, food)for food in food_list]
        if state.hasFood(pacman_pos[0], pacman_pos[1]):
            food_distance.append(0)
        if not ghost_distance:
            ghost_distance.append(float("inf"))

        if min(ghost_distance) < 2:
            return -float("inf")
        if not food_distance:
            return float("inf")
        return state.getScore() - min(food_distance)

    def evaluationFunction2(self, prevstate, state,action):
        """
        A very poor evsaluation function. You can do better!
        """
        currentgamestate = state
        pacman_pos = currentgamestate.getPacmanPosition()
        food = currentgamestate.getFood()
        ghost_states = currentgamestate.getGhostStates()
        ghost_distance = [self.distancer.getDistance(pacman_pos, ghost.configuration.pos)for ghost in ghost_states if ghost.scaredTimer == 0]
        scared_distance = [self.distancer.getDistance(pacman_pos, ghost.configuration.pos)for ghost in ghost_states if ghost.scaredTimer != 0]
        capsule_distance = [self.distancer.getDistance(pacman_pos, capsule)for capsule in currentgamestate.getCapsules()]
        food_list = []

        for h in range(food.height):
            for w in range(food.width):
                if food[w][h]:
                    food_list.append((w, h))
        food_distance = [self.distancer.getDistance(pacman_pos, food)for food in food_list]
        if prevstate.getScore() < currentgamestate.getScore():
            food_distance.append(0)
        if not ghost_distance:
            ghost_distance.append(float("inf"))
        if not capsule_distance or currentgamestate.getCapsules().__len__() < prevstate.getCapsules().__len__():
            capsule_distance.append(0)
            scared_distance.append(0)
        # print ((scared_distance,not scared_distance))
        # if scared_distance:
        #   capsule_distance = [-capsule for capsule in capsule_distance]
        if not scared_distance or scared_distance.__len__() < [self.distancer.getDistance(prevstate.getPacmanPosition(), ghost.configuration.pos) for ghost in prevstate.getGhostStates() if ghost.scaredTimer != 0].__len__():
            scared_distance.append(0)
        if min(ghost_distance) < 2:
            return -float("inf")
        if not food_distance:
            return float("inf")
        #print ((prevstate.getPacmanPosition(), - min(food_distance)  -10* min(capsule_distance) - 20*min(scared_distance),action,(min(food_distance),min(capsule_distance),min(scared_distance),state.getScore())))
        return - min(food_distance)  - 10* min(capsule_distance) - 20*min(scared_distance) + state.getScore()


#MyPacmanAgent=BaselineAgent
Pacman = MyPacmanAgent