from pathlib import Path
from collections import deque

#• 0 si es una casilla libre (flujo vehicular bajo)
#• 1 si es un muro
#• 2 si es el punto de partida del vehículo
#• 3 si es una casilla con flujo vehicular alto
#• 4 si es un pasajero
#• 5 si es el destino


class City():
    def __init__(self, filename):
        
        #read the file
        #with open(filename) as f:
        file_path = Path(__file__).resolve().parent / filename
        with open(file_path, encoding="utf-8") as f:
            contents = f.read()

        #validation that should only have one starting point
        if contents.count('2') != 1:
            raise Exception('Debe haber solo un punto de partida')

        #validation that should only have one destination point
        if contents.count('5') != 1:
            raise Exception('Debe haber solo un destino')    
        
        #determine width and height of the city
        contents = contents.splitlines() # this returns an array
        self.height = len(contents) # the height is the number of lines
        self.width = max(len(line) for line in contents) # the width is the most largest line in the array
        
        self.matrix = []
        self.passengers = []
        self.high_flow = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == '2': 
                        self.start = (i, j) #save my starting point
                        row.append('2')
                    elif contents[i][j] == '3':
                        self.high_flow.append((i, j))
                        row.append('3')
                    elif contents[i][j] == '4':
                        self.passengers.append((i, j))
                        row.append('4')
                    elif contents[i][j] == '5':
                        self.goal = (i, j) # save my destination point
                        row.append('5')
                    else:
                        row.append(contents[i][j])
                except IndexError:
                    row.append('0')
            self.matrix.append(row) #this is a 2D array
    
    def print(self):
        print()
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.goal:
                    print("X", end="")
                elif (i, j) == self.start:
                    print("R", end="")
                elif self.matrix[i][j] == '1':
                    print("█", end="")
                elif self.matrix[i][j] == '3':
                    print("+", end="")
                elif self.matrix[i][j] == '4':
                    print("P", end="")
                else:
                    print(" ", end="")
            print()
        print()

             

class Robotaxi():
    def __init__(self, y, x, city):
        self.column = x
        self.row = y
        self.city = city
        self.matrix = city.matrix
        self.update_sensors()
        self.bfs()

    def position(self):
        return (self.row, self.column)
    
    def move(self, y, x):
        self.matrix[self.row][self.column] = '0'
        self.matrix[y][x] = '2'
        self.row = y
        self.column = x
        self.update_sensors()

    def update_sensors(self):
        self.left = self.column - 1 >= 0 and self.matrix[self.row][self.column - 1] != '1'
        self.up = self.row - 1 >= 0 and self.matrix[self.row - 1][self.column] != '1'
        self.right = self.column + 1 <= (len(self.matrix[self.row]) - 1) and self.matrix[self.row][self.column + 1] != '1'
        self.down = self.row + 1 <= (len(self.matrix) - 1) and self.matrix[self.row + 1][self.column] != '1'

    def find_position(self, to_move):
        match to_move:
            case "right":
                return (self.row, self.column + 1)
            case "down":
                return (self.row + 1, self.column)
            case "left":
                return (self.row, self.column - 1)
            case "up":
                return (self.row - 1, self.column)


    def bfs(self):
        print(f"Empezo {self.left} , {self.right}, {self.down}, {self.up}")
        queue = deque()
        queue.append(self.position())
        set = {self.position()}
        count = 0

        while(True):
            count += 1
            print(count)
            print(queue)

            if not queue: 
                raise Exception(f"No hay solución y {count}")
            
            self.move(*(queue.popleft()))
            self.update_sensors()

            if self.position() == self.city.goal:
                return print(f"Lo encontroooo {self.position}")

            paths = []
            if self.right:
                movement = self.find_position("right")
                if movement not in set:
                    paths.append(movement)
                set.add(movement)
            if self.left:
                movement = self.find_position("left")
                if movement not in set:
                    paths.append(movement)
                set.add(movement)
            if self.up:
                movement = self.find_position("up")
                if movement not in set:
                    paths.append(movement)
                set.add(movement)
            if self.down:
                movement = self.find_position("down")
                if movement not in set:
                    paths.append(movement)
                set.add(movement)

            queue.extend(paths)
            





city = City("city1.txt")
print(city.matrix)
city.print()
robotaxi = Robotaxi(*(city.start), city)