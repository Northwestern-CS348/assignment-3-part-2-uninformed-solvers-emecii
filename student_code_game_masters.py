from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        ans = []

        ask1 = parse_input("fact: (on ?X peg1)")
        ask2 = parse_input("fact: (on ?X peg2)")
        ask3 = parse_input("fact: (on ?X peg3)")

        answers = [self.kb.kb_ask(ask1), self.kb.kb_ask(ask2),self.kb.kb_ask(ask3)]

        for answer in answers:
            disk = []
            if answer:
                disk = [int(str(a).split(":")[1][-1]) for a in answer]
                #disk = (for d in answer)
                disk.sort()
                #disk = tuple(disk)
            ans.append(tuple(disk))

        #print(tuple(ans))
        return tuple(ans)


        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        data = str(movable_statement).split(" ")
        state = self.getGameState()
        #print (data)

        delete1 = 'fact: (on ' + data[1] + ' ' + data[2] + ')'
        self.kb.kb_retract(parse_input(delete1))
        self.kb.kb_retract(parse_input('fact: (top ' + data[1] + ' ' + data[2] + ')'))
        #ask1 = parse_input("fact: (top ?X " + data[2] + ")")
        if len(state[int(data[2][-1])-1]) == 1:
            self.kb.kb_add(parse_input('fact: (empty ' + data[2] + ')'))
        else:
            top = "disk" + str(state[int(data[2][-1])-1][1])
            self.kb.kb_add(parse_input('fact: (top ' + top + ' ' + data[2] + ')'))

        if len(state[int(data[3][-2])-1]) == 0:
            self.kb.kb_retract(parse_input('fact: (empty ' + data[3]))
        else:
            top = "disk" + str(state[int(data[3][-2])-1][0])
            self.kb.kb_retract(parse_input('fact: (top ' + top + ' ' + data[3]))
        self.kb.kb_add(parse_input('fact: (top ' + data[1] + ' ' + data[3]))
        self.kb.kb_add(parse_input('fact: (on ' + data[1] + ' ' + data[3]))
        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        ans = [[],[],[]]
        for i in range(0, len(ans)):
            line = ans[i]
            for j in range(1,4):
                ask = parse_input("fact: (coordinate ?X pos" + str(j) + " pos" + str(i+1) + ")")
                a = self.kb.kb_ask(ask)
                num = str(a).split(":")[2].split("\n")[0][-1]
                #print (a)
                #print ("****")
                #print (num)
                if num == "y":
                    #print ("now find empty")
                    #print (a)
                    line.append(-1)
                else:
                    line.append(int(num))
        new_ans = tuple([tuple(line) for line in ans])
        print (new_ans)
        return new_ans
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        oldfact1 = Fact(Statement(["coordinate", terms[0], terms[1], terms[2]]))
        oldfact2 = Fact(Statement(["coordinate", 'empty', terms[3], terms[4]]))
        self.kb.kb_retract(oldfact1)
        self.kb.kb_retract(oldfact2)
        newfact1 = Fact(Statement(["coordinate", terms[0], terms[3], terms[4]]))
        newfact2 = Fact(Statement(["coordinate", 'empty', terms[1], terms[2]]))
        self.kb.kb_assert(newfact1)
        self.kb.kb_assert(newfact2)


        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
