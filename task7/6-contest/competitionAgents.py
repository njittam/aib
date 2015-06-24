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
    def __init__(self, walls, distancer):
        self.walls = walls
        self.explored = []
        self.corridors = []
        self.distancer = distancer
        self.getDistance = self.distancer.getDistance

    def time_to_get_out_corridor(self, pacman, ghost):
        "returns true if pacman can escape from a ghost through an entrance or exit"
        temp = [(entrance, entry) for (entrance, corridors, entry) in self.corridors if pacman in corridors]
        if not temp:
            return (True, (-2, -2)), (True, (-2, -2)), False
        (entrance, entry) = temp[0]
        if entrance == (-1, -1):
            print("Theo doesn't believe that this code isn't called")
            return (False, entrance), (False, entry), True
        elif entry == (-1, -1):
            return (self.getDistance(entrance, pacman) < self.getDistance(entrance, ghost), entrance), (False, entry), True
        else:
            #print ((self.getDistance(entrance, pacman), self.getDistance(entrance, ghost), entrance, self.getDistance(entry, pacman),self.getDistance(entry, ghost)))
            return (self.getDistance(entrance, pacman) < self.getDistance(entrance, ghost), entrance), (self.getDistance(entry, pacman) < self.getDistance(entry, ghost) , entry), True

    def can_can_pacman_enter_coridor(self, pacman, ghost):
        entrys_and_entrances = flatten([])

    def get_things(self):
        returnlist = []
        walls_data = self.walls.data
        for x in range(self.walls.width):
            for y in range(self.walls.height):
                if not walls_data[x][y] and self.is_corridor((x, y)) and (x, y) not in self.explored:
                    entrance, lasttile = self.goto_entrance((x, y))
                    coridorlist, exit = self.goto_exit(entrance, lasttile)
                    for each in coridorlist:
                        self.explored.append(each)
                    returnlist.append((entrance, coridorlist, exit))
        self.corridors = returnlist
        return returnlist

    def get_neighbours(self, tile):
        (x, y) = tile
        neighbors = []
        if not self.walls.data[x][y + 1]:
            neighbors.append((x, y + 1))
        if not self.walls.data[x + 1][y]:
            neighbors.append((x + 1, y))
        if not self.walls.data[x][y - 1]:
            neighbors.append((x, y - 1))
        if not self.walls.data[x - 1][y]:
            neighbors.append((x - 1, y))
        return neighbors

    def is_corridor(self, tile):
        return self.get_neighbours(tile).__len__() < 3

    def goto_entrance(self, tile):
        visited = [tile]
        end_visited = []
        neighbors = self.get_neighbours(tile)
        if not neighbors:
            return (-1, -1), tile
        last_tile = tile
        tile = neighbors[0]
        while self.is_corridor(tile):
            visited.append(tile)
            neighbors = [n for n in self.get_neighbours(tile) if n not in visited]
            if not neighbors:
                if tile not in end_visited:
                    visited = [tile]
                    last_tile = tile
                    end_visited.append(tile)
                else:
                    return (-1, -1), tile
            else:
                last_tile = tile
                tile = neighbors[0]
        return tile, last_tile

    def goto_exit(self, entrance, tile):
        visited = [entrance, tile]
        corridor_list = [tile]
        neighbors = [n for n in self.get_neighbours(tile) if n not in visited]
        if not neighbors:
            return corridor_list, (-1, -1)
        tile = neighbors[0]
        visited.remove(entrance)
        while self.is_corridor(tile):
            visited.append(tile)
            corridor_list.append(tile)
            neighbors = [n for n in self.get_neighbours(tile) if n not in visited]
            if not neighbors:
                return corridor_list, (-1, -1)
            else:
                tile = neighbors[0]
        return corridor_list, tile



class CompetitionAgent(Agent):
    """
    A base class for competition agents.  The convenience methods herein handle
    some of the complications of the game.

    Recommended Usage:  Subclass CompetitionAgent and override getAction.
    """

    #############################
    # Methods to store key info #
    #############################

    def __init__(self, index=0, timeForComputing=.1):
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
        self.corridors = None

        # Time to spend each turn on computing maze distances
        self.timeForComputing = timeForComputing

        # Access to the graphics
        self.display = None

        # useful function to find functions you've defined elsewhere..
        # self.usefulFunction = util.lookup(usefulFn, globals())
        self.get_distance = None

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
        self.corridors = Corridors(game_state.data.layout.walls, self.distancer)
        self.corridors.get_things()
        #for c in self.corridors.corridors:
        #    print(c)
        self.get_distance = self.distancer.getDistance
        # get_tunnels(game_state.data.layout)
        food = game_state.getFood()
        self.food_list = []
        for h in range(food.height):
            for w in range(food.width):
                if food[w][h]:
                    self.food_list.append((w, h))
        foods = [(self.distancer.getDistance(game_state.getPacmanPosition(), food), food) for food in self.food_list]
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
        scores = []
        for action in legal_moves:
            successor_game_state = game_state.generatePacmanSuccessor(action)
            scores.append(self.evaluationFunction(successor_game_state))

        # get the best action
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"
        return legal_moves[chosen_index]

    def evaluationFunction(self, state):
        # Useful information you can extract from a GameState (pacman.py)
        return state.getScore()


