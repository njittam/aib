# Theo Pijkeren -s4481046
# Mattijn Kreuzen -s4446402

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
    "a class that computes all the corridors in a layout"
    def __init__(self, walls, distancer):
        self.walls = walls
        self.explored = []
        self.corridors = []
        self.distancer = distancer
        self.getDistance = self.distancer.getDistance

    def time_to_get_out_corridor(self, pacman, ghost):
        """returns true if pacman can escape from a ghost through an entrance or exit.
            it returns 2 tuples with a boolean and a position of an entrance.
            if that boolean is true then can pacman escape trough the exit from the ghost.
            and it returns a boolean that is true if pacman is in a corridor.
        """
        temp = [(entrance, entry) for (entrance, corridors, entry) in self.corridors if pacman in corridors]  # a list with coridors where pacman is in.
        if not temp:  # if there are no items in temp then pacman isn't in a corridor
            return (True, (-2, -2)), (True, (-2, -2)), False
        (entrance, entry) = temp[0]
        if entrance == (-1, -1):    # there are no exits so pacman can't escape
            print("Theo doesn't believe that this code isn't called")
            return (False, entrance), (False, entry), True
        elif entry == (-1, -1):  # the corridor has a dead end so pacman can only escape on one exit
            return (self.getDistance(entrance, pacman) < self.getDistance(entrance, ghost), entrance), (False, entry), True
        else:  # a corridor has 2 ends so both need to be checked.
            return (self.getDistance(entrance, pacman) < self.getDistance(entrance, ghost), entrance), (self.getDistance(entry, pacman) < self.getDistance(entry, ghost) , entry), True

    def compute_corridors(self):
        # returns a list with all the corridors and there entrances
        # (entrance1, list_of_tiles, entrance2)
        return_list = []
        walls_data = self.walls.data
        for x in range(self.walls.width):
            for y in range(self.walls.height):
                if not walls_data[x][y] and self.is_corridor((x, y)) and (x, y) not in self.explored:
                    entrance, last_tile = self.goto_entrance((x, y))
                    corridor_list, entry = self.goto_exit(entrance, last_tile)
                    for each in corridor_list:
                        self.explored.append(each)
                    return_list.append((entrance, corridor_list, entry))
        self.corridors = return_list
        return return_list

    def get_neighbours(self, tile):
        """returns the neighbours of a tile"""
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
        """returns true if a tile has less then 3 neighbours"""
        return self.get_neighbours(tile).__len__() < 3

    def goto_entrance(self, tile):
        """go to the entrance and return the entrance and the last tile before the corridor"""
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
        """" move from the entrance to the end of the corridor and return the ending
         and a list of tiles in the corridor"""
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
        self.corridors.compute_corridors()
        self.get_distance = self.distancer.getDistance
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

    def evaluationFunction(self, prevstate, next_state, action):
        """
        Our evaluation function is based on the following things:
            if a Ghost is next to pacman move away from it.
            if there is a there are scared ghosts then dont pick up the capsules
            if pacman cant get out of a corridor then dont go into it.
            and of course try to get the most points!

        """
        stop_value = 0
        if action == Directions.STOP: # give the Stop Action a lower evaluation function
            stop_value = 20
        pacman_pos = next_state.getPacmanPosition()
        food = next_state.getFood()

        # create some usefull lists
        ghost_states = next_state.getGhostStates()
        ghost_distance = [self.distancer.getDistance(pacman_pos, ghost.configuration.pos) for ghost in ghost_states if
                          ghost.scaredTimer == 0]  # a list with all the distances between pacman and non-scared ghosts
        scared_distance = [self.distancer.getDistance(pacman_pos, ghost.configuration.pos) for ghost in ghost_states if
                           ghost.scaredTimer != 0]  # a list with all the distances between pacman and scared ghosts
        capsule_distance = [self.distancer.getDistance(pacman_pos, capsule) for capsule in
                            next_state.getCapsules()]  # a list with all the distances between pacman and the capsules
        ghost_escapes = [self.corridors.time_to_get_out_corridor(pacman_pos, ghost.configuration.pos) for ghost in next_state.getGhostStates() if ghost.scaredTimer == 0]  # a list with the output of time_to_get_out_corridor for all ghosts
        escape_through_exit_from_ghosts = [(entrance[0], entry[0]) for (entrance, entry, in_corridor) in ghost_escapes if in_corridor]  # a list with booleans if can escape through an exit from a ghost.  empty if pacman doesn't move into a corridor
        food_list = []  # a list with the positions of all foods.
        for h in range(food.height):
            for w in range(food.width):
                if food[w][h]:
                    food_list.append((w, h))
        food_distance = [self.distancer.getDistance(pacman_pos, food) for food in food_list] # a list with all the distances between pacman and the foods

        # some fixing in the lists.
        if prevstate.getScore() < next_state.getScore(): # if pacman is on food the minimum distance is 0
            food_distance.append(0)
        if not ghost_distance:  # if there are no ghosts then add a fictional ghost.
            ghost_distance.append(float("inf"))
        if not capsule_distance or next_state.getCapsules().__len__() < prevstate.getCapsules().__len__(): # if pacman is on a capsule then a distance is 0
            capsule_distance.append(0)
        if not scared_distance or scared_distance.__len__() < [
            self.distancer.getDistance(prevstate.getPacmanPosition(), ghost.configuration.pos) for ghost in
            prevstate.getGhostStates() if ghost.scaredTimer != 0].__len__():
            scared_distance.append(0) # if pacman is on a scared ghost then the distance is 0
        if min(ghost_distance) < 2: # a ghost is dangeriously close to pacman.
            return -10001 # pacman FLEE!!
        if not food_distance: # similar to isWin
            return float("inf")
        
        # the actual function
        if prevstate.getCapsules().__len__() > next_state.getCapsules().__len__():
            if [self.distancer.getDistance(pacman_pos, ghost.configuration.pos) for ghost in prevstate.getGhostStates() if
                           ghost.scaredTimer != 0]:
                return -1000 - stop_value
            else:
                return float("inf")
        if escape_through_exit_from_ghosts:
            entrance_not_safe = [entrance for (entrance, entry) in escape_through_exit_from_ghosts if not entrance] # empty if safe
            entry_not_safe = [entry for (entrance, entry) in escape_through_exit_from_ghosts if not entry] # empty if safe
            if entrance_not_safe and entry_not_safe and not self.corridors.is_corridor(prevstate.getPacmanPosition()):
                return -10000 - stop_value  # if it isn't saf don't go there pacman.
            if not entrance_not_safe and not entry_not_safe:
                return - min(food_distance) - 10 * min(capsule_distance) - 20 * min(scared_distance) + next_state.getScore() - stop_value # if it is safe then do this evaluationfunction
        return - min(food_distance) - 10 * min(capsule_distance) - 20 * min(scared_distance) + next_state.getScore() - stop_value # if it is safe then do this evaluationfunction


# MyPacmanAgent=BaselineAgent
Pacman = MyPacmanAgent