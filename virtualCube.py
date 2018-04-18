import random
from copy import deepcopy

class AlgorithmError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class VirtualCube:
    def __init__(self, *args, **kwargs):
        self.config(*args, **kwargs)
        self.reset()

    def __str__(self, *args, **kwargs):
        output = str("  "*3 + " ".join(self._tiles[1][1][2][::-1]) + "  "*3 + "\n"
                     + "  "*3 + " ".join(self._tiles[1][1][1][::-1]) + "  "*3 + "\n"
                     + "  "*3 + " ".join(self._tiles[1][1][0][::-1]) + "  "*3 + "\n"
                     + " ".join(self._column(self._tiles[2][0][::-1], 0)) + " "
                     + " ".join(self._tiles[0][0][0]) + " "
                     + " ".join(self._column(self._tiles[2][1], 2)) + "\n"
                     + " ".join(self._column(self._tiles[2][0][::-1], 1)) + " "
                     + " ".join(self._tiles[0][0][1]) + " "
                     + " ".join(self._column(self._tiles[2][1], 1)) + "\n"
                     + " ".join(self._column(self._tiles[2][0][::-1], 2)) + " "
                     + " ".join(self._tiles[0][0][2]) + " "
                     + " ".join(self._column(self._tiles[2][1], 0)) + "\n"
                     + "  "*3 + " ".join(self._tiles[1][0][0]) + "  "*3 + "\n"
                     + "  "*3 + " ".join(self._tiles[1][0][1]) + "  "*3 + "\n"
                     + "  "*3 + " ".join(self._tiles[1][0][2]) + "  "*3 + "\n"
                     + "  "*3 + " ".join(self._tiles[0][1][2]) + "  "*3 + "\n"
                     + "  "*3 + " ".join(self._tiles[0][1][1]) + "  "*3 + "\n"
                     + "  "*3 + " ".join(self._tiles[0][1][0]) + "  "*3)
        return output

    def config(self, *args, **kwargs):
        if "command" in kwargs.keys():
            self._command = kwargs.pop("command")
        else:
            self._command = None
        if "colours" in kwargs.keys():
            self._colours = kwargs.pop("colours")
        else:
            self._colours = [["w", "y"], ["r", "o"], ["g", "b"]]

    def reset(self, *args, **kwargs):
        self._tiles = list(map(lambda x: [[[x[0]]*3]*3, [[x[1]]*3]*3],
                              self._colours))

        if self._command != None:
            self._command()

    def scramble(self, *args, **kwargs):
        moves = ["U", "D", "F", "B", "L", "R"]
        variant = ["", "'", "2"]
        last = None
        alg = ""
        for i in range(random.randint(15, 26)):
            m = moves[:]
            if last != None:
                m.remove(last)
            move = random.choice(m)
            last = move
            var = random.choice(variant)
            alg += move + var + " "
        self.algorithm(alg[0:len(alg)-1])

        if self._command != None:
            self._command()

    @property
    def tiles(self, *args, **kwargs):
        return deepcopy(self._tiles)

    def _column(self, array, i):
        return list(map(lambda x: x[i], array))

    def algorithm(self, alg):
        commands = alg.strip().split(" ")
        for command in commands:
            if command[0].upper() == "U":
                if len(command) == 2:
                    if command[1] == "'":
                        turns = -1
                    elif command[1] == "2":
                        turns = 2
                    else:
                        raise AlgorithmError("{} is not a valid move".format(command))
                elif len(command) == 1:
                    turns = 1
                else:
                    raise AlgorithmError("{} is not a valid move".format(command))
                self.up(turns, command=False)
            elif command[0].upper() == "D":
                if len(command) == 2:
                    if command[1] == "'":
                        turns = -1
                    elif command[1] == "2":
                        turns = 2
                    else:
                        raise AlgorithmError("{} is not a valid move".format(command))
                elif len(command) == 1:
                    turns = 1
                else:
                    raise AlgorithmError("{} is not a valid move".format(command))
                self.down(turns, command=False)
            elif command[0].upper() == "F":
                if len(command) == 2:
                    if command[1] == "'":
                        turns = -1
                    elif command[1] == "2":
                        turns = 2
                    else:
                        raise AlgorithmError("{} is not a valid move".format(command))
                elif len(command) == 1:
                    turns = 1
                else:
                    raise AlgorithmError("{} is not a valid move".format(command))
                self.front(turns, command=False)
            elif command[0].upper() == "B":
                if len(command) == 2:
                    if command[1] == "'":
                        turns = -1
                    elif command[1] == "2":
                        turns = 2
                    else:
                        raise AlgorithmError("{} is not a valid move".format(command))
                elif len(command) == 1:
                    turns = 1
                else:
                    raise AlgorithmError("{} is not a valid move".format(command))
                self.back(turns, command=False)
            elif command[0].upper() == "L":
                if len(command) == 2:
                    if command[1] == "'":
                        turns = -1
                    elif command[1] == "2":
                        turns = 2
                    else:
                        raise AlgorithmError("{} is not a valid move".format(command))
                elif len(command) == 1:
                    turns = 1
                else:
                    raise AlgorithmError("{} is not a valid move".format(command))
                self.left(turns, command=False)
            elif command[0].upper() == "R":
                if len(command) == 2:
                    if command[1] == "'":
                        turns = -1
                    elif command[1] == "2":
                        turns = 2
                    else:
                        raise AlgorithmError("{} is not a valid move".format(command))
                elif len(command) == 1:
                    turns = 1
                else:
                    raise AlgorithmError("{} is not a valid move".format(command))
                self.right(turns, command=False)
            else:
                raise AlgorithmError("{} is not a valid move".format(command))

        if self._command != None:
            self._command()

    def up(self, turns=1, command=True):
        face = deepcopy(self._tiles[0][0])
        for n in range(3):
            if turns % 4 == 1:
                self._tiles[0][0][n] = self._column(face[::-1], n)
            elif turns % 4 == 2:
                self._tiles[0][0][n] = face[2-n][::-1]
            elif turns % 4 == 3:
                self._tiles[0][0][n] = self._column(face, 2-n)

        if turns % 4 == 1:
            row = self._tiles[1][0][0][:]
            self._tiles[1][0][0] = self._tiles[2][1][0][:]
            self._tiles[2][1][0] = self._tiles[1][1][0][:]
            self._tiles[1][1][0] = self._tiles[2][0][0][:]
            self._tiles[2][0][0] = row
        elif turns % 4 == 2:
            row = self._tiles[1][0][0][:]
            self._tiles[1][0][0] = self._tiles[1][1][0][:]
            self._tiles[1][1][0] = row
            row = self._tiles[2][0][0][:]
            self._tiles[2][0][0] = self._tiles[2][1][0][:]
            self._tiles[2][1][0] = row
        elif turns % 4 == 3:
            row = self._tiles[1][0][0][:]
            self._tiles[1][0][0] = self._tiles[2][0][0][:]
            self._tiles[2][0][0] = self._tiles[1][1][0][:]
            self._tiles[1][1][0] = self._tiles[2][1][0][:]
            self._tiles[2][1][0] = row

        if self._command != None and command:
            self._command()
            
    def down(self, turns=1, command=True):
        face = deepcopy(self._tiles[0][1])
        for n in range(3):
            if turns % 4 == 1:
                self._tiles[0][1][n] = self._column(face, 2-n)
            elif turns % 4 == 2:
                self._tiles[0][1][n] = face[2-n][::-1]
            elif turns % 4 == 3:
                self._tiles[0][1][n] = self._column(face[::-1], n)

        if turns % 4 == 1:
            row = self._tiles[1][0][2][:]
            self._tiles[1][0][2] = self._tiles[2][0][2][:]
            self._tiles[2][0][2] = self._tiles[1][1][2][:]
            self._tiles[1][1][2] = self._tiles[2][1][2][:]
            self._tiles[2][1][2] = row
        elif turns % 4 == 2:
            row = self._tiles[1][0][2][:]
            self._tiles[1][0][2] = self._tiles[1][1][2][:]
            self._tiles[1][1][2] = row
            row = self._tiles[2][0][2][:]
            self._tiles[2][0][2] = self._tiles[2][1][2][:]
            self._tiles[2][1][2] = row
        elif turns % 4 == 3:
            row = self._tiles[1][0][2][:]
            self._tiles[1][0][2] = self._tiles[2][1][2][:]
            self._tiles[2][1][2] = self._tiles[1][1][2][:]
            self._tiles[1][1][2] = self._tiles[2][0][2][:]
            self._tiles[2][0][2] = row

        if self._command != None and command:
            self._command()

    def front(self, turns=1, command=True):
        face = deepcopy(self._tiles[1][0])
        for n in range(3):
            if turns % 4 == 1:
                self._tiles[1][0][n] = self._column(face[::-1], n)
            elif turns % 4 == 2:
                self._tiles[1][0][n] = face[2-n][::-1]
            elif turns % 4 == 3:
                self._tiles[1][0][n] = self._column(face, 2-n)

        if turns % 4 == 1:
            row = self._tiles[0][0][2][:]
            self._tiles[0][0][2] = self._column(deepcopy(self._tiles[2][0]), 2)[::-1]
            for n in range(3):
                self._tiles[2][0][n] = [*self._tiles[2][0][n][0:2],
                                        self._tiles[0][1][2][n]]
            self._tiles[0][1][2] = self._column(deepcopy(self._tiles[2][1]), 0)[::-1]
            for n in range(3):
                self._tiles[2][1][n] = [row[n], *self._tiles[2][1][n][1:3]]
        elif turns % 4 == 2:
            row = self._tiles[0][0][2][:]
            self._tiles[0][0][2] = self._tiles[0][1][2][::-1]
            self._tiles[0][1][2] = row[::-1]
            row = self._column(self._tiles[2][0], 2)
            for n in range(3):
                self._tiles[2][0][n] = [*self._tiles[2][0][n][0:2],
                                        self._tiles[2][1][2-n][0]]
            for n in range(3):
                self._tiles[2][1][n] = [row[2-n], *self._tiles[2][1][n][1:3]]
        elif turns % 4 == 3:
            row = self._tiles[0][0][2][:]
            self._tiles[0][0][2] = self._column(deepcopy(self._tiles[2][1]), 0)
            for n in range(3):
                self._tiles[2][1][n] = [self._tiles[0][1][2][2-n],
                                        *self._tiles[2][1][n][1:3]]
            self._tiles[0][1][2] = self._column(deepcopy(self._tiles[2][0]), 2)
            for n in range(3):
                self._tiles[2][0][n] = [*self._tiles[2][0][n][0:2], row[2-n]]

        if self._command != None and command:
            self._command()

    def back(self, turns=1, command=True):
        face = deepcopy(self._tiles[1][1])
        for n in range(3):
            if turns % 4 == 1:
                self._tiles[1][1][n] = self._column(face[::-1], n)
            elif turns % 4 == 2:
                self._tiles[1][1][n] = face[2-n][::-1]
            elif turns % 4 == 3:
                self._tiles[1][1][n] = self._column(face, 2-n)

        if turns % 4 == 1:
            row = self._tiles[0][0][0][:]
            self._tiles[0][0][0] = self._column(deepcopy(self._tiles[2][1]), 2)
            for n in range(3):
                self._tiles[2][1][n] = [*self._tiles[2][1][n][0:2],
                                        self._tiles[0][1][0][2-n]]
            self._tiles[0][1][0] = self._column(deepcopy(self._tiles[2][0]), 0)
            for n in range(3):
                self._tiles[2][0][n] = [row[2-n], *self._tiles[2][0][n][1:3]]
        elif turns % 4 == 2:
            row = self._tiles[0][0][0][:]
            self._tiles[0][0][0] = self._tiles[0][1][0][::-1]
            self._tiles[0][1][0] = row[::-1]
            row = self._column(self._tiles[2][0], 0)
            for n in range(3):
                self._tiles[2][0][n] = [self._tiles[2][1][2-n][2],
                                        *self._tiles[2][0][n][1:3]]
            for n in range(3):
                self._tiles[2][1][n] = [*self._tiles[2][1][n][0:2], row[2-n]]
        elif turns % 4 == 3:
            row = self._tiles[0][0][0][:]
            self._tiles[0][0][0] = self._column(deepcopy(self._tiles[2][0]), 0)[::-1]
            for n in range(3):
                self._tiles[2][0][n] = [self._tiles[0][1][0][n],
                                        *self._tiles[2][0][n][1:3]]
            self._tiles[0][1][0] = self._column(deepcopy(self._tiles[2][1]), 2)[::-1]
            for n in range(3):
                self._tiles[2][1][n] = [*self._tiles[2][1][n][0:2], row[n]]

        if self._command != None and command:
            self._command()

    def left(self, turns=1, command=True):
        face = deepcopy(self._tiles[2][0])
        for n in range(3):
            if turns % 4 == 1:
                self._tiles[2][0][n] = self._column(face[::-1], n)
            elif turns % 4 == 2:
                self._tiles[2][0][n] = face[2-n][::-1]
            elif turns % 4 == 3:
                self._tiles[2][0][n] = self._column(face, 2-n)

        if turns % 4 == 1:
            row = self._column(deepcopy(self._tiles[0][0]), 0)
            for n in range(3):
                self._tiles[0][0][n] = [self._tiles[1][1][2-n][2],
                                        *self._tiles[0][0][n][1:3]]
            for n in range(3):
                self._tiles[1][1][n] = [*self._tiles[1][1][n][0:2],
                                        self._tiles[0][1][n][0]]
            for n in range(3):
                self._tiles[0][1][n] = [self._tiles[1][0][2-n][0],
                                        *self._tiles[0][1][n][1:3]]
            for n in range(3):
                self._tiles[1][0][n] = [row[n], *self._tiles[1][0][n][1:3]]
        elif turns % 4 == 2:
            row = self._column(deepcopy(self._tiles[0][0]), 0)
            for n in range(3):
                self._tiles[0][0][n] = [self._tiles[0][1][2-n][0],
                                        *self._tiles[0][0][n][1:3]]
            for n in range(3):
                self._tiles[0][1][n] = [row[2-n], *self._tiles[0][1][n][1:3]]
            row = self._column(deepcopy(self._tiles[1][0]), 0)
            for n in range(3):
                self._tiles[1][0][n] = [self._tiles[1][1][2-n][2],
                                        *self._tiles[1][0][n][1:3]]
            for n in range(3):
                self._tiles[1][1][n] = [*self._tiles[1][1][n][0:2], row[2-n]]
        elif turns % 4 == 3:
            row = self._column(deepcopy(self._tiles[0][0]), 0)
            for n in range(3):
                self._tiles[0][0][n] = [self._tiles[1][0][n][0],
                                        *self._tiles[0][0][n][1:3]]
            for n in range(3):
                self._tiles[1][0][n] = [self._tiles[0][1][2-n][0],
                                       *self._tiles[1][0][n][1:3]]
            for n in range(3):
                self._tiles[0][1][n] = [self._tiles[1][1][n][2],
                                        *self._tiles[0][1][n][1:3]]
            for n in range(3):
                self._tiles[1][1][n] = [*self._tiles[1][1][n][0:2], row[2-n]]#

        if self._command != None and command:
            self._command()

    def right(self, turns=1, command=True):
        face = deepcopy(self._tiles[2][1])
        for n in range(3):
            if turns % 4 == 1:
                self._tiles[2][1][n] = self._column(face[::-1], n)
            elif turns % 4 == 2:
                self._tiles[2][1][n] = face[2-n][::-1]
            elif turns % 4 == 3:
                self._tiles[2][1][n] = self._column(face, 2-n)

        if turns % 4 == 1:
            row = self._column(deepcopy(self._tiles[0][0]), 2)
            for n in range(3):
                self._tiles[0][0][n] = [*self._tiles[0][0][n][0:2],
                                        self._tiles[1][0][n][2]]
            for n in range(3):
                self._tiles[1][0][n] = [*self._tiles[1][0][n][0:2],
                                        self._tiles[0][1][2-n][2]]
            for n in range(3):
                self._tiles[0][1][n] = [*self._tiles[0][1][n][0:2],
                                        self._tiles[1][1][n][0]]
            for n in range(3):
                self._tiles[1][1][n] = [row[2-n], *self._tiles[1][1][n][1:3]]
        elif turns % 4 == 2:
            row = self._column(deepcopy(self._tiles[0][0]), 2)
            for n in range(3):
                self._tiles[0][0][n] = [*self._tiles[0][0][n][0:2],
                                        self._tiles[0][1][2-n][2]]
            for n in range(3):
                self._tiles[0][1][n] = [*self._tiles[0][1][n][0:2], row[2-n]]
            row = self._column(deepcopy(self._tiles[1][0]), 2)
            for n in range(3):
                self._tiles[1][0][n] = [*self._tiles[1][0][n][0:2],
                                        self._tiles[1][1][2-n][0]]
            for n in range(3):
                self._tiles[1][1][n] = [row[2-n], *self._tiles[1][1][n][1:3]]
        elif turns % 4 == 3:
            row = self._column(deepcopy(self._tiles[0][0]), 2)
            for n in range(3):
                self._tiles[0][0][n] = [*self._tiles[0][0][n][0:2],
                                        self._tiles[1][1][2-n][0]]
            for n in range(3):
                self._tiles[1][1][n] = [self._tiles[0][1][n][2],
                                        *self._tiles[1][1][n][1:3]]
            for n in range(3):
                self._tiles[0][1][n] = [*self._tiles[0][1][n][0:2],
                                        self._tiles[1][0][2-n][2]]
            for n in range(3):
                self._tiles[1][0][n] = [*self._tiles[1][0][n][0:2], row[n]]

        if self._command != None and command:
            self._command()