class TimeoutAgent(Agent):
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
        evaluation_scores = [
            (action, self.evaluationFunction(game_state, game_state.generatePacmanSuccessor(action), action)) for
            action in game_state.getLegalActions(0)]
        best_actions = [action[0] for action in evaluation_scores if
                        action[1] == max([score[1] for score in evaluation_scores])]
        return best_actions[random.choice(range(best_actions.__len__()))]

    def evaluationFunction(self, prevstate, state, action):
        """
        A very poor evsaluation function. You can do better!
        """
        stop_value = 0
        if action == Directions.STOP: # give the Stop Action a lower evaluation function
            stop_value = 20
        currentgamestate = state
        pacman_pos = currentgamestate.getPacmanPosition()
        food = currentgamestate.getFood()
        ghost_states = currentgamestate.getGhostStates()
        ghost_distance = [self.distancer.getDistance(pacman_pos, ghost.configuration.pos) for ghost in ghost_states if
                          ghost.scaredTimer == 0]
        scared_distance = [self.distancer.getDistance(pacman_pos, ghost.configuration.pos) for ghost in ghost_states if
                           ghost.scaredTimer != 0]
        capsule_distance = [self.distancer.getDistance(pacman_pos, capsule) for capsule in
                            currentgamestate.getCapsules()]
        ghost_escapes = [self.corridors.time_to_get_out_corridor(pacman_pos, ghost.configuration.pos) for ghost in state.getGhostStates() if ghost.scaredTimer == 0]
        escape_through_exit_from_ghosts = [(entrance[0], entry[0]) for (entrance, entry, in_corridor) in ghost_escapes if in_corridor]
        food_list = []

        for h in range(food.height):
            for w in range(food.width):
                if food[w][h]:
                    food_list.append((w, h))
        food_distance = [self.distancer.getDistance(pacman_pos, food) for food in food_list]
        if prevstate.getScore() < currentgamestate.getScore():
            food_distance.append(0)
        if not ghost_distance:
            ghost_distance.append(float("inf"))
        if not capsule_distance or currentgamestate.getCapsules().__len__() < prevstate.getCapsules().__len__():
            capsule_distance.append(0)
            scared_distance.append(0)
        if not scared_distance or scared_distance.__len__() < [
            self.distancer.getDistance(prevstate.getPacmanPosition(), ghost.configuration.pos) for ghost in
            prevstate.getGhostStates() if ghost.scaredTimer != 0].__len__():
            scared_distance.append(0)
        if min(ghost_distance) < 2:
            return -10001
        if not food_distance:
            return float("inf")
        if prevstate.getCapsules().__len__() > state.getCapsules().__len__():
            if [self.distancer.getDistance(pacman_pos, ghost.configuration.pos) for ghost in prevstate.getGhostStates() if
                           ghost.scaredTimer != 0]:
                return -1000 - stop_value
            else:
                return float("inf")
        if escape_through_exit_from_ghosts:
            a = [entrance for (entrance, entry) in escape_through_exit_from_ghosts if not entrance] and True
            b = [entry for (entrance, entry) in escape_through_exit_from_ghosts if not entry] and True
            if a and b and not self.corridors.is_corridor(prevstate.getPacmanPosition()):
                return -10000 - stop_value
            if not a and not b:
                return - min(food_distance) - 10 * min(capsule_distance) - 20 * min(scared_distance) + state.getScore() - stop_value + get_out_of_corridor_value
                return - min(food_distance) - 10 * min(capsule_distance) - 20 * min(scared_distance) + state.getScore() - 2*self.get_distance(entrance, pacman_pos) - stop_value+ get_out_of_corridor_value
        return - min(food_distance) - 10 * min(capsule_distance) - 20 * min(scared_distance) + state.getScore() - stop_value + get_out_of_corridor_value


# MyPacmanAgent=BaselineAgent
Pacman = MyPacmanAgent