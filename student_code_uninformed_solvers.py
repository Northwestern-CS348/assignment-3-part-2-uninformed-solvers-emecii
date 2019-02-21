from queue import Queue
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        state = self.currentState
        #print (type(state))
        self.visited[state] = True
        #print (type(self.gm.getGameState()))
        moves = self.gm.getMovables()
        print ("CURRENTSTATE" + str(self.currentState.state))
        print ("MOVABLES:")
        if moves:
            for m in moves:
                print (str(m))
        print ("CHILDINDEX:")
        print (state.nextChildToVisit)
        print ("*********")
        if state.state == self.victoryCondition:
            return True
        #if no child to expand then go back
        if not moves or state.nextChildToVisit >= len(moves):
            self.currentState = state.parent
            if state.requiredMovable is not None:
                self.gm.reverseMove(state.requiredMovable)
        # expand
        else:

            next_move = moves[state.nextChildToVisit]
            self.gm.makeMove(next_move)
            state.nextChildToVisit += 1

            #if to parent or if visited then skip
            while (((state.parent is not None) and (self.gm.getGameState() == state.parent.state))) or GameState(self.gm.getGameState(), 0, None) in self.visited:
                print ("PARENT FOUND!")
                self.gm.reverseMove(next_move)
                if state.nextChildToVisit >= len(moves):
                    self.currentState = state.parent
                    return False
                else:
                    next_move = moves[state.nextChildToVisit]
                    self.gm.makeMove(next_move)
                    state.nextChildToVisit += 1

            next_state = GameState(self.gm.getGameState(), state.depth + 1, next_move)
            next_state.parent = state
            #next_state.requiredMovable = next_move
            state.children.append(next_state)
            self.currentState = next_state
        print (state.nextChildToVisit)
        return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = Queue()
        self.queue.put([self.currentState, []])
        self.first_step = False

    def gm_init(self):
        state = self.currentState
        while state.parent:
            self.gm.reverseMove(state.requiredMovable)
            state = state.parent

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.first_step == False:
            self.first_step = True
            if self.solveOneStep():
                return True
        if self.queue:
            self.gm_init()
            ele = self.queue.get()
            #print (len(ele))
            state = ele[0]
            premoves = ele[1]

            for m in premoves:
                self.gm.makeMove(m)
            if state.state == self.victoryCondition:
                return True
            self.visited[state] = True
            print("CURRENTSTATE:")
            print(self.gm.getGameState())
            print("*******")
            moves = self.gm.getMovables()
            for m in moves:
                self.gm.makeMove(m)
                if (((state.parent is not None) and (self.gm.getGameState() == state.parent.state))) or GameState(self.gm.getGameState(), 0, None) in self.visited:
                    self.gm.reverseMove(m)
                    continue
                self.visited[GameState(self.gm.getGameState(), 0, None)] = True
                new_pmv = [i for i in premoves]
                new_pmv.append(m)
                next_state = GameState(self.gm.getGameState(), state.depth+1, m)
                next_state.parent = state
                state.children.append(next_state)
                self.queue.put([next_state, new_pmv])
                self.gm.reverseMove(m)
            self.currentState = state

            #for i in range(len(premoves)-1, -1, -1):
            #    mv = premoves[i]
            #    self.gm.reverseMove(mv)
        return False