# ----------------------------------- Test -----------------------------------

if __name__ == "__main__":
    cube = VirtualCube()
    print(str(cube) + "\n")

    moves = []

    while True:
        alg = input("> ")

        if alg.lower() == "undo":
            alg = moves.pop(-1)
            commands = alg.upper().strip().split(" ")[::-1]
            alg = ""
            for command in commands:
                if command[0] == "U":
                    if len(command) > 1:
                        if command[1] == "'":
                            alg += "U "
                        elif command[1] == "2":
                            alg += "U2 "
                        else:
                            alg += "U' "
                    else:
                        alg += "U' "
                elif command[0] == "D":
                    if len(command) > 1:
                        if command[1] == "'":
                            alg += "D "
                        elif command[1] == "2":
                            alg += "D2 "
                        else:
                            alg += "D' "
                    else:
                        alg += "D' "
                elif command[0] == "F":
                    if len(command) > 1:
                        if command[1] == "'":
                            alg += "F "
                        elif command[1] == "2":
                            alg += "F2 "
                        else:
                            alg += "F' "
                    else:
                        alg += "F' "
                elif command[0] == "B":
                    if len(command) > 1:
                        if command[1] == "'":
                            alg += "B "
                        elif command[1] == "2":
                            alg += "B2 "
                        else:
                            alg += "B' "
                    else:
                        alg += "B' "
                elif command[0] == "L":
                    if len(command) > 1:
                        if command[1] == "'":
                            alg += "L "
                        elif command[1] == "2":
                            alg += "L2 "
                        else:
                            alg += "L' "
                    else:
                        alg += "L' "
                elif command[0] == "R":
                    if len(command) > 1:
                        if command[1] == "'":
                            alg += "R "
                        elif command[1] == "2":
                            alg += "R2 "
                        else:
                            alg += "R' "
                    else:
                        alg += "R' "
            print("\n" + alg)
            cube.algorithm(alg[0:len(alg)-1])
            print("\n" + str(cube) + "\n")
        elif alg.lower() == "reset":
            cube.reset()
            print("\n" + str(cube) + "\n")
        elif alg.lower() == "scramble":
            cube.scramble()
            print("\n" + str(cube) + "\n")
        else:
            try:
                cube.algorithm(alg)
                moves.append(alg)
                print("\n" + str(cube) + "\n")
            except AlgorithmError:
                print("\n{} is not a valid command\n".format(alg))
